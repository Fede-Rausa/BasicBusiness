#import tkinter as tk
import customtkinter as ctk
from salesManager import SalesManager
from salesViewer import SalesViewer
from finance import FinanceManager
from cost_analysis import CostManager
from quantity_viewer import QuantityViewer

class SalesTask:
    def __init__(self, root):
        self.root = root
        self.after_ids = []
        self.SalesManager = SalesManager
        self.SalesViewer = SalesViewer
        self.FinanceManager = FinanceManager
        self.CostManager = CostManager
        self.QuantityViewer = QuantityViewer

        #sales manager block
        self.SM = SalesManager(self, root)

        #finance block
        #self.FM = FinanceManager(self, tk.Toplevel(root))

        #cost block
        self.CM = None
        #self.CM = CostManager(self, tk.Toplevel(root))        

        #sales viewer block
        self.svlist = []

        #self.svlist.append(SalesViewer(self, tk.Toplevel(root)))
        #self.update_sv()

        self.qvlist = []

        root.protocol("WM_DELETE_WINDOW", self.on_closing)


        
    def update_sv(self):   #update the sales viewers
        for sv in self.svlist:
            sv.update()

    def update_qv(self):   #update the quantity viewers
        for qv in self.qvlist:
            qv.update()

    def schedule_task(self, delay, task):
        after_id = self.root.after(delay, task)
        self.after_ids.append(after_id)

    def on_closing(self):
        # Cancel any scheduled after calls here if needed
        for after_id in self.after_ids:
            self.root.after_cancel(after_id)
        self.root.quit()
        self.root.destroy()



root = ctk.CTk()
root.update_idletasks()
applicazione = SalesTask(root)
root.mainloop()