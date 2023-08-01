import tkinter as tk
from tkinter.filedialog import askopenfilename as askf
from tkinter.filedialog import askdirectory as askd
import os, subprocess, platform
import tkinter.font as tkFont
import tkinter.ttk as ttk
from tkinter.scrolledtext import ScrolledText
import numpy as np
from tkinter.messagebox import showinfo
from os import environ as env
import datetime
import reppalemail as eml 
import shutil, time
import dkey
from cryptography.fernet import Fernet
import base64
import shlex
import winreg
from pathlib import Path
import yaml
#from lockfile import Lock
route = ""
try:
    with open("./cfg/config.yml", "r") as ymlfile:
        cfg = yaml.safe_load(ymlfile)
    route = cfg["auth"]["netkey"]  
except:
    print('key file failed')
print(route)
print(os.path.exists(f'{route}'))
key = ""
if os.path.exists(f'{route}') :

    key = Path(route).read_bytes()
    print('network initialise key \n\n\n\n\n netkey \n\n\n\n network key')
 

    #try:
    #    key = dkey.DKey().key
    #    print('dkey')
    #except:        
    #    print('default key :(')
    #    key = Path('./keys.key')
else:
    try:
        key = dkey.DKey().key
        print('dkey')
    except:        
        print('default key :(')
        key = Path('./keys.key')

print('printing key')
print(key)
fernet = Fernet(key)

colors=['grey','red','white','blue','orange','yellow','green','pink','orange','purple']


car_header=['Location', 'Modified', 'Created', 'Encrypted' ]
car_list=[]
curComp = None
curClient = None
curCat = None
baseFiles=[]

sys = platform.system()

def create_client(company, user):
    print('creating client')
    window = tk.Tk()
    window.winfo_toplevel().title("Create Client")
    window.geometry("1200x650")
    fields=[f'{company}']
    frame = ttk.Frame(window, borderwidth=5)
    folderName = tk.Entry(frame)
    f = tk.Label(frame, text= "Folder Name")
    f.grid(column=0,row=0)
    folderName.grid(column=1,row=0,sticky='w')
    name = tk.Entry(frame)
    namel = tk.Label(frame, text= "Name")
    namel.grid(column=0,row=1)
    name.grid(column=1,row=1,sticky='w')
    addr = tk.Entry(frame)
    addrl = tk.Label(frame, text= "Address")
    addrl.grid(column=0,row=2)
    addr.grid(column=1,row=2,sticky='w')
    city = tk.Entry(frame)
    cityl = tk.Label(frame, text= "City")
    cityl.grid(column=0,row=3)
    city.grid(column=1,row=3,sticky='w')
    state = tk.Entry(frame)
    statel = tk.Label(frame, text= "State")
    statel.grid(column=0,row=4)
    state.grid(column=1,row=4,sticky='w')
    zip = tk.Entry(frame)
    zipl = tk.Label(frame, text= "ZIP")
    zipl.grid(column=0,row=5)
    zip.grid(column=1,row=5,sticky='w')
    phone = tk.Entry(frame)
    phonel = tk.Label(frame, text= "Phone")
    phonel.grid(column=0,row=6)
    phone.grid(column=1,row=6,sticky='w')
    email = tk.Entry(frame)
    emaill = tk.Label(frame, text= "Email")
    emaill.grid(column=0,row=7)
    email.grid(column=1,row=7,sticky='w')
    notes = ScrolledText(frame, wrap='word')
    notes.grid(column=1,row=8,sticky='w')
    xtra = tk.Entry(frame, width=100)
    xtral = tk.Label(frame, text= "addl Folders")
    xtral.grid(column=0,row=9)
    xtra.grid(column=1,row=9,sticky='w')
    
    def gen_list(list):
        list.append(folderName.get())
        list.append(name.get())
        list.append(addr.get())
        list.append(city.get())
        list.append(state.get())
        list.append(zip.get())
        list.append(phone.get())
        list.append(email.get())
        list.append(notes.get(1.0,'end'))
        
        for x in xtra.get().split(','):
            list.append(x)
        n = 0
        for i in list :
                            
            print(f'{n} is {i}')
            n = n +1
        create(list, window, user, company)
