#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Title        : RetroPie_OLED.py
Author       : zzeromin, member of Raspberrypi Village
Creation Date: Nov 13, 2016
Blog         : http://rasplay.org, http://forums.rasplay.org/, https://zzeromin.tumblr.com/
Thanks to    : smyani, zerocool, GreatKStar
Free and open for all to use. But put credit where credit is due.

Reference    :
https://github.com/adafruit/Adafruit_Python_SSD1306.git
https://github.com/haven-jeon/piAu_volumio

Notice       :
installed python package: python-pip python-imaging python-dev python-smbus i2c-tools
This code edited for rpi3 Retropie v4.0.2 and later by zzeromin
"""

import time
import os
from sys import exit
from subprocess import *
from time import *
from datetime import datetime

import Adafruit_GPIO.SPI as SPI
import Adafruit_SSD1306

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

# Raspberry Pi pin configuration:
RST = 24
# Note the following are only used with SPI:
DC = 23
SPI_PORT = 0
SPI_DEVICE = 0

# 128x32 display with hardware I2C:
#disp = Adafruit_SSD1306.SSD1306_128_32(rst=RST)

# 128x64 display with hardware I2C:
disp = Adafruit_SSD1306.SSD1306_128_64(rst=RST)

def run_cmd(cmd):
    # runs whatever is in the cmd variable in the terminal
    p = Popen(cmd, shell=True, stdout=PIPE)
    output = p.communicate()[0]
    return output

def get_ip_address(cmd, cmdeth):
    # ip & date information
    ipaddr = run_cmd(cmd)

    # selection of wlan or eth address
    count = len(ipaddr)
    if count == 0 :
        ipaddr = run_cmd(cmdeth)
    return ipaddr

def get_cpu_temp():
    tempFile = open("/sys/class/thermal/thermal_zone0/temp")
    cpu_temp = tempFile.read()
    tempFile.close()
    return float(cpu_temp)/1000

def get_cpu_speed():
    tempFile = open("/sys/devices/system/cpu/cpu0/cpufreq/scaling_cur_freq")
    cpu_speed = tempFile.read()
    tempFile.close()
    return float(cpu_speed)/1000

def main():

    # Initialize library.
    disp.begin()

    # Clear display.
    disp.clear()
    disp.display()

    # Create blank image for drawing.
    # Make sure to create image with mode '1' for 1-bit color.
    width = disp.width
    height = disp.height
    image = Image.new('1', (width, height))

    # Get drawing object to draw on image.
    draw = ImageDraw.Draw(image)

    # Draw a black filled box to clear the image.
    draw.rectangle((0,0,width,height), outline=0, fill=0)

    # Draw some shapes.
    # First define some constants to allow easy resizing of shapes.
    padding = 2
    shape_width = 20
    top = padding
    bottom = height-padding
    x = padding

    # Load default font.
    font_system = ImageFont.truetype('/home/pi/RetroPie-OLED/NanumGothic_Coding_Bold.ttf', 15)
    font_rom = ImageFont.truetype('/home/pi/RetroPie-OLED/NanumGothic_Coding_Bold.ttf', 15)

    #get ip address of eth0 connection
    cmdeth = "ip addr show eth0 | grep 'inet ' | awk '{print $2}' | cut -d/ -f1"
    #get ip address of wlan0 connection
    cmd = "ip addr show wlan0 | grep 'inet ' | awk '{print $2}' | cut -d/ -f1"
    #cmd = "ip addr show wlan1 | grep 'inet ' | awk '{print $2}' | cut -d/ -f1"

    #get ip address of eth0 connection    
    ipaddr = get_ip_address(cmd, cmdeth)

    old_Temp = new_Temp = get_cpu_temp()
    old_Speed = new_Speed = get_cpu_speed()

    while True:
#		draw.rectangle((0,0,width,height), outline=0, fill=0)

		try:
			f = open('/dev/shm/runcommand.log', 'r')
#                except FileNotFoundError:
		except IOError:
                	msg1 = "Welcome"
                	msg2 = "RetroPie v4.1"
                	ipaddr = get_ip_address(cmd, cmdeth)

                	draw.rectangle((0,0,width,height), outline=0, fill=0)
                	draw.text((0, top), unicode(msg1).center(1,' '), font=font_system, fill=255)
                	draw.text((0, top+15), unicode(msg2).center(2, ' '), font=font_rom, fill=255)
                	draw.text((0, top+30), datetime.now().strftime( "%b %d %H:%M:%S" ), font=font_rom, fill=255)
                	draw.text((0, top+45), "IP " + ipaddr, font=font_rom, fill=255)
                        disp.image(image)
                        disp.display()
#			sleep(3)
#			break
			pass
		else:
			system = f.readline()
			system = system.replace("\n","")
			systemMap = {
				"gba":"GameBoy Advance",
				"mame-libretro":"MAME",
				"msx":"MSX",
				"fba":"FinalBurn Alpha",
				"nes":"Famicom",   # Nintendo Entertainment System
				"snes":"Super Famicom", # Super Nintendo Entertainment System
				"notice":"TURN OFF",
			}
			system = systemMap.get(system)
			rom = f.readline()
			rom = rom.replace("\n","")
			f.close()
			
			ipaddr = get_ip_address(cmd, cmdeth)
			new_Temp = get_cpu_temp()
			new_Speed = int( get_cpu_speed() )

			if old_Temp != new_Temp or old_Speed != new_Speed :
				old_Temp = new_Temp
				old_Speed = new_Speed
			
#			print datetime.now().strftime( "%b %d %H:%M:%S" )
#			print "IP " + ipaddr
                        draw.rectangle((0,0,width,height), outline=0, fill=0)
			draw.text((0, top), unicode(system).center(1,' '), font=font_system, fill=255)
			draw.text((0, top+15), unicode(rom).center(2, ' '), font=font_rom, fill=255)
			draw.text((0, top+30), datetime.now().strftime( "%b %d %H:%M:%S" ), font=font_rom, fill=255)
			draw.text((0, top+45), "IP " + ipaddr, font=font_rom, fill=255)
                        disp.image(image)
                        disp.display()
			sleep(3)

			draw.rectangle((0,0,width,height), outline=0, fill=0)
			draw.text((0, top), unicode(system).center(1,' '), font=font_system, fill=255)
			draw.text((0, top+15), unicode(rom).center(2, ' '), font=font_rom, fill=255)
			draw.text((0, top+30), "CPU Temp: " + str( new_Temp ), font=font_rom, fill=255)
			draw.text((0, top+45), "CPU Speed: " + str( new_Speed ), font=font_rom, fill=255)
			disp.image(image)
			disp.display()
			sleep(3)

if __name__ == "__main__":
    import sys

    try:
        main()

    # Catch all other non-exit errors
    except Exception as e:
        sys.stderr.write("Unexpected exception: %s" % e)
        sys.exit(1)

    # Catch the remaining exit errors
    except:
        sys.exit(0)
