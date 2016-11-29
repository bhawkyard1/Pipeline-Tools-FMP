import os
import subprocess
import shutil
import glob
import util

#http://olivermarshall.net/how-to-upload-a-file-to-google-drive-from-the-command-line/

class driveobj:
	def __init__( self, _name ):
		self.m_name = _name
		#Don't assign!
		#self.m_id = self.calcID()
		self.calcID()
		
	def getListEntry( self, name ):
		return subprocess.check_output( ["~/gdrive list -m 9999 | grep -w " + name], shell = True )
		
	def calcID( self ):
		spl = self.m_name.split('/')
		id = 'root'
		context = gdrive_ChildrenFromID( id )
		#Nested things yeah
		for i in spl:
			for line in context:
				if i in line:
					id = line.split(' ')[0]
					break
			context = gdrive_ChildrenFromID( id )
		self.m_id = id
		print "id set to " + self.m_id
		
	def getChildren( self ):
		cmd = "~/gdrive list --query " + '"' + "'" + self.m_id + "'" + " in parents" + '"'
		line = subprocess.check_output( [cmd], shell = True )
		children = line.split('\n')
		#First entry is the header.
		del children[0]
		#Clip to filename
		for idx, child in enumerate(children):
			children[idx] = [i for i in child.split(' ') if i != '']
		children = [i for i in children if i != []]
		return [i[1] for i in children]
		
	def getTimeStamp( self ):
		line = self.getListEntry().split(' ')
		line = [i for i in line if i != '']
		date = i[3]
		time = i[4]
		
	def getID(self):
		return self.m_id
		
	def getName(self):
		return self.m_name
	

def pull():
	print "Pulling latest project version... " + glob.globs["PROJECT_ROOT"].split('/')[-1]
	
	project = driveobj( glob.globs["PROJECT_ROOT"].split('/')[-1] )
	project.calcID()
	
	downsync( project.getID(), glob.globs["PROJECT_ROOT"] )
	
	#projectID = gdrive_IDFromName( glob.globs["PROJECT_ROOT"].split('/')[-1] )
	#temppath = glob.globs["PROJECT_ROOT"] + "_downloading"
	#cmd = "~/gdrive download -r " + project.m_id + " --path " + glob.globs["PROJECT_ROOT"] + "_downloading"
	#subprocess.Popen( [cmd], shell = True ).wait()
	#
	#for root, dirs, files in os.walk( glob.globs["PROJECT_ROOT"] + "/production" ):
	#	files = []
	#	for dir in dirs:
	#		rp = os.path.relpath( glob.globs["PROJECT_ROOT"] + "/production/" + dir, glob.globs["PROJECT_ROOT"] )
	#		ap = os.path.join( root, dir )
	#		if util.getConfigValue( glob.globs["PROJECT_ROOT"] + "/production/" + dir, "CHECKEDOUT" ) == "False" and util.folderExists( temppath + "/production/" + dir ):
	#			util.copyAsset( temppath, dir, glob.globs["PROJECT_ROOT"] )
	#
	#shutil.rmtree( temppath, ignore_errors = True )
	#
	#util.log( glob.globs["PROJECT_ROOT"], "Project pulled." )
	
	print "Download complete."

def push():
	print "Pushing project to online repo..."
	util.log( glob.globs["PROJECT_ROOT"], "Project pushed to online repo." )
	
	#Rename project temporarily
	temproot = glob.globs["PROJECT_ROOT"] + "_uploading"
	os.rename( glob.globs["PROJECT_ROOT"], temproot )
	
	os.makedirs( glob.globs["PROJECT_ROOT"] )
	
	for root, dirs, files in os.walk( temproot + "/production" ):
		files = []
		for dir in dirs:
			rp = os.path.relpath( temproot + "/production/" + dir, temproot )
			ap = os.path.join( root, dir )
			if util.getConfigValue( temproot + "/production/" + dir, "CHECKEDOUT" ) == "True":
				util.setConfigValue( temproot + "/" + rp, "CHECKEDOUT", "False" )
				util.copyAsset( temproot, dir, glob.globs["PROJECT_ROOT"] )
	
	shutil.copy( temproot + "/config.txt", glob.globs["PROJECT_ROOT"] + "/config.txt" )
	shutil.copy( temproot + "/log.txt", glob.globs["PROJECT_ROOT"] + "/log.txt" )
	
	upsync( glob.globs["PROJECT_ROOT"], glob.globs["PROJECT_ROOT"].split('/')[-1] )
	
	shutil.rmtree( glob.globs["PROJECT_ROOT"], ignore_errors = True )
	os.rename( temproot, glob.globs["PROJECT_ROOT"] )
				
	print "Upload complete."

def gdrive_ChildrenFromID( _id ):
	line = subprocess.check_output( ["~/gdrive list --query " + '"' + "'" + _id + "'" + " in parents" + '"'], shell = True )
	return line.split('\n')

def gdrive_IDFromName( _path ):
	line = subprocess.check_output( ["~/gdrive list -m 9999 | grep -w " + _path], shell = True )
	return line.split(' ')[0]
	
def upload( _path ):
	print "Uploading " + _path
	cmd = "~/gdrive upload " + _path + '/ -r'
	subprocess.Popen( [cmd], shell = True ).wait()
	
def upsync( _local, _remote ):
	id = ""
	try:
		id = gdrive_IDFromName( _remote )
	except:
		subprocess.Popen( ['~/gdrive mkdir ' + _remote], shell = True ).wait()
		id = gdrive_IDFromName( _remote )
	print "HERE!"
	cmd = "~/gdrive sync upload " + _local + " " + id
	subprocess.Popen( [cmd], shell = True ).wait()
	
def downsync( _remote, _local ):
	cmd = "~/gdrive sync download " + _remote + " " + _local
	subprocess.Popen( [cmd], shell = True ).wait()
	