#    frame.pack(side='top', fill='both', expand=True)    
    frame.grid(row=0, column=0, sticky="nsew") 
    button = tk.Button(text="Create", master=window, command=lambda: gen_list(fields))
    button.grid()
    window.mainloop()
    

    
def open_client(company, client, user):
    reset_list()
    curComp = company
    curClient = client
    fileicon={}
    filepath = f'{company}/{client}'
    window = tk.Tk()
    
    window.winfo_toplevel().title(f"{client}")
#    frame = ttk.Frame(window, borderwidth=5, relief="ridge")
    
    catagories = {}
    lastCat=[]
    lastCat.append(None)
    count = 0
    btnc = 0
    sb = tk.Scrollbar(window, orient='vertical')
    lb = tk.Text(window, width= 20)
    
    sb.pack(fill='both', side='left',expand=False)
    basecats=['NOTES', 'POA', 'AGREEMENT', 'TRANSCRIPTS', '433s', 'IRS CORRESPONDENCE', 'CLIENT CORRESPONDENCE', 'GENERAL INFO', 'TAX RETURNS'] 
    extras= np.setdiff1d(os.listdir(filepath),basecats)
    def refresh(comapny, client, window, user):
        print('refresh') 
        window.destroy()
        open_client(company,client,user)


    def create_folder():
        createfwin = tk.Tk()
        def createfolder(cwin, folder, cat):
            os.mkdir(f'{filepath}/{cat}/{folder}')
            if os.path.exists(f'{filepath}/{cat}/{folder}'):
                createfwin.destroy()
            else:
                showinfo(message= "Please make sure a catagoy is selected in the box above before hitting create")
        tk.Label(createfwin, text="Please select a catagory and type in a folder name to continue.").grid(row=0, column=0, columnspan=5)
        listbox = tk.Listbox(createfwin, height=30, width=100)
        print(os.listdir(filepath))
        for name in os.listdir(filepath):
            print(name)
            listbox.insert('end', name)
        
        #scrollbar = tk.Scrollbar(cwin)
        #scrollbar.pack(side='left', fill='both')
        listbox.grid(row=1,column=1, columnspan = 3, rowspan= 5)
        #listbox.config(yscrollcommand = scrollbar.set)
        #scrollbar.config(command = listbox.yview)
    
        ent = tk.Entry(createfwin)
        tk.Label(createfwin, text='New Folder Name').grid(column = 0, row = 6)
        cbtn = tk.Button(createfwin, text='CREATE', command=lambda: createfolder(createfwin, ent.get(), listbox.get(listbox.curselection())))
        ent.grid(row=6, column = 1, columnspan = 2)
        cbtn.grid(column = 3, row = 7)
        
    def create_catagory():
        createfwin = tk.Tk()
        def createcatagory(cwin, folder):
            os.mkdir(f'{filepath}/{folder}')
            if os.path.exists(f'{filepath}/{folder}'):
                createfwin.destroy()
            else:
                showinfo(message= "Please make sure a catagoy is selected in the box above before hitting create")
        tk.Label(createfwin, text="Please select a catagory and type in a folder name to continue.").grid(row=0, column=0, columnspan=5)
        ent = tk.Entry(createfwin)
        tk.Label(createfwin, text='New Folder Name').grid(column = 0, row = 6)
        cbtn = tk.Button(createfwin, text='CREATE', command=lambda: createcatagory(createfwin, ent.get()))
        ent.grid(row=6, column = 1, columnspan = 2)
        cbtn.grid(column = 3, row = 7)
    
    r = tk.Button(lb, text="reload", command=lambda: refresh(curComp, curClient, window, user), width = 20)
    email = tk.Button(lb, text="email", command=lambda: eml.open_email(user, filepath), width = 20)

    lb.window_create('end', window=email)
    lb.insert('end', '\n')
    lb.window_create('end', window=r)
    lb.insert('end', '\n')

        
    def make_buttons(catagory, btnname, count, btnc, h, w):
        
        color = ""
        digit = get_digit(btnc, 0)
          
        btn = tk.Button(text=f'{btnname}',bg=colors[digit-1], master=lb, command=lambda: view_catagory(catagory), height=h, width=w )
        lb.window_create('end', window=btn)
        #grid(column=0,row=count, rowspan=15)
        lb.insert('end', '\n')
        
    def make_button(btnname, count, btnc, h, w):
          
        btn = tk.Button(text=f'{btnname}', master=lb, command=lambda: create_folder(), height=h, width=w )
        lb.window_create('end', window=btn)
        #grid(column=0,row=count, rowspan=15)
        lb.insert('end', '\n')

        
        
    def get_digit(number, n):
        return number // 10**n % 10
        
    make_button('New Folder',count,btnc,1,20)
    make_button('New Tab',count,btnc,1,20)           
    
    for name in basecats:
        
        count = count + 16 
        btnc = btnc + 1
        make_buttons(name, name, count, btnc, 3, 20)

    for extra in extras:
        
        count = count + 16
        btnc = btnc + 1        
        make_buttons(extra, extra, count, btnc, 3, 20)
    count = count + 16
    btnc = btnc + 1
   
    def mydestroy(awin):
        #cus I need windows destroyed weird
        awin.destroy()
        
    def enccat(fpath):

        for item in os.listdir(fpath):
            if os.path.isdir(item):
                enccat(item)
            else:
                print(f'encrypting {item}')
        
        #mydestroy(tem)
        
        

    def view_catagory(catagory):
        
        if 'listbox' in catagories :
            print(f'current cat is {lastCat[0]}')
            
            print('reencrypting')
            dir = f'{filepath}/{lastCat[0]}'
            enccat(dir)
            
            
            reset_list()
            print(car_list)
            catagories['listbox'].label.destroy()
            catagories['listbox'].frame.destroy()
            catagories['listbox'].tree.destroy()
            catagories['enc_button'].destroy()
            catagories['encall_button'].destroy()
            
        print(f'{filepath}/{catagory}')
        curCat = catagory   
        lastCat[0] = curCat
        for name in os.listdir(f'{filepath}/{catagory}'):               
           #insert parent folders
            baseFiles.append(f'{name}')
            encrypted = False
            
            tryfile = Path(f'{filepath}/{catagory}/{name}')
            if not os.path.isdir(tryfile):
                data = tryfile.read_bytes()
                if data.endswith(bytes('True','utf-8')):
                    encrypted = True
                
                
                modded = datetime.datetime.fromtimestamp(os.path.getmtime(f'{filepath}/{catagory}/{name}'))
                created = datetime.datetime.fromtimestamp(os.path.getctime(f'{filepath}/{catagory}/{name}'))
                car_list.append([f'{filepath}/{catagory}/{name}', f'{modded}', f'{created}', f'{encrypted}'])
            else: 
                modded = datetime.datetime.fromtimestamp(os.path.getmtime(f'{filepath}/{catagory}/{name}'))
                created = datetime.datetime.fromtimestamp(os.path.getctime(f'{filepath}/{catagory}/{name}'))
                car_list.append([f'{filepath}/{catagory}/{name}', f'{modded}', f'{created}', 'na'])
        print(baseFiles)
        print(car_list)
        print(curCat)
        print(curClient)
        print(curComp)

        def repcrypt(decfile):
            
            for selected_item in decfile.selection():
                item = decfile.item(selected_item)
                print(item['values'][0])
                record = item['values'][0]
                with open(f'{record}', 'rb') as d :
                    dec = d.read()
                    #check for encyption flag
                    if dec.endswith(bytes('True','utf-8')):
                        return
                enc = fernet.encrypt(dec)
                with open(f'{record}', 'wb') as d :
                    d.write(enc + bytes('True','utf-8'))
                #with open(f'{record}', 'ab') as d :
                #   d.write(bytes('True','utf-8'))
                    #item['values'][3] = 'true'
                    decfile.item(selected_item, text=item['text'], values = (item['values'][0],item['values'][1],item['values'][2], True))
        def encall():
            for name in os.listdir(f'{filepath}/{catagory}'):               
               #insert parent folders
                encrypted = False
                
                tryfile = Path(f'{filepath}/{catagory}/{name}')
                data = tryfile.read_bytes()
                if data.endswith(bytes('True','utf-8')):
                    encrypted = True
                else:
                    enc = fernet.encrypt(data)
                    with open(f'{tryfile}', 'wb') as d :
                        d.write(enc + bytes('True','utf-8'))
                        view_catagory(catagory)
                
                
        encallButton = tk.Button(window, text='encrypt all', command=lambda:encall())
        encButton = tk.Button(window, text='encrypt', command=lambda:repcrypt(catagories['listbox'].tree))             
        catagories['enc_button'] = encButton
        catagories['enc_button'].pack(side='right', anchor='ne') 
        catagories['encall_button'] = encallButton
        catagories['encall_button'].pack(side='right', anchor='ne') 
        catagories['listbox'] = MultiColumnListbox()
        catagories['listbox'].tree.insert('', 'end', text=f'{curCat}', values=[f'{curComp}/{curClient}/{curCat}','na','na'])
