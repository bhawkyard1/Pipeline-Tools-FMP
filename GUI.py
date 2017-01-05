import sys
import platform

if platform.system() == "Linux":
	sys.path.append("/public/devel/2015/gaffer/lib/python2.7/lib-tk")
	sys.path.append("/opt/realflow/lib/python/lib-dynload")
	sys.path.append("~/tk8.6.6/unix")
	
import sync

reload(sync)
	
import Tkinter as tk
import util
import glob

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

def updateTextColour( _bool, _text ):
	col = "salmon"
	if _bool:
		col = "green"
	_text.configure( bg = col )

#This checks whether the current asset has dependants. If it does, we warn the user, and may or may not execute the supplied command.
def dependanciesCheck( _cmd ):
	deps = util.getDependants( glob.globs["CUR_ASSET"] )
	msg = "Uh oh! " + glob.globs["CUR_ASSET"] + " has the following dependants :"
	for i in deps:
		msg += " " + i
	msg += ". Continue?"
	if len(deps) > 0:
		root = tk.Tk()
		root.minsize(width = 384, height = 128)
		root.maxsize(width = 384, height = 128)
		root.grid()  
		txt = tk.Text(root, height = 2, width = 256)
		txt.pack()
		txt.insert(tk.END, msg)
		txt.configure(state = tk.DISABLED)
		
		frm_yesno = tk.Frame(root)
		frm_yesno.pack()
		
		btn_yes = tk.Button(root, text = 'Yes', command = lambda : confirmationYes( root, _cmd ))
		btn_yes.pack(in_ = frm_yesno, side = tk.LEFT)

		btn_no = tk.Button(root, text = 'No', command = lambda : closeWindow( root ))
		btn_no.pack(in_ = frm_yesno, side = tk.LEFT)	
	else:
		_cmd()				

#Set active project, then update GUI elements
def dispatchActiveProject( _arg ):
	util.setActiveProject( _arg )
	txt_curdir.configure(state = tk.NORMAL)
	txt_curdir.delete( "1.0", tk.END )
	txt_curdir.insert(tk.END, "Active Project : " + glob.globs["PROJECT_ROOT"])
	updateTextColour( util.folderExists(glob.globs["PROJECT_ROOT"]), txt_curdir )
	btnProjectDep()
	txt_curdir.configure(state = tk.DISABLED)

def updateText(_item, _string):	
	updateTextColour( util.getConfigValue( curAssetProductionPath(), "CHECKEDOUT" ) == "True", _item )
	_item.configure(state = tk.NORMAL)
	_item.delete( "1.0", tk.END )
	_item.insert(tk.END, _string)
	_item.configure(state = tk.DISABLED)

def genAssetText():
	return ("Active Asset : " + glob.globs["CUR_ASSET"] + 
	"\nChecked Out : " + util.getConfigValue( glob.curAssetProductionPath(), "CHECKEDOUT" ) +
	"\nStage : " + glob.g_PRODUCTION_STAGES[util.getAssetStage( glob.globs["CUR_ASSET"] )] + 
	"\nDependencies : " + str(util.getDependencies( glob.globs["CUR_ASSET"] )).strip('[]') + 
	"\nDependants : " + str(util.getDependants( glob.globs["CUR_ASSET"] )).strip('[]') + 
	"\nDescription : " + util.getDesc( glob.globs["CUR_ASSET"] ) + "\n")

#Run a command on an asset, update GUI
def dispatchActiveAsset( _cmd ):
	_cmd()
	updateText(txt_curassdir, genAssetText())
	btnAssetDep()

def closeWindow( _win ):
	_win.destroy()	

def confirmationYes(_win, _cmd, *_args):
	_cmd( *_args )
	closeWindow( _win )
	#fuck me I feel ill looking at this
	#if _update:
	updateText(txt_curassdir, genAssetText())
	updateTextColour( util.folderExists(glob.globs["PROJECT_ROOT"]), txt_curdir )
	btnProjectDep()

