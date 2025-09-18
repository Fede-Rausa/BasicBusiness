import tkinter as tk
import pandas as pd
from datetime import datetime
import numpy as np

class QuantityViewer:
    def __init__(self, parent, root):
        
        self.root=root
        self.parent = parent
        self.root.title("Quantity Viewer")
        self.path_dataset = "datiCassa.csv"
        self.path_impo = "impostazioniCassa.csv"
        self.opts = ['TODO', 'STBY', 'DONE']
        self.time_format = "%d/%m/%y %H:%M:%S"

        self.head = tk.Frame(self.root)
        self.head.grid(row = 1, column = 1, pady = 3)
        self.base = tk.Frame(self.root)
        self.base.grid(row = 2, column = 1, pady = 3)


        self.importa_dati()
        self.load_impo()
        self.gen_rows0()
        self.setupUi()


    def importa_dati(self):
        self.dataset = pd.read_csv(self.path_dataset, sep=';', decimal=',')
        #filter data by today 
        tformat = "%Y-%m-%d %H:%M:%S.%f"   #2025-09-17 14:39:40.405671
        #self.dataset = self.dataset[self.dataset['ts'] != '0']
        if (self.dataset['ts'][0] == '0'):
            self.dataset = self.dataset.drop([0])

        ts = [datetime.strptime(s, tformat).date() for s in  self.dataset['ts']]
        today = datetime.now().date()
        self.dataset = self.dataset[today==np.array(ts)]

    def load_impo(self):
        self.impo = pd.read_csv(self.path_impo, sep=';', decimal=',')




    def setupUi(self):
        self.head_label = tk.Label(self.head, text='timestamp: ' )
        self.head_label.grid(row=0, column = 1)

        #retrieve time info
        time_lab = datetime.now().strftime(self.time_format)

        #retrieve last id
        #cli = np.array(self.dataset['cliente'])
        #last_id = cli[len(cli)-1]
        self.dataset = self.dataset.reset_index()
        last_id = self.dataset['cliente'][self.dataset.shape[0]-1]

        #update head
        self.head_label.config(text = 'last order: ' + str(last_id) + '        last update: ' + time_lab, 
                               font = ("Arial", self.fontsize - 3 ))


        # code for creating table
        total_rows = len(self.rows)
        total_columns = len(self.rows[0])

        cells = []
        for i in range(total_rows):
            rowcell = []
            for j in range(total_columns):
                
                e = tk.Entry(self.base, width=20, fg='blue',
                             font = ("Arial", self.fontsize, "bold"))
                
                e.grid(row=i, column=j)
                e.insert(tk.END, self.rows[i][j])  #lst[i][j])

                rowcell.append(e)
            cells.append(rowcell)
        self.cells = cells



    def gen_rows(self):  #called from external
        self.gen_rows0()
        self.updateUi()

    def gen_rows0(self):
        prod_names = self.impo['prodotto']
        status = self.dataset['status']
        n_rows = len(prod_names)
        n_cols = 5 # PROD, todo, STBY , DONE, TOT


        rows = [['PROD'] + self.opts + ['TOT']]

        for p in prod_names:
            sums = []
            for o in self.opts:
                sums.append(self.dataset[p][status==o].sum())
            tot = sum(sums)
            row = [p] + sums + [tot]
            rows.append(row)

        self.rows = rows
        self.fontsize = int(self.parent.SM.spinfont2.get())
        #self.cf = ("Arial", self.fontsize , "bold")

        #print(int(self.parent.SM.spinfont2.get()))

    
    def updateUi(self):

        #retrieve time info
        time_lab = datetime.now().strftime(self.time_format)

        #retrieve last id
        self.dataset = self.dataset.reset_index()
        last_id = self.dataset['cliente'][self.dataset.shape[0]-1]

        #update head
        self.head_label.config(text = 'last order: ' + str(last_id) + '        last update: ' + time_lab,
                               font = ("Arial", self.fontsize - 3))

        #update cells 
        total_rows = len(self.rows)
        total_columns = len(self.rows[0])

        for i in range(total_rows):
            for j in range(total_columns):
                #self.cells[i][j].destroy()
                self.cells[i][j].delete(0,tk.END)
                self.cells[i][j].insert(0, self.rows[i][j])
                self.cells[i][j].config(font = ("Arial", self.fontsize , "bold"))

        #self.setupUi()



    def update(self):
        self.importa_dati()
        self.gen_rows()


