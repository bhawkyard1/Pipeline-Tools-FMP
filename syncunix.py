import os
import subprocess
import shutil
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
			rp = os.path.relpath( glob.assetProductionPath( dir ), glob.globs["PROJECT_ROOT"] )
			ap = os.path.join( root, dir )
			if util.getConfigValue( glob.assetProductionPath( dir ), "CHECKEDOUT" ) == "True":
				upload( ap, rp )
				
	print "done"
	#cmd = "~/gdrive upload " + glob.globs["PROJECT_ROOT"] + '/ -r'# + " --path " + glob.globs["ONLINE_ROOT"]
	#print cmd
	#util.log( glob.globs["PROJECT_ROOT"], "Project pushed." )
	#subprocess.Popen( [cmd], shell = True ).wait(

def gdrive_GetID( _path ):
	line = subprocess.check_output( ["~/gdrive list | grep " + _path], shell = True )
	return line.split(' ')[0]
	
def gdrive_MakeDir( _path ):
	folders = _path.split("/")
	curID = ""
	for f in folders:
		curID = subprocess.check_output( ["~/gdrive mkdir " + f], shell = True )
		curID = curID.split(' ')[1]
	
def upload( _absPath, _remotePath ):
	print "Uploading " + _absPath + " to " + _remotePath
	
	parentID = ""
	try:
		parentID = gdrive_GetID( _remotePath )		
	except:
		print "Path does not exist! Creating folders..."
		subprocess.Popen( ["~/gdrive mkdir" + _remotePath], shell = True ).wait()
		parentID = gdrive_GetID( _remotePath )
		
	cmd = "~/gdrive upload " + _absPath + '/ -r' + " --p " + parentID
		
	subprocess.Popen( [cmd], shell = True ).wait()