#        def upload(catagory):
#            newlist = os.listdir(filepath)
#            view_catagory(catagory)

    lb.pack(side='left', fill='y')
    window.state('zoomed')
    lb.config(yscrollcommand=sb.set)
    sb.config(command = lb.yview)
    def onclose():
        print(f'closing {window}')
        pass
        
    window.protocol("WM_DELETE_WINDOW", onclose())
    window.mainloop()




def reset_list():
    car_list.clear()
    baseFiles.clear()



def create(inputList, oldwin, user, company):
    #create folders
    #create contact
    print('creating')
    folderName = inputList[1]
    print(folderName)
    name = inputList[2]
    addr = inputList[3]
    city = inputList[4]
    state = inputList[5]
    zip = inputList[6]
    phone = inputList[7]
    email = inputList[8]
    info = inputList[9]
    basePath = f'{company}'
    os.mkdir(f'{basePath}\{folderName}')
  #      try:
 #           os.mkdir(f'{basePath}\\{folderName}')
#            print(f'made folder: {basePath}\\{folderName}')
#        except:
#            print('caught')
    clientPath=f'{basePath}\{folderName}\\'
    os.mkdir(f'{clientPath}NOTES')
    os.mkdir(f'{clientPath}POA')
    os.mkdir(f'{clientPath}AGREEMENT')
    os.mkdir(f'{clientPath}TRANSCRIPTS')
    os.mkdir(f'{clientPath}TRANSCRIPTS\\ACCOUNT')
    os.mkdir(f'{clientPath}TRANSCRIPTS\\WAGES and INCOME')
    os.mkdir(f'{clientPath}TRANSCRIPTS\\RETURN')
    os.mkdir(f'{clientPath}433s')
    os.mkdir(f'{clientPath}IRS CORRESPONDENCE')
    os.mkdir(f'{clientPath}CLIENT CORRESPONDENCE')
    os.mkdir(f'{clientPath}GENERAL INFO')
    os.mkdir(f'{clientPath}TAX RETURNS')
    with open(f'{clientPath}NOTES\\ContactCardfor{folderName}.txt','w') as f:
        f.writelines(name)
        f.writelines(addr)
        f.writelines(city + ', ' + state + ' ' + zip)
    n = 0
    for x in range (10, len(inputList)) :
        n = n + 1
        print(f'{n} is {x}')
        try: 
            os.mkdir(f'{clientPath}{inputList[x]}')   
        except:
            print(f'path exists: {inputList[x]}')
    oldwin.destroy()
    open_client(inputList[0], folderName, user)

