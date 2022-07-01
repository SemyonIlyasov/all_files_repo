from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
import ast
import subprocess
from binascii import unhexlify

import ST7735

rtc_time = subprocess.check_output("sudo hwclock -r", shell=True)
info = rtc_time.split(" ")
data = info[0]
time_str = info[1].split(".")[0]
time = time_str.split(":")
print(time)

disp = ST7735.ST7735(port=0, cs=0, dc=24, backlight=None, rst=25, width=128, height=160, rotation=90, invert=False)

WIDTH = disp.width
HEIGHT = disp.height

img = Image.new('RGB', (WIDTH, HEIGHT))
draw = ImageDraw.Draw(img)

# Function to reverse a string
def reverse(string):
	string = "".join(reversed(string))
	return string


# Load default font.
font = ImageFont.load_default()

while(True):
    hwclock = subprocess.check_output("sudo hwclock -r", shell=True)
    new_info = hwclock.split(" ")
    new_data = new_info[0]
    new_time_str = new_info[1].split(".")[0]
    new_time = new_time_str.split(":")
    print(new_time)
    if(int(new_time[2]) != int(time[2])):
# Write some text
#draw.text((5, 5), "Hello World!", font=font, fill=(255, 255, 255))
        time = new_time
        time_str = new_time_str
        data = new_data
        draw.rectangle((0,0,160,128), fill=(0,0,0))
        draw.text((0,0), data + "  " +  time_str, font=font, fill=(255,255,255))
        draw.text((5,35), "Bec: ", font=font, fill=(255,255,255))
        draw.text((75,35), "kg", font=font, fill=(255,255,255))
        draw.text((5,25), "RFID: ", font=font, fill=(255,255,255))
#draw.rectangle((0,0,160,128), fill=(0,0,0))
        with open("/home/www/AutoFarm/weight.txt","r") as fileWeight:
	       line = fileWeight.readline()
	       draw.text((35,35), line, font=font, fill=(255,255,255))

        with open("/home/www/AutoFarm/tag.txt","r") as fileTag:
            line = fileTag.readline()
	    #print(line)
            numstr = line[1:21]
	    #print(numstr)
	    unhexstr = unhexlify(numstr)
	    #print(unhexstr)
	    line = reverse(unhexstr)
 	    #print(line)
	    line = str( ast.literal_eval( "0x"+line))
	    #print(line)
            draw.text((35,25), line, font=font, fill=(255,255,255))

# Write buffer to display hardware, must be called to make things visible on the
# display!
        disp.display(img)
