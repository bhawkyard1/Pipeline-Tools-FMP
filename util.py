import os
import shutil
import zipfile
import datetime
import getpass
import file

import glob
import strings

curAsset = glob.curAsset
curProject = glob.curProject

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
	temp = open("temp.txt", 'w')
	with open( _path ) as old_file:
		for line in old_file:
			if strings.dirfmt(line.split( ' ' )[0]) == _key:
				temp.write( _key + ' ' + _val + '\n' )
			else:
				temp.write( line )
					
	temp.close()
	#Remove original file
	os.remove( _path )
	#Move new file
	shutil.move("temp.txt", os.path.abspath( _path ) )
	
#Reads a config file and appends to a set of values held by a key	
def appendConfigValue( _path, _key, _toAppend ):
	#Create temp file
	temp = open("temp.txt", 'w')
	with open( _path ) as old_file:
		for line in old_file:
			splitLine = line.split(' ')
			if strings.dirfmt(splitLine[0]) == _key:
				orig = ""
				if len(splitLine) > 1:
					orig = strings.dirfmt(splitLine[1]) + ","
				temp.write( _key + ' ' + orig + ',' + _toAppend + '\n' )
			else:
				temp.write( line )
					
	temp.close()
	#Remove original file
	os.remove( _path )
	#Move new file
	shutil.move("temp.txt", os.path.abspath( _path ) )

#0 : file path
#1 : config key to search for  
def getConfigValue( _path, _key ):
	val = ""
	if not fileExists( _path ):
		return val
		
	with open( _path, 'r') as read:
		for line in read:
			lspl = line.split(' ')
			if lspl[0] == _key and len(lspl) > 1:
				val = lspl[1]
		if val == "":
			return ""
					
	read.close()
    
	return val.splitlines()[0]

#Returns the asset description.
def getDesc( _asset ):
	desc = glob.globs["PROJECT_ROOT"] + "/production/" + _asset + "/desc.txt"
	data = ""
	if not fileExists( desc ):
		return data
	with open(desc, 'r') as f:
		data = f.read().replace('\n', '')
	return data
	
#Returns a list of assets which depend on _asset
def getDependants( _asset ):
	read = strings.dirfmt( getConfigValue( glob.globs["PROJECT_ROOT"] + "/production/" + _asset + "/config.txt", "DEPENDANTS" ) ).split(',')
	return strings.cleanStringArray( read )
	
#Returns a list of containing _assets dependencies
def getDependencies( _asset ):
	read = strings.dirfmt( getConfigValue( glob.globs["PROJECT_ROOT"] + "/production/" + _asset + "/config.txt", "DEPENDENCIES" ) ).split(',')
	return strings.cleanStringArray( read )
	
#Is _asset1 dependant on _asset2?
def isDependant( _asset1, _asset2 ):
	deps = getDependencies( _asset1 )
	return _asset2 in deps
    
#Sets the active project
def setActiveProject( _path ):
	_path = strings.dirfmt(_path)
	print "Setting active project to " + _path

	setConfigValue( "config.txt", "PROJECT_ROOT", _path ) 
	glob.globs["PROJECT_ROOT"] = _path
    
#Creates a project
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
	f.write("FLINK\nBLINK\nDEPENDENCIES\nDEPENDANTS\nCHECKEDOUT False\n")
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
	#Clean dependencies
	print "Here are the dependencies : "
	print getDependencies( glob.globs["CUR_ASSET"] )
	print "Here are the dependants : "
	print getDependants( glob.globs["CUR_ASSET"] )
	
	#Delete asset across all stages
	stage = getAssetStage( glob.globs["CUR_ASSET"] ) + 1
	for i in range( stage ):
		deleteAssetStage( glob.globs["CUR_ASSET"], i )
		
	#Log event
	log( glob.globs["PROJECT_ROOT"], "Asset " + glob.globs["CUR_ASSET"] + " deleted!" )
	
#cur_asset is dependant on _asset
def addDependancy( _asset ):
	_asset = strings.dirfmt(_asset)
	path = glob.globs["PROJECT_ROOT"] + "/production/"
	
	if _asset == glob.globs["CUR_ASSET"] or not folderExists(path + glob.globs["CUR_ASSET"]) or not folderExists(path + _asset):
		return
	
	#Make cur asset dependant on _asset
	appendConfigValue( glob.globs["PROJECT_ROOT"] + "/production/" + glob.globs["CUR_ASSET"] + "/config.txt", "DEPENDENCIES", _asset )
	#Add cur asset to _asset's dependants
	appendConfigValue( glob.globs["PROJECT_ROOT"] + "/production/" + _asset + "/config.txt", "DEPENDANTS", glob.globs["CUR_ASSET"] )
	
	print glob.globs["CUR_ASSET"] + " is now dependant on " + _asset
	log( glob.globs["PROJECT_ROOT"] + "/production/" + glob.globs["CUR_ASSET"], "Now dependant on asset " + _asset )
	log( glob.globs["PROJECT_ROOT"], glob.globs["CUR_ASSET"] + " has become dependant on " + _asset )
	
