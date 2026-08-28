---
title: "Tesseract"
author: "Hridhaan Shetty"
description: "Tesseract is a retro-style MP3 player with 32-bit stereo output to speakers and headphones, an LCD display, and battery charging for on-the-go listening."
created_at: "2026-08-21"
---

# August 22: Finished the schematic

The schematic has been completed. I repurposed an RP2354B devboard design that I had made before, and remodeled it for the RP2354A. I added a stereo speaker amplifier (PAM8403D), the hall effect potentiometer for the wheel (AS5600-ASOM), and an FPC connector for the LCD display (ST7789).

![Schematic design](/photos/journal-082226-01.png)

Time spent: **1.5 hours**

# August 22: Finished the schematic (again)

I forgot the microSD card slot in the previous journal lmao
Added that in, it's the 9 pin version which means there is a pin for card detection. There are 10KΩ pull-up resistors on the 4 SPI lines.

![Schematic design 2](/photos/journal-082226-02.png)

Time spent: **1 hour**

# August 22: Added footprints for symbols

The footprints were added. This took no time at all, since most of them were already assigned as I copied it from a previous design.

![Footprints](/photos/journal-082226-03.png)

Time spent: **0.5 hours**

# August 24: Created the PCB layout

The layout is done! The screen at the top has the FPC connector 15mm down, according to the display diagram below. The RP2354A and crystal are close to each other, along with their passive components. The battery charging has its own section, as well as the audio, microSD, and USB connector.

![ST7789 display dimensions](/photos/journal-082426-01-01.png)
![PCB layout](/photos/journal-082426-01-02.png)

Time spent: **2 hours**

# August 26: Routed the PCB (Part 1)

The routing on the front and back layers is done. This layer was used for all the signals and all the peripherals for the microcontroller.
Next, I have to add vias for ground and power routing.

![PCB signal routing](/photos/journal-082626-01.png)

Time spent: **2 hours**

# August 26: Routed the PCB (Part 2)

The routing is finished! The second layer (green) has a ground plane, while the third layer (orange) is for power signals. Vias are connected from each ground/power pad in order to connect it to the inner layers.
M3 mounting holes are added at the corners, and a big NPTH hole is added near the display to fit the FPC connector of the display. 
The SD card footprint was changed to fit one from LCSC.

![PCB routing finished](/photos/journal-082626-02.png)

Time spent: **2 hours**

# August 27: Modeled the case (Part 1)

The case is basically halfway done. The geometry for the bottom and top cases is finished, as well as the mounting holes for the PCB to screw into, the display cutout, the wheel, and the magnet holes to connect the top and bottom cases. I really only need to add cutouts for ports and speaker grills, and anything else I see fit.

I learned to use Onshape for this project, but it was quite similar to Fusion 360.

![Prototype case](/photos/journal-082726-01.png)

Time spent: **3 hours**

# August 27: Modeled the case (Part 2)

The case is done! The speaker grills, port cutouts, and button caps are modeled, with 0.4-0.7mm tolerances. It looks kind of ugly, but oh well.

![Prototype case](/photos/journal-082826-01.png)

Time spent: **1 hour**

# August 28: Created firmware

I created a very simple firmware in MicroPython for the device. This initializes the peripherals, reads a file "metadata.json" from the SD card, and plays the songs in order, displaying the covers, artists, and respective albums.

![Firmware snippet](/photos/journal-082826-02.png)

Time spent: **1.5 hours**

# August 28: Added slide switch

Since I realized I had no way to turn the device on/off, I added a right-angled slide switch. This required updating the schematic, PCB, and case.

![Updated PCB](/photos/journal-082826-03-01.png)
![Updated case](/photos/journal-082826-03-02.png)

Time spent: **1 hour**