def confirmation( _msg, _cmd, _update, *_args ):
	root = tk.Tk()
	root.minsize(width = 384, height = 128)
	root.maxsize(width = 384, height = 128)
	root.grid()  
	txt = tk.Text(root, height = 2, width = 256)
	txt.pack()
	txt.insert(tk.END, _msg)
	txt.configure(state = tk.DISABLED)
	
	frm_yesno = tk.Frame(root)
	frm_yesno.pack()
	
	btn_yes = tk.Button(root, text = 'Yes', command = lambda : confirmationYes( root, _cmd, *_args ))
	btn_yes.pack(in_ = frm_yesno, side = tk.LEFT)

	btn_no = tk.Button(root, text = 'No', command = lambda : closeWindow( root ))
	btn_no.pack(in_ = frm_yesno, side = tk.LEFT)
	
def btnProjectDep():
	s = None
	print "fexists " + str( util.folderExists( glob.globs["PROJECT_ROOT"] ) )
	if util.folderExists( glob.globs["PROJECT_ROOT"] ):
		s = tk.NORMAL
	else:
		s = tk.DISABLED
	for key in projDependantBtns:
		print "Setting " + key + " to " + str(s)
		projDependantBtns[key].configure(state = s)
	btnAssetDep()
		
def btnAssetDep():
	s = None
	if curAssetName() != "" and util.folderExists( curAssetProductionPath() ):
		s = tk.NORMAL
	else:
		s = tk.DISABLED
	for key in assDependantBtns:
		assDependantBtns[key].configure(state = s)

assDependantBtns = {}
projDependantBtns = {}

root = tk.Tk()
root.title('Project Manager')    
root.minsize(width = 512, height = 512)
root.maxsize(width = 512, height = 512)
root.grid()  

#############################
###### CREATE PROJECT #######
#############################
txt_curdir = tk.Text(root, height = 2, width = 512)
txt_curdir.pack()
txt_curdir.insert(tk.END, "Active Project : " + glob.globs["PROJECT_ROOT"])
txt_curdir.configure(state = tk.DISABLED)
updateTextColour( util.folderExists( glob.globs["PROJECT_ROOT"] ), txt_curdir )

frm_selproj = tk.Frame(root)
frm_selproj.pack()

txt_projdir = tk.Text(frm_selproj, height = 1, width = 48)
txt_projdir.pack(in_ = frm_selproj, side = tk.LEFT)
txt_projdir.insert(tk.END, glob.globs["PROJECT_ROOT"])

btn_setactiveproj = tk.Button(frm_selproj, text = 'Set Active Project', command = lambda : dispatchActiveProject( txt_projdir.get("1.0", tk.END) ) )
btn_setactiveproj.pack(in_ = frm_selproj, side = tk.LEFT)

#############################
########## LOGGING ##########
#############################
frm_log = tk.Frame(root)
frm_log.pack()

txt_log = tk.Text(frm_log, height = 1, width = 48)
txt_log.pack(in_ = frm_log, side = tk.LEFT)

projDependantBtns["btn_log"] = tk.Button(frm_log, text = 'Add Log', command = lambda : util.log( glob.globs["PROJECT_ROOT"], "(COMMENT)" + txt_log.get("1.0", tk.END) ) )
projDependantBtns["btn_log"].pack(in_ = frm_log, side = tk.LEFT)

#############################
###### PROJECT MANIP ########
#############################
frm_manipproj = tk.Frame(root)
frm_manipproj.pack()

btn_createproj = tk.Button(root, text = 'Create', command = lambda : sequence( util.createProject( glob.globs["PROJECT_ROOT"] ), updateTextColour( util.folderExists(glob.globs["PROJECT_ROOT"]), txt_curdir ), btnProjectDep() ))
btn_createproj.pack(in_ = frm_manipproj, side = tk.LEFT)

projDependantBtns["btn_deleteproj"] = tk.Button(root, text = 'Delete', command = lambda : sequence( confirmation( "Whoa! Are you sure you want to delete " + glob.globs["PROJECT_ROOT"] + "?", util.deleteProject, False ), updateTextColour( util.folderExists(glob.globs["PROJECT_ROOT"]), txt_curdir ) ) )
projDependantBtns["btn_deleteproj"].pack(in_ = frm_manipproj, side = tk.LEFT)

projDependantBtns["btn_backupproj"] = tk.Button(root, text = 'Backup', command = util.backupProject )
projDependantBtns["btn_backupproj"].pack(in_ = frm_manipproj, side = tk.LEFT)

frm_syncproj = tk.Frame(root)
frm_syncproj.pack()

projDependantBtns["btn_pullproj"] = tk.Button(root, text = 'Pull Project', command = lambda : sync.pull())
projDependantBtns["btn_pullproj"].pack(in_ = frm_syncproj, side = tk.LEFT)

