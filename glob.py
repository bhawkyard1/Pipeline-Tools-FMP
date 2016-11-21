import strings

globs = {
	"PROJECT_ROOT" : "",
	"CUR_ASSET" : "",
	"ONLINE_ROOT" : ""
		}

g_PRODUCTION_STAGES = ["none", "production", "approval", "implementation"]

def loadConfig():
	with open("config.txt") as conf:
		for line in conf:
			lspl = line.split(' ')
			if len(lspl) > 1:
				globs[lspl[0]] = strings.dirfmt(lspl[1])

def curAsset():
	return globs["PROJECT_ROOT"] + "/production/" + globs["CUR_ASSET"]
	
def curProject():
	return globs["PROJECT_ROOT"]
