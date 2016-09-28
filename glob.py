PROJECT_ROOT = ""

global varrefs
varrefs = {"PROJECT_ROOT" : PROJECT_ROOT}

def loadConfig():
	print "load config call"
	with open("config.txt") as conf:
		for line in conf:
			lspl = line.split(' ')
			print lspl
			varrefs[ lspl[0] ] = lspl[1]
			print varrefs
