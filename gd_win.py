import subprocess
import os

cwd = os.getcwd()
gdcall = '"' + cwd + "\\gdrive" + '"'

def get(_name):
	print "get()"
	return subprocess.check_output( gdcall + " list -m 9999 | findstr " + '"' + _name + '"' )
	
def getChildren(_id):
	line = subprocess.check_output( gdcall + " list --query " + '"' + "'" + _id + "'" + " in parents" + '"')
	return line.split('\n')
	
def getID(_name):
	print "getID -> " + gdcall + " list -m 9999 | findstr " + '"' + _name + '"'
	line = subprocess.check_output( gdcall + " list -m 9999 | findstr " + '"' + _name + '"' )
	return line.split(' ')[0]

def resolvePath( _path ):	
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
		subprocess.Popen( gdcall + ' mkdir ' + _remote, shell = True ).wait()
		id = resolvePath( _remote )
	print "HERE!"
	cmd = gdcall + " sync upload " + _local + " " + id
	subprocess.Popen( cmd, shell = True ).wait()
	
def downsync( _remote, _local ):
	cmd = gdcall + " sync download --keep-remote " + _remote + " " + _local
	subprocess.Popen( cmd, shell = True ).wait()
