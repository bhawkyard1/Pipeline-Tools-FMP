import os
import shutil
import zipfile
import datetime
import tempfile
import getpass

import glob
import strings

def genTimeStamp():
	day = datetime.date.today()
	hour = datetime.datetime.now()
	
	return str(day.year) + "-" + str(day.month) + "-" + str(day.day) + "-" + str(hour.hour) + "h" + str(hour.minute) + "m" + str(hour.second) + "s"
	
def log( _path, _msg ):
	f = open( _path + "/log.txt", 'a' )
	f.write(getpass.getuser() + " @ " + genTimeStamp() + " : " + _msg + '\n')
	f.close()

def createTextFile( _name ):
	f = open( _name, 'a' )
	f.close()

#0 : file path
#1 : config key to search for
#2 : value to set to
def setConfigValue( _path, _key, _val ):
	#Create temp file
	f, fname = tempfile.mkstemp()
	with open(fname,'w') as new_file:
		with open( _path ) as old_file:
			for line in old_file:
				if strings.dirfmt(line.split( ' ' )[0]) == _key:
					new_file.write( _key + ' ' + _val + '\n' )
				else:
					new_file.write( line )
					
	new_file.close()
	os.close(f)
	#Remove original file
	os.remove( _path )
	#Move new file
	shutil.move(fname, os.path.abspath( _path ) )
	
#Reads a config file and appends to a set of values held by a key	
def appendConfigValue( _path, _key, _toAppend ):
	#Create temp file
	f, fname = tempfile.mkstemp()
	with open(fname,'w') as new_file:
		with open( _path ) as old_file:
			for line in old_file:
				splitLine = line.split(' ')
				if strings.dirfmt(splitLine[0]) == _key:
					orig = ""
					if len(splitLine) > 1:
						orig = strings.dirfmt(splitLine[1]) + ","
					new_file.write( _key + ' ' + orig + ',' + _toAppend + '\n' )
					new_file.write( _key + ' ' + orig + ',' + _toAppend + '\n' )
				else:
					new_file.write( line )
					
	new_file.close()
	os.close(f)
	#Remove original file
	os.remove( _path )
	#Move new file
	shutil.move(fname, os.path.abspath( _path ) )

#0 : file path
#1 : config key to search for  
def getConfigValue( _path, _key ):
	val = None
	with open( _path, 'r') as read:
		for line in read:
			lspl = line.split(' ')
			if lspl[0] == _key and len(lspl) > 1:
				val = lspl[1]
		if val == None:
			return None
					
	read.close()
    
	return val.splitlines()[0]
    
#0 : project path
def setActiveProject( _path ):
	_path = strings.dirfmt(_path)
	print "Setting active project to " + _path

	setConfigValue( "config.txt", "PROJECT_ROOT", _path ) 
	glob.globs["PROJECT_ROOT"] = _path
    
#0 : path
def createProject ( _path ):
	#Format path
	_path = strings.dirfmt(_path)
	
	print "Creating new project " + _path

	if not folderExists( _path ):
		os.mkdir( _path )
		os.mkdir( _path + "/production" )
		os.mkdir( _path + "/approval" )
		os.mkdir( _path + "/implementation" )
		setConfigValue( "config.txt", "PROJECT_ROOT", _path )
		glob.PROJECT_ROOT = _path
		createTextFile( _path + "/config.txt" )
		createTextFile( _path + "/log.txt" )
		log( _path, "Project created!")
	else:
		respose = raw_input( "This project already exists! Would you like to overwrite?" )
		#TO DO string similarity checks
	
#Deletes active project
def deleteProject ():
	shutil.rmtree( glob.globs["PROJECT_ROOT"], ignore_errors = True )

#Backs up active project
def backupProject():
	path = strings.dirfmt( glob.globs["PROJECT_ROOT"] )
	stamp = "(BACKUP-" + genTimeStamp()
	
	print "Backing up project " + path + " to " + path + stamp
	
	log( path, "Project backed up!" )
	shutil.copytree( path, path + stamp )
	shutil.make_archive( path + stamp, 'zip', path )
	shutil.rmtree( path + stamp )
	
