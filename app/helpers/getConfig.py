from configparser import SafeConfigParser
import os
def getConfPart(name, section='main'):
	parser = SafeConfigParser()
	# Get absolute dir for config file
	parser.read(os.path.join(os.path.abspath(os.path.dirname(__file__)), 'config.ini'))
	return parser.get(section, name)