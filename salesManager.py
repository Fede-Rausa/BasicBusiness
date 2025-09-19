import tkinter as tk
from tkinter.scrolledtext import ScrolledText
import customtkinter as ctk
import pandas as pd
import numpy as np
import datetime as dt
import os
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from help import testoHelp
from datetime import datetime
# import seaborn as sns

class SalesManager:

    def __init__(self, parent, root):
        self.parent = parent
        self.root = root
        self.root.title("Sales Order Form")

        self.path_dataset = "datiCassa.csv"
        self.path_impo = "impostazioniCassa.csv"
        self.path_sconti = "scontiCassa.csv"

        self.basicHeaders = np.array(['cliente', 'status', 'scontoSpeciale', 'sconto', 'prezzo', 'giorno', 'ts', 'NOTE'])
        self.opts = ['TODO', 'DONE', 'STBY']
        self.cats = ['Panini', 'Contorni', 'Bibite', 'Dolci', 'Frutta', 'Drink', 'Primi', 'Secondi', 'Antipasti', 'Pizze', 'Mare', 'Fritti'] #['P', 'C', 'B']
        
        self.impostazioniGet()
        self.importaDati()

        # create ui for cassa
        self.setupCassaUI()
        self.fill_cassa()
        self.aggiornasconti()
        self.setupPlot()
        self.setupOrdini()
        self.setupImpoUI()
        self.setupPanelOpt()
        self.setupHelp()
        self.setupMenu()
        self.IDCLIENT()
        #self.hideshowcassa(True)
        self.show_frame('cassa')
        self.prezzoFattura = 0
        
    def impostazioniGet(self):
        if os.path.exists(self.path_impo):
            self.impo = pd.read_csv(self.path_impo, sep=';', decimal=',')
            # Ordina per categoria ogni volta che leggi il file
            ordine_categoria = self.cats  #['P', 'C', 'B']
            self.impo['categoria'] = pd.Categorical(self.impo['categoria'], categories=ordine_categoria, ordered=True)
            self.impo = self.impo.sort_values('categoria').reset_index(drop=True)
        else:
            self.gen_example_impo()

    def gen_example_impo(self):
        impo = {
            'prodotto' : ['salamella', 'speck', 'vegetariano', 'patatine', 'an cipolla', 'piadanutella', 'birra','acqua', 'spritz', 'mela'],
            'prezzo':   [4, 4, 4, 3, 3, 3, 3, 1.2, 3, 1.2],
            'categoria':  [self.cats[0]]*3 + [self.cats[1]]*2 + [self.cats[3]] + [self.cats[2]]*3 + [self.cats[4]]   #['P', 'P', 'P', 'C', 'C', 'C', 'B', 'B', 'B']
        }

        impo = pd.DataFrame(impo)

        # Ordina per categoria prima di salvare
        ordine_categoria = self.cats #['P', 'C', 'B']
        impo['categoria'] = pd.Categorical(impo['categoria'], categories=ordine_categoria, ordered=True)
        impo = impo.sort_values('categoria').reset_index(drop=True)

        impo.to_csv(self.path_impo, sep=';', decimal=',', index=False)
        self.impo = impo



    def importaDati(self):
        if (os.path.exists(self.path_dataset)):
            self.dataset = pd.read_csv(self.path_dataset, sep=';', decimal=',')
            print('dati trovati')
            # if (len(self.dataset) > 2):           #problema della rimozione della prima riga di 0
            #     if (self.dataset['ts'][0] == '0'):
            #         self.dataset = self.dataset.drop([0])
            #         print([i for i in self.dataset.index])
            #         self.dataset = self.dataset.reset_index()
            #         print([i for i in self.dataset.index])
            #         print(len(self.dataset))
        else:
            print('dati non trovati, dati generati')
            self.creaDati()

    def creaDati(self):
        df = pd.DataFrame(columns = np.append(self.basicHeaders, np.array(self.impo['prodotto'])).tolist() )
        df.loc[0] = [0] * df.shape[1]
        df.to_csv(self.path_dataset, sep=';', index=False)
        self.dataset = pd.read_csv(self.path_dataset, sep=';', decimal=',')

    def aggiornaDati(self, newrow):
        df = self.dataset
        df.loc[len(df)] = newrow.tolist()
        df.to_csv(self.path_dataset, sep=';', index=False, decimal=',')
        self.parent.update_sv()      #ricarica i sales viewer
        self.parent.update_qv()      #ricarica i quantity viewer

    def aggiornaDati0(self):
        df = self.dataset
        df.to_csv(self.path_dataset, sep=';', index=False, decimal=',')

    def backupDati(self):
        df = self.dataset
        ts = str(dt.datetime.now())
        df.to_csv(("backup_cassa_"+ts).replace('.', '_').replace(':','_')+'.csv', sep=';', index=False, decimal=',')

    def setupMenu(self):
        self.menubar = tk.Menu(self.root)
        self.root.config(menu=self.menubar)
        self.menubar.add_command(label="CASSA", command = lambda: self.show_frame('cassa'))#hideshowcassa(True))
        self.menubar.add_command(label="SALES_REPORT", command = self.plotta)
        self.menubar.add_command(label="ORDINI", command = lambda: self.show_frame('order'))#hideshoworder(True))
        self.menubar.add_command(label="TOOLS", command = lambda: self.show_frame('panelopt'))  #hideshowpanelopt(True))
        self.menubar.add_command(label="PRODS&PRICES", command = lambda: self.show_frame('impo')) #hideshowimpo(True))
        self.menubar.add_command(label="HELP", command = lambda: self.show_frame('help'))#hideshowhelp(True))

    def show_frame(self, fr_name):
        frames =      [self.cassa_frame, self.order_frame, self.impo_frame, self.help_frame, self.plot_frame, self.opt_frame]
        fr_names = np.array(['cassa',         'order',          'impo',         'help',           'plot',     'panelopt'])
        id = np.where(fr_names == fr_name)[0] #np.where restituisce l'array degli indici dove è vero, perciò va selezionato [0]
        for i in range(len(frames)):
            if (i != id):
                frames[i].pack_forget()
            else:
                frames[i].pack(expand=True, padx=5, pady=5, fill=tk.BOTH)

            if (fr_names[i] == 'order'):
                self.fill_scrollbar()



