import tkinter as tk
import customutils as cu
import login as enter






#from tkinter.filedialog import askopenfilename as askf





window = tk.Tk()
fill = tk.Label(text='              \n               ').grid(column=0, row=0)
greeting = tk.Label(text='''Hello {USER}. Please login to continue. 
BETA TEST. To log in, simply hit "create user"''', foreground="blue", background="white", width=100, height=10, anchor='n').grid(column=1, row=0)
entry = tk.Entry().grid(column=1, row=1)
entry2 = tk.Entry(show="*", width=15).grid(column=1,row=2)
button = tk.Button(text="login", master=window)
button2 = tk.Button(text="create_user", master=window)
configs = tk.Button(text='config', master=window, anchor='e')




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

    
    
button.bind("<Button-1>", login)
button2.bind("<Button-1>", create_user)
window.bind("<Key>", handle_keypress)
window.winfo_toplevel().title("Login")
window.state('zoomed')
button.grid(column=1,row=3)
button2.grid(column=1,row=4)
configs.grid(column=3, row=0)
window.mainloop()





#if __name__ == '__main__' :
#    main()
