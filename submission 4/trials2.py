
#!/usr/bin/python
# Example using a character LCD plate.
import time
import threading

import Adafruit_CharLCD as LCD
import weather

threadlock = threading.Lock()
class myThread (threading.Thread):
	
	

	def __init__(self,threadID,name,q):
		threading.Thread.__init__(self)
		self.threadID = threadID	
		self.name = name
		self.q = q

	def run(self):
		threadlock.acquire()
		while not isButtonPressed():
			self.q()
		threadlock.release()
			
""""""""""
Function returns true if a button is pressed and False otherwise. 
"""""""""

def isButtonPressed():
	for button in buttons:
		if lcd.is_pressed(button[0]):
			return True

	return False

""""""""""
Function which prints Temperature Data with a message if "isButtonPressed" 
function is true and sleeps for 2 seconds if not.
"""""""""
def printTemp():
	if isButtonPressed():
		return
	t = weather.readTempCel()
	lcd.clear()
	lcd.message('Temp is:'+ str(t)+"C")
	if not isButtonPressed():
		time.sleep(2)



""""""""""
Function which prints Humidity Data with a message if "isButtonPressed" 
function is true and sleeps for 2 seconds if not.
"""""""""

def printHumid():
	if isButtonPressed():
		return
	h = weather.readHumid()
	lcd.clear()
	lcd.message('Humidity is:'+ str(h))
	if not isButtonPressed():
		time.sleep(2)
		
""""""""""
Function which prints menu (" Humidity & Temp") with a message 
if "isButtonPressed" function is true and sleeps for 2 seconds if not.
"""""""""

def printMenu():
	if isButtonPressed():
		return
	lcd.clear()
	lcd.message('Humidity & Temp')
	if not isButtonPressed():
		time.sleep(2)
		
		
""""""""""
Assigning 3 different threads to Temp, Humidity and Menu respectively. 
Each thread prints these values with their messages.
"""""""""

thread1 = myThread(1,"Temp_Thread",printTemp)
thread2 = myThread(2,"Humid_Thread",printHumid)
thread3 = myThread(3,"Menu_Thread",printMenu)

""""""""""
Initialize the LCD using the pins 
"""""""""


lcd = LCD.Adafruit_CharLCDPlate()

""""""""""
create some custom characters for fun 
"""""""""


lcd.create_char(1, [2, 3, 2, 2, 14, 30, 12, 0])
lcd.create_char(2, [0, 1, 3, 22, 28, 8, 0, 0])
lcd.create_char(3, [0, 14, 21, 23, 17, 14, 0, 0])
lcd.create_char(4, [31, 17, 10, 4, 10, 17, 31, 0])
lcd.create_char(5, [8, 12, 10, 9, 10, 12, 8, 0])
lcd.create_char(6, [2, 6, 10, 18, 10, 6, 2, 0])
lcd.create_char(7, [31, 17, 21, 21, 21, 21, 17, 31])

""""""""""
Make list of button value, text, and backlight color.
"""""""""


buttons = ( (LCD.SELECT, 'Select', (1,1,1)),
            (LCD.LEFT,   'Temp:'  , (1,0,0)),
             (LCD.UP,     'Humidity:'    , (0,1,0)),
             (LCD.DOWN,   'Humidity:'  , (0,1,0)),
             (LCD.RIGHT,  'Temp:' , (1,0,0)) ) 


print ('Press Ctrl-C to quit.')
lcd.clear()
lcd.message('Humidity & Temp')


""""""""""
Loops through all the buttons and runs the suitable thread depending 
on which button is pressed. If no button is pressed the thread 
will keep on running and hence updating the Data displayed every second.
"""""""""
while True:
	# Loop through each button and check if it is pressed.
	for button in buttons:
		if lcd.is_pressed(button[0]):
			time.sleep(1)
			# Button is pressed, change the message and backlight.
			if 'Temp' in button[1]:
				thread1.run()
			if 'Humidity' in button[1]:
				thread2.run()
			if 'Select' in button[1]:
				thread3.run()
			lcd.set_color(button[2][0], button[2][1], button[2][2])
	

			
			
