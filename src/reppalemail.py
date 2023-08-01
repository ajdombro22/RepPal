import tkinter as tk
import yaml
from tkinter.messagebox import showinfo
import smtplib
from email.mime.text import MIMEText
import imaplib, email
from tkinter import ttk

with open("./cfg/config.yml", "r") as ymlfile:
    cfg = yaml.safe_load(ymlfile)
    
try:
    edetails = cfg["email"]
    uname = cfg["email"]["username"]
except:
    print('no email set up')

def open_email(user, client):
    print(f'opening exchange with {client}')
    window = tk.Tk()
    if uname :
        print(uname)
    window.mainloop()
    
def attach_email(win):
    win.destroy()
    newemailwin = tk.Tk()
    emailargs = []
    tk.Label(text='Username').grid(row=0, column=0)
    tk.Label(text='Password').grid(row=1, column=0)
    uname = tk.Entry()
    password = tk.Entry()
    tk.Label(text='Connection Method:').grid(row=2, column=0)
    combo = ttk.Combobox(state='readonly', values=['ipop3','imap'])
    def contype():
        method = combo.get()
        if method == 'ipop3':
            print('ipop3')
        elif method == 'imap':
            print('imap')
        else:
            showinfo(message='try again')
    
    combo.grid(row=3, column=0)
    def check_new_email(arglist):
        print('checking')
 
    tk.Button(text='save and continue', command=lambda: check_new_email(emailargs)).grid(row=-1, column=4)
    uname.grid(row=0, column=1, columnspan=2)
    password.grid(row=1, column=1, columnspan=2)
    newemailwin.mainloop()

def send_email(subject, body, sender, recipients, password):
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = ', '.join(recipients)
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp_server:
       smtp_server.login(sender, password)
       smtp_server.sendmail(sender, recipients, msg.as_string())
    print("Message sent!")