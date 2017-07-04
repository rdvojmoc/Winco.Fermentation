from losantmqtt import Device
import logging

module_logger = logging.getLogger('Winco.Fermentation.losantHelper')

device = None

# initialize mqtt connection with losant
def init(deviceId, key, secret):
	global device
	
	# Construct device
	device = Device(deviceId, key, secret)

	# Connect to Losant.
	device.connect(blocking=False)


# send state measurement to Losant
def sendMeasurement(state):
	device.loop()
	if device.is_connected():
		device.send_state(state)
	else:
		module_logger.debug("Device is not connected!")
