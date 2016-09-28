import getpass
import util
import strings
import glob
import inspect

commands = { 	"createproject" : util.createProject,
				"createasset" : util.createAsset
 }

def execute( _command, _args ):
	for cmd in commands:
		if strings.match(cmd, _command, 2):
			commands[cmd](_args[0], _args[1])
			return
			
	print "I am sorry, I do not understand."

def run():
	done = False
	while not done:
		cmd = raw_input( "What would you like to do, " + getpass.getuser() + "? " )
		sliced = cmd.split()
		execute( sliced[0], sliced[1:] )
		done = True

print "Asset manager v0.1"

glob.loadConfig()	

print "Active project is " + glob.PROJECT_ROOT
	
run()



