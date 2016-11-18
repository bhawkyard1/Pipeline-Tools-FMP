import os
import glob
import util

def pull():
	util.deleteProject()
	os.bash( "gdrive download " + glob.globs["ONLINE_ROOT"] + " --path " + glob.globs["PROJECT_ROOT"] )

def push():
	os.bash( "gdrive download " + glob.globs["PROJECT_ROOT"] + " --path " + glob.globs["ONLINE_ROOT"]