#cur_asset is no longer dependant on this asset
def removeDependancy( _asset ):
	_asset = strings.dirfmt(_asset)
	path = glob.globs["PROJECT_ROOT"] + "/production/"
	
	if _asset == glob.globs["CUR_ASSET"] or not folderExists(path + glob.globs["CUR_ASSET"]) or not folderExists(path + _asset):
		return
	
	olddeps = getDependencies( glob.globs["CUR_ASSET"] )
	newdeps = ""
	print "DEPENDENCIES : "
	for dep in olddeps:
		print dep + ", " + _asset
		if dep != _asset:
			newdeps += dep + ","
			
	setConfigValue( path + glob.globs["CUR_ASSET"] + "/config.txt", "DEPENDENCIES", newdeps )
		
	print glob.globs["CUR_ASSET"] + " is no longer dependant on " + _asset
	log( glob.globs["PROJECT_ROOT"] + "/production/" + glob.globs["CUR_ASSET"], "No longer dependant on asset " + _asset )
	log( glob.globs["PROJECT_ROOT"], glob.globs["CUR_ASSET"] + " is no longer dependant on " + _asset )	
	
def backupAsset ( _args ):
	pass

#Forwards-link
#Gets the most promoted version of an asset, as a path.
#Depends on config.txt links being in order	
def flink( _path ):
	_path = strings.dirfmt( _path )
	return getConfigValue( _path + "/config.txt", "FLINK" )
	
def getAssetStage( _asset ):
	#Check asset exists
	stage = 0
		
	if len(_asset) == 0 or not folderExists( curAsset() ):
		return stage
	
	stage = 1
	fl = flink( curAsset() )
	
	while fl != "":
		fl = flink(fl)
		stage += 1
		
	return stage
	
#0 : Asset name
def promoteAsset ():
	asset = glob.globs["CUR_ASSET"]
	stage = getAssetStage( asset )
	if stage == 3:
		print "Failed : Asset already prepared for implementation!"
		return	
	
	print "Promoting " + asset + " to " + glob.g_PRODUCTION_STAGES[stage + 1]
		
	src = glob.g_PRODUCTION_STAGES[stage]
	src = glob.globs["PROJECT_ROOT"] + strings.slashes(src, True, True) + asset
	dst = glob.g_PRODUCTION_STAGES[stage + 1]
	dst = glob.globs["PROJECT_ROOT"] + strings.slashes(dst, True, True) + asset
	
	shutil.copytree( src, dst )	
	
	setConfigValue( src + "/config.txt", "FLINK", dst)
	setConfigValue( dst + "/config.txt", "BLINK", src)
	
	log( curAsset(), "Asset promoted to " + glob.g_PRODUCTION_STAGES[stage + 1] )
	log( curProject(), "Asset " + asset + " promoted to " + glob.g_PRODUCTION_STAGES[stage + 1] )
	
def demoteAsset():
	asset = glob.globs["CUR_ASSET"]
	stage = getAssetStage( asset )
	if stage <= 1:
		print "Failed : Asset is not past production stage!"
		return
		
	print "Demoting " + asset + " to " + glob.g_PRODUCTION_STAGES[stage - 1]
	
	deleteAssetStage( asset, stage )
	
	#Asset to have flink altered
	clip = glob.g_PRODUCTION_STAGES[stage - 1]
	clip = curProject() + strings.slashes(clip, True, True) + asset
	
	setConfigValue( clip + "/config.txt", "FLINK", "")
	
	log( curAsset(), "Asset demoted to " + glob.g_PRODUCTION_STAGES[stage - 1] )
	log( curProject(), "Asset " + asset + " demoted to " + glob.g_PRODUCTION_STAGES[stage - 1] )		

def folderExists ( _path ):
	return os.path.exists( _path )

def fileExists( _path ):
	return os.path.isfile( _path )
	
def getCurFiles( ):
	filenames = []
	dupes = []
	for root, dir, files in os.walk( curAsset() ):
		for f in files:
			j = os.path.join( root, f )
			filenames.append( j )
	print filenames
	for Ai, A in enumerate(filenames):
		for Bi, B in enumerate(filenames):
			#Ignore duplicates.
			if A == B:
				continue
			cA = strings.clipFileExtension( A )
			cAname = strings.removeNumbersFromString( cA )
			Aext = A.split('.')[-1]
			cB = strings.clipFileExtension( B )
			cBname = strings.removeNumbersFromString( cB )
			Bext = B.split('.')[-1]
			print "ca is " + cA + " cb is " + cB
			#If the names match this closely, they are probably duplicate files.
			if strings.lev( cAname, cBname ) < 1 and Aext == Bext:
				if cA > cB and B not in dupes:
					dupes.append( B )
				elif cB > cA and A not in dupes:
					dupes.append( A )
	for i in dupes:
		filenames.remove( i )
	for i in filenames:
		print "Opening " + i
		file.openFile( i )
