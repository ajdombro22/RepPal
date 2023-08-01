import tkinter as tk
from tkinter.filedialog import askopenfilename as askf
from tkinter.filedialog import askdirectory as askd
import os, subprocess, platform
import tkinter.font as tkFont
import tkinter.ttk as ttk
from tkinter.scrolledtext import ScrolledText
import numpy as np
from tkinter.messagebox import showinfo

colors=['grey','red','white','blue','orange','yellow','green','pink','orange','purple']


car_header=['Location', 'Modified', 'Created' ]
car_list=[]
curComp = None
curClient = None
curCat = None
baseFiles=[]

sys = platform.system()

def create_client(company):
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
    name.insert(0,'name')
    name.grid(column=1,row=1,sticky='w')
    addr = tk.Entry(frame)
    addr.insert(0,'address')
    addr.grid(column=1,row=2,sticky='w')
    city = tk.Entry(frame)
    city.insert(0,'city')
    city.grid(column=1,row=3,sticky='w')
    state = tk.Entry(frame)
    state.insert(0,'state')
    state.grid(column=1,row=4,sticky='w')
    zip = tk.Entry(frame)
    zip.insert(0,'zip')
    zip.grid(column=1,row=5,sticky='w')
    phone = tk.Entry(frame)
    phone.insert(0,'phone')
    phone.grid(column=1,row=6,sticky='w')
    email = tk.Entry(frame)
    email.insert(0,'email')
    email.grid(column=1,row=7,sticky='w')
    notes = ScrolledText(frame, wrap='word')
    notes.grid(column=1,row=8,sticky='w')
    xtra = tk.Entry(frame, width=100)
    xtra.insert(0,'test')
    f = tk.Label(frame, text="test")
    f.grid(column=0,row=9)
    xtra.grid(column=1,sticky='w')
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
            
        create(list, window)
#    frame.pack(side='top', fill='both', expand=True)    
    frame.grid(row=0, column=0, sticky="nsew") 
    button = tk.Button(text="Create", master=window, command=lambda: gen_list(fields))
    button.grid()
    window.mainloop()

def open_client(company, client):
    curComp = company
    curClient = client
    fileicon={}
    filepath = f'{company}/{client}'
    window = tk.Tk()
    window.winfo_toplevel().title(f"{client}")
#    frame = ttk.Frame(window, borderwidth=5, relief="ridge")
    print(filepath)
    catagories = {}
    count = 2
    btnc = 0
    v = ttk.Scrollbar(window, orient='vertical')
     #for vertical scrollbar
    v.grid(column=0)
    f = tk.Frame(window).grid(column=1, row=0)
    t = tk.Text(f, yscrollcommand = v.set)
    v.config(command=t.yview)
    #pack(side='left', fill='y')
    basecats=['NOTES', 'POA', 'AGREEMENT', 'TRANSCRIPTS', '443\'s', 'IRS CORRESPONDENCE', 'CLIENT CORRESPONDENCE', 'GENERAL INFO', 'TAX RETURNS'] 
    extras= np.setdiff1d(os.listdir(filepath),basecats)
    def refresh(comapny, client, window):
        print('refresh') 
        window.destroy()
        open_client(company,client)

    
    
    r = tk.Button(f, text="reload", command=lambda: refresh(curComp, curClient, window)).grid(column=0, row=0)
    email = tk.Button(f, text="email", command=lambda: refresh(curComp, curClient, window )).grid(column=0, row = 1)

        
    def make_buttons(catagory, btnname, count, btnc):
        print(name)
        color = ""
        digit = get_digit(btnc, 0)
        
        #frame.grid_rowconfigure(count, weight=1)  
        btn = tk.Button(t, text=f'{btnname}',bg=colors[digit-1], command=lambda: view_catagory(catagory), height=3, width=20 ).grid(column=0,row=count)
        t.window_create("end", window=btn)
        t.insert("end","\n \n \n")
        #grid(column=0,row=count, rowspan=15)
        
    def get_digit(number, n):
        return number // 10**n % 10
           
    for name in basecats:
        print(name)
        count = count + 16 
        btnc = btnc + 1
        make_buttons(name, name, count, btnc)

    for extra in extras:
        print(extra)
        count = count + 16
        btnc = btnc + 1        
        make_buttons(extra, extra, count, btnc)
        
        

    
    def view_catagory(catagory):
        if 'listbox' in catagories :
            print('window exists')
            print(car_list)
            reset_list()
            print(car_list)
            catagories['listbox'].label.destroy()
            catagories['listbox'].frame.destroy()
            catagories['listbox'].tree.destroy()
        print(f'{filepath}/{catagory}')
        curCat = catagory
        for name in os.listdir(f'{filepath}/{catagory}'):               
           #insert parent folders
           baseFiles.append(f'{name}')
           
           car_list.append([f'{filepath}/{catagory}/{name}', 'na', 'na'])
        print(baseFiles)
        print(car_list)
        print(curCat)
        print(curClient)
        print(curComp)
        catagories['listbox'] = MultiColumnListbox()
        catagories['listbox'].tree.insert('', 'end', text=f'{curCat}', values=[f'{curComp}/{curClient}/{curCat}','na','na'])

    window.state('zoomed')
    t.configure(state="disabled")
    t.grid(column=0)
    f.grid_columnconfigure(0, weight=1)
        
    window.mainloop()