############################################################################################################ CASSA

    def setupCassaUI(self):
        # Create a main frame to center everything
        self.cassa_frame = tk.Frame(self.root)
        self.cassa_frame.pack(expand=True, pady=5, padx=5)  
        #NB: I frame vanno posizionati solo DOPO l'assegnazione

    def aggiornasconti(self):
        if (os.path.exists(self.path_sconti)):
            sconti = pd.read_csv(self.path_sconti, sep=';', decimal=',')

            for i in range(len(self.discount_spins)):
                sb = self.discount_spins[i]
                dn = self.discount_names[i]
                sb.delete(0, 'end')
                sb.insert(0, sconti[dn][0])

            #old good work
            # self.scontoPC.delete(0, "end")
            # self.scontoPC.insert(0, sconti['scontoPC'][0])
            # self.scontoPB.delete(0, "end")
            # self.scontoPB.insert(0, sconti['scontoPB'][0])
            # self.scontoCB.delete(0, "end")
            # self.scontoCB.insert(0, sconti['scontoCB'][0])

    def fill_cassa(self):
        self.cassa_frame.destroy()
        # Create a main frame to center everything
        self.cassa_frame = tk.Frame(self.root)
        self.cassa_frame.pack(expand=True, pady=5, padx=5)  

        box_frame = tk.Frame(self.cassa_frame, bd=2, relief="groove")
        box_frame.grid(row=0,column=0, pady=1)

        customer_frame = tk.Frame(self.cassa_frame, bd=2, relief="groove")
        customer_frame.grid(row=0,column=1, padx=10, pady=1)

        sconti_frame = tk.Frame(self.cassa_frame, bd=2, relief="groove")
        sconti_frame.grid(row=0,column=2, pady=1)

        #NB: I frame vanno posizionati solo DOPO l'assegnazione   

        self.used_cats = []
        for c in self.cats:
            #print(c)
            #print(c in list(self.impo['categoria']))
            if (c in list(self.impo['categoria'])):
                self.used_cats.append(c)
        
        catTag = self.used_cats #self.cats  #['P', 'C', 'B'] # self.cats
        catName = self.used_cats #self.cats  #['Panini', 'Contorni', 'Bibite'] #self.cats

        self.sbListQ = []
        self.sbListS = []

        #auto ordering of category boxes
        cat_counts = [np.array(self.impo['categoria'] == catTag[k]).astype(int).sum() for k in range(len(self.used_cats))]
        cat_indexes = [k for k in range(len(self.used_cats))]
        
        max_col = 3
        cat_rows = []
        cat_cols = []
        cols_counts = []
        cols_boxes = [0]*max_col

        sub_box_frames = []
        for i in range(max_col):
            sub_box_frame = tk.Frame(box_frame)
            sub_box_frame.grid(row=0, column=i)
            sub_box_frames.append(sub_box_frame)

        for k in cat_indexes:
            if (k < max_col):
                cat_rows.append(0)
                cat_cols.append(k)
                cols_counts.append(cat_counts[k])
                cols_boxes[k] += 1
            else:
                cols_sums = np.array(cols_counts) + cat_counts[k]
                id_min = np.argmin(cols_sums)
                cols_boxes[id_min] += 1
                cols_counts[id_min] = cols_sums[id_min]
                cat_cols.append(id_min)
                cat_rows.append(cols_boxes[id_min] - 1)


        for k in range(len(self.used_cats)):

            #very old work
            #cat_frame.grid(row=0, column=k, padx=0, pady=0) 

            #old way
            # cat_frame = tk.Frame(box_frame, bd=2, relief="groove", padx=0, pady=0)
            # cat_frame.grid(row = cat_rows[k], column = cat_cols[k], padx=0, pady=0)  #advanced auto ordering

            #new way
            cat_frame = tk.Frame(sub_box_frames[cat_cols[k]], bd=2, relief="groove", padx=0, pady=0)
            cat_frame.grid(row = cat_rows[k], column = 0, padx=0, pady=0)  #advanced auto ordering, with space compression


            labelFrame = tk.Label(cat_frame, text=catName[k], font=("Arial", 14, "bold"))
            labelFrame.grid(row=0, column=0)
            formFrame = tk.Frame(cat_frame)
            formFrame.grid(row=1, column=0, pady=0)

            prod_df = self.impo[self.impo['categoria'] == catTag[k]]

            tk.Label(formFrame, text='quantità', font = ("Arial", 10)).grid(row=0, column=2)
            tk.Label(formFrame, text='sconto', font = ("Arial", 10)).grid(row=0, column=4)

            for p in range(prod_df.shape[0]):
                prodName = prod_df.iloc[p]['prodotto']
                prodPrice = prod_df.iloc[p]['prezzo']
                p = p+1
                # print(type(prodPrice))
                # prodPrice = str(prodPrice)
                # print(type(prodPrice))

                tk.Label(formFrame, 
                        text= f"{prodName} - (€  {prodPrice:.2f})", 
                        font=("Arial", 12)).grid(row=p, column=0)
                #NB: solo gli oggetti possono essere posizionati senza essere assegnati
                #in generale questo vale per tutti quelli che non vengono chiamati da altri oggetti o funzioni
        
                #sbinbox quantità
                spinbox = tk.Spinbox(formFrame, from_=0, to=99, increment=1, width=2, 
                relief="sunken", repeatdelay=500, repeatinterval=100,
                font=("Arial", 12), bg="aliceblue", fg="blue", command=self.on_spinbox_change)
                spinbox.grid(row=p, column=2)   #se usi un oggetto in una funzione devi assegnarlo prima di posizionarlo
                self.sbListQ.append(spinbox)

                #spinbox sconti fissi
                spinSconto = tk.Spinbox(formFrame, from_=0, to=900, increment=0.01, width=5, 
                relief="sunken", repeatdelay=500, repeatinterval=100,
                font=("Arial", 12), bg="aliceblue", fg="green", command=self.on_spinbox_change)
                spinSconto.grid(row=p, column=4)   #se usi un oggetto in una funzione devi assegnarlo prima di posizionarlo
                self.sbListS.append(spinSconto)

                ctk.CTkButton(formFrame, text='+', fg_color = 'lightgreen', 	
                        text_color="black",hover_color="orange", corner_radius=1000, font=("Arial", 20), width = 50, height=30,
                        command = lambda sb=spinbox: self.updt_spin(sb, 1)
                        ).grid(row=p, column=1, padx=10, pady=10)
                ctk.CTkButton(formFrame, text='-', fg_color = 'lightblue', 	
                        text_color="black", hover_color="orange", corner_radius=1000, font=("Arial", 20), width = 50, height=30,
                        command = lambda sb=spinbox: self.updt_spin(sb, -1)
                        ).grid(row=p, column=3, padx=10, pady=10)



        ##AREE UI per fattura, note e resto        
        conti_frame = tk.Frame(customer_frame, bd=2, relief="groove")
        conti_frame.grid(row=0, column= 0, pady = 0)
        resto_frame = tk.Frame(customer_frame, pady = 0, padx=2, bd=2, relief="groove" )
        resto_frame.grid(row = 2, column = 0, pady = 10)
        note_frame = tk.Frame(customer_frame)#, bd=2, relief="groove")
        note_frame.grid(row=1, column= 0, pady = 0)

        #resto_e_sconti_frame = tk.Frame(self.cassa_frame)
        #resto_e_sconti_frame.grid(row=3, column = max_col)


        ##RESTO UI
        tk.Label(resto_frame, text='CONSEGNA', font=("Arial", 14)).grid(row=1, column=0)
        tk.Label(resto_frame, text='RESTO', font=("Arial", 14)).grid(row=2, column=0)
        self.valore_resto = tk.DoubleVar()
        self.valore_resto.set('0')
        tk.Label(resto_frame, textvariable=self.valore_resto, font=("Arial", 14)).grid(row=2, column=1)
        self.valore_consegna = tk.Spinbox(resto_frame, text='20', increment=0.01, from_=0, to=99, width=5, 
        command=self.calcola_resto, font=("Arial", 12))
        self.valore_consegna.grid(row=1, column=1)
        tk.Button(resto_frame, text='calcola resto', command=self.calcola_resto, font=("Arial", 12)).grid(row=3, column=1, pady=10)


        ##SCONTO COPPIE DI CATEGORIE UI
        #sconti_frame = tk.Frame(self.cassa_frame, bd=2, relief="groove", pady = 1, padx=1)
        #sconti_frame.grid(row=0, column=max_col+1)

        tk.Label(sconti_frame, text='IMPOSTA SCONTI', font = ("Arial",8)).grid(row=0, column=0)
        tk.Label(sconti_frame, text='', font = ("Arial",8)).grid(row=1, column=0)


        #ottieni coppie di categorie univoche
        k = len(self.used_cats)
        vals = np.arange(k).tolist()
        couples = []
        for i in vals:
            if i > 0:
                for j in range(i):
                    couples.append((i,j))

        L = len(couples)


        s_names = []
        s_value = []
        s_spinbox = []
        for i in range(L):
            id_A, id_B = couples[i]
            A = self.used_cats[id_A]
            B = self.used_cats[id_B]
            name = A+'_'+B
            s_names.append(name)
            tk.Label(sconti_frame, text=name, font = ("Arial",10)).grid(row=2+i, column=0)
            sb = tk.Spinbox(sconti_frame, increment=0.01, from_=0, to=99, width=5, command=self.on_spinbox_change)
            sb.grid(row=2+i, column=1)
            s_spinbox.append(sb)
            sv = tk.StringVar(sconti_frame, "0")
            tk.Label(sconti_frame, textvariable = sv, font = ("Arial",10)).grid(row=2+i, column=2)
            s_value.append(sv)

        self.discount_spins = s_spinbox
        self.discount_couples = couples
        self.discount_names = s_names
        self.discount_values = s_value

        def salvasconti():
            sconti = pd.DataFrame(columns = s_names)
            sconti.loc[0] = [sb.get() for sb in s_spinbox]
            sconti.to_csv(self.path_sconti, sep=';', index=False, decimal=',')


        tk.Button(sconti_frame, text='salva sconti', command=salvasconti,
                 font=("Arial", 10)).grid(row=0, column=1)



        #old good work
        # tk.Label(sconti_frame, text="sconto P+C", font = ("Arial",10)).grid(row=2, column=0)
        # tk.Label(sconti_frame, text="sconto P+B", font = ("Arial",10)).grid(row=3, column=0)
        # tk.Label(sconti_frame, text="sconto C+B", font = ("Arial",10)).grid(row=4, column=0)
        # self.scontoPC = tk.Spinbox(sconti_frame, increment=0.01, from_=0, to=99, width=5, command=self.on_spinbox_change)
        # self.scontoPC.grid(row=2, column=1)
        # self.scontoPB = tk.Spinbox(sconti_frame, increment=0.01, from_=0, to=99, width=5, command=self.on_spinbox_change)
        # self.scontoPB.grid(row=3, column=1)
        # self.scontoCB = tk.Spinbox(sconti_frame, increment=0.01, from_=0, to=99, width=5, command=self.on_spinbox_change)
        # self.scontoCB.grid(row=4, column=1)
        # self.scontoPCT = tk.StringVar(sconti_frame, "0")
        # tk.Label(sconti_frame, textvariable= self.scontoPCT, font = ("Arial",10)).grid(row=2, column=2)
        # self.scontoPBT = tk.StringVar(sconti_frame, "0")
        # tk.Label(sconti_frame, textvariable= self.scontoPBT, font = ("Arial",10)).grid(row=3, column=2)
        # self.scontoCBT = tk.StringVar(sconti_frame, "0")
        # tk.Label(sconti_frame, textvariable= self.scontoCBT, font = ("Arial",10)).grid(row=4, column=2)






        ##FATTURA UI
        tk.Label(conti_frame, text='sconto special:', font=("Arial", 14)).grid(row=1, column=0)
        tk.Label(conti_frame, text='sconto:', font=("Arial", 14)).grid(row=2, column=0)
        tk.Label(conti_frame, text='PREZZO BASE:', font=("Arial", 14)).grid(row=3, column=0)
        tk.Label(conti_frame, text='PREZZO:', font=("Arial", 14, "bold")).grid(row=4, column=0)

        ctk.CTkButton(conti_frame, text='CONFERMA', fg_color='#f46881', hover_color='red', width=10,
                    command=self.conferma).grid(row=5, column=0)
        ctk.CTkButton(conti_frame, text='CLEAR', hover_color='blue', width=10,
                    command=self.pulisci).grid(row=5, column=1, pady=2, padx=2)



        self.scontoS = tk.Spinbox(conti_frame, increment=0.01, from_=0, to=99, width=5, font = ('Arial', 12),
                                command=self.on_spinbox_change)
        self.scontoS.grid(row=1, column=1)

        self.scontoT = tk.StringVar(value='0')
        self.prezzoB = tk.StringVar(value='0')
        self.prezzoT = tk.StringVar(value='0')
        tk.Label(conti_frame, textvariable=self.scontoT, font=("Arial", 14)).grid(row=2, column=1)
        tk.Label(conti_frame, textvariable=self.prezzoB, font=("Arial", 14)).grid(row=3, column=1)
        tk.Label(conti_frame, textvariable=self.prezzoT, font=("Arial", 14, "bold")).grid(row=4, column=1)

        ##note e id cliente UI


        tk.Label(note_frame, text='status cliente:', font=("Arial", 12)).grid(row=0, column=0)
        selFiltri = self.opts
        self.actualStatus = tk.StringVar()
        self.actualStatus.set(selFiltri[0])
        drop = ctk.CTkComboBox(note_frame , variable=self.actualStatus , values = selFiltri)
        drop.grid(row = 1, column = 0)

        #drop = tk.OptionMenu(note_frame , self.actualStatus , *selFiltri) # dropdown
        #drop.grid(row = 1, column = 0)


        tk.Label(note_frame, text='ID cliente:', font=("Arial", 12)).grid(row=2, column=0)
        self.NOME = tk.Entry(note_frame, text='', font=("Arial", 12))
        self.NOME.grid(row=3, column=0)
        tk.Label(note_frame, text='NOTE:', font=("Arial", 12)).grid(row=4, column=0)
        self.NOTE = tk.Text(note_frame, width = 30, height=4)
        self.NOTE.grid(row=5, column=0)

    def calcola_resto(self):
        self.valore_resto.set('€ '+str(float(self.valore_consegna.get()) - self.prezzoFattura))
        
    def updt_spin(self, sb, add):
        new = int(sb.get()) + add
        if (new<0):
            new=0
        sb.delete(0,"end")
        sb.insert(0, str(new))
        self.on_spinbox_change()
        
    def on_spinbox_change(self):
        self.fattura()

    def calcola_fattura(self):
        Qvet = np.array([int(q.get()) for q in self.sbListQ])
        Svet = np.array([float(q.get()) for q in self.sbListS])
        Pvet = np.array(self.impo['prezzo'])

        prezzoBase = np.dot(Qvet, Pvet)
        sconto1 = np.dot(Qvet, Svet)
        sconto0 = float(self.scontoS.get())


        qcounts = [np.sum(Qvet[np.array(self.impo['categoria'] == c)]) for c in self.used_cats]
        disconuts_spins = self.discount_spins
        discount_couples = self.discount_couples

        sconto2 = 0
        discounts_c = []
        for i in range(len(discount_couples)):
            a,b = discount_couples[i]
            d = min(qcounts[a], qcounts[b]) * float(disconuts_spins[i].get())
            discounts_c.append(d)
            sconto2 += d


        #old good work
        # contaPanini = np.array(self.impo['categoria'] == 'Panini')
        # contaContorni = np.array(self.impo['categoria'] == 'Contorni')
        # contaBibite = np.array(self.impo['categoria'] == 'Bibite')

        # scontoPC = min(np.sum(Qvet[contaPanini]), np.sum(Qvet[contaContorni])) * float(self.scontoPC.get())
        # scontoPB = min(np.sum(Qvet[contaPanini]), np.sum(Qvet[contaBibite])) * float(self.scontoPB.get())
        # scontoCB = min(np.sum(Qvet[contaContorni]), np.sum(Qvet[contaBibite])) * float(self.scontoCB.get())

        # sconto2 = scontoPC + scontoPB + scontoCB

        sconto = sconto2 + sconto1 + sconto0 

        prezzoFattura = round(prezzoBase - sconto, 2)
        return Qvet, Svet, Pvet, sconto, sconto0, discounts_c, prezzoBase, prezzoFattura

    def fattura(self):
        Qvet, Svet, Pvet, sconto, sconto0, discounts_c, prezzoBase, prezzoFattura = self.calcola_fattura()
        self.prezzoFattura = prezzoFattura
        self.scontoT.set("€ "+str(round(sconto, 2)))
        self.prezzoB.set("€ "+str(round(prezzoBase,2)))
        self.prezzoT.set("€ "+str(self.prezzoFattura))

        for i in range(len(self.discount_values)):
            self.discount_values[i].set("€ "+str(round(discounts_c[i], 2)))

        #old good work
        # self.scontoPCT.set("€ "+str(round(scontoPC,2)))
        # self.scontoPBT.set("€ "+str(round(scontoPB,2)))
        # self.scontoCBT.set("€ "+str(round(scontoCB,2)))

        self.calcola_resto()

    def conferma(self):
        Qvet, Svet, Pvet, sconto, sconto0, discount_c, prezzoBase, prezzoFattura = self.calcola_fattura()
        prezzo = prezzoBase - sconto
        clientID = self.NOME.get()
        note = self.NOTE.get("1.0","end").replace("\n", "")
        orario = dt.datetime.now()
        giorno = ['lun', 'mar', 'mer', 'gio', 'ven', 'sab', 'dom'][orario.weekday()]

        riga = np.append(np.array([clientID, self.actualStatus.get(), sconto0, sconto, prezzo, giorno, str(orario), note]), Qvet)
        
      
        if (prezzoBase>0):
            self.aggiornaDati(riga)
            print(riga)
            self.stampa_fattura()
        else:
            print('ordine nullo')
        self.pulisci()
        self.IDCLIENT()      

    def pulisci(self):
        
        for j in range(len(self.sbListQ)):
            self.sbListQ[j].delete(0,"end")
            self.sbListQ[j].insert(0, "0")
        
        self.scontoS.delete(0,"end")
        self.scontoS.insert(0, "0")

        self.valore_consegna.delete(0,"end")
        self.valore_consegna.insert(0, "0")
        self.calcola_resto()

        self.NOTE.delete("1.0","end")
        self.NOME.delete(0,"end")
        # self.IDCLIENT()
        self.fattura()

    def IDCLIENT(self):
        # id = len(self.dataset)
        # self.NOME.insert(0,'cli:'+str(id + 10))
        if self.dataset.empty or "cliente" not in self.dataset.columns:
            new_id_num = 1
        else:
            ids = self.dataset["cliente"].dropna().astype(str)
            nums = []
            for id_str in ids:
                if id_str.startswith("cli:"):
                    try:
                        nums.append(int(id_str.split(":")[1]))
                    except ValueError:
                        pass
        last_id = max(nums) if nums else 0
        new_id_num = last_id + 1

        new_id = f"cli:{new_id_num:02d}"
        self.NOME.delete(0, "end")
        self.NOME.insert(0, new_id)


    def stampa_fattura(self):
        import win32print
        import win32ui
        
        Qvet, Svet, Pvet, sconto, sconto0, discount_c, prezzoBase, prezzoFattura = self.calcola_fattura()
        clientID = self.NOME.get()
        note = self.NOTE.get("1.0","end").replace("\n", "")
        
        testo = f"Cliente: {clientID}\n"
        testo += "Prodotti:\n"
        for i, qty in enumerate(Qvet):
            if qty > 0:
                testo += f"   - {self.impo.iloc[i]['prodotto']} x{int(qty)} - EUR {self.impo.iloc[i]['prezzo']*qty:.2f}\n"
        testo += f"\nTotale: EUR {prezzoFattura:.2f}\n"
        testo += f"Note: {note}\n"
        testo += "\n" * 15

        printer_name = "paninoteca"  

        try:
            hprinter = win32print.OpenPrinter(printer_name)
            try:
                hjob = win32print.StartDocPrinter(hprinter, 1, ("Scontrino", None, "RAW"))
                win32print.StartPagePrinter(hprinter)
                win32print.WritePrinter(hprinter, testo.encode("utf-8"))
                win32print.EndPagePrinter(hprinter)
                win32print.EndDocPrinter(hprinter)
            finally:
                win32print.ClosePrinter(hprinter)
        except Exception as e:
            print(f"Errore di stampa: {e}")








