import os
import glob
import util

#http://olivermarshall.net/how-to-upload-a-file-to-google-drive-from-the-command-line/

def pull():
	util.deleteProject()
	os.bash( "gdrive download " + glob.globs["ONLINE_ROOT"] + " --path " + glob.globs["PROJECT_ROOT"] )

def push():
	os.bash( "gdrive download " + glob.globs["PROJECT_ROOT"] + " --path " + glob.globs["ONLINE_ROOT"]