def reset_list():
    car_list.clear()
    baseFiles.clear()



def create(inputList, oldwin):
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
    basePath = f'.\src\Companies\{os.path.basename(inputList[0])}'
    print(f'{basePath}\{folderName}')
    os.mkdir(f'{basePath}\\{folderName}')
  #      try:
 #           os.mkdir(f'{basePath}\\{folderName}')
#            print(f'made folder: {basePath}\\{folderName}')
#        except:
#            print('caught')
    clientPath=f'{basePath}\\{folderName}\\'
    print(clientPath)
    os.mkdir(f'{clientPath}NOTES')
    os.mkdir(f'{clientPath}POA')
    os.mkdir(f'{clientPath}AGREEMENT')
    os.mkdir(f'{clientPath}TRANSCRIPTS')
    os.mkdir(f'{clientPath}433s')
    os.mkdir(f'{clientPath}IRS CORRESPONDENCE')
    os.mkdir(f'{clientPath}CLIENT CORRESPONDENCE')
    os.mkdir(f'{clientPath}GENERAL INFO')
    os.mkdir(f'{clientPath}TAX RETURNS')
    with open(f'{clientPath}NOTES\\ContactCardfor{folderName}.txt','w') as f:
        f.writelines(name)
        f.writelines(addr)
        f.writelines(city + ', ' + state + ' ' + zip)
    for x in range (10, len(inputList)) :
        os.mkdir(f'{clientPath}\\{inputList[x]}')   

    oldwin.destroy()
    open_client(inputList[0], folderName)

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
                record = item['values']
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
            if sys == 'Darwin':
                subprocess.call(('open', filePath))
            elif sys == 'Windows':
                os.startfile(filePath)
            else:
                subprocess.call(('xdg-open', filePath))
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
        self.label.grid(column= 1, row=0)
        self.frame = ttk.Frame()
        self.style = ttk.Style(self.frame)
        #self.frame.pack(fill='both', expand=True)
        self.frame.grid(column=1, row=1, rowspan=100, columnspan=1000, sticky='ew')
        # create a treeview with dual scrollbars
        self.tree = ttk.Treeview(columns=car_header)
        #, show="tree headings"
        vsb = ttk.Scrollbar(orient="vertical",
            command=self.tree.yview)
        hsb = ttk.Scrollbar(orient="horizontal",
            command=self.tree.xview)
        self.tree.configure(yscrollcommand=vsb.set,
            xscrollcommand=hsb.set)
        self.tree.grid(column=0, row=0, sticky='ns', in_=self.frame)
        vsb.grid(column=1, row=0, sticky='ns', in_=self.frame)
        hsb.grid(column=0, row=1, sticky='ew', in_=self.frame)
#        self.tree.pack(side='left', fill='both', expand=True)
#        vsb.pack(side='left',fill='y')
#        hsb.pack(side='bottom', fill='x')
        
        #self.frame.grid_columnconfigure(0, weight=1)
        #self.frame.grid_rowconfigure(0, weight=1)
        self.frame.grid_propagate(False)

        self.frame.grid_columnconfigure(1, weight=1)
        self.frame.grid_rowconfigure(1, weight=1)



    def _build_tree(self):

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
                #insert children and recurse 
                for item in os.listdir(self.tree.item(parent)['values'][0]):
                    print(parent +" is parent")
                    base = self.tree.item(parent)['values'][0]
                    child = self.tree.insert(parent, 'end',text=f'{os.path.basename(item)}', values=[f'{base}/{item}','na','na'])
                    self.tree.move(child, parent,'end')
                    print(child + " is child")
                    add_children(child)
        
        
        for item in car_list:
            head = self.tree.insert('', 'end', text=f'{os.path.basename(item[0])}', values=item)
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