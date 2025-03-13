#imports
import ntcore
import time
import sys
import board
import neopixel
from math import sqrt


#setting up neopixels
num_pixels = 69 #73 on the fried strip
pixels = neopixel.NeoPixel(board.D18, num_pixels, brightness=0.2, auto_write=False, pixel_order=neopixel.GRB)
pixels_pin = board.D18

#network tables subscriber setup
inst = ntcore.NetworkTableInstance.getDefault()
table = inst.getTable("SmartDashboard")
dupes = ntcore.PubSubOptions(keepDuplicates = True)
objHor = table.getDoubleTopic("objHorizontal").subscribe(0)
objDist=table.getDoubleTopic("objDistance").subscribe(0)
detectingAlgae=table.getBooleanTopic("detectingAlgae").subscribe(0)
#xNegative=table.getDoubleTopic("xn").subscribe(0)
#yNegative=table.getDoubleTopic("yn").subscribe(0)
inst.startClient4("example client")
inst.setServerTeam(4169)
inst.startDSClient()

#color assignment
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
yellow = (255,175,0)
orange = (255,75,0)
pink = (255,0,128)
purple = (255,0,255)
teal = (0,225,75)
pale = (225,90,25)
grey = (75,75,75)
white = (225,225,225)
off = (0,0,0)

#Red flashing on
#def turnRight(color, timeOn):
	#pixels[0 : 18] = [color] * 18
	#pixels.show()
	#time.sleep(timeOn)
	#pixels.fill((0, 0, 0))
	
#flashing on
def flash(color, timeOn, timeOff, repeat):
	for i in range(repeat):
		pixels.fill(color)
		pixels.show()
		time.sleep(timeOn)
		pixels.fill(off)
		pixels.show()
		time.sleep(timeOff)
		
	
	
#Example of static green turning on for a few seconds.
#def pickedUp(color, timeOn, timeOff):
	#for i in range(0, 3):
		#pixels.fill(color)
		#pixels.show()
		#time.sleep(timeOn)
		#pixels.fill((0, 0, 0))
		#time.sleep(timeOff)


#Example of running functions in a pattern (kinda useless)

#for i in range(0,3):
	#pixels.fill(red)
	#pixels.show()
	#time.sleep(1)
	#pixels.fill(off)

# def subsetmove(startpix):
	# pixels[startpix + 5] = white
	# pixels.show()
	# time.sleep(0.05)

# def subsetmove_rev(startpix):
	# pixels[startpix - 5] = white
	# pixels.show()
	# time.sleep(0.05)

#Moves a strip of light down the neopixel strip			
# for i in range(1, num_pixels - 5):
	# subsetmove(i)
	# pixels[i] = off

#Moves a strip of light back up the neopixel strip
# for i in reversed(range(5, num_pixels + 5)):
	# subsetmove_rev(i)
	# if i < num_pixels:
		# pixels[i] = off

#objDist2 = 100000 #100
pixels.fill(off)


def dispCompass(objHor, objDist, pickedUp):
	xInRange = False
	yInRange = False
	pickedUp = False
	
	pixels.fill(off)
	offset = 0
	if 0.0 < abs(objHor) < 10.0:
		yInRange = True
	else:
		offset = round(sqrt(abs(objHor)))
		if  objHor < 0.0:
			offset = -offset
			#The offset cannot be greater than 10 because that's what each section of LEDs is limited to
		if offset > 10:
			offset = 10
		if offset < -10: 
			offset = -10
	if 80.0 < objDist < 96.0:
		xInRange = True
		
	if xInRange == True and yInRange == True:
		flash(blue, 0.05, 0.075, 5)
	# time.sleep(1)
	
	#pickedUp = True
	if pickedUp == True:
		flash(green, 0.05, 0.05, 5)
		
	lowerlimitL = 10 + offset
	detectingAlgae = True # FOR TESTING ONLY
	if detectingAlgae == True: #This makes sure that the lights are only on if the robot is detecting algae
		for i in range(lowerlimitL, lowerlimitL + 2): 
			pixels[i] = red
		for i in range(lowerlimitL + 23, lowerlimitL + 25):
			pixels[i] = red
		for i in range(lowerlimitL + 46, lowerlimitL + 48):
			pixels[i] = red
	else:
		pixels.fill(off)
	pixels.show()
	print(f"Offset = {offset}")

	
# objHor2 = 1000 #1 #For testing purposes
# objDist2 = 10000 #20 #For testing purposes

# sample compass sequence

pixels.fill(off)
dispCompass(1.0, 100.0, False)
time.sleep(1)
dispCompass(20.0, 90.0, False)
time.sleep(1)
dispCompass(250.0, 50.0, False)
time.sleep(1)
dispCompass(-250.0, 200.0, False)
time.sleep(1)
pixels.fill(off)
pixels.show()


#network tables value loop
while True:
    time.sleep(0.1)
    getHoriz = objHor.get()
    getDist = objDist.get()
    getAlgaeDet = detectingAlgae.get()
    print(f"horizdist = {getHoriz} dist = {getDist} detecting = {getAlgaeDet}")
    dispCompass(getHoriz, getDist, getAlgaeDet)

