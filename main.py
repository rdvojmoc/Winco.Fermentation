import serial
import sys, os, getopt, time, signal, json
import losantHelper

dirName = os.path.dirname(os.path.abspath(__file__))
secrets = {}
settings = {}

# initialize the serial port
serialPort = serial.Serial('/dev/ttyS1', 9600, timeout=2)
if serialPort.isOpen() == False:
	print("ERROR: Failed to initialize serial port!")
	exit()

# function to close the serial port
def closePort():
	if serialPort.isOpen():
		serialPort.close()

# function to run before ending the program
def endMeasurements():
	closePort()

# Signal interrupt handler
def signalHandler(signal, frame):
	endMeasurements()
	sys.exit()

def loadJSONConfig(filePath):
	configuration = {};
	with open( filePath ) as f:
		try:
			configuration = json.load(f)
		except:
			print("ERROR: expecting JSON file")
			sys.exit()
	return configuration
	
# define a signal to run a function when ctrl+c is pressed
signal.signal(signal.SIGINT, signalHandler)

def mainProgram():
	print("Starting wine fermentation data collection...");
	
	secrets = loadJSONConfig('/'.join([dirName, "secrets.json"]))
	settings = loadJSONConfig('/'.join([dirName, "settings.json"]))

	losantHelper.init(secrets["deviceId"], secrets["key"], secrets["secret"])
	
	print("Initialization done.")

	while True:
		# get a reading from the plant
		serialPort.write('r')
		
		state = {"OutsideTemperature": serialPort.readline(), "WellWaterTemperature": serialPort.readline()}
		
		losantHelper.sendMeasurement(state)
		
		# delay between readings
		time.sleep(20)
	
	#close serial
	endMeasurements()

if __name__ == "__main__":
	mainProgram()