from argon2 import PasswordHasher
import companies as c
import base64
import yaml
from tkinter.messagebox import showinfo
import string
import tkinter as tk

with open("./cfg/config.yml", "r") as ymlfile:
    cfg = yaml.safe_load(ymlfile)
route = cfg["auth"]["route"]    
  
ph = PasswordHasher()
db={}

print(f'{route} is the password file route')
try:
    with open(f'{route}/.hashedpass','r') as f :
        for line in f:
            data = line.split(',')
            db[data[0]] = f'{data[1]},{data[2]},{data[3][:-1]}'
            print(f' the working password db is {db}')
except :
    print('password file empty')
    db = {}

def login(username, password, w):
    print("logging in to db")
    print(db.keys())
    if username in db.keys() and ph.verify(db[username], password):
        print("user found, password matched")
        w.destroy()
        print('window destroyed?')
        c.open(username)
        return True
    print('login failed')
    return False
    
def create_user(username, password, window):
    '''check for user'''
    print('creating user')
   
        
    if username in db :
        print('username in db already')
        showinfo(message='username in db already')
        return False
        '''check username rules'''
    if not user_rules(username)[0]:
        print('not following username rules')
        '''check password rules'''
        showinfo(message=f'not following username rules. Missing: ')
        return False
    ppass = pswd_rules(password)
    if not ppass[0]:
        errmsg = ''
        if not ppass[1]:
            errmsg = errmsg + 'missing special (*) chars \n'
        if not ppass[2]:
            errmsg = errmsg + 'missing CAPITAL \n'
        if not ppass[3]:
            errmsg = errmsg + 'missing lowercase \n'
        if not ppass[1]:
            errmsg = errmsg + 'missing number (1234567890) \n'
        if not ppass[4]:
            errmsg = errmsg + 'missing length of at least 8 \n'
        showinfo(message=f'not following password rules. Missing: \n{errmsg} ') 
    else:
        print(pswd_rules(password)[0])
        if len(db) == 0 :
            new_pass = ph.hash(password)
            with open(f'{route}/.hashedpass','a') as f :
                f.writelines(f'{username},{new_pass}\n')
                db[username] = new_pass
                return 
        print('successful combo, creating')
        loginwin = tk.Tk()
        tk.Label(loginwin,text='Username').grid(row=1, column=0)
        tk.Label(loginwin,text='Password').grid(row=2, column=0)
        uname = tk.Entry(loginwin)
        p =  tk.Entry(loginwin)
        a = tk.Button(loginwin, text='authenticate', command=lambda:adduser(username, password, uname.get(), p.get(),loginwin, window))
        
        uname.grid(row=1,column=1,columnspan=4,sticky='ew')
        p.grid(row=2,column=1,columnspan=4,sticky='ew')
        a.grid(row=3,column=3)
        loginwin.mainloop()



def adduser(username, password, uname, p, w, x):
    print("logging in to db")
    print(db.keys())
    print(ph.hash(p))
    print(p)
    print(uname)
    if username == 'Admin' :
        new_pass = ph.hash(password)
        with open(f'{route}/.hashedpass','a') as f :
            f.writelines(f'{username},{new_pass}')
            f.writelines('\n')
            db[username] = new_pass
        print('attempting login')
        login(username, password, x)
        #showinfo('fuck')
        
        return True
    if uname in db.keys() and ph.verify(db[uname], p) :
        print("user found, password matched")
        
        w.destroy()
        print('hashing pass')
        new_pass = ph.hash(password)
        '''login'''
        print(new_pass)
        print('writing')
        with open(f'{route}/.hashedpass','a') as f :
            f.writelines(f'{username},{new_pass}')
            f.writelines('\n')
            db[username] = new_pass
        print('attempting login')
        try:
            login(username, password, x)
        except:
            showinfo(message='bad logon')        
        return True
                    

        return True
    return False
  
    
def user_rules(username):
    print(username)
    return [True]


    
def pswd_rules(pswd):
    print(pswd)
    special_chars = string.punctuation
    bools = list(map(lambda char: char in special_chars, pswd))
    up = False
    low = False
    n = False
    for c in pswd :
        if not up and c.isupper():
            up = True
        if not low and c.islower():
            low = True
        if not n and c.isnumeric():
            n = True
        if up and low and n:
            break
            
    l = len(pswd) > 7
    all = False
    if bools and l and up and low and n:
        all = True
    return [all,bools,up,low,n,l]
