import tkinter as tk
import customutils as cu
import login as enter
import yaml
from tkinter.filedialog import askdirectory as askd
import os
import getpass
print("Env thinks the user is [%s]" % (os.getlogin()))
print("Effective user is [%s]" % (getpass.getuser()))



#from tkinter.filedialog import askopenfilename as askf





window = tk.Tk()
configs = tk.Button(text='config', master=window)
greeting = tk.Label(text='''Hello {USER}. Please login to continue. 
"''', foreground="blue", background="white", width=100, height=10)
entry = tk.Entry()
entry2 = tk.Entry(show="*", width=15)
button = tk.Button(text="login", master=window)
button2 = tk.Button(text="create_user", master=window)




def handle_keypress(event):
    """Print the character associated to the key pressed"""
#    print(event.char)
    
def login(event):
    print("The button was clicked!")
    name = entry.get()
    pswd = entry2.get()
    print(f'{name} , {pswd}')
#    cu.open_file(entry,window)
    enter.login(entry.get(),entry2.get(),window)
#    cu.open_file()
def create_user(event):
    enter.create_user(entry.get(),entry2.get(),window)
    
def open_configs(event):
    settings={}
    buttonContainer=[]
    with open("./cfg/config.yml", "r") as ymlfile:
        cfg = yaml.safe_load(ymlfile)
        print('editing config')
        confwin = tk.Tk()
        confwin.winfo_toplevel().title("config")
        tk.Label(text='''
        Please choose your options here. The list will grow as the prgram does.
        ''', master=confwin).grid(column=0, row=0)
        def pick_dir(f):
            print(f'starting at {f}')
            file = askd(initialdir=f)
        count = 1
        for label in cfg :
            #print(label)
            tk.Label(text=f'{label}', master=confwin).grid(column=0, row=count)
            settings[f'{label}']={}
            count = count + 1            
            for item in cfg[f'{label}']:
                if item == 'netkey' or item == 'route' :
                    tk.Label(text=f'{item}', master=confwin, anchor='e').grid(column=1, row=count, sticky='ew')
                    val = cfg[f'{label}'][f'{item}']
                    print(val)
                    print(f' no buttong for {val}')
                    ent = tk.Entry(master=confwin)
                    ent.insert(0,val)
                    ent.config(state='disabled')

                    settings[f'{label}'][f'{item}'] = ent
                    ent.grid(column=2, columnspan =2, row=count, sticky='ew')
                    count = count + 1
                elif item == 'companies':
                    tk.Label(text=f'{item}', master=confwin, anchor='e').grid(column=1, row=count, sticky='ew')
                    val = cfg[f'{label}'][f'{item}']
                    print(val)
                    ent = tk.Entry(master=confwin)
                    ent.insert(0,val)
                
                    #issue, using last value due to lambda
                    
                    bval = val
                    btn = tk.Button(text='select', command=lambda: pick_dir(bval), master=confwin)
                    buttonContainer.append(btn)
                    btn.grid(column=4, row=count)
                    #BROKENNNNNNNNN
                    #settings[f'{label}'][f'{item}'] = {}
                    settings[f'{label}'][f'{item}'] = ent
                    ent.grid(column=2, columnspan =2, row=count, sticky='ew')
                    count = count + 1
                    
                else:
                    #items = item.split(':')
                    tk.Label(text=f'{item}', master=confwin, anchor='e').grid(column=1, row=count, sticky='ew')
                    val = cfg[f'{label}'][f'{item}']
                    print(val)
                    ent = tk.Entry(master=confwin)
                    ent.insert(0,val)
                
                    #issue, using last value due to lambda
                    print(f'making button that starts at {val}')

                    #BROKENNNNNNNNN
                    #settings[f'{label}'][f'{item}'] = {}
                    settings[f'{label}'][f'{item}'] = ent
                    ent.grid(column=2, columnspan =2, row=count, sticky='ew')
                    count = count + 1
            #for item in buttonContainer :
            #    print(f'{item} is being packed')
            #    item.grid(column=4, row=count)
        def dump(conf):
            #print(conf)
            modded = {}
            nkey = None
            passwdfile = r'.\cfg'
            for cat in conf:
                modded[f'{cat}'] = {}
                for item in conf[f'{cat}']:
                    #print(f'{item}')
                    #print(conf[cat])
                    print(conf[f'{cat}'][f'{item}'])
                    if item == "companies" and str(conf[f'{cat}'][f'{item}'].get()) != r'.\Companies':
                        nkey = os.path.dirname(str(conf[f'{cat}'][f'{item}'].get())) + r'\cfg\.network.key' 
                        passwdfile = os.path.dirname(str(conf[f'{cat}'][f'{item}'].get())) + r'\cfg'
                        
                        print(f'''
                        network key detected
                        |||||||||||||||
                        {nkey}
                        |||||||||||||||
                        {passwdfile} is password hash file
                        |||||||||||||||''')
                    if item == 'netkey':
                        print(f'nkey file is {nkey}')
                        if nkey == None :
                            nkey = 'None'
                        modded[f'{cat}'][f'{item}'] = nkey
                        #modded[f'{cat}'][f'{item}'] = str(conf[f'{cat}'][f'{item}'].get())
                    elif item == 'route':
                        modded[f'{cat}'][f'{item}'] = passwdfile
                    else:
                        modded[f'{cat}'][f'{item}'] = conf[f'{cat}'][f'{item}'].get()
                    
            #print(modded)        
            with open("./cfg/config.yml", "w") as ymlfile: 
                yaml.dump(modded,ymlfile)   
            print(open("./cfg/config.yml").read) 
        print(cfg)
        print('')
        print(settings)
        count = count + 2
        tk.Button(text="save", master=confwin, command=lambda: dump(settings)).grid(column=4,row=count)
    confwin.mainloop()
    
       

button.bind("<Button-1>", login)
button2.bind("<Button-1>", create_user)
#window.bind("<Key>", handle_keypress)
configs.bind("<Button-1>", open_configs)
window.winfo_toplevel().title("Login")
window.state('zoomed')
configs.pack(side='right', anchor='ne')
greeting.pack()
entry.pack()
entry2.pack()
button.pack()
button2.pack()

window.mainloop()





#if __name__ == '__main__' :
#    main()
