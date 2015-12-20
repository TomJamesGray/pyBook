import re
def getArgsBy(argString,regExp,strip=True):
	# Use regexp to split arguments into list
	if strip:
		argString = argString.strip()
	args = re.split(regExp,argString)

	return args