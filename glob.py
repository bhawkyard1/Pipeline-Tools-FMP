globs = {"PROJECT_ROOT" : "", "CUR_ASSET" : ""}

def loadConfig():
	with open("config.txt") as conf:
		for line in conf:
			lspl = line.split(' ')
			globs[lspl[0]] = lspl[1]
