import sys
import platform

if platform.system() == "Linux":
	sys.path.append("/public/devel/2015/gaffer/lib/python2.7/lib-tk")
	sys.path.append("/opt/realflow/lib/python/lib-dynload")
	sys.path.append("~/tk8.6.6/unix")
	
if platform.system() == "Linux":
	import gd_unix as gd
elif platform.system() == "Windows":
	import gd_win as gd
	
reload(gd)
	
import Tkinter as tk
import util
import glob
import strings

curAssetName = glob.curAssetName
curAssetProductionPath = glob.curAssetProductionPath

glob.loadConfig()

def sequence(*functions):
    def func(*args, **kwargs):
        return_value = None
        for function in functions:
            return_value = function(*args, **kwargs)
        return return_value
    return func
    
def closeWindow( _win ):
	_win.destroy()	
	
def push():
	local = strings.dirfmt(txt_localdirset.get("1.0", tk.END))
	remote = strings.dirfmt(txt_remotedirset.get("1.0", tk.END))
	print "Pushing " + local + " to " + remote
	gd.upsync( '"' + local + '"', remote )
	
def pull():
	gd.downsync( driveobj( txt_remotedirset.get("1.0", tk.END).split('/')[-1] ).calcID().getID(), txt_remotedirset.get("1.0", tk.END) )

root = tk.Tk()
root.title('Sync Folder Tool')    
root.minsize(width = 512, height = 128)
root.maxsize(width = 512, height = 128)
root.grid()  

frm_local = tk.Frame(root)
frm_local.pack()

txt_localdir = tk.Text(frm_local, height = 2, width = 16)
txt_localdir.pack(in_ = frm_local, side = tk.LEFT)
txt_localdir.insert(tk.END, "Local path")
txt_localdir.configure(state = tk.DISABLED)

txt_localdirset = tk.Text(frm_local, height = 2, width = 256)
txt_localdirset.pack(in_ = frm_local, side = tk.LEFT)
txt_localdirset.insert(tk.END, glob.globs["PROJECT_ROOT"])

frm_remote = tk.Frame(root)
frm_remote.pack()

txt_remotedir = tk.Text(frm_remote, height = 2, width = 16)
txt_remotedir.pack(in_ = frm_remote, side = tk.LEFT)
txt_remotedir.insert(tk.END, "Remote path")
txt_remotedir.configure(state = tk.DISABLED)

txt_remotedirset = tk.Text(frm_remote, height = 2, width = 256)
txt_remotedirset.pack(in_ = frm_remote, side = tk.LEFT)
txt_remotedirset.insert(tk.END, glob.globs["ONLINE_ROOT"])

frm_btns = tk.Frame(root)
frm_btns.pack()

btn_push = tk.Button(frm_btns, text = 'Push', width = 30, command = push )
btn_push.pack(in_ = frm_btns, side = tk.RIGHT)

btn_pull = tk.Button(frm_btns, text = 'Pull', width = 30, command = pull )
btn_pull.pack(in_ = frm_btns, side = tk.RIGHT)

quitButton = tk.Button(root, text = 'Quit', command = quit)            
quitButton.pack()

root.mainloop()     
