import os
import sys
import subprocess

g_unix_file_to_bash = { 
"ma": "goMaya", 
"mb": "goMaya" 
	}

def openFile( _path ):
	if sys.platform.startswith('linux'):
		ext = _path.split('.')[-1]
		if ext in g_unix_file_to_bash:
			subprocess.call([g_unix_file_to_bash[ext], _path])
		else:
			subprocess.call(["xdg-open", _path])
	else:
		os.startfile(_path)
	
