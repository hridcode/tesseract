---
title: "Tesseract"
author: "Hridhaan Shetty"
description: "Tesseract is a retro-style MP3 player with 32-bit stereo output to speakers and headphones, an LCD display, and battery charging for on-the-go listening."
created_at: "2026-08-21"
---

# August 22: Finished the schematic

The schematic has been completed. I repurposed an RP2354B devboard design that I had made before, and remodeled it for the RP2354A. I added a stereo speaker amplifier (PAM8403D), the hall effect potentiometer for the wheel (AS5600-ASOM), and an FPC connector for the LCD display (ST7789).

![Schematic design](/photos/journal-082226.png)

Time spent: **1.5 hours**

# August 22: Finished the schematic (again)

I forgot the microSD card slot in the previous journal lmao
Added that in, it's the 9 pin version which means there is a pin for card detection. There are 10KΩ pull-up resistors on the 4 SPI lines.

![Schematic design 2](/photos/journal-082226-02.png)