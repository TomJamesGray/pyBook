from configparser import SafeConfigParser
import os
def getConfPart(name, section='main'):
	parser = SafeConfigParser()
	# Get absolute dir for config file
	configLocation = __file__.replace("app/helpers/getConfig.py","config.ini")

	parser.read(configLocation)
	return parser.get(section, name)