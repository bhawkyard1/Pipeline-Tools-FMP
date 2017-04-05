import subprocess

def get(name):
	return subprocess.check_output( ["~/gdrive list -m 9999 | grep -w " + name], shell = True )
	
def getChildren( _id ):
	line = subprocess.check_output( ["~/gdrive list --query " + '"' + "'" + _id + "'" + " in parents" + '"'], shell = True )
	return line.split('\n')
	
def getID( _path ):
	line = subprocess.check_output( ["~/gdrive list -m 9999 | grep -w " + _path], shell = True )
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
	fid = resolvePath( _remote )

	if fid == 'root':
		print "Creating folder " + _remote + "!"
		subprocess.Popen( ['~/gdrive mkdir ' + _remote], shell = True ).wait()
		fid = resolvePath( _remote )
	cmd = "~/gdrive sync upload " + _local + " " + fid
	print "Calling " + cmd
	#subprocess.Popen( [cmd], shell = True ).wait()
	
	
def downsync( _remote, _local ):
	cmd = "~/gdrive sync download --keep-remote " + _remote + " " + _local
	print "Calling " + cmd
	subprocess.Popen( [cmd], shell = True ).wait()

def query(fid):
	cmd = "~/gdrive info " + fid
	print "Calling " + cmd
	subprocess.Popen( [cmd], shell = True ).wait()
