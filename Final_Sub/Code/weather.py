#Imports
import urllib.request
import time
import numpy as np
import pylab
import matplotlib.pyplot as plt
import matplotlib.animation as anim
import datetime
from webiopi.devices.sensor.onewiretemp import DS18S20

"""""""""""
Assign the Temperature sensor

"""""""""
tmp0 = DS18S20(slave="10-000802de680d")




""""""""""
Function to Read The Temperature Data on to Raspberry Pi from embedded web server 

"""""""""

def readTempFar():

	temp = 0
	with urllib.request.urlopen('http://192.168.1.7/temp') as response:
   		temp = response.read()

	temp = temp[13:]
	return round(float(temp[:-2]),2)
	
""""""""""
Function Convert Temperature that was read in from Fahrenheit into Celsius

"""""""""

def readTempCel(): return (readTempFar() - 32.0)/1.8

""""""""""
Function to Read The Humidity Data on to Raspberry Pi from embedded web server 

"""""""""

def readHumid():

	humid = 0
	with urllib.request.urlopen('http://192.168.1.7/humidity') as response:
   		humid = response.read()

	humid = humid[9:]
	return round(float(humid[:-1]),2)
	
""""""""""
Function to print The Temperature and Humidity Data every second for 100 seconds. 
"""""""""

def printData():

	for i in range (1,100):
		
		print("Temperature: ",readTempFar(),"F")
		print("Humidity: ",readHumid())
		time.sleep(1)

""""""""""
Function to write The Temperature and Humidity Data every second for 100 seconds to a file. 
Also writes the data taken from the DS18S20 temperature sensor 
"""""""""
def writeData():

	file = open("Weather_Data3.txt","w")
	file2 = open("Weather_Data4.txt","w")
	
	for i in range(0,1000):

		file.write("Temperature :"+str(readTempCel())+" Humidity :"
				+str(readHumid())+"\n")
		file2.write("Temperature :"+str(tmp0.getCelsius())+"\n")
		time.sleep(1)

	file.close() 

		
	
""""""""""
Function to plot a self updating graph for Temperature and Humidity Data. As well as the temperature from DS18S20 sensor.
"""""""""


def animData():
	
	plotFigure = pylab.figure()
	measurements = []
	#Empty arrays of time and measurement values to plot
	measurements_1 = []
	timeVals = []

	def updatePlot(i):
	
		
		timeVals.append(time.time()-start_time) #Store the current time
		measurements.append(round(readTempCel(), 1))	# Store the measurement
		measurements_1.append(round(readHumid()))
		#measurements_1.append(round(tmp0.getCelsius(),2))
		plotFigure.clear()			# Clear the old plot
		pylab.title("Temperature vs Time")
		pylab.xlabel("Time (seconds)")
		pylab.ylabel("Temperature (Celsius)")
		pylab.plot(timeVals,measurements, label ="DHT22")	# Make the new plot
		#pylab.plot(timeVals,measurements_2, label = "DS18B20")
		pylab.legend()

	
	start_time = time.time()
	ani = anim.FuncAnimation(plotFigure,updatePlot, interval=1000)
	pylab.legend()
	pylab.show()	
	
	return measurements, measurements_1
	
""""""""""
Function to plot a self updating graph for Temperature and Humidity Data. 
As well as a graph of Temperature against Humidity. 
"""""""""
	
def plotF():
	measurements, measurements_1 = animData()
	plt.plot(measurements_1, measurements)
	plt.title("Temperature vs Humidity")
	plt.xlabel("Humidity (A.U)")
	plt.ylabel("Temperature(Celsius)")
	plt.show()


def main():
	
	writeData()
	#animData()
	#plotF()
	return
	
	
main()
	