############################################################################################################ IMPOSTAZIONI

    def setupImpoUI(self):
        self.impo_frame = tk.Frame(self.root)
        self.impo_frame.pack(expand=True, pady=5, padx=5)  

        ##nuovo form per le impostazioni
        self.impoListForm = tk.Frame(self.impo_frame)
        self.impoListForm.pack(side = tk.TOP)
        impoControl = tk.Frame(self.impo_frame)
        impoControl.pack(side = tk.TOP)

        #per avere informazioni dall'oggetto
        self.listaNomiProdotti = []
        self.listaCategorieProdotti = []
        self.listaPrezziProdotti = []
        #per eliminare l'oggetto
        self.listaIndiciProdotti = []
        self.listaRigheProdotti = []
        self.lastID = 0
        tk.Button(impoControl, text="AGGIUNGI PRODOTTO +", command=self.aggiungiProdotto).pack(side=tk.TOP)
        tk.Button(impoControl, text="CONFERMA IMPOSTAZIONI E RIGENERA DATI", command=self.confermaImpostazioni).pack(side=tk.TOP)
        tk.Label(impoControl, text='* P = panino, C = contorno, B = bibita', font = ("Arial", 8)).pack(side=tk.TOP)

        self.auto_fill_impo()  #riempi in automatico con i dati già presenti

    def aggiungiProdotto(self, nome_prod=None, prezzo_prod=None, cat_prod=None):
        row = tk.Frame(self.impoListForm)
        row.pack(side=tk.TOP)
        nome = tk.Entry(row)
        nome.pack(side=tk.LEFT)
        tk.Label(row, text="€", font=('Arial', 10)).pack(side=tk.LEFT)
        prezzo = tk.Spinbox(row, from_=0, to=99, increment=0.01, 
                            font=('Arial', 10), width=6, repeatinterval=100, repeatdelay=500)
        prezzo.pack(side=tk.LEFT, padx=10)

        clicked = tk.StringVar()
        clicked.set(self.cats[0]) # initial menu text
        drop = tk.OptionMenu(row , clicked , *self.cats) # dropdown
        drop.pack(side=tk.LEFT, padx=10) 

        tk.Button(row, text='RIMUOVI -', font=('Arial', 10), command= lambda x=self.lastID: self.rimuoviRigaImpo(x)).pack(side=tk.LEFT)

        #per avere informazioni dall'oggetto
        self.listaNomiProdotti.append(nome)
        self.listaCategorieProdotti.append(clicked)
        self.listaPrezziProdotti.append(prezzo)
        #per eliminare l'oggetto
        self.listaIndiciProdotti.append(self.lastID)
        self.listaRigheProdotti.append(row)
        self.lastID += 1

        if (nome_prod != None):    
            #aggiorna entry
            nome.delete(0,tk.END)    
            nome.insert(0,nome_prod)
            #aggiorna spinbox (come entry)
            prezzo.delete(0,tk.END)
            prezzo.insert(0,prezzo_prod)
            #aggiorna dropdown
            clicked.set(cat_prod)

    
    def auto_fill_impo(self):
        prezzi = self.impo['prezzo']
        prodotti = self.impo['prodotto']
        categorie = self.impo['categoria']

        for r in range(len(categorie)):
            self.aggiungiProdotto(prodotti[r], prezzi[r], categorie[r])




    def rimuoviRigaImpo(self, id):
        id = self.listaIndiciProdotti.index(id)
        self.listaRigheProdotti[id].destroy()

        self.listaRigheProdotti.pop(id)
        self.listaIndiciProdotti.pop(id)
        self.listaPrezziProdotti.pop(id)
        self.listaCategorieProdotti.pop(id)
        self.listaNomiProdotti.pop(id)


    def confermaImpostazioni(self):
        N = len(self.listaNomiProdotti)
        df = pd.DataFrame(columns=['prodotto', 'prezzo', 'categoria'])
        for i in range(N):
            prod = self.listaNomiProdotti[i].get()
            prezzo = float(self.listaPrezziProdotti[i].get())
            cat = self.listaCategorieProdotti[i].get()
            df.loc[i] = [prod, prezzo, cat]

        # Ordina il DataFrame per categoria P, C, B
        ordine_categoria = self.cats #['P', 'C', 'B']  #self.cats
        df['categoria'] = pd.Categorical(df['categoria'], categories=ordine_categoria, ordered=True)
        df = df.sort_values('categoria').reset_index(drop=True)

        df.to_csv(self.path_impo, sep=';', index=False, decimal=',')
        self.impo = df
        self.fill_cassa()
        #self.hideshowcassa(False)
        self.backupDati()
        self.creaDati()