class MultiColumnListbox(object):

    def __init__(self):
        self.nodeCount = 0
        self.tree = None
        self.label = None
        self.frame = None
        self.style = None
        self._setup_widgets()
        self._build_tree()
        def item_selected(event):
            for selected_item in self.tree.selection():
                item = self.tree.item(selected_item)
                print(item)
#                record = item['values'][1]
#                with open(f'{record}', 'rb') as d :
#                    dec = d.read()
#                enc = fernet.encrypt(dec)
#                with open(f'{record}', 'wb') as d :
#                    d.write(enc)
                #if record[0] :
                #self.tree.item(self.tree.selection(), open=True)
            # show a message
                #showinfo(title='Information', message=','.join(record))
        def handleOpenEvent(event):
            open_children(tree.focus())
            
        def openFileHandler(event):
            item = self.tree.selection()
            filePath = self.tree.item(item)['values'][0]
            print(f'opening {filePath}')
            parent = self.tree.item(item)
            if os.path.isdir(filePath) : 
                
                if sys == 'Darwin':
                    file = askf(initialdir='~/Downloads')
                elif sys == 'Windows':
                    print('~/Downloads')
                    file = askf(initialdir='~/Downloads')
                else:
                    file = askf(initialdir='C:')
                shutil.copyfile(file, f'{filePath}/{os.path.basename(file)}')

                #enc = fernet.excrypt(f'{filePath}/{os.path.basename(file)}')
                #insert into tree TODOTODOTODOTODOTODOTODOTODOTODOTODOTODOTODOTODOTODOTODO cus ti doesnt update in real time
                encrypted = False
            
                tryfile = Path(f'{filePath}/{os.path.basename(file)}')
                data = tryfile.read_bytes()
                if data.endswith(bytes('True','utf-8')):
                    encrypted = True
                modded = datetime.datetime.fromtimestamp(os.path.getmtime(f'{filePath}/{os.path.basename(file)}'))
                created = datetime.datetime.fromtimestamp(os.path.getctime(f'{filePath}/{os.path.basename(file)}'))
                child = self.tree.insert(item[0], 'end',text=f'{os.path.basename(file)}', values=[f'{filePath}/{os.path.basename(file)}',f'{modded}',f'{created}', f'{encrypted}'])
                #print(child + " is child")
                #print(item)
                self.tree.move(child, item,'end')
                
                with open(f'{filePath}/{os.path.basename(file)}', 'rb') as d :
                    dec = d.read()
                enc = fernet.encrypt(dec)
                enc = enc + bytes('True', 'utf-8')
                
                with open(f'{filePath}/{os.path.basename(file)}', 'wb') as d :
                    d.write(enc)
                    print("encrypted")
                print(file)
                
            else:   
                def dectaxdox(a):
                    with open(f'{a}', 'rb') as e :
                        nec = e.read()
                        
                        enc = nec[:-4]
                        
                        
                        selected_item = self.tree.selection()[0]
                        titem = self.tree.item(item)
                        self.tree.item(selected_item, text=titem['text'], values = (titem['values'][0],titem['values'][1],titem['values'][2], False))
                        
                        
                    try:    
                        dec = fernet.decrypt(enc)
                        with open(f'{a}', 'wb') as d :
                            d.write(dec)
                           
                    except Exception as e:
                        print(f'already done? {e}')
                if sys == 'Darwin':
                    dectaxdox(filePath)
                    subprocess.call(('open', filePath))

                elif sys == 'Windows':
                    
                    dectaxdox(filePath)
                    #filePathLock = f'{filePath}.lock'
                    #with open(filePathLock, 'a'): pass
                    #    print('locked')
                    os.startfile(filePath)
                    print('unlocked')
                else:
                    with open(f'{filePath}','rb') as e:
                        enc = e.read()
                    dec = fernet.decrypt(enc)
                    with open(f'{filePath}','wb') as e:
                        e.write(dec)
                    print(f"decrypted {filePath}")
                    subprocess.call(('xdg-open', filePath))
                    with open(f'{filePath}', 'rb') as d :
                        dec = d.read()
                    enc = fernet.encrypt(dec)
                    with open(f'{filePath}', 'wb') as d :
                        d.write(enc)
                    #enc = fernet.excrypt(f'{filePath}')
        self.tree.bind('<Double-1>', openFileHandler)
        self.tree.bind('<<TreeViewOpen>>', handleOpenEvent)
        self.tree.bind('<<TreeviewSelect>>', item_selected)
       









    def _setup_widgets(self):
        s = """Click on header to sort by that column
To change width of column drag boundary
Click the side tabs to select your folder tab
        """
        self.label = ttk.Label(wraplength="4i", justify="left", anchor="n",
            padding=(10, 2, 10, 6), text=s)
        self.label.pack(fill='x')
        self.frame = ttk.Frame()
        self.style = ttk.Style(self.frame)
        self.frame.pack(fill='both', expand=True)
        # create a treeview with dual scrollbars
        self.tree = ttk.Treeview(columns=car_header)
        #, show="tree headings"
        vsb = ttk.Scrollbar(orient="vertical",
            command=self.tree.yview)
        hsb = ttk.Scrollbar(orient="horizontal",
            command=self.tree.xview)
        self.tree.configure(yscrollcommand=vsb.set,
            xscrollcommand=hsb.set)
        self.tree.grid(column=0, row=0, sticky='nsew', in_=self.frame)
        vsb.grid(column=1, row=0, sticky='ns', in_=self.frame)
        hsb.grid(column=0, row=1, sticky='ew', in_=self.frame)
#        self.tree.pack(side='left', fill='both', expand=True)
#        vsb.pack(side='left',fill='y')
#        hsb.pack(side='bottom', fill='x')
        
        self.frame.grid_columnconfigure(0, weight=1)
        self.frame.grid_rowconfigure(0, weight=1)



    def _build_tree(self):
        #self.tree.column("#0", minwidth=50)
        #self.tree.column("#0", width=100, anchor='e', stretch=True)
        #print(self.tree.column("#0"))
        for col in car_header:

            self.tree.heading(col, text=col.title(),
                command=lambda c=col: sortby(self.tree, c, 0))
            # adjust the column's width to the header string
            self.tree.column(col,
                width=tkFont.Font().measure(col.title()))
        #helper to expand hierarchy
        def add_children(parent):
            # check if the parent is a dir
            if os.path.isdir(self.tree.item(parent)['values'][0]) :
                print(self.tree.item(parent)['values'][0] + 'is teh parent value')
                #insert children and recurse 
                for item in os.listdir(self.tree.item(parent)['values'][0]):
                    print(item)
                    print(parent +" is parent")
                    base = self.tree.item(parent)['values'][0]
                    modded = datetime.datetime.fromtimestamp(os.path.getmtime(f'{base}/{item}'))
                    created = datetime.datetime.fromtimestamp(os.path.getctime(f'{base}/{item}'))
                    child = self.tree.insert(parent, 'end',text=f'{os.path.basename(item)}', values=[f'{base}/{item}',f'{modded}',f'{created}'])
                    self.tree.move(child, parent,'end')
                    print(child + " is child")
                    add_children(child)
        #set expand button column width (not working + children not indenting)
        
        
        for item in car_list:
 
            head = self.tree.insert('', 'end', text=f'{os.path.basename(item[0])}', values=item)
            print('adding children for ' + item[0])
            add_children(head)           
            # adjust column's width to fit values
            for ix, val in enumerate(item):
                col_w = tkFont.Font().measure(val)
                if self.tree.column(car_header[ix],width=None)<col_w:
                    self.tree.column(car_header[ix], width=col_w)
                    
                        
        
    def open_children(parent):
        self.tree.item(parent, open=True)
        for child in self.tree.get_children(parent):
            open_children(child)
            
    #add kids
    print("oh boy")


    

def sortby(tree, col, descending):
    """sort tree contents when a column header is clicked on"""
    # grab values to sort
    data = [(tree.set(child, col), child) \
        for child in tree.get_children('')]
    # if the data to be sorted is numeric change to float
    #data =  change_numeric(data)
    # now sort the data in place
    data.sort(reverse=descending)
    for ix, item in enumerate(data):
        tree.move(item[1], '', ix)
    # switch the heading so it will sort in the opposite direction
    tree.heading(col, command=lambda col=col: sortby(tree, col, \
        int(not descending)))