projDependantBtns["btn_pushproj"] = tk.Button(root, text = 'Push Project', command = lambda : sync.push())
projDependantBtns["btn_pushproj"].pack(in_ = frm_syncproj, side = tk.LEFT)

#############################
####### CREATE ASSET ########
#############################
txt_curassdir = tk.Text(root, height = 8, width = 512)
txt_curassdir.pack()
txt_curassdir.insert(tk.END, genAssetText())
txt_curassdir.configure( bg = "salmon" )
txt_curassdir.configure(state = tk.DISABLED)

frm_selass = tk.Frame(root)
frm_selass.pack()

txt_assdir = tk.Text(frm_selass, height = 1, width = 48)
txt_assdir.pack(in_ = frm_selass, side = tk.LEFT)
txt_assdir.insert(tk.END, glob.globs["CUR_ASSET"])

projDependantBtns["btn_setactiveass"] = tk.Button(frm_selass, text = 'Set Active Asset', command = lambda : sequence( util.setActiveAsset( txt_assdir.get("1.0", tk.END) ), updateText(txt_curassdir, genAssetText()), btnAssetDep() ) )
projDependantBtns["btn_setactiveass"].pack(in_ = frm_selass, side = tk.LEFT)

#############################
######## MANIP ASSET ########
#############################
frm_manipass = tk.Frame(root)
frm_manipass.pack()

projDependantBtns["btn_createass"] = tk.Button(root, text = 'Create', command = lambda : dispatchActiveAsset( util.createAsset ))
projDependantBtns["btn_createass"].pack(in_ = frm_manipass, side = tk.LEFT)

assDependantBtns["btn_checkoutass"] = tk.Button(root, text = 'Checkout', command = lambda : dispatchActiveAsset( util.checkoutAsset ))
assDependantBtns["btn_checkoutass"].pack(in_ = frm_manipass, side = tk.LEFT)

assDependantBtns["btn_promoass"] = tk.Button(root, text = 'Promote', command = lambda : dispatchActiveAsset( util.promoteAsset ))
assDependantBtns["btn_promoass"].pack(in_ = frm_manipass, side = tk.LEFT)

assDependantBtns["btn_demoass"] = tk.Button(root, text = 'Demote', command = lambda : dispatchActiveAsset( util.demoteAsset ))
assDependantBtns["btn_demoass"].pack(in_ = frm_manipass, side = tk.LEFT)

assDependantBtns["btn_deleteass"] = tk.Button(root, text = 'Delete', command = lambda : sequence( confirmation( "Whoa! Are you sure you want to delete " + glob.globs["CUR_ASSET"] + "?", dependanciesCheck, True, util.deleteAsset ) ) )
assDependantBtns["btn_deleteass"].pack(in_ = frm_manipass, side = tk.LEFT)

assDependantBtns["btn_backupass"] = tk.Button(root, text = 'Backup', command = quit)
assDependantBtns["btn_backupass"].pack(in_ = frm_manipass, side = tk.LEFT)

#############################
##### MANIP ASSET DEPS ######
#############################
frm_manipassdep = tk.Frame(root)
frm_manipassdep.pack()

assDependantBtns["btn_adddepass"] = tk.Button(root, text = 'Add dependancy', command = lambda : sequence(util.addDependancy( txt_assdir.get("1.0", tk.END) ), updateText(txt_curassdir, genAssetText())))
assDependantBtns["btn_adddepass"].pack(in_ = frm_manipassdep, side = tk.LEFT)

assDependantBtns["btn_rmdepass"] = tk.Button(root, text = 'Remove dependancy', command = lambda : sequence(util.removeDependancy( txt_assdir.get("1.0", tk.END) ), updateText(txt_curassdir, genAssetText())))
assDependantBtns["btn_rmdepass"].pack(in_ = frm_manipassdep, side = tk.LEFT)

#############################
######## OPEN ASSET #########
#############################
frm_openass = tk.Frame(root)
frm_openass.pack()
assDependantBtns["btn_openass"] = tk.Button( root, text = 'Open Asset', command = util.getCurFiles )
assDependantBtns["btn_openass"].pack(in_ = frm_openass, side = tk.LEFT)

quitButton = tk.Button(root, text = 'Quit', command = quit)            
quitButton.pack()

btnProjectDep()

root.mainloop()      
	       


          