############################################################################################################ TOOLS

    def setupPanelOpt(self):
        self.opt_frame = tk.Frame(self.root)
        self.opt_frame.pack(expand=True,pady=5, padx=5, fill=tk.BOTH)

        panelopt_frame = tk.Frame(self.opt_frame)
        panelopt_frame.pack(pady=10, padx=10, side=tk.TOP)

        def call_gen_rows():
            #self.parent.SV.gen_rows() #correct for just one sales viewer

            pop_ids = []
            for i in range(len(self.parent.svlist)):  
                sv = self.parent.svlist[i]
                try:
                    sv.gen_rows()
                except Exception as e:
                    print('errore in call_gen_rows')
                    print(e)
                    pop_ids.append(i)

                #if (sv is not None):
                #    sv.gen_rows()
                #else:
                #    pop_ids.append(i)
            for i in pop_ids:
                self.parent.svlist.pop(i)

        def call_gen_rows2():
            pop_ids = []
            for i in range(len(self.parent.qvlist)):  
                qv = self.parent.qvlist[i]
                try:
                    qv.gen_rows()
                except Exception as e:
                    print('errore in call_gen_rows2')
                    print(e)
                    pop_ids.append(i)       

            for i in pop_ids:
                self.parent.qvlist.pop(i)               

                

        #filtra per tipo di ordine
        selFiltri = self.opts
        selFiltri.append('ALL')
        self.selezione = tk.StringVar()
        self.selezione.set('ALL')
        drop = tk.OptionMenu(panelopt_frame , self.selezione , *selFiltri,
        command = lambda e: call_gen_rows()) # dropdown
        drop.pack(side=tk.LEFT, padx=10) 

        # cambia le dimensioni del font
        tk.Label(panelopt_frame, text='Regola Font:', font=('Calibri', '12', 'bold')).pack(side=tk.LEFT, padx=10) # display selected

        self.spinfont = tk.Spinbox(panelopt_frame, from_=5, to=50, increment=1, 
                                font=('Calibri', '12', 'bold'), width=5, 
                                repeatinterval=100, repeatdelay=500,
                                command = call_gen_rows)
        self.spinfont.pack(side=tk.LEFT)
        self.spinfont.delete(0, tk.END)
        self.spinfont.insert(0, "20")

        tk.Button(panelopt_frame, text='open sales viewer', 
                    command = self.apri_panel,
                    font=('Calibri', '12', 'bold')).pack(side=tk.LEFT, padx=10)
        

        qpanelopt_frame = tk.Frame(self.opt_frame)
        qpanelopt_frame.pack(pady=10, padx=10, side=tk.TOP)

        tk.Label(qpanelopt_frame, text='Regola Font:', font=('Calibri', '12', 'bold')).pack(side=tk.LEFT, padx=10) # display selected

        self.spinfont2 = tk.Spinbox(qpanelopt_frame, from_=5, to=50, increment=1, 
                                font=('Calibri', '12', 'bold'), width=5, 
                                repeatinterval=100, repeatdelay=500,
                                command = call_gen_rows2)
        
        self.spinfont2.pack(side=tk.LEFT)
        self.spinfont2.delete(0, tk.END)
        self.spinfont2.insert(0, "16")


        tk.Button(qpanelopt_frame, text='open quantity viewer', 
                command = self.apri_quantitypanel,
                font=('Calibri', '12', 'bold')).pack(side=tk.LEFT, padx=10)
        
        tk.Button(self.opt_frame, text='open cost analyzer', 
                    command = self.apri_costi,
                    font=('Calibri', '12', 'bold')).pack(side=tk.TOP, padx=10, pady=10)

        tk.Button(self.opt_frame, text='open finance manager', 
                    command = self.apri_finance,
                    font=('Calibri', '12', 'bold')).pack(side=tk.TOP, padx=10, pady=10)



    def apri_quantitypanel(self):
        parent = self.parent
        windowB = tk.Toplevel(self.root)
        parent.qvlist.append(parent.QuantityViewer(parent, windowB))
        for qv in parent.qvlist:
            qv.update()
    
    def apri_panel(self):
        parent = self.parent
        windowB = tk.Toplevel(self.root)
        #parent.SV = parent.SalesViewer(parent, windowB)
        parent.svlist.append(parent.SalesViewer(parent, windowB))
        for sv in parent.svlist:
            sv.update()
        #parent.SV.update()


    def apri_costi(self):
        parent = self.parent
        windowB = tk.Toplevel(self.root)
        parent.FM = parent.CostManager(parent, windowB)


    def apri_finance(self):
        parent = self.parent
        windowB = tk.Toplevel(self.root)
        parent.FM = parent.FinanceManager(parent, windowB)


    def setupHelp(self):
        self.help_frame = tk.Frame(self.root)
        self.help_frame.pack(expand=True, pady=5, padx=5, fill=tk.BOTH)  
        
        testo = testoHelp().txt

        scroll_bar = tk.Scrollbar(self.help_frame)
        scroll_bar.pack(side=tk.RIGHT)
        manuale = ScrolledText(scroll_bar, font=('Calibri', 15), width=150, height=100)     
        manuale.insert(tk.END, testo)
        manuale.pack(side=tk.LEFT, padx=10, pady=10, expand=True, fill=tk.BOTH)

    # def hideshowcassa(self, cassaOn):
    #     if (cassaOn):
    #         self.hideshowplot(False)
    #         self.hideshoworder(False)
    #         self.hideshowimpo(False)
    #         self.hideshowhelp(False)
    #         self.hideshowpanelopt(False)
    #         self.cassa_frame.pack(expand=True, pady=20)
    #     else:
    #         self.cassa_frame.pack_forget()

    # def hideshowplot(self, plotOn):
    #     if (plotOn):
    #         self.hideshowcassa(False)
    #         self.hideshoworder(False)
    #         self.hideshowimpo(False)
    #         self.hideshowhelp(False)
    #         self.hideshowpanelopt(False)
    #         self.plot_frame.pack(expand=True, pady=5, padx=5, fill=tk.BOTH)
    #     else:
    #         self.plot_frame.pack_forget()

    # def hideshoworder(self, orderOn):
    #     if (orderOn):
    #         self.hideshowcassa(False)
    #         self.hideshowplot(False)
    #         self.hideshowimpo(False)
    #         self.hideshowhelp(False)
    #         self.hideshowpanelopt(False)
    #         self.order_frame.pack(expand=True, pady=5, padx=5, fill=tk.BOTH)
    #         self.fill_scrollbar()
    #     else: 
    #         self.order_frame.pack_forget()

    # def hideshowimpo(self, impoOn):
    #     if (impoOn):
    #         self.hideshowcassa(False)
    #         self.hideshowplot(False)
    #         self.hideshoworder(False)
    #         self.hideshowpanelopt(False)
    #         self.hideshowhelp(False)
    #         self.impo_frame.pack(expand=True, pady=5, padx=5) 
    #     else:
    #         self.impo_frame.pack_forget()

    # def hideshowpanelopt(self, poOn):
    #     if (poOn):
    #         self.hideshowcassa(False)
    #         self.hideshowplot(False)
    #         self.hideshoworder(False)
    #         self.hideshowhelp(False)
    #         self.hideshowimpo(False)
    #         self.opt_frame.pack(expand=True, pady=5, padx=5) 
    #     else:
    #         self.opt_frame.pack_forget()            

    # def hideshowhelp(self, helpOn):
    #     if (helpOn):
    #         self.hideshowcassa(False)
    #         self.hideshowplot(False)
    #         self.hideshoworder(False)
    #         self.hideshowimpo(False)
    #         self.hideshowpanelopt(False)
    #         self.help_frame.pack(expand=True, pady=5, padx=5) 
    #     else:
    #         self.help_frame.pack_forget()        




