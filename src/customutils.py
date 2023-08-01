import tkinter as tk
from tkinter.filedialog import askopenfilename as askf
from tkinter.filedialog import asksaveasfilename as asksf

usernamedb=[]

def open_file(entry,window):
    """Open a file for editing."""
    filepath = askf(
        filetypes=[("Rep Files", "*.repf"), ("All Files", "*.*")]
    )
    if not filepath:
        return
    entry.delete("0", tk.END)
#    entry2.delete("1.0", tk.END)
    with open(filepath, mode="r", encoding="utf-8") as input_file:
        text = input_file.read()
#        entry.insert(tk.END, text)
    window.title(f"Company - {filepath}")
    
    
def save_file(entry,window):
    """Save the current file as a new file."""
    filepath = asksf(
        defaultextension=".txt",
        filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")],
    )
    if not filepath:
        return
    with open(filepath, mode="w", encoding="utf-8") as output_file:
        text = entry.get("1.0", tk.END)
        output_file.write(text)
    window.title(f"Company(saved) - {filepath}")



