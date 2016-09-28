import getpass
import util
import strings
import glob
import inspect

commands = { 	
				"createproject" : util.createProject,
				"createasset" : util.createAsset,
				"setactiveproject" : util.setActiveProject
 }

def execute( _command, _args ):
	for cmd in commands:
		if strings.match(cmd, _command, 2):
			commands[cmd](_args)
			return
			
	print "I am sorry, I do not understand."

def run():
	done = False
	while not done:
		cmd = raw_input( "What would you like to do, " + getpass.getuser() + "? " )
		sliced = cmd.split()
		execute( "createproject", ["projects/", "pr1"] )
		execute( "createasset", ["ASS"] )
		#execute( sliced[0], sliced[1:] )

print "Asset manager v0.1"

glob.loadConfig()	

print "Active project is " + glob.globs["PROJECT_ROOT"]
	
run()




