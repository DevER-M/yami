import tkinter as tk
import ttkbootstrap as ttk

window = ttk.Window(themename="darkly")
window.title('idk')
font="Calibri 20 bold"

def idk():
    side = entryInt.get()
    print(side)
    output_string.set(side*side)
    

title = ttk.Label(window,text="print on console",font=font)
title.pack()

input_frame = ttk.Label(master=window,text="enter something",font=font)
entryInt= tk.IntVar()
entry = ttk.Entry(master=input_frame,textvariable=entryInt)
button = ttk.Button(master=input_frame,text="Go",command=idk)
entry.pack(side="left")
button.pack(side="left")
input_frame.pack(pady=10)

output_string = tk.StringVar()
output_label = ttk.Label(
    master = window,
    text = "aah",
    font=font,
    textvariable=output_string
)
output_label.pack()

window.mainloop()