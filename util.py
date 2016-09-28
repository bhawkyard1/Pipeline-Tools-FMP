import os
import shutil
import zipfile
import datetime
import tempfile

def createProject ( _path, _name ):
	print "Creating new project " + _name + " in directory " + _path
	if not fileExists( _path + _name ):
		os.mkdir( _path + _name )
		os.mkdir( _path + _name + "/production" )
		os.mkdir( _path + _name + "/approval" )
		os.mkdir( _path + _name + "/implementation" )
	else:
		respose = raw_input( "This project already exists! Would you like to overwrite?" )
		#TO DO string similarity checks

def deleteProject ( _path ):
	pass
	
def backupProject ( _path ):	
	day = datetime.date.today()
	hour = datetime.datetime.now()
	stamp = "(BACKUP-" + str(day.year) + "-" + str(day.month) + "-" + str(day.day) + "-" + str(hour.hour) + "h" + str(hour.minute) + "m" + str(hour.second) + "s)"
	
	print "Backing up project " + _path + " to " + _path + stamp
	
	shutil.copytree( _path, _path + stamp )
	shutil.make_archive( _path + stamp, 'zip', _path )
	shutil.rmtree( _path + stamp )
	
	
def backupAsset ( _path ):
	pass
	
def submitAsset ( _path ):
	pass
	
def approveAsset ( _path ):
	pass

def folderExists ( _path ):
	return os.path.exists( _path )

def fileExists( _path ):
	pass
	
#_path : file path
#_key : config key to search for
#_value : value to set to
def setConfigValue( _path, _key, _value ):
	#Create temp file
    f, fname = tempfile.mkstemp()
    with open(fname,'w') as new_file:
        with open(_path) as old_file:
            for line in old_file:
				print line.split(' ')[0]
				if line.split( ' ' )[0] == _key:
					new_file.write( _key + ' ' + _value )
				else:
					new_file.write( line )
					
    new_file.close()
    os.close(f)
    #Remove original file
    os.remove(_path)
    #Move new file
    shutil.move(fname, os.path.abspath( _path ) )

createProject( os.path.expanduser("~/"), "my_second_project" )
backupProject( os.path.expanduser("~/") + "my_second_project")
setConfigValue( "config.txt", "PROJECT_ROOT", "ben" )