############################################################################################################ REPORT-PLOT

    def setupPlot(self):

        self.plot_frame = tk.Frame(self.root, bd=2, relief="groove")
        self.plot_frame.pack(expand=True, pady=5, padx=5, fill=tk.BOTH) 

        self.report_frame = tk.Frame(self.plot_frame, bd=2, relief="groove")
        self.report_frame.pack(side = tk.LEFT)

        #old good work
        # price_lab = tk.Label(self.report_frame, font=('Arial', 14))
        # price_lab.pack(side=tk.LEFT, pady=10)
        # dis_lab = tk.Label(self.report_frame)
        # dis_lab.pack(side=tk.LEFT, pady=10)
        # self.report_labs = price_lab, dis_lab

        # self.fig, self.axs = plt.subplots(3, 3, figsize=(15, 12))
        # self.canvas = FigureCanvasTkAgg(self.fig, master=self.plot_frame)
        # self.canvas.draw()
        # self.canvas.get_tk_widget().pack(pady=10, padx=10, fill=tk.BOTH)


        #new work
        report_lab = tk.Label(self.report_frame, font=('Arial', 14))
        report_lab.pack(side=tk.TOP, pady=10)
        
        self.plot_id = ctk.StringVar(value="prod_sales")
        report_dd = ctk.CTkComboBox(self.report_frame, values=["prod_sales", "day_revenue"],
                                            command=self.call_plot, variable=self.plot_id)
        
        self.plot_id.set("prod_sales")
        report_dd.pack(side=tk.TOP, pady=10)


        self.report_labs = report_lab

        fig1 , axs1 = plt.subplots(2, 2, figsize=(15, 12))
        fig2, axs2 = plt.subplots(2,2, figsize=(15,12))
        fig3, axs3 = plt.subplots(1,1, figsize=(15,12))
        canv1 = FigureCanvasTkAgg(fig1, master=self.plot_frame)
        canv1.draw()
        canv1.get_tk_widget().pack(pady=10, padx=10, fill=tk.BOTH)
        canv2 = FigureCanvasTkAgg(fig2, master=self.plot_frame)
        canv2.draw()
        canv2.get_tk_widget().pack(pady=10, padx=10, fill=tk.BOTH)
        canv3 = FigureCanvasTkAgg(fig3, master=self.plot_frame)
        canv3.draw()
        canv3.get_tk_widget().pack(pady=10, padx=10, fill=tk.BOTH)

        self.axs_list = axs1, axs2, axs3
        self.canv_list = canv1, canv2, canv3
        

    def call_plot(self, plot_id):
        if plot_id == 'prod_sales':
            self.prod_charts()
        
        if plot_id == 'day_revenue':
            self.day_charts()


        #ctk.CTkButton(master = self.plot_frame, text="Refresh Plot", command=self.plotta).pack(side=tk.TOP)
        #self.hideshowplot(False)

    def build_report(self):
        tot_price = self.dataset['prezzo'].astype(float).sum()
        tot_dis = self.dataset['sconto'].astype(float).sum()
        tot_quantity = self.dataset[self.impo['prodotto']].astype(int).sum(axis=1).sum()
        tot_orders = np.array(self.dataset['prezzo'].astype(float) > 0).astype(int).sum()

        report_lab = self.report_labs
        report_lab.config(text = 'RICAVI: '+ str(tot_price) + '€' + '\n' 
                         + 'SCONTI: '+str(tot_dis) + '€' + '\n' 
                         + '#CLIENTI: ' + str(tot_orders)+ '\n'
                         + '#VENDUTO: ' + str(tot_quantity)  )

    def prod_charts(self):

        axs1 , axs2, axs3 = self.axs_list# = self.axs_list#, axs2, axs3 = self.axs_list
        canv1, canv2, canv3 = self.canv_list# = self.canv_list#, canv2, canv3 = self.canv_list

        canv2.get_tk_widget().pack_forget()
        canv3.get_tk_widget().pack_forget()
        canv1.get_tk_widget().pack(pady=10, padx=10, fill=tk.BOTH)

        if (len(self.dataset) > 2):

            colonne = list(self.impo['prodotto']) #+ ['sconto', 'prezzo']
            for c in colonne:
                self.dataset[c] = pd.to_numeric(self.dataset[c])


            df = self.dataset.copy()
            if (df['ts'][0] == '0') or (df['ts'][0] == 0):
               df = df.drop([0])

            #filter data by today 
            tformat = "%Y-%m-%d %H:%M:%S.%f"   #2025-09-17 14:39:40.405671
            ts = [datetime.strptime(s, tformat).date() for s in  df['ts']]
            df['date'] = ts

            # df['date'] = self.dataset['ts']

            pivoTab = df.pivot_table(index = 'date', 
                                            values = colonne,
                                            aggfunc='sum',
                                            sort=False).T

            for c in self.used_cats:
                nomi = np.array(self.impo['prodotto'])[self.impo['categoria']==c].tolist()
                pivoTab_p = df.pivot_table(index = 'date', 
                                                values = nomi,
                                                aggfunc='sum',
                                                sort=False).T
                newrow = pivoTab_p.sum(axis=0)
                newrow.name = 'tot' + c
                pivoTab = pd.concat([pivoTab, newrow.to_frame().T])

            ####totale di ogni voce
            pivoTab = pivoTab.assign(TOT = pivoTab.sum(axis=1))
            
            #####creazione tabella
            for c in pivoTab.columns:
                    pivoTab[c] = pivoTab[c].astype(int)

            axs1[0][1].clear()
            axs1[0][1].axis('off')
            axs1[0][1].table(cellText = pivoTab.values, rowLabels = pivoTab.index, colLabels=pivoTab.columns, loc ='center')


            #pie chart

            #df1 = self.dataset[self.impo['prodotto']]
            #totali = [df1[prod].astype(int).sum() for prod in self.impo['prodotto']]
            prod_names = self.impo['prodotto']
            totali = pivoTab['TOT'][prod_names]


            axs1[0][0].clear()
            wedges, texts, autotexts = axs1[0][0].pie(totali, labels = prod_names, startangle=45, autopct='%1.1f%%')#,pctdistance=1.25, labeldistance=.6) #autopct=absolute_value)
            axs1[0][0].set_title('ventite totali')
            # Extract colors from the pie chart wedges
            colors = [wedge.get_facecolor() for wedge in wedges]

            # barplot 
            # prod_names = self.impo['prodotto'] 
            # prod_q = []
            # for p in prod_names:
            #     prod_q.append(self.dataset[p].astype(int).sum())

            #df_barplot = pd.DataFrame({'product':prod_names, 'quantity': totali})

            y_pos = np.arange(len(prod_names))


            axs1[1][0].axis('off')
            axs1[1][1].clear()
            #axs1[1][1] = sns.barplot(df_barplot, y='product', x='quantity', hue='product', orient='h')
            axs1[1][1].barh(y_pos, totali, tick_label=prod_names, color = colors)
            axs1[1][1].set_yticks(y_pos, labels=prod_names)
            axs1[1][1].set_xlabel('quantity')
            axs1[1][1].set_ylabel('product')
 
            canv1.draw()


    def day_charts(self):
        if (len(self.dataset) > 0):

            axs1 , axs2, axs3 = self.axs_list# = self.axs_list#, axs2, axs3 = self.axs_list
            canv1, canv2, canv3 = self.canv_list# = self.canv_list#, canv2, canv3 = self.canv_list

            canv1.get_tk_widget().pack_forget()
            canv3.get_tk_widget().pack_forget()
            canv2.get_tk_widget().pack(pady=10, padx=10, fill=tk.BOTH)


            #get data
            df = self.dataset.copy()
            if (df['ts'][0] == '0') or (df['ts'][0] == 0):
                df = df.drop([0])

            #get dates
            tformat = "%Y-%m-%d %H:%M:%S.%f"
            tformat2 = "%d/%m/%y"
            date = [datetime.strptime(t, tformat).strftime(tformat2)  for t in df['ts']]
            df['date'] = date

            #get totals
            prod_names = self.impo['prodotto']
            prod_totals = np.array(df[prod_names].sum(axis=1))
            


            date_u = np.unique(date)
            ricavi = []
            sconti = []
            n_ordini = []
            n_vendite = []

            
            for d in date_u:
                ricavi.append(df['prezzo'][df['date']==d].astype(float).sum())
                sconti.append(df['sconto'][df['date']==d].astype(float).sum())
                n_ordini.append(np.array(df['date']==d).astype(int).sum())
                n_vendite.append(np.array(prod_totals[df['date']==d]).astype(int).sum())

            #df_barplot = pd.DataFrame({'date': unici, 'revenue': ricavi})

            axs2[1][0].axis('off')

            axs2[1][1].clear()
            axs2[1][1].bar(date_u, ricavi) #= sns.barplot(df_barplot, y='date', x='revenue', orient='v')
            axs2[1][1].set_title('ricavi per giorni')
            axs2[1][1].set_xlabel('date')
            axs2[1][1].set_ylabel('revenue')


            axs2[0][0].clear()
            axs2[0][0].axis('off')
            axs2[0][0].pie(ricavi, labels = date_u, startangle=45, autopct='%1.1f%%')
            axs2[0][0].set_title('% ricavi per giorni')


            date_u = date_u.tolist()
            s_ricavi = np.array(ricavi).sum()
            m_ricavi = np.round(np.array(ricavi).mean(), 2)
            ricavi.append(s_ricavi)
            ricavi.append(m_ricavi)
            s_sconti = np.array(sconti).sum()
            m_sconti = np.round(np.array(sconti).mean(), 2)
            sconti.append(s_sconti)
            sconti.append(m_sconti)       
            s_n_vendite = np.array(n_vendite).astype(int).sum()
            m_n_vendite = np.round(np.array(n_vendite).astype(int).mean(), 2)
            n_vendite.append(s_n_vendite)
            n_vendite.append(m_n_vendite)                      
            s_n_ordini = np.array(n_ordini).sum()
            m_n_ordini = np.round(np.array(n_ordini).mean(), 2)
            n_ordini.append(s_n_ordini)
            n_ordini.append(m_n_ordini)         

            date_u.append('TOT')
            date_u.append('MEAN')

            tab = pd.DataFrame({'ricavi': ricavi, 'sconti': sconti, 'n_ordini': n_ordini, 'n_vendite': n_vendite})
            tab.index = date_u

            axs2[0][1].clear()
            axs2[0][1].axis('off')
            axs2[0][1].table(cellText = tab.values, rowLabels = tab.index, colLabels=tab.columns, loc ='center')


            canv2.draw()


    def pie_chart(self):


        # Pie

        # self.fig, self.axs = plt.subplots(2, 2, figsize=(13, 9))
        # self.canvas = FigureCanvasTkAgg(self.fig, master=self.plot_frame)
        # self.canvas.draw()
        # self.canvas.get_tk_widget().pack(pady=10, padx=10, fill=tk.BOTH)
        

        #self.axs[0][0].clear()
        if (len(self.dataset) > 2):

            df1 = self.dataset[self.impo['prodotto']]
            totali = [df1[prod].astype(int).sum() for prod in self.impo['prodotto']]

            self.axs[0][0].clear()
            self.axs[0][0].pie(totali, labels = self.impo['prodotto'], startangle=45, autopct='%1.1f%%')#,pctdistance=1.25, labeldistance=.6) #autopct=absolute_value)
            self.axs[0][0].set_title('ventite totali')

            # self.axs[0].clear()
            # self.axs[0].pie(totali, labels = self.impo['prodotto'], startangle=45, autopct='%1.1f%%')#,pctdistance=1.25, labeldistance=.6) #autopct=absolute_value)
            # self.axs[0].set_title('ventite totali')


    def table_chart(self):
        
        # data for plotting
        colonne = list(self.impo['prodotto']) #+ ['sconto', 'prezzo']
        for c in colonne:
            self.dataset[c] = pd.to_numeric(self.dataset[c])

        # Pivot
        #self.axs[0][1].clear()
        if (len(self.dataset) > 0):
            
            df = self.dataset.copy()
            if (df['ts'][0] == '0') or (df['ts'][0] == 0):
               df = df.drop([0])

            #filter data by today 
            tformat = "%Y-%m-%d %H:%M:%S.%f"   #2025-09-17 14:39:40.405671
            ts = [datetime.strptime(s, tformat).date() for s in  df['ts']]
            df['date'] = ts

            # df['date'] = self.dataset['ts']

            pivoTab = df.pivot_table(index = 'date', 
                                            values = colonne,
                                            aggfunc='sum',
                                            sort=False).T

            for c in self.used_cats:
                nomi = np.array(self.impo['prodotto'])[self.impo['categoria']==c].tolist()
                pivoTab_p = df.pivot_table(index = 'date', 
                                                values = nomi,
                                                aggfunc='sum',
                                                sort=False).T
                newrow = pivoTab_p.sum(axis=0)
                newrow.name = 'tot' + c
                pivoTab = pd.concat([pivoTab, newrow.to_frame().T])

            ####totale di ogni voce
            pivoTab = pivoTab.assign(TOT = pivoTab.sum(axis=1))
            
            #####creazione tabella
            for c in pivoTab.columns:
                    pivoTab[c] = pivoTab[c].astype(int)

            self.axs[1][0].clear()
            self.axs[1][0].axis('off')
            self.axs[1][0].table(cellText = pivoTab.values, rowLabels = pivoTab.index, colLabels=pivoTab.columns, loc ='center')
            #self.axs[1][0].set_title('totali per giorno')  #questo titolo si sovrappone alla tabella

            # self.axs[1].clear()
            # self.axs[1].axis('off')
            # self.axs[1].table(cellText = pivoTab.values, rowLabels = pivoTab.index, colLabels=pivoTab.columns, loc ='center')
            # self.axs[1].set_title('totali per giorno')  #questo titolo si sovrappone alla tabella


    def barplot_chart(self):
        # barplot
        
        if (len(self.dataset) > 0):
            prod_names = self.impo['prodotto'] 
            prod_q = []
            for p in prod_names:
                prod_q.append(self.dataset[p].astype(int).sum())

            df_barplot = pd.DataFrame({'product':prod_names, 'quantity': prod_q})

            y_pos = np.arange(len(prod_names))

            # self.axs[2][2].clear()
            # self.axs[2][2] = sns.barplot(df_barplot, y='product', x='quantity', hue='product', orient='h')

            # self.axs[2].clear()
            # self.axs[2] = sns.barplot(df_barplot, y='product', x='quantity', hue='product', orient='h')


            # self.axs[0][2].barh(y_pos, prod_q, tick_label=prod_names)
            # self.axs[0][2].set_yticks(y_pos, labels=prod_names)
            # self.axs[0][2].set_xlabel('quantity')
            # self.axs[0][2].set_ylabel('product')


    def info_chart2(self):
        # barplot
        
        if (len(self.dataset) > 0):

            #get data
            df = self.dataset.copy()
            if (df['ts'][0] == '0') or (df['ts'][0] == 0):
                df = df.drop([0])

            #get dates
            tformat = "%Y-%m-%d %H:%M:%S.%f"
            tformat2 = "%d/%m/%y"
            date = [datetime.strptime(t, tformat).strftime(tformat2)  for t in df['ts']]
            df['date'] = date

            #get totals
            prod_names = self.impo['prodotto']
            prod_totals = np.array(df[prod_names].sum(axis=1))
            


            date_u = np.unique(date)
            ricavi = []
            sconti = []
            n_ordini = []
            n_vendite = []

            
            for d in date_u:
                ricavi.append(df['prezzo'][df['date']==d].astype(float).sum())
                sconti.append(df['sconto'][df['date']==d].astype(float).sum())
                n_ordini.append(np.array(df['date']==d).astype(int).sum())
                n_vendite.append(np.array(prod_totals[df['date']==d]).astype(int).sum())

            #df_barplot = pd.DataFrame({'date': unici, 'revenue': ricavi})

            self.axs[2][0].clear()
            self.axs[2][0].bar(date_u, ricavi) #= sns.barplot(df_barplot, y='date', x='revenue', orient='v')
            self.axs[2][0].set_title('ricavi per giorni')
            self.axs[2][0].set_xlabel('date')
            self.axs[2][0].set_ylabel('revenue')

            # self.axs[0].clear()
            # self.axs[0].bar(unici, ricavi) #= sns.barplot(df_barplot, y='date', x='revenue', orient='v')
            # self.axs[0].set_title('ricavi per giorni')
            # self.axs[0].set_xlabel('date')
            # self.axs[0].set_ylabel('revenue')


            self.axs[0][2].clear()
            self.axs[0][2].axis('off')
            self.axs[0][2].pie(ricavi, labels = date_u, startangle=45, autopct='%1.1f%%')
            self.axs[0][2].set_title('% ricavi per giorni')

            # self.axs[2].clear()
            # self.axs[2].axis('off')
            # self.axs[2].pie(ricavi, labels = unici, startangle=45, autopct='%1.1f%%')
            # self.axs[2].set_title('% ricavi per giorni')



            date_u = date_u.tolist()
            s_ricavi = np.array(ricavi).sum()
            m_ricavi = np.round(np.array(ricavi).mean(), 2)
            ricavi.append(s_ricavi)
            ricavi.append(m_ricavi)
            s_sconti = np.array(sconti).sum()
            m_sconti = np.round(np.array(sconti).mean(), 2)
            sconti.append(s_sconti)
            sconti.append(m_sconti)       
            s_n_vendite = np.array(n_vendite).astype(int).sum()
            m_n_vendite = np.round(np.array(n_vendite).astype(int).mean(), 2)
            n_vendite.append(s_n_vendite)
            n_vendite.append(m_n_vendite)                      
            s_n_ordini = np.array(n_ordini).sum()
            m_n_ordini = np.round(np.array(n_ordini).mean(), 2)
            n_ordini.append(s_n_ordini)
            n_ordini.append(m_n_ordini)         


            date_u.append('TOT')
            date_u.append('MEAN')

            tab = pd.DataFrame({'ricavi': ricavi, 'sconti': sconti, 'n_ordini': n_ordini, 'n_vendite': n_vendite})
            tab.index = date_u

            self.axs[1][2].clear()
            self.axs[1][2].axis('off')
            self.axs[1][2].table(cellText = tab.values, rowLabels = tab.index, colLabels=tab.columns, loc ='center')

            # self.axs[1].clear()
            # self.axs[1].axis('off')
            # self.axs[1].table(cellText = tab.values, rowLabels = tab.index, colLabels=tab.columns, loc ='center')



    def plotta(self):
        #self.hideshowplot(True)
        self.show_frame('plot')
        self.build_report()
        self.call_plot(self.plot_id.get())



        #old good work
        # self.build_report()
        # self.info_chart2()
        # self.pie_chart()
        # self.table_chart()
        # self.barplot_chart()
        
        # self.axs[0][1].axis('off')
        # self.axs[1][1].axis('off')
        # self.axs[2][1].axis('off')


        #new work
        #self.build_report()
        #self.prod_charts()
        #self.day_charts()

        
        #self.canvas.draw()




