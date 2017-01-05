import subprocess

def get(name):
	return subprocess.check_output( ["~/gdrive list -m 9999 | grep -w " + name], shell = True )
	
def getChildren( _id ):
	line = subprocess.check_output( ["~/gdrive list --query " + '"' + "'" + _id + "'" + " in parents" + '"'], shell = True )
	return line.split('\n')
	
def getID( _path ):
	line = subprocess.check_output( ["~/gdrive list -m 9999 | grep -w " + _path], shell = True )
	return line.split(' ')[0]
	
def upsync( _local, _remote ):
	id = ""
	try:
		id = getID( _remote )
	except:
		subprocess.Popen( ['~/gdrive mkdir ' + _remote], shell = True ).wait()
		id = getID( _remote )
	print "HERE!"
	cmd = "~/gdrive sync upload " + _local + " " + id
	subprocess.Popen( [cmd], shell = True ).wait()
	
def downsync( _remote, _local ):
	cmd = "~/gdrive sync download --keep-remote " + _remote + " " + _local
	subprocess.Popen( [cmd], shell = True ).wait()
