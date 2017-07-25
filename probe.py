import time

class Probe(object):
	def __init__(self, address):
		self._address = address
	
	
	def temp_raw(self):
		f = open(self._address, 'r')
		lines = f.readlines()
		f.close()
		return lines
	
	def read_temp(self):
		lines = self.temp_raw()
		while lines[0].strip()[-3:] != 'YES':
			time.sleep(0.2)
			lines = temp_raw()
		temp_output = lines[1].find('t=')
		if temp_output != -1:
			temp_string = lines[1].strip()[temp_output+2:]
			temp_c = float(temp_string) / 1000.0
			temp_f = temp_c * 9.0 / 5.0 + 32.0
			return temp_c