import tkinter as tk
import customtkinter as ctk

##this is an example code for the strategy used to create, delete and update toplevel windows from a main window
##the same strategy is used to control the sales viewer and the quantity viewer from the sales manager

class sub_win:
    def __init__(self, root):
        self.root = root

        self.lab = tk.Label(self.root, text='init')
        self.lab.pack(side=tk.TOP)


        # Bind to window destruction
        self.root.bind('<Destroy>', self.on_destroy)
        self.destroyed = False
    
    def on_destroy(self, event):
        # Mark as destroyed when window is closed
        if event.widget == self.root:
            self.destroyed = True


class main_win:
    def __init__(self, root):
        self.root = root


        self.e = tk.Entry(root)
        self.e.pack(side=tk.TOP)
        self.b_v = tk.Button(root, text='update value', command=self.update_sub)
        self.b_v.pack(side=tk.TOP)
        self.s = tk.Spinbox(root, from_=0, to=100, increment=1, 
                                font=('Calibri', '12', 'bold'), width=5, 
                                repeatinterval=100, repeatdelay=500,
                                command = self.update_sub)
        self.s.pack(side=tk.TOP)
        self.b_w = tk.Button(root, text='new win', command=self.gen_win)
        self.b_w.pack(side=tk.TOP)

        self.toplist = []




    def gen_win(self):
        new = tk.Toplevel(self.root)
        self.toplist.append(sub_win(new))
        self.update_sub()

    def update_sub(self):

        self.toplist = [t for t in self.toplist if not t.destroyed]
        for l in self.toplist:
            l.lab.config(text=self.e.get(), font = ('Arial', self.s.get()))


root = ctk.CTk()
root.update_idletasks()
applicazione = main_win(root)
root.mainloop()

