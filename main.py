import serial
import logging
import sys, os, getopt, time, signal, json
import losantHelper

dirName = os.path.dirname(os.path.abspath(__file__))
logger = logging.getLogger('Winco.Fermentation')
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
	logger.info("Service stopped.")

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

def createLogger():
	# create file handler which logs even debug messages
	logger.setLevel(logging.DEBUG);
	
	fh = logging.FileHandler('Winco.Fermentation.log')
	fh.setLevel(logging.DEBUG)
	
	formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
	fh.setFormatter(formatter)
	# add the handlers to the logger
	logger.addHandler(fh)


def mainProgram():
	createLogger()

	logger.info("Starting wine fermentation data collection...")
	
	secrets = loadJSONConfig('/'.join([dirName, "secrets.json"]))
	settings = loadJSONConfig('/'.join([dirName, "settings.json"]))

	losantHelper.init(secrets["deviceId"], secrets["key"], secrets["secret"])
	
	logger.info("Initialization done.");

	while True:
		# get a reading from the plant
		serialPort.write('r')
		
		state = {"OutsideTemperature": serialPort.readline(), "WellWaterTemperature": serialPort.readline()}
		
		logger.debug(state)
		
		losantHelper.sendMeasurement(state)
		
		# delay between readings
		time.sleep(20)
	
	#close serial
	endMeasurements()

if __name__ == "__main__":
	mainProgram()