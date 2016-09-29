globs = {"PROJECT_ROOT" : "", "CUR_ASSET" : ""}

def loadConfig():
	with open("config.txt") as conf:
		for line in conf:
			lspl = line.split(' ')
			if len(lspl) > 1:
				globs[lspl[0]] = lspl[1]
