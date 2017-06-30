from losantmqtt import Device

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

