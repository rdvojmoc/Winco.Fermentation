import logging
import sys, os, getopt, time, signal, json
import losantHelper
from probe import Probe

dirName = os.path.dirname(os.path.abspath(__file__))
logger = logging.getLogger()
secrets = {}
settings = {}

# load modprobe drivers
os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')

# function to run before ending the program
def endMeasurements():
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
	
	fh = logging.FileHandler('/'.join([dirName,'Winco.Fermentation.log']))
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
	
	wellTempProbe = Probe('/sys/bus/w1/devices/28-000004d029cc/w1_slave')
	outsideTempProbe = Probe('/sys/bus/w1/devices/28-000004d109a8/w1_slave')
	vineBottomTempProbe = Probe('/sys/bus/w1/devices/28-031683b233ff/w1_slave')
	
	logger.info("Initialization done.");

	while True:
		# get a reading from the plant
		state = {"OutsideTemperature": outsideTempProbe.read_temp(), "WellWaterTemperature": wellTempProbe.read_temp(), "VineTemeperatureBottom": vineBottomTempProbe.read_temp()}

		logger.debug(state)
		
		losantHelper.sendMeasurement(state)
		
		# delay between readings
		time.sleep(10)
	
	#close
	endMeasurements()

	
if __name__ == "__main__":
	mainProgram()
