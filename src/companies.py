import tkinter as tk
import os
from tkinter.filedialog import askopenfilename as askf
from tkinter.filedialog import askdirectory as askd
import tkinter.messagebox as box
import clients as clients
import tkinter.font as tkFont
import tkinter.ttk as ttk
import yaml


with open("./cfg/config.yml", "r") as ymlfile:
    cfg = yaml.safe_load(ymlfile)
route = cfg["auth"]["companies"]  

def open(user):
    window = tk.Tk()
    window.winfo_toplevel().title("Company Select")
    greeting = tk.Label(text=f"Hello {user}.", foreground="blue", background="white", width=100, height=10).pack()
    button = tk.Button(text="Pick Company", master=window, command=lambda: open_company(window, user)).pack()
    button2 = tk.Button(text="create Company", master=window, command=lambda: create_company(user, window)).pack()
    window.mainloop()
    
def open_company(window, user):
    company = ""
#    if False:
#        errwin = tk.Tk()
#        errwin.winfo_toplevel().title("Error")
#        greeting = tk.Label(text=f"Hello, {company} does not exist or cannot be accessed. Please crete it or contact an administrator.", foreground="blue", background="white", width=100, height=10)
#        greeting.pack()
#        errwin.mainloop() 
    print('opening ' + f'{route}')
#    filepath = askd(initialdir=r'./src/Companies',title='Please select a Company')
    filepath = askd(initialdir=f'{route}',title='Please select a Company')
    if not filepath:
        return
    print(filepath)
    cwin = tk.Tk()
    company = filepath.split('\\')[-1]
    
    print(company)
    listbox = tk.Listbox(cwin, height=30, width=100)
    print(os.listdir(filepath))
    for name in os.listdir(filepath):
        print(name)
        listbox.insert('end', name)
        
    scrollbar = tk.Scrollbar(cwin)
    scrollbar.pack(side='left', fill='both')
    listbox.pack()
    listbox.config(yscrollcommand = scrollbar.set)
    scrollbar.config(command = listbox.yview)
    
    
    def refresh():
        newlist = os.listdir(filepath)
        listbox.delete(0,'end')
        for file in newlist:
            listbox.insert('end', file)
    refresh = tk.Button(master=cwin, text="refresh", command=refresh)
    refresh.pack()
    choose = tk.Button(text="Select Client", master=cwin, command=lambda: clients.open_client(filepath, listbox.get(listbox.curselection()), user))
    choose.pack()
    button = tk.Button(text="Create Client", master=cwin, command=lambda: clients.create_client(company, user))
    button.pack()
    
    window.destroy()
    

    
    cwin.winfo_toplevel().title(f"{company}")
    cwin.state('zoomed')

    
    cwin.mainloop()
    
    
def create_company(user, win):
    window = tk.Tk()
    window.winfo_toplevel().title("Create Company")
    window.geometry("1200x650")
    fields=[]
    frame = ttk.Frame(window, borderwidth=5)
    folderName = tk.Entry(frame)
    f = tk.Label(frame, text= "Folder Name")
    f.grid(column=0,row=0)
    folderName.grid(column=1,row=0,sticky='w')
#    frame.pack(side='top', fill='both', expand=True)    
    frame.grid(row=0, column=0, sticky="nsew") 
    button = tk.Button(text="Create", master=window, command=lambda: create(folderName.get(), win, window, user))
    button.grid()
    window.mainloop()
    
def create(name, parentParentWin, parentWin, user):
    print(f'{route}/{name}')
    os.makedirs(f'{route}/{name}')
    parentWin.destroy()
    open_company(user,parentParentWin)
    
    
    
def dialog() :
    box.showinfo( 'Selection' , 'Your Choice: ' + \
    listbox.get( listbox.curselection() ) )
    
    
    




















#advanced