############################################################################################################ ORDINI

    def setupOrdini(self):
        self.order_frame = tk.Frame(self.root)
        self.order_frame.pack(expand=True, pady=5, padx=5)  

        scrollbar = tk.Scrollbar(self.order_frame)    # Creiamo una barra di scorrimento verticale
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)


        #header control
        head_command = tk.Frame(self.order_frame)   #crea header
        head_command.pack(side=tk.TOP)

        tk.Label(head_command, text='Seleziona status di ogni ordine                ', 
                 font=('Arial', 12)).pack(side=tk.LEFT, padx=20)

        tk.Label(head_command, text='Seleziona status degli ordini selezionati:', 
                 font=('Arial', 12)).pack(side=tk.LEFT, padx=1)
        
        #global dropdown
        clicked = tk.StringVar()
        clicked.set('TODO')

        drop = tk.OptionMenu(head_command, clicked, *self.opts,
        command = lambda sel = clicked : self.change_status_global(sel) )  # Create Dropdown menu 
        drop.pack(side=tk.LEFT, padx=1)

        self.ord_canvas = tk.Canvas(self.order_frame, yscrollcommand=scrollbar.set)  # Creiamo un canvas che conterrà il frame scrollabile
        self.ord_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)
        scrollbar.config(command=self.ord_canvas.yview)

        self.scrollable_frame = tk.Frame(self.ord_canvas)    # Creiamo un frame all'interno del canvas
        self.ord_canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")  # Creiamo un window per il canvas, che conterrà il frame scrollabile
        def on_configure(event):  # Funzione per aggiornare la dimensione del canvas al ridimensionamento del frame
                self.ord_canvas.configure(scrollregion=self.ord_canvas.bbox("all"))
        self.scrollable_frame.bind("<Configure>", on_configure)

        self.fill_scrollbar()

    def fill_scrollbar(self):
        self.scrollable_frame.destroy()

        self.scrollable_frame = tk.Frame(self.ord_canvas)    # Creiamo un frame all'interno del canvas
        self.ord_canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")  # Creiamo un window per il canvas, che conterrà il frame scrollabile
        def on_configure(event):  # Funzione per aggiornare la dimensione del canvas al ridimensionamento del frame
                self.ord_canvas.configure(scrollregion=self.ord_canvas.bbox("all"))
        self.scrollable_frame.bind("<Configure>", on_configure)

        # Stile personalizzato
        label_font = ("Arial", 14)
        button_font = ("Arial", 8, "bold")
        row_height = 1  # altezza righe separatrici
        self.check_list = []

        for i in range(len(self.dataset)):
                i = len(self.dataset) - (i+1)
                
                str_Nome = self.dataset.loc[i, "cliente"]

                #print(self.dataset.columns) #debug sul dataset
                str_Status = self.dataset.loc[i, "status"]
                str_gg = self.dataset.loc[i, "giorno"]

                row_frame = tk.Frame(self.scrollable_frame, pady=5)
                row_frame.pack(fill=tk.X)

                label_nome = tk.Label(row_frame, text=str_Nome, font=label_font)
                label_nome.pack(side=tk.LEFT, padx=10)


                #check box for automatic selection
                checkVar = tk.IntVar()
                checkVar.set(0)
                self.check_list.append(checkVar)

                def read_cv(cv):
                    #print(cv.get())

                    checkinput = ctk.CTkCheckBox(row_frame,  text='',  variable=checkVar, 
                                                onvalue=1, offvalue=0,
                                                command = lambda cv = checkVar: read_cv(cv))
                    checkinput.pack(side=tk.LEFT, padx=5)                


                #dropdown for single selection
                clicked = tk.StringVar()
                clicked.set(str_Status)

                label_status = tk.Label(row_frame, text=str_Status, textvariable=clicked, font=label_font)
                label_status.pack(side=tk.LEFT, padx=10)

                #clicked.set(self.opts[0])  # initial menu text 
                drop = tk.OptionMenu(row_frame, clicked, *self.opts,
                command = lambda sel = i, id = i: self.change_status(id, sel) )  # Create Dropdown menu 
                drop.pack(side=tk.LEFT, padx=10)


                #day label
                label_giorno = tk.Label(row_frame, text=str_gg, font=label_font)
                label_giorno.pack(side=tk.LEFT, padx=10)

                #cancel order button
                btn = tk.Button(row_frame, text="REMOVE", font=button_font,
                command=lambda r = i: self.remove_row(r))
                btn.pack(side=tk.LEFT, padx=200)

                # Aggiungiamo una linea di separazione
                separatore = tk.Frame(self.scrollable_frame, height=row_height, bg="gray")
                separatore.pack(fill=tk.X, pady=1)
        

    def remove_row(self, id):        
        self.dataset = self.dataset.drop(self.dataset.index[id]).reset_index(drop=True)
        self.aggiornaDati0()
        #print(self.dati)
        self.parent.update_sv()
        self.parent.update_qv()
        self.fill_scrollbar()
        

    def change_status_global(self, status):
        ''' cambia lo status di tutti gli ordini selezionati, dal dropdown in alto'''
        cl = self.check_list
        ids = np.array([i for i in range(len(cl)) if cl[i].get()==1])
        for i in ids:
            i = len(self.dataset) - (i+1) #inverti l'ordine delle righe
            self.change_status(i, status)
        self.fill_scrollbar()


    def change_status(self, id, status):
        ''' cambia lo status del singolo ordine '''
        #print(id)
        #print(status)
        self.dataset.loc[id, 'status'] = status
        self.aggiornaDati0()
        #self.fill_scrollbar()
        #self.parent.SV.update()
        self.parent.update_sv()
        self.parent.update_qv()


############################################################################################################ SCONTI


    def setupScontiUi(self):
        sconti_frame = tk.Frame(self.root)
        sconti_frame.pack(expand=True, pady=5, padx=5)

        scontiControl = tk.Frame(sconti_frame)
        scontiControl.pack(side = tk.TOP)

        self.scontiCatForm = tk.Frame(sconti_frame)
        self.scontiCatForm.pack(side = tk.LEFT)

        self.scontiListForm = tk.Frame(sconti_frame)
        self.scontiListForm.pack(side = tk.LEFT)

        self.scontoList = []
        