#0 : project path
def setActiveAsset( _asset ):
	_asset = strings.dirfmt( _asset )
	print "Setting active asset to " + _asset

	setConfigValue( "config.txt", "CUR_ASSET", _asset ) 
	glob.globs["CUR_ASSET"] = _asset

#0 : asset name
def createAsset():
	_name = strings.dirfmt( glob.globs["CUR_ASSET"] )
	print "Creating asset " + _name
	dst = glob.globs["PROJECT_ROOT"] + "/production/" + _name
	os.mkdir( dst )
	f = open( dst + "/config.txt", 'a' )
	f.write("FLINK\nBLINK\nDEPENDENCIES")
	f.close()
	f = open( dst + "/desc.txt", 'a' )
	f.write("Describe your asset here...")
	f.close()
	createTextFile( dst + "/log.txt" )
	
	log( glob.globs["PROJECT_ROOT"], "Asset " + _name + " created!" )
	log( dst, "Asset created!" )

def deleteAssetStage( _asset, _stage ):
	#To do fix links
	shutil.rmtree( glob.globs["PROJECT_ROOT"] + '/' + glob.g_PRODUCTION_STAGES[_stage] + '/' + _asset, ignore_errors = True )
	
def deleteAsset():
	stage = getAssetStage( glob.globs["CUR_ASSET"] ) + 1
	for i in range( stage ):
		deleteAssetStage( glob.globs["CUR_ASSET"], i )
	log( glob.globs["PROJECT_ROOT"], "Asset " + glob.globs["CUR_ASSET"] + " deleted!" )
	
#cur_asset is dependant on _asset
def addDependancy( _asset ):
	appendConfigValue( glob.globs["PROJECT_ROOT"] + "/production/" + glob.globs["CUR_ASSET"] + "/config.txt", "DEPENDENCIES", _asset )
	print glob.globs["CUR_ASSET"] + " is now dependant on " + _asset
	log( glob.globs["PROJECT_ROOT"] + "/production/" + glob.globs["CUR_ASSET"], "Now dependant on asset " + _asset )
	log( glob.globs["PROJECT_ROOT"], glob.globs["CUR_ASSET"] + " has become dependant on " + _asset )
	
def backupAsset ( _args ):
	pass

#Forwards-link
#Gets the most promoted version of an asset, as a path.
#Depends on config.txt links being in order	
def flink( _asset ):
	_asset = strings.dirfmt( _asset )
	return getConfigValue( _asset + "/config.txt", "FLINK" )
	
def getAssetStage( _asset ):
	#Check asset exists
	stage = 0
		
	if len(_asset) == 0 or not folderExists( glob.globs["PROJECT_ROOT"] + "/production/" + _asset ):
		return stage
	
	stage = 1
	fl = flink( glob.globs["PROJECT_ROOT"] + "/production/" + _asset )
	
	while fl != None:
		fl = flink(fl)
		stage += 1
		
	return stage
	
#0 : Asset name
def promoteAsset ():
	_asset = glob.globs["CUR_ASSET"]
	stage = getAssetStage( _asset )
	if stage == 3:
		print "Failed : Asset already prepared for implementation!"
		return	
	
	print "Promoting " + _asset + " to " + glob.g_PRODUCTION_STAGES[stage + 1]
		
	src = glob.g_PRODUCTION_STAGES[stage]
	src = glob.globs["PROJECT_ROOT"] + strings.slashes(src, True, True) + _asset
	dst = glob.g_PRODUCTION_STAGES[stage + 1]
	dst = glob.globs["PROJECT_ROOT"] + strings.slashes(dst, True, True) + _asset
	
	shutil.copytree( src, dst )	
	
	setConfigValue( src + "/config.txt", "FLINK", dst)
	setConfigValue( dst + "/config.txt", "BLINK", src)
	
	log( glob.globs["PROJECT_ROOT"] + "/production/" + _asset, "Asset promoted to " + glob.g_PRODUCTION_STAGES[stage + 1] )
	log( glob.globs["PROJECT_ROOT"], "Asset " + _asset + " promoted to " + glob.g_PRODUCTION_STAGES[stage + 1] )

def folderExists ( _path ):
	return os.path.exists( _path )

def fileExists( _path ):
	return os.path.isfile( _path )
