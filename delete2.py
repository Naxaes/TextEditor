from tkinter import *

root = Tk()


text_area = Frame(root, bd=2, relief=SUNKEN)
text_area.grid_rowconfigure(0, weight=1)
text_area.grid_columnconfigure(0, weight=1)

scrollbar_x = Scrollbar(text_area, orient=HORIZONTAL)
scrollbar_x.grid(row=1, column=0, sticky=E + W)
scrollbar_y = Scrollbar(text_area)
scrollbar_y.grid(row=0, column=1, sticky=N + S)

text = Text(text_area, wrap=NONE, bd=0, xscrollcommand=scrollbar_x.set, yscrollcommand=scrollbar_y.set)
text.grid(row=0, column=0, sticky=N+S+E+W)

scrollbar_x.config(command=text.xview)
scrollbar_y.config(command=text.yview)

text_area.pack(side=TOP)


output_area = Frame(root, bd=2, relief=SUNKEN)
output_area.grid_rowconfigure(0, weight=1)
output_area.grid_columnconfigure(0, weight=1)

scrollbar_x = Scrollbar(output_area, orient=HORIZONTAL)
scrollbar_x.grid(row=1, column=0, sticky=E + W)
scrollbar_y = Scrollbar(output_area)
scrollbar_y.grid(row=0, column=1, sticky=N + S)

text = Text(output_area, wrap=NONE, bd=0, xscrollcommand=scrollbar_x.set, yscrollcommand=scrollbar_y.set)
text.grid(row=0, column=0, sticky=N+S+E+W)

scrollbar_x.config(command=text.xview)
scrollbar_y.config(command=text.yview)

output_area.pack(side=BOTTOM)







mainloop()