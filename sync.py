import platform
import os
import subprocess
import shutil
import glob
import util

if platform.system() == "Linux":
	import gd_unix as gd
elif platform.system() == "Windows":
	import gd_win as gd
	
reload(gd)

#http://olivermarshall.net/how-to-upload-a-file-to-google-drive-from-the-command-line/

class driveobj:
	def __init__( self, _name ):
		self.m_name = _name
		#Don't assign!
		#self.m_id = self.calcID()
		self.calcID()
		
	def getListEntry( self, name ):
		return gd.get(name)
		
	def calcID( self ):
		self.m_id = gd.resolvePath(self.m_name)
		print "id set to " + self.m_id
		
	def getChildren( self ):
		#cmd = "~/gdrive list --query " + '"' + "'" + self.m_id + "'" + " in parents" + '"'
		#line = subprocess.check_output( [cmd], shell = True )
		children = gd.getChildren( self.m_id )
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
	
	gd.downsync( project.getID(), glob.globs["PROJECT_ROOT"] )
	
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
	
	gd.upsync( glob.globs["PROJECT_ROOT"], glob.globs["PROJECT_ROOT"].split('/')[-1] )
	
	shutil.rmtree( glob.globs["PROJECT_ROOT"], ignore_errors = True )
	os.rename( temproot, glob.globs["PROJECT_ROOT"] )
				
	print "Upload complete."
	
