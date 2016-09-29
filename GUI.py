import Tkinter as tk
import util
import glob

glob.loadConfig()

def sequence(*functions):
    def func(*args, **kwargs):
        return_value = None
        for function in functions:
            return_value = function(*args, **kwargs)
        return return_value
    return func

#Set active project, then update GUI elements
def dispatchActiveProject( _arg ):
	util.setActiveProject( _arg )
	txt_curdir.configure(state = tk.NORMAL)
	txt_curdir.delete( "1.0", tk.END )
	txt_curdir.insert(tk.END, "Active Project : " + glob.globs["PROJECT_ROOT"])
	txt_curdir.configure(state = tk.DISABLED)

def updateText(_item, _string):
	_item.configure(state = tk.NORMAL)
	_item.delete( "1.0", tk.END )
	_item.insert(tk.END, _string)
	_item.configure(state = tk.DISABLED)

def genAssetText():
	return "Active Asset : " + glob.globs["CUR_ASSET"] + "\nStage : " + glob.g_PRODUCTION_STAGES[util.getAssetStage( glob.globs["CUR_ASSET"] )] + "\n"

#Set active asset, then update GUI elements
def dispatchSetActiveAsset( _arg ):
	util.setActiveAsset( _arg )
	updateText(txt_curassdir, genAssetText())

#Run a command on an asset, update GUI
def dispatchActiveAsset( _cmd ):
	_cmd()
	updateText(txt_curassdir, genAssetText())

def closeWindow( _win ):
	_win.destroy()	

def confirmationYes(_win, _cmd, _update):
	_cmd()
	closeWindow( _win )
	
	#fuck me I feel ill looking at this
	if _update:
		updateText(txt_curassdir, genAssetText())

def confirmation( _cmd, _update ):
	root = tk.Tk()
	root.minsize(width = 256, height = 128)
	root.maxsize(width = 256, height = 128)
	root.grid()  
	txt = tk.Text(root, height = 2, width = 256)
	txt.pack()
	txt.insert(tk.END, "Whoa! Are you sure?")
	txt.configure(state = tk.DISABLED)
	
	frm_yesno = tk.Frame(root)
	frm_yesno.pack()
	
	btn_yes = tk.Button(root, text = 'Yes', command = lambda : confirmationYes( root, _cmd, _update ))
	btn_yes.pack(in_ = frm_yesno, side = tk.LEFT)

	btn_no = tk.Button(root, text = 'No', command = lambda : closeWindow( root ))
	btn_no.pack(in_ = frm_yesno, side = tk.LEFT)	

root = tk.Tk()
root.title('Project Manager')    
root.minsize(width = 512, height = 512)
root.maxsize(width = 512, height = 512)
root.grid()  

#Projects
txt_curdir = tk.Text(root, height = 2, width = 512)
txt_curdir.pack()
txt_curdir.insert(tk.END, "Active Project : " + glob.globs["PROJECT_ROOT"])
txt_curdir.configure(state = tk.DISABLED)

frm_selproj = tk.Frame(root)
frm_selproj.pack()

txt_projdir = tk.Text(frm_selproj, height = 1, width = 48)
txt_projdir.pack(in_ = frm_selproj, side = tk.LEFT)
txt_projdir.insert(tk.END, glob.globs["PROJECT_ROOT"])

btn_setactiveproj = tk.Button(frm_selproj, text = 'Set Active Project', command = lambda : dispatchActiveProject( txt_projdir.get("1.0", tk.END) ) )
btn_setactiveproj.pack(in_ = frm_selproj, side = tk.LEFT)

frm_manipproj = tk.Frame(root)
frm_manipproj.pack()

btn_createproj = tk.Button(root, text = 'Create', command = lambda : util.createProject( glob.globs["PROJECT_ROOT"] ))
btn_createproj.pack(in_ = frm_manipproj, side = tk.LEFT)

btn_deleteproj = tk.Button(root, text = 'Delete', command = lambda : confirmation( util.deleteProject, False ) )
btn_deleteproj.pack(in_ = frm_manipproj, side = tk.LEFT)

btn_backupproj = tk.Button(root, text = 'Backup', command = util.backupProject )
btn_backupproj.pack(in_ = frm_manipproj, side = tk.LEFT)


#Assets
txt_curassdir = tk.Text(root, height = 8, width = 512)
txt_curassdir.pack()
txt_curassdir.insert(tk.END, "Active Asset : " + glob.globs["CUR_ASSET"] + "\n")
txt_curassdir.insert(tk.END, "Stage : " + glob.g_PRODUCTION_STAGES[util.getAssetStage( glob.globs["CUR_ASSET"] )] + "\n")
txt_curassdir.configure(state = tk.DISABLED)

frm_selass = tk.Frame(root)
frm_selass.pack()

txt_assdir = tk.Text(frm_selass, height = 1, width = 48)
txt_assdir.pack(in_ = frm_selass, side = tk.LEFT)
txt_assdir.insert(tk.END, glob.globs["CUR_ASSET"])

btn_setactiveass = tk.Button(frm_selass, text = 'Set Active Asset', command = lambda : dispatchSetActiveAsset( txt_assdir.get("1.0", tk.END) ) )
btn_setactiveass.pack(in_ = frm_selass, side = tk.LEFT)

frm_manipass = tk.Frame(root)
frm_manipass.pack()

btn_createass = tk.Button(root, text = 'Create', command = lambda : dispatchActiveAsset( util.createAsset ))
btn_createass.pack(in_ = frm_manipass, side = tk.LEFT)

btn_promoass = tk.Button(root, text = 'Promote', command = lambda : dispatchActiveAsset( util.promoteAsset ))
btn_promoass.pack(in_ = frm_manipass, side = tk.LEFT)

btn_deleteass = tk.Button(root, text = 'Delete', command = lambda : confirmation( util.deleteAsset, True ))
btn_deleteass.pack(in_ = frm_manipass, side = tk.LEFT)

btn_backupass = tk.Button(root, text = 'Backup', command = quit)
btn_backupass.pack(in_ = frm_manipass, side = tk.LEFT)

btn_adddepass = tk.Button(root, text = 'Add dependancy', command = lambda : sequence(util.addDependancy( txt_assdir.get("1.0", tk.END) ), updateText(txt_curassdir, genAssetText())))
btn_adddepass.pack(in_ = frm_manipass, side = tk.LEFT)


quitButton = tk.Button(root, text = 'Quit', command = quit)            
quitButton.pack()


root.mainloop()                    


          
