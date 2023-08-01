import os
import tkinter as tk
import dkey
from tkinter import filedialog as fd
from tkinter.messagebox import showinfo
from ctypes import windll
import shutil
import time
import networkkeygen as nk


defParams = {
    'auth': {'companies' : './Companies',
            'route': './cfg',
            'netkey' : 'None'},
    'personalisation' : {'darkmode' : 'False',
                        'greeting' : 'Hello!'}
}

confParams = {
    'auth': {'companies' : './Companies',
            'route': './cfg',
            'netkey' : 'None'},
    'personalisation' : {'darkmode' : 'False',
                        'greeting' : 'Hello!'}
}

installfolder="C:\\Program Files"
print(installfolder)


    
def writeparams(custom):
    if custom :
        with open('./cfg/config.yml','w') as c:
            for cat in confParams.keys():
                c.writelines(f'{cat} : \n')
                for subcat in confParams[cat].keys():
                    print(f'{confParams[cat][subcat]}')
                    c.writelines(f'  {subcat} : {confParams[cat][subcat]} \n')
    else:
        with open('./cfg/config.yml','w') as c:
            for cat in defParams.keys():
                c.writelines(f'{cat} : \n')
                for subcat in confParams[cat].keys():
                    c.writelines(f'  {subcat} : {confParams[cat][subcat]} \n')


def writeandinstall():
    writeparams(True)
    p = os.popen("\"./Scripts/pyinstaller.exe\" --noconfirm --onedir --console --hidden-import \"pyyaml\" --add-data \"./cfg;cfg/\" --add-data \"./Companies;Companies/\" ./RepPal.py")
    p.read()
    p.close()

def solo(win):
    win.destroy()
    if os.path.exists("C:\Program Files\RepPal"):
        p = os.popen("\".\Scripts\pyinstaller.exe\" --noconfirm --onedir --console --hidden-import \"pyyaml\" ./RepPal.py")
        p.read()
        p.close()
        showinfo(
            title='Updating complete',
            message='Update complete, cleaning up'
        )
        cleanup()
    else:
        writeparams(False)
        k = os.popen("py repkeygen.py")
        k.read()
        k.close()        
        p = os.popen("\".\Scripts\pyinstaller.exe\" --noconfirm --onedir --console --hidden-import \"pyyaml\" --add-data \"./cfg;cfg/\" --add-data \"./Companies;Companies/\" ./RepPal.py")
        p.read()
        p.close()
        showinfo(
            title='base install complete',
            message='base install complete, cleaning up'
        )
        cleanup()
def selectfile(cat, subcat, filetypes):
    
    filename = fd.askopenfilename(title="select a file", initialdir='.', filetypes=filetypes)
    confParams[cat][subcat] = filename
    
def selectfolder(cat, subcat):
    filename = fd.askdirectory(titel="select a folder")
    installfolder = filename
    
def selectinstallfolder():
    global installfolder
    s = installfolder
    filename = fd.askdirectory(initialdir=s, title="select a folder")
    installfolder = filename
    
    
def network(win):
    win.destroy()
    window = tk.Tk()
    
    label = tk.Label(text='Hello, please select if you want to do a client (user) or server install').pack(side='top')
    c = tk.Button(window, text='client', command = lambda: client(window)).pack(side='left', anchor='e')
    s = tk.Button(window, text='server', command = lambda: server(window)).pack(side='right', anchor='w')
    window.mainloop()





