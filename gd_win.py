import subprocess
import os

cwd = os.getcwd()
gdcall = '"' + cwd + "\\gdrive" + '"'

def get(_name):
	print "get()"
	return subprocess.check_output( gdcall + " list -m 9999 | findstr " + '"' + _name + '"' )
	
def getChildren(_id):
	print "Getting children of " + _id
	line = subprocess.check_output( gdcall + " list --query " + '"' + "'" + _id + "'" + " in parents" + '"')
	print "Children are " + line
	return line.split('\n')
	
def getID(_name):
	print "Getting ID of " + _name
	line = subprocess.check_output( gdcall + " list -m 9999 | findstr " + '"' + _name + '"' )
	return line.split(' ')[0]

def resolvePath( _path ):
	print "Resolving path " + _path	
	spl = _path.split('/')
	id = 'root'
	context = getChildren( id )
	#Nested things yeah
	for i in spl:
		for line in context:
			if i in line:
				id = line.split(' ')[0]
				break
		context = getChildren( id )
	return id
	
def upsync( _local, _remote ):
	id = ""
	try:
		id = resolvePath( _remote )
	except:
		print "Calling " + gdcall + ' mkdir ' + _remote
		subprocess.Popen( gdcall + ' mkdir ' + _remote ).wait()
		id = resolvePath( _remote )
	cmd = gdcall + " sync upload " + _local + " " + id
	print "Calling " + cmd
	subprocess.Popen( cmd ).wait()
	
def downsync( _remote, _local ):
	cmd = gdcall + " sync download --keep-remote " + _remote + " " + _local
	subprocess.Popen( cmd, shell = True ).wait()
