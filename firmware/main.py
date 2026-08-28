from machine import Pin, SPI, I2C, I2S
import lib.as5600
import lib.st7789
import lib.sdcard
import lib.spleen8, lib.spleen16
import os, vfs
import time
import json
import wave

display_spi = SPI(0, baudrate=60000000, polarity=0, phase=0, sck=Pin(2), mosi=Pin(3))
display_cs = Pin(5, Pin.OUT)
display_dc = Pin(6, Pin.OUT)
display_rst = Pin(7, Pin.OUT)
display = lib.st7789.ST7789(display_spi, width=240, height=320, cs=display_cs, dc=display_dc, reset=display_rst, rotation=1)
width, height = 320, 240

wheel_i2c_bus = I2C(0, scl=Pin(1), sda=Pin(0))
wheel_dir = Pin(4)
wheel = lib.as5600.AS5600(wheel_i2c_bus)

sd_spi = SPI(1, sck=Pin(14), mosi=Pin(15), miso=Pin(12))
sd_cs = Pin(13, Pin.OUT)
sd_cd = Pin(11)
sd = lib.sdcard.SDCard(sd_spi, sd_cs)
vfs.mount(sd, '/sd')

audio_bus = I2S(0, sck=Pin(23), ws=Pin(24), sd=Pin(25), mode=I2S.TX, bits=16, format=I2S.STEREO, rate=48000, ibuf=4096)

def color565(red, green=0, blue=0):
    """
    Convert red, green and blue values (0-255) into a 16-bit 565 encoding.
    """
    if isinstance(red, (tuple, list)):
        red, green, blue = red[:3]
    return (red & 0xF8) << 8 | (green & 0xFC) << 3 | blue >> 3

def text(font, text, x, y, color, cx=0, cy=0):
    x = x - ((font.WIDTH * len(text)) * cx) // 2
    y = y - (font.HEIGHT // 2) * cy
    display.text(font, text, x, y, color)

display.init()

if sd_cd.value() == 0:
    display.fill(0xFFFF)
    text(lib.spleen16, "No SD card is inserted.", width // 2, height // 2, 0x0000, 1, 1)
    while sd_cd.value() == 0:
        pass

display.fill(0xFFFF)
text(lib.spleen16, "Reading metadata.json...", width // 2, height // 2, 0x0000, 1, 1)

try:
    with open("/sd/metadata.json", "r") as f:
        metadata = json.load(f)
except Exception as e:
    display.fill(0xFFFF)
    text(lib.spleen16, "Error occured. Restart your device.", width // 2, height // 2, 0x0000, 1, 1)

# metadata = [
#     {
#         'name': 'Mural',
#         'artists': ['Lupe Fiasco'],
#         'album': 'Tetsuo & Youth',
#         'cover': 'cover001.png',
#         'file': 'file001.wav'
#     }
# ]

display.fill(0xFFFF)
text(lib.spleen16, f"Found {len(metadata)} songs", width // 2, height // 2, 0x0000, 1, 1)

time.sleep(1)

wave_current_file = -1
wave_current_object = None
wave_current_frame = 0
wave_current_cover = None
wave_current_length = 0
playing = False

def format_time(seconds):
    m, s = divmod(seconds, 60)
    m, s = int(m), int(s)
    return f"{m}:{s:03}"

def cut_string(text, length, char_length):
    if len(text) > length // char_length:
        return text[:length//char_length-3] + '...'
    return text

def cue(song):
    global playing, wave_current_object, wave_current_file, wave_current_frame, wave_current_cover, wave_current_length
    playing = False

    wave_current_file = song
    wave_current_frame = 0
    wave_current_object = wave.open(metadata[song]["file"])
    with open(metadata[song]["cover"], "rb") as f:
        wave_current_cover = bytearray(f.read())

    wave_current_length = wave_current_object.getnframes() // wave_current_object.getframerate()

    playing = True

while True:
    written = None
    if playing:
        frames = wave_current_object.getnframes(512)
        if wave_current_object.getnchannels() == 1:
            buf = bytearray([0 for _ in range(1024)])
            buf[0::2] = frames
            buf[1::2] = frames
            frames = buf

        written = audio_bus.write(frames)

        display.fill(0xFFFF)
        display.blit_buffer(wave_current_cover, 30, 30, 100, 100)

        text(lib.spleen16, cut_string(metadata[wave_current_file]["name"], 160, 16), 138, 30, 0x0000)
        text(lib.spleen8, cut_string(", ".join(metadata[wave_current_file]["artists"]), 160, 16), 138, 60, 0x0000)
        text(lib.spleen8, cut_string(metadata[wave_current_file]["album"], 160, 16), 138, 70, 0x0000)

        while len(written) < 1024:
            pass

        wave_current_frame += 512 
        