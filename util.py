import os
import shutil
import zipfile
import datetime
import tempfile

import glob
import strings

def createTextFile( _name ):
	f = open( _name, 'a' )
	f.close()

#0 : file path
#1 : config key to search for
#2 : value to set to
def setConfigValue( _args ):
	#Create temp file
    f, fname = tempfile.mkstemp()
    with open(fname,'w') as new_file:
        with open(_args[0]) as old_file:
            for line in old_file:
				if line.split( ' ' )[0] == _args[1]:
					new_file.write( _args[1] + ' ' + _args[2] )
				else:
					new_file.write( line )
					
    new_file.close()
    os.close(f)
    #Remove original file
    os.remove(_args[0])
    #Move new file
    shutil.move(fname, os.path.abspath( _args[0] ) )

#0 : file path
#1 : config key to search for  
def getConfigValue( _args ):
	val = None
	with open(_args[0],'w') as read:
		for line in read:
			lspl = line.split(' ')
			if lspl[0] == _args[1] and len(lspl > 1):
				val = lspl[1]
					
	read.close()
    
	return val
    
#0 : project path
def setActiveProject( _args ):
	print "Setting active project to " + _args[0]
	if len(_args) == 0:
		print "No arguments provided, 1 needed!"
		return 
	setConfigValue( ["config.txt", "PROJECT_ROOT", _args[0]] ) 
	glob.globs["PROJECT_ROOT"] = _args[0]
    
#0 : path
def createProject ( _args ):
	#Format path
	_args[0] = strings.dirfmt(_args[0])
	
	print "Creating new project " + _args[0]

	if not folderExists( _args[0] ):
		os.mkdir( _args[0] )
		os.mkdir( _args[0] + "/production" )
		os.mkdir( _args[0] + "/approval" )
		os.mkdir( _args[0] + "/implementation" )
		setConfigValue( ["config.txt", "PROJECT_ROOT", _args[0]] )
		glob.PROJECT_ROOT = _args[0]
		createTextFile( _args[0] + "/config.txt" )
	else:
		respose = raw_input( "This project already exists! Would you like to overwrite?" )
		#TO DO string similarity checks
	
#0 : project path
def deleteProject ( _args ):
	pass

#0 : project path	
def backupProject ( _args ):
	path = ""
	if len(_args[0]) == 0:
		path = glob.PROJECT_ROOT
	else:
		path = _args[0]	
	day = datetime.date.today()
	hour = datetime.datetime.now()
	stamp = "[BACKUP:" + str(day.year) + ":" + str(day.month) + ":" + str(day.day) + "|" + str(hour.hour) + "h:" + str(hour.minute) + "m:" + str(hour.second) + "s]"
	
	print "Backing up project " + path + " to " + path + stamp
	
	shutil.copytree( path, path + stamp )
	shutil.make_archive( path + stamp, 'zip', path )
	shutil.rmtree( path + stamp )
	
#0 : asset name
def createAsset ( _name ):
	dst = glob.globs["PROJECT_ROOT"] + "/production/" + _name[0]
	os.mkdir( dst )
	f = open( dst + "/config.txt", 'a' )
	f.write("FLINK\nBLINK")
	f.close()
	f = open( dst + "/desc.txt", 'a' )
	f.write("Describe your asset here...")
	f.close()
	
def backupAsset ( _args ):
	pass

#Forwards-link
#Gets the most promoted version of an asset, as a path.
#Depends on config.txt links being in order	
def flink( _asset ):
	if len( _asset.split('/') ) < 2:
		_asset = "/production/" + _asset
	return getConfigValue( [glob.globs["PROJECT_ROOT"] + _asset, "FLINK"] )
	
def promoteAsset ( _args ):
	pass

def folderExists ( _path ):
	return os.path.exists( _path )

def fileExists( _path ):
	pass
