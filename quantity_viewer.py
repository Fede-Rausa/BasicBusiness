import tkinter as tk
import pandas as pd



class QuantityViewer:
    def __init__(self, parent, root):
        
        self.root=root
        self.parent = parent
        self.root.title("Quantity Viewer")
        self.path_dataset = "datiCassa.csv"
        self.path_impo = "impostazioniCassa.csv"
        self.opts = ['TODO', 'STBY', 'DONE']


        self.importa_dati()
        self.load_impo()
        self.gen_rows0()
        self.setupUi()


    def importa_dati(self):
        self.dataset = pd.read_csv(self.path_dataset, sep=';', decimal=',')

    def load_impo(self):
        self.impo = pd.read_csv(self.path_impo, sep=';', decimal=',')




    def setupUi(self):
        # code for creating table
        total_rows = len(self.rows)
        total_columns = len(self.rows[0])

        cells = []
        for i in range(total_rows):
            rowcell = []
            for j in range(total_columns):
                
                e = tk.Entry(self.root, width=20, fg='blue',
                            font=self.cf)  #self.cf)#('Arial',16,'bold'))
                
                e.grid(row=i, column=j)
                e.insert(tk.END, self.rows[i][j])  #lst[i][j])

                rowcell.append(e)
            cells.append(rowcell)
        self.cells = cells



    def gen_rows(self):
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
        self.cf = ("Arial", int(self.parent.SM.spinfont2.get()), "bold")

        print(int(self.parent.SM.spinfont2.get()))

    
    def updateUi(self):
        total_rows = len(self.rows)
        total_columns = len(self.rows[0])

        for i in range(total_rows):
            for j in range(total_columns):
                #self.cells[i][j].destroy()
                self.cells[i][j].delete(0,tk.END)
                self.cells[i][j].insert(0, self.rows[i][j])
                self.cells[i][j].config(font = self.cf)

        #self.setupUi()



    def update(self):
        self.importa_dati()
        self.gen_rows()


