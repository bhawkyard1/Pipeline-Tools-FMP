import Tkinter as tk
import util
import glob

glob.loadConfig()

def dispatchActiveProject( _arg ):
	util.setActiveProject( [_arg] )
	txt_curdir.configure(state = tk.NORMAL)
	txt_curdir.delete( "1.0", tk.END )
	txt_curdir.insert(tk.END, "Active Project : " + glob.globs["PROJECT_ROOT"])
	txt_curdir.configure(state = tk.DISABLED)

root = tk.Tk()
root.title('Project Manager')    
root.minsize(width=512, height=512)
root.maxsize(width=512, height=512)
root.grid()  

txt_curdir = tk.Text(root, height = 2, width = 512)
txt_curdir.pack()
txt_curdir.insert(tk.END, "Active Project : " + glob.globs["PROJECT_ROOT"])
txt_curdir.configure(state = tk.DISABLED)

frm_selproj = tk.Frame(root)
frm_selproj.pack(side = tk.TOP)

txt_projdir = tk.Text(frm_selproj, height = 1, width = 48)
txt_projdir.pack(in_ = frm_selproj, side = tk.LEFT)
txt_projdir.insert(tk.END, glob.globs["PROJECT_ROOT"])

btn_setactiveproj = tk.Button(frm_selproj, text = 'Set Active Project', command = lambda : dispatchActiveProject( txt_projdir.get("1.0", tk.END) ) )
btn_setactiveproj.pack(in_ = frm_selproj, side = tk.LEFT)

'''
btn_createproj = tk.Button(root, text = 'Create Project', command = quit)
btn_createproj.pack()

btn_deleteproj = tk.Button(root, text = 'Delete Project', command = quit)
btn_deleteproj.pack()

txt_assdir = tk.Text(root, height = 2, width = 512)
txt_assdir.pack()
txt_assdir.insert(tk.END, "new_asset")

quitButton = tk.Button(root, text = 'Quit', command = quit)            
quitButton.pack()
'''

root.mainloop()                    


          