def server(win):
    win.destroy()
    if os.path.exists("C:/Program Files/RepPal/"):
        p = os.popen("\"./Scripts/pyinstaller.exe\" --noconfirm --onedir --console --hidden-import \"pyyaml\" ./RepPal.py")
        p.read()
        p.close()
    else:
        k = os.popen("py networkkeygen.py")
        k.read()
        k.close()
        k = os.popen("py repkeygen.py")
        k.read()
        k.close()  
    #need to customise server install later
        window = tk.Tk()
        rep = tk.Button(window, text='Install location', command=lambda: selectinstallfolder()).pack(fill='x')
        def serverinstall(dir, t):
            t.destroy()
            print(f'installing to {installfolder} . Speak now or forever hold your peace.')
            #time.sleep(5)
            nk.genkey()
            confParams['auth']['netkey'] = f'{installfolder}\\cfg\\.network.key' 
            writeparams(True)
            p = os.popen("\"./Scripts/pyinstaller.exe\" --noconfirm --onedir --console --hidden-import \"pyyaml\" --add-data \"./cfg;cfg/\" --add-data \"./Companies;Companies/\" ./RepPal.py")
            p.read()
            p.close()
            showinfo(
                title='base install complete',
                message='base install complete, cleaning up'
            )
            print(installfolder)
            try:
                cleanupserver()
            except:
                print('cleanup failed')
            print('done...')
        s = tk.Button(window, text='Execute', command=lambda: serverinstall(installfolder, window)).pack(fill='x')
        window.mainloop()

def client(win):
    win.destroy()
    if os.path.exists("C:/Program Files/RepPal/"):
        p = os.popen("\"./Scripts/pyinstaller.exe\" --noconfirm --onedir --console --hidden-import \"pyyaml\" ./RepPal.py")
        p.read()
        p.close()
    else:
        window = tk.Tk()
        cfg = tk.Button(window, text='Config Location', command=lambda: selectfile('auth','netkey',(('config file', 'config.yml')))).pack(fill='x')
        companies = tk.Button(window, text='Company Files', command=lambda: selectfolder('auth','companies')).pack(fill='x')
        netkey = tk.Button(window, text='Encryption Key', command=lambda: selectfile('auth','netkey',(('config file', 'config.yml')))).pack(fill='x')
        save = tk.Button(window, text="install now", command=lambda: writeandinstall()).pack(fill='x')
        
        
        
        writeparams(True)
        p = os.popen("\"./Scripts/pyinstaller.exe\" --noconfirm --onedir --console --hidden-import \"pyyaml\" --add-data \"./cfg;cfg/\" --add-data \"./Companies;Companies/\" ./RepPal.py")
        p.read()
        p.close()
        


def cleanup():
#    s = os.popen("cleanup.bat")
#    s.read()
#    s.close()
    shutil.move('cleanup.bat', '..\cleanup.bat')
    #bat_file_path = '..\cleanup.bat'  # from OP
    #result = windll.shell32.ShellExecuteW(
     #   None,  
      #  'runas',  
       # 'cmd.exe', 
        #' '.join(['/c', bat_file_path]),  # parameters
        #None,
        #1,
    #)
    #success = result > 32
    #print(success)    
def cleanupserver():
    global installfolder
    shutil.move('cleanupserver.bat', '..\cleanupserver.bat')
    #bat_file_path = '..\cleanupserver.bat'  # from OP
    #x = ' '.join(['/c', bat_file_path, f'"{installfolder}"'])
    #print(x)
    print(f'''  
    
    
    |||||||||||||
    {installfolder}
    |||||||||||||
    
    
    
    
    ''')
    #result = windll.shell32.ShellExecuteW(
     #   None,  
      #  'runas',  
       # 'cmd.exe', 
        #' '.join(['/c', bat_file_path, f'"{installfolder}"']),  # parameters
        #None,
        #1,
    #)
    #print(result)
    #success = result > 32
    #print(success)   
    
if __name__ == '__main__' :
    w = tk.Tk()
    print(os.path.exists("C:/Program Files/RepPal/"))
    label = tk.Label(text='Hello, please select if you want to do a user (personal computer) or server install').pack(side='top')
    s = tk.Button(w, text='user', command=lambda: solo(w))
    s.pack(side='bottom', fill='x')
    n = tk.Button(w, text='server', command=lambda: network(w))
    n.pack(side='bottom', fill='x')
    w.mainloop()
