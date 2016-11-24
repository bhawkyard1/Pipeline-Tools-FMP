import os
import subprocess
import glob
import util

#http://olivermarshall.net/how-to-upload-a-file-to-google-drive-from-the-command-line/

def pull():
	print "Pulling latest project version..."
	util.deleteProject()
	cmd = "~/gdrive download " + glob.globs["ONLINE_ROOT"] + '/ -r'# + " --path " + glob.globs["PROJECT_ROOT"]
	subprocess.Popen( [cmd], shell = True ).wait()
	util.log( glob.globs["PROJECT_ROOT"], "Project pulled." )

def push():
	print "Pushing project to online repo..."
	for root, dirs, files in os.walk( glob.globs["PROJECT_ROOT"] + "/production" ):
		files = []
		for dir in dirs:
			rp = os.path.relpath( dir, glob.globs["PROJECT_ROOT"] )
			print "checking " + root + ", " + rp + ", " + dir + " " + util.getConfigValue( glob.assetProductionPath( dir ), "CHECKEDOUT" )
			if util.getConfigValue( glob.assetProductionPath( dir ), "CHECKEDOUT" ) == "True":
				pass
				#upload( rp, rp )
				
	print "done"
	#cmd = "~/gdrive upload " + glob.globs["PROJECT_ROOT"] + '/ -r'# + " --path " + glob.globs["ONLINE_ROOT"]
	#print cmd
	#util.log( glob.globs["PROJECT_ROOT"], "Project pushed." )
	#subprocess.Popen( [cmd], shell = True ).wait(
		
def upload( _localPath, _remotePath ):
	print "Uploading " + _localPath + " to " + _remotePath
	cmd = "~/gdrive upload " + _localPath + '/ -r' + " --p " + _remotePath
	subprocess.Popen( [cmd], shell = True ).wait()
