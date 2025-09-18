import tkinter as tk
import pandas as pd

class SalesViewer:
    def __init__(self, parent, root):
        self.root=root
        self.parent = parent
        self.root.title("Sales Viewer")
        self.path_dataset = "datiCassa.csv"
        self.basicHeaders = ['cliente', 'status', 'scontoSpeciale', 'sconto', 'prezzo', 'giorno', 'ts', 'NOTE']
        self.keepHeaders = ['status', 'cliente']
        self.opts = ['TODO', 'DONE', 'STBY']

        self.setupUi()
        #self.update()

    def importa_dati(self):
        self.dataset = pd.read_csv(self.path_dataset, sep=';', decimal=',')
        
    def setupUi(self):

        self.list_frame = tk.Frame(self.root)
        self.list_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.intro = tk.Frame(self.list_frame)
        self.intro.pack()
        lab = tk.Label(self.intro, text="Lista ordini")
        lab.pack(side=tk.LEFT)

        ###qui possono andare i filtro e regolatore font

        # Crea una scrollbar
        self.scrollbar = tk.Scrollbar(self.list_frame)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Crea una lista per contenere le righe
        self.lista_righe = tk.Listbox(self.list_frame, yscrollcommand=self.scrollbar.set, 
        font = ("Calibri", 20) )
        self.lista_righe.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.scrollbar.config(command=self.lista_righe.yview)



        
    def rowToOrder(self, row):
        cliente_status = row.loc[self.keepHeaders]
        cliente_status = " | ".join(str(value) for value in cliente_status)
        crow = row.drop(self.basicHeaders)
        qstr = ' '
        for i in range(len(crow)):
            if crow[i] != 0:
                qstr = (qstr + ' __ ' + crow.index[i].upper() + ': ' +str(crow[i]))
        qstr = cliente_status + " | " + qstr
        return qstr


    def gen_rows(self):
        #print(type(self.lista_righe))

        try:
            self.lista_righe.delete(0, tk.END)
        except:
            print("Error deleting items from listbox, it may not be initialized yet.")
            return 

        # control font of panel text
        self.lista_righe.config(font=('Calibri', int(self.parent.SM.spinfont.get())))

        #mystatus = self.selezione.get()
        mystatus = self.parent.SM.selezione.get()
        #print(mystatus)

        if (mystatus == 'ALL'):
            filtrato = self.dataset
        else:
            filtrato = self.dataset.loc[self.dataset['status']==mystatus].reset_index(drop=True)
    

        N = len(filtrato)
        sep = "_____________________________________________________________________________________________________________________________________________________________________________________________________________________________________________"

        #count_note = 0
        for i in range(N):
            j = N-(i+1)
            #idt = i*2 + count_note
            idt = (N-j-1)*2 #+ count_note
            idr = idt + 1

            row = filtrato.loc[j]
            riga_testo = self.rowToOrder(row)

            self.lista_righe.insert(tk.END, riga_testo)

            note = row.loc['NOTE']
            if (type(note)==type('str') and note!=''):
                #count_note+=1
                self.lista_righe.insert(tk.END, 'NOTE: '+note)
            else:
                self.lista_righe.insert(tk.END, sep)

            #self.lista_righe.insert(tk.END, sep)  

            self.lista_righe.itemconfig(idr, {'bg':'white'})

            status = row['status']    
            if status=='TODO':
                self.lista_righe.itemconfig(idt, {'bg':'lightblue'})
            if status=='STBY':
                self.lista_righe.itemconfig(idt, {'bg':'lightgreen'})
            if status=='DONE':
                self.lista_righe.itemconfig(idt, {'bg':'red'})



    def update(self):
        self.importa_dati()
        self.gen_rows()
        #self.root.after(2000, self.update)  # call update again after 2 seconds


        # is_sep = False 
        # for j in range(N*2):
        #     if (is_sep):
        #         self.lista_righe.itemconfig(j, {'bg':'aliceblue'})
        #     else:
        #         self.lista_righe.itemconfig(j, {'bg':'white'})
        #     is_sep = not is_sep
