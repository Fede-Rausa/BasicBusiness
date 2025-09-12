import tkinter as tk
import pandas as pd
import numpy as np
import datetime as dt
import os
#from tkintertable import TableCanvas, TableModel
from tkinter import ttk

class CostManager:
    def __init__(self, parent, root):
        self.parent = parent
        self.root = root
        self.root.title("Cost Analysis tool")
        self.ingprice_path = 'prezzi_ingredienti.csv'
        self.proding_path = 'prodotti_ingredienti.csv'
        self.listaspesa_path = 'lista_spesa.csv'
        self.costo_venduto_path = 'costo_venduto.csv' 

        
        #tipi ingredienti
        self.setupIngUi()
        self.auto_fill_ingredients()
        #ingredienti per piatto
        self.setupTableMenuUi()
        self.auto_fill_ricette()

        #costo del venduto
        self.setupCostoVendutoUi()

        #lista della spesa
        self.setupListaSpesaUi()

        self.setupMenu()

        self.show_frame('ing')

    
    def setupMenu(self):
        self.menubar = tk.Menu(self.root)
        self.root.config(menu=self.menubar)
        self.menubar.add_command(label="INGREDIENTI", command = lambda: self.show_frame('ing'))
        self.menubar.add_command(label="RICETTE", command = lambda: self.show_frame('ricette'))
        self.menubar.add_command(label="COSTO DEL VENDUTO", command = lambda: self.show_frame('cv'))
        self.menubar.add_command(label="LISTA DELLA SPESA", command = lambda: self.show_frame('ls'))



    def show_frame(self, fr_name):
        frames = [self.menu_frame, self.ing_frame, self.cv_frame, self.ls_mat]
        fr_names = np.array(['ricette', 'ing','cv', 'ls'])
        id = np.where(fr_names == fr_name)[0] #np.where restituisce l'array degli indici dove è vero, perciò va selezionato [0]
        for i in range(len(frames)):
            if (i != id):
                frames[i].pack_forget()
            else:
                frames[i].pack(expand=True, padx=5, pady=5, fill=tk.BOTH)




##################### INSERIMENTO INGREDIENTI

    def setupIngUi(self):
        #liste sorgenti dati
        self.lista_ing_ui = []
        self.lista_ping_ui = []
        #liste container
        self.lista_ing_id = []
        self.lista_ing_r = []

        self.ing_frame = tk.Frame(self.root)
        self.ing_frame.pack(expand=True, padx=5, pady=5, fill=tk.BOTH)

        buttons_fr = tk.Frame(self.ing_frame)
        buttons_fr.pack(side=tk.TOP)

        tk.Button(buttons_fr, text='add ingredient with kg price', 
                    command = self.addIngRow,
                    font=('Calibri', '12', 'bold')).pack(side=tk.LEFT)
        tk.Button(buttons_fr, text='remove last', 
                    command = self.rmIngRow,
                    font=('Calibri', '12', 'bold')).pack(side=tk.LEFT)
        tk.Button(buttons_fr, text='RESET INGREDIENTS', 
                    command = self.auto_fill_ingredients,
                    font=('Calibri', '12', 'bold')).pack(side=tk.LEFT)
        tk.Button(buttons_fr, text='UPDATE INGREDIENTS', 
                    command = self.export_ingredients,
                    font=('Calibri', '12', 'bold')).pack(side=tk.LEFT)
        
        calculator_frame = tk.Frame(self.ing_frame)
        calculator_frame.pack(side=tk.LEFT)

        #self.mat_frame = tk.Frame(self.ing_frame)
        #self.mat_frame.grid(row = 4, column = 1)

        scrollbar = tk.Scrollbar(self.ing_frame)    # Creiamo una barra di scorrimento verticale
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)#grid(row=4, column=10)

        self.mat0_frame = tk.Canvas(self.ing_frame, yscrollcommand=scrollbar.set)  # Creiamo un canvas che conterrà il frame scrollabile
        self.mat0_frame.pack(side=tk.TOP)#grid(row=4, column=1)
        scrollbar.config(command=self.mat0_frame.yview)

        self.mat_frame = tk.Frame(self.mat0_frame)    # Creiamo un frame all'interno del canvas
        self.mat0_frame.create_window((0, 0), window=self.mat_frame, anchor="nw")  # Creiamo un window per il canvas, che conterrà il frame scrollabile
        def on_configure(event):  # Funzione per aggiornare la dimensione del canvas al ridimensionamento del frame
                self.mat0_frame.configure(scrollregion=self.mat0_frame.bbox("all"))
        self.mat_frame.bind("<Configure>", on_configure)

        myFont = ('Arial', 14)
        row = tk.Frame(self.mat_frame)
        row.pack(side=tk.TOP)#grid(row=1, column=1)
        tk.Label(row,  text='Ingredient', font=myFont).pack(side=tk.LEFT)#grid(row=1, column=1, padx=5)
        tk.Label(row,  text='Kg Price', font=myFont).pack(side=tk.LEFT)#grid(row=1, column=2, padx=0)

    def addIngRow(self, nome_ing = None, pr_ing = None):
        myFont = ('Arial', 10)

        i = len(self.lista_ing_ui)
        r = i + 2

        row = tk.Frame(self.mat_frame)
        row.pack(side=tk.TOP)#grid(row=r, column=1)

        nome = tk.Entry(row, font=myFont)
        nome.pack(side=tk.LEFT)#grid(row = r, column = 1, padx = 5)
        prezzoKg = tk.Spinbox(row, from_=0, to=99, increment=0.01, 
        font=myFont, width=6, repeatinterval=100, repeatdelay=500)
        prezzoKg.pack(side=tk.LEFT)#grid(row = r, column = 2, padx = 5)

        tk.Label(row, text='€', font=myFont).pack(side=tk.LEFT)#grid(row = r, column = 3, padx = 5)

        self.lista_ing_ui.append(nome)
        self.lista_ping_ui.append(prezzoKg)
        self.lista_ing_r.append(row)

        if (nome_ing != None):
            nome.delete(0,tk.END)
            nome.insert(0, nome_ing)
            prezzoKg.delete(0,tk.END)
            prezzoKg.insert(0, pr_ing)


    def rmIngRow(self):
        id = len(self.lista_ing_r) - 1
        self.lista_ing_r[id].destroy()
        self.lista_ing_r.pop(id)
        self.lista_ing_ui.pop(id)
        self.lista_ping_ui.pop(id)


    def export_ingredients(self):
        nomi = np.array([n.get() for n in self.lista_ing_ui])
        prezzi = np.array([n.get() for n in self.lista_ping_ui]).astype(float)
        prezzi = prezzi[nomi != '']
        nomi = nomi[nomi != '']

        df = pd.DataFrame({
            'ingredienti': nomi,
            'prezziKg': prezzi
        })
        df.to_csv(self.ingprice_path, sep=';', decimal=',', index=False)
        
        print(nomi)
        print(prezzi)

    def auto_fill_ingredients(self):
        if (os.path.exists(self.ingprice_path)):
            df = pd.read_csv(self.ingprice_path, sep=';', decimal=',')
            nomi = df['ingredienti']
            prezzi = df['prezziKg']

            for i in range(len(self.lista_ing_r)):
                self.rmIngRow()

            for i in range(df.shape[0]):
                self.addIngRow(nomi[i], prezzi[i])
        else:
            print('ingredienti non trovati, ingredienti generati')
            nomi = np.array(['pane azimut', 'pomodori', 'mozzarella', 'prosciutto', 'funghi', 'olive', 'cipolla', 'salsiccia', 'peperoni', 'wurstel', 'patate'])
            prezzi = np.array([1.5, 0.5, 3.5, 2.5, 1.5, 1.5, 0.5, 3.5, 1.5, 1.5, 0.5])
            df = pd.DataFrame({'ingredienti':nomi, 'prezziKg':prezzi})
            df.to_csv(self.ingprice_path, sep=';', decimal=',', index=False)
            self.auto_fill_ingredients()

                


############### DESCRIZIONE PRODOTTO

    def setupTableMenuUi(self):
        self.menu_frame = tk.Frame(self.root)
        self.menu_frame.pack(expand=True, padx=5, pady=5, fill=tk.BOTH)
        self.ing_names = np.array([p.get() for p in self.lista_ing_ui])

        font0 = ('Verdana', 12)
        tk.Label(self.menu_frame, text='ricettario e costo unitario', font=font0).pack(side=tk.TOP)
        box0 = tk.Frame(self.menu_frame)
        box0.pack(side=tk.TOP)
        tk.Button(box0, text='compute costs', font=font0, command=self.compute_unit_costs).pack(side=tk.LEFT)
        tk.Button(box0, text='reset data', font=font0, command=self.auto_fill_ricette).pack(side=tk.LEFT)
        tk.Button(box0, text='update data', font=font0, command=self.export_ricette).pack(side=tk.LEFT)


        self.lista_liste_ing = []
        self.lista_liste_imp = []
        self.lista_liste_row = []
        self.lista_mat_ing = []
        self.cost_unit_ui = []

        def scroll_area(main_frame):
            scrollbar = tk.Scrollbar(main_frame)    # Creiamo una barra di scorrimento verticale
            scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

            mat0 = tk.Canvas(main_frame, yscrollcommand=scrollbar.set)  # Creiamo un canvas che conterrà il frame scrollabile
            mat0.pack(side=tk.TOP, expand=True, fill=tk.BOTH, padx=(500,0))
            scrollbar.config(command=mat0.yview)

            mat1 = tk.Frame(mat0)    # Creiamo un frame all'interno del canvas
            mat0.create_window((0, 0), window=mat1, anchor='center')  # Creiamo un window per il canvas, che conterrà il frame scrollabile
            def on_configure(event):  # Funzione per aggiornare la dimensione del canvas al ridimensionamento del frame
                    mat0.configure(scrollregion=mat0.bbox("all"))
            mat1.bind("<Configure>", on_configure)
            return mat1

        self.table_frame = scroll_area(self.menu_frame)

        self.auto_fill_start()


    def auto_fill_start(self):
        #carica dati
        self.ing_names = np.array([p.get() for p in self.lista_ing_ui])
        self.ing_prices = np.array([p.get() for p in self.lista_ping_ui]).astype(float)
        self.prod_names = self.parent.SM.impo['prodotto']
        self.prod_prices = np.array(self.parent.SM.impo['prezzo']).astype(float)

        for p in self.prod_names:
            self.add_row(p)

    def add_row(self, nome):

        id = len(self.lista_liste_ing)
        self.lista_liste_ing.append([])
        self.lista_liste_imp.append([])
        self.lista_liste_row.append([])

        myFont = ('Calibri', 12)

        row = tk.Frame(self.table_frame, relief='sunken', bd=2)
        row.pack(side=tk.TOP)

        tk.Label(row, text=nome, font=myFont).pack(side=tk.LEFT, padx=2)

        box1 = tk.Frame(row)
        box1.pack(side=tk.LEFT)

        mat = tk.Frame(row)
        mat.pack(side=tk.LEFT)
        self.lista_mat_ing.append(mat)

        tk.Button(box1, text='add ingredient', font=myFont, command=lambda: self.add_subrow(mat, id)).pack(side=tk.TOP, padx=2)
        tk.Button(box1, text='remove last', font=myFont, command=lambda: self.rm_subrow(id)).pack(side=tk.TOP, padx=2)

        #tk.Label(row, text='costo unitario: € ', font =myFont).pack(side=tk.LEFT)
        

        init_str = 'costo unitario: € 0\nprezzo unitario: € 0\nmargine unitario: € 0'
        costo_unitario = tk.Label(row, text=init_str, font = myFont)
        costo_unitario.pack(side=tk.LEFT)
        self.cost_unit_ui.append(costo_unitario)
        
        

    def add_subrow(self, frame, id):

        font0 = ('Calibri', 12)

        row = tk.Frame(frame, relief='sunken', bd=2)
        row.pack(side=tk.TOP)

        selFiltri = self.ing_names 
        actualStatus = tk.StringVar()
        actualStatus.set(selFiltri[0])
        tipo_opt = tk.OptionMenu(row, actualStatus, *selFiltri) # dropdown
        tipo_opt.config(font=font0)
        tipo_opt.pack(side=tk.LEFT, padx=10)

        tk.Label(row, text='g per unit: ', font=font0).pack(side=tk.LEFT)
        quant = tk.Spinbox(row, from_=0, to=9990, increment=5, width=5, 
            relief="groove", repeatdelay=500, repeatinterval=100,
            font=font0, bg="aliceblue", fg="green")#, command=self.on_spinbox_change)
        quant.pack(side=tk.LEFT)
        

        self.lista_liste_row[id].append(row)
        self.lista_liste_ing[id].append(actualStatus)
        self.lista_liste_imp[id].append(quant)

    def rm_subrow(self, id0):
        id1 = len(self.lista_liste_ing[id0]) - 1
        if (id1 >=0):
            self.lista_liste_row[id0][id1].destroy()
            self.lista_liste_row[id0].pop(id1)
            self.lista_liste_ing[id0].pop(id1)
            self.lista_liste_imp[id0].pop(id1)
    
    def rm_all_subrows(self, id0):
        N_ = len(self.lista_liste_ing[id0])
        if (N_ > 0):
            for i in range(N_):
                id1 = N_ - 1 - i
                #print(id1)
                self.lista_liste_row[id0][id1].destroy()
                self.lista_liste_row[id0].pop(id1)
                self.lista_liste_ing[id0].pop(id1)
                self.lista_liste_imp[id0].pop(id1)

    def compute_unit_costs(self):
        self.ing_names = np.array([p.get() for p in self.lista_ing_ui])
        self.ing_prices = np.array([p.get() for p in self.lista_ping_ui]).astype(float)

        N_prods = len(self.prod_names)
        self.prezzi_ing_kg = dict(zip(self.ing_names, self.ing_prices)) #dict(zip(keys, values))

        self.cost_unit = []
        for i in range(N_prods):
            ing_list, gram_list = self.extract_ing_ui_lists(ing_list_ui=self.lista_liste_ing[i], 
                                                            gram_list_ui=self.lista_liste_imp[i])
            uc = self.compute_uc(ing_list, gram_list)  #unit cost
            up = self.prod_prices[i]              #unit sell price
            um = np.round(up - uc,2)                          #unit margin
            tx = f'costo unitario: € {uc}\nprezzo unitario: € {up}\nmargine unitario: € {um}'
            self.cost_unit_ui[i].config(text=tx)
            self.cost_unit.append(uc)


    
    def compute_uc(self, ing_list, gram_list):
        # uc = 0
        # for j in len(ing_list):
        #     price = prezzi_ing_kg[ing_list[j]]
        #     q = gram_list[j]
        #     uc += price*q
        #uc = uc/1000

        prices = np.array([self.prezzi_ing_kg[ing_list[j]] for j in range(len(ing_list))]).astype(float)
        quantities = np.array(gram_list).astype(float)
        uc = np.dot(prices, quantities)/1000
        return uc
    
    def extract_ing_ui_lists(self, ing_list_ui, gram_list_ui):
        N_ing = len(ing_list_ui)
        ing_list = [ing_list_ui[i].get() for i in range(N_ing)]
        gram_list = [gram_list_ui[i].get() for i in range(N_ing)]
        return ing_list, gram_list


    def export_ricette(self):

        N_prods = len(self.prod_names)
        self.prezzi_ing_kg = dict(zip(self.ing_names, self.ing_prices)) #dict(zip(keys, values))

        prodotto = []
        ingrediente = []
        grammi = []
        costi = []

        for i in range(N_prods):
            ing_list, gram_list = self.extract_ing_ui_lists(ing_list_ui=self.lista_liste_ing[i], 
                                                            gram_list_ui=self.lista_liste_imp[i])
            gram_list = np.array(gram_list).astype(float)
            for j in range(len(ing_list)):
                prodotto.append(self.prod_names[i])
                ingrediente.append(ing_list[j])
                grammi.append(gram_list[j])
                pkg = self.prezzi_ing_kg[ing_list[j]]
                costi.append(pkg*gram_list[j]/1000)

        df = pd.DataFrame({
            'prodotto':prodotto,
            'ingrediente':ingrediente,
            'grammi':grammi,
            'costi':costi
        })
        df.to_csv(self.proding_path, sep=';', decimal=',', index=False)

        self.compute_unit_costs()


    def auto_fill_ricette(self):
        if (os.path.exists(self.proding_path)):
            df = pd.read_csv(self.proding_path, sep=';', decimal=',')
            prods = np.array(df['prodotto'])
            ings = np.array(df['ingrediente'])
            grams = np.array(df['grammi']).astype(float)
        else:
            #inizializza un dataframe con le variabili d'ambiente
            #ATTENTO: devi modificarlo quando le variabili d'ambiente vengono modificate
            df = pd.DataFrame({
                'prodotto':self.prod_names,
                'ingrediente':np.repeat(self.ing_names[0], len(self.prod_names)),
                'grammi':np.repeat(0, len(self.prod_names))
            })

            #inzializza un dataframe vuoto
            #df = pd.DataFrame(columns = ['prodotto', 'ingrediente', 'grammi'])

            df.to_csv(self.proding_path, sep=';', decimal=',', index=False)
            self.auto_fill_ricette()

            #non richiamare questa funzione (l'hai appena già richiamata)
            return

        ###verifica che tutti gli ingredienti siano registrati nelle variabili d'ambiente
        ingprice_df = pd.read_csv(self.ingprice_path, sep=';', decimal=',')
        bools = df['ingrediente'].isin(ingprice_df['ingredienti'])
        at_least_one_false = not (bools).all()
        if (at_least_one_false):
            df = df[bools]

            if (df.empty): #se il dataframe è vuoto rimuovi il file, in modo che ci sia il refill automatico del primo ingrediente
                os.remove(self.proding_path)
            else:  #altrimenti aggiornalo
                df.to_csv(self.proding_path, sep=';', decimal=',', index=False)

            self.auto_fill_ricette()
            #non richiamare questa funzione (l'hai appena già richiamata)
            return

        #self.ing_names = np.array([p.get() for p in self.lista_ing_ui])
        #rimuovi tutti gli ingredienti in df['ingrediente'] che non sono in self.ing_names


        ## svuota ingredienti per tutti i prodotti
        for i in range(len(self.prod_names)):
            self.rm_all_subrows(i)        
            prod_name = self.prod_names[i]
            count = (prods==prod_name).sum()
            if (count > 0):
                for j in range(count):
                    #print(prod_name, ings[j], j, i)
                    self.add_subrow(frame=self.lista_mat_ing[i], id=i)


        ## riempi ingredienti per tutti i prodotti
        for i in range(len(self.prod_names)):
            prod_name = self.prod_names[i]
            bool_id = (prods==prod_name)
            ings_list = ings[bool_id]
            grams_list = grams[bool_id]
            if (len(ings_list) > 0):
                for j in range(len(ings_list)):
                    self.lista_liste_ing[i][j].set(ings_list[j])
                    self.lista_liste_imp[i][j].delete(0,"end")
                    self.lista_liste_imp[i][j].insert(0, grams_list[j])

        self.compute_unit_costs()


################ COSTO DEL VENDUTO

    def setupCostoVendutoUi(self):
        self.cv_frame = tk.Frame(self.root)
        self.cv_frame.pack(expand=True, padx=5, pady=5, fill=tk.BOTH)

        font0= ('Calibri', 12)
        tk.Label(self.cv_frame, text= 'COSTO DEL VENDUTO', font=font0).pack(side=tk.TOP)
        tk.Button(self.cv_frame, text='refresh and update display', 
                  command=self.add_rows_cv, font = font0).pack(side=tk.TOP)

        self.tab_cv = tk.Frame(self.cv_frame)
        self.tab_cv.pack(side=tk.TOP)
        self.cv_pretty_table = ttk.Treeview(self.cv_frame, columns=list(), show="headings")
        self.cv_rows = []
        self.add_rows_cv()
        

    def load_treeview_in_frame_cv(self, df, frame):
        """
        Loads a pandas DataFrame into a Treeview inside a specified frame.

        Args:
            df: The pandas DataFrame to display.
            frame: The Tkinter Frame widget to contain the Treeview.
        """

        # Define a function to clear all the items present in Treeview
        for item in self.cv_pretty_table.get_children():
            self.cv_pretty_table.delete(item)

        #df['budget'] = df['budget'].apply(lambda x: '€ '+str(x))
        #df['quantity'] = df['quantity'].apply(lambda x: str(x)+' g')

        
        self.cv_pretty_table.config(columns=list(df.columns), height=df.shape[0])

        # Add column headings
        for col in df.columns:
            self.cv_pretty_table.heading(col, text=col)
            self.cv_pretty_table.column(col, width=100, anchor=tk.W) # Adjust width as needed.

        # Insert data rows
        for index, row in df.iterrows():
            self.cv_pretty_table.insert("", tk.END, values=list(row))

        self.cv_pretty_table.pack(fill=tk.Y, expand=True)



    def add_rows_cv(self):
        font0 = ('Calibri', 12)
        
        #self.rm_rows_cv()
        impo = self.parent.SM.impo
        df1 = self.parent.SM.dataset[impo['prodotto']]


        #la conversione pd.to_numeric è necessaria per evitare errori di tipo 
        # (con coerce le stringhe diventano NaN e la somma non dà errore)
        self.qtotali = [pd.to_numeric(df1[prod], errors='coerce').sum() for prod in impo['prodotto']]

        nome_l = []
        cu_l = []
        qt_l = []

        for i in range(len(self.prod_names)):
            nome = self.prod_names[i]
            cu = self.cost_unit[i]
            qt = self.qtotali[i]
            #ct = cu*qt
            #lab = tk.Label(self.tab_cv, text= f'prodotto: {nome} | unità vendute: {qt} | costo unitario: € {cu} | costo del venduto: € {ct}', font=font0)
            #lab.pack(side=tk.TOP)
            #self.cv_rows.append(lab)
            cu_l.append(cu)
            qt_l.append(qt)
            nome_l.append(nome)
            #print(f'tipo:{type(cu)}, tipo qt: {type(qt)}')
        df = pd.DataFrame({
            'prodotto':nome_l,
            'costo unitario':cu_l,
            'quantità venduta':qt_l,
            'costo del venduto':np.array(cu_l)*np.array(qt_l)
        })
        df['costo unitario'] = df['costo unitario'].apply(lambda x: '€ '+str(x))
        df['costo del venduto'] = df['costo del venduto'].apply(lambda x: '€ '+str(x))
        df.to_csv(self.costo_venduto_path, sep=';', decimal=',', index=False)

        self.load_treeview_in_frame_cv(df, self.tab_cv)
        
        
    def rm_rows_cv(self):
        for i in range(len(self.cv_rows)):
            self.cv_rows[i].destroy()
        self.cv_rows = []

#################### LISTA DELLA SPESA

    def setupListaSpesaUi(self):

        self.ls_mat = tk.Frame(self.root)
        self.ls_mat.pack(expand=True, padx=5, pady=5, fill=tk.BOTH)

        font0= ('Calibri', 12)
        
        self.qp_frame = tk.Frame(self.ls_mat)
        self.qp_frame.pack(side=tk.LEFT, padx=10)
        tk.Label(self.qp_frame, text= 'QUANTITÁ DA PRODURRE', font=font0).pack(side=tk.TOP)

        self.ls_frame = tk.Frame(self.ls_mat)
        self.ls_frame.pack(side=tk.LEFT, padx=10)

        
        tk.Label(self.ls_frame, text= 'LISTA DELLA SPESA', font=font0).pack(side=tk.TOP)
        tk.Button(self.ls_frame, text='refresh display and update data', command=self.compute_ls, 
                  font = font0).pack(side=tk.TOP)
        
        #self.add_rows_ls()


        self.lista_qp_ui = []
        self.lista_qp_row = []
        self.fill_qp_frame()


        self.ls_rows = []

        #self.ls_pretty_table = None
        self.ls_pretty_table = ttk.Treeview(self.ls_frame, columns=list(), show="headings", height=10)
        self.compute_ls()

        
        #table = TableCanvas(tk.Toplevel(self.root))
        #table.show()


    def fill_qp_frame(self):
        self.prod_names = self.parent.SM.impo['prodotto']
        self.empty_qp_frame()
        for i in range(len(self.prod_names)):
            nome = self.prod_names[i]
            row = tk.Frame(self.qp_frame)
            row.pack(side=tk.TOP)
            tk.Label(row, text=nome, font=('Calibri', 12)).pack(side=tk.LEFT)
            quant = tk.Spinbox(row, from_=0, to=9990, increment=1, width=5, 
            relief="groove", repeatdelay=500, repeatinterval=100,
            font=('Calibri', 12), bg="aliceblue", fg="blue")#, command=self.compute_ls)
            quant.pack(side=tk.LEFT)
            self.lista_qp_ui.append(quant)
            self.lista_qp_row.append(row)
            

    def empty_qp_frame(self):
        for i in range(len(self.lista_qp_ui)):
            self.lista_qp_row[i].destroy()
        self.lista_qp_ui = []
        self.lista_qp_row = []


    def compute_ls(self):

        nomi_ing = []
        q_ing = []
        budget_ing = []

        qp_list = [int(p.get()) for p in self.lista_qp_ui]
        #self.lista_liste_ing
        #self.lista_liste_imp
        #self.prezzi_ing_kg

        for i in range(len(qp_list)):
            Q = qp_list[i]
            ing_list, gram_list = self.extract_ing_ui_lists(ing_list_ui=self.lista_liste_ing[i], 
                                                            gram_list_ui=self.lista_liste_imp[i])
            gram_list = np.array(gram_list).astype(float)
            for j in range(len(ing_list)):
                ing = ing_list[j]
                q = gram_list[j]
                qt = q*Q
                p = self.prezzi_ing_kg[ing]
                uc = np.round(p*q/1000,2)
                tc = uc*Q
                nomi_ing.append(ing)
                q_ing.append(qt)
                budget_ing.append(tc)
        
        nomi_ing = np.array(nomi_ing)
        q_ing = np.array(q_ing)
        budget_ing = np.array(budget_ing)

        df = pd.DataFrame({
            'ingredient':nomi_ing,
            'quantity':q_ing,
            'budget':budget_ing
        })
        df = df.groupby('ingredient')[['quantity','budget']].sum()
        df['ingredient'] = df.index
        df = df[['ingredient','quantity','budget']]
        self.ls_nomi_ing = df['ingredient']
        self.ls_q_ing = df['quantity']
        self.ls_budget_ing = df['budget']

        df.to_csv(self.listaspesa_path, sep=';', decimal=',', index=False)
        #print(df)

        #self.add_rows_ls()
        

        #self.ls_pretty_table.destroy()
        #self.ls_pretty_table = self.display_dataframe_in_treeview(df, tk.Toplevel(self.root))
        # if (self.ls_pretty_table != None):
        #     print(self.ls_pretty_table)
        #     print('destroying')
        #     self.ls_pretty_table.destroy()
        # else:
        #     print('no table to destroy')


        self.load_treeview_in_frame_ls(df, self.ls_frame)
        

    def display_dataframe_in_treeview(self, df, root):
        """
        Displays a pandas DataFrame in a Tkinter Treeview.

        Args:
            df: The pandas DataFrame to display.
            root: The Tkinter root window.
        """

        tree = ttk.Treeview(root, columns=list(df.columns), show="headings")

        # Add column headings
        for col in df.columns:
            tree.heading(col, text=col)
            tree.column(col, width=100, anchor=tk.W) # Adjust width as needed.

        # Insert data rows
        for index, row in df.iterrows():
            tree.insert("", tk.END, values=list(row))
        #tree.pack(side=tk.TOP)#fill=tk.BOTH, expand=True)
        return tree


    def load_treeview_in_frame_ls(self, df, frame):
        """
        Loads a pandas DataFrame into a Treeview inside a specified frame.

        Args:
            df: The pandas DataFrame to display.
            frame: The Tkinter Frame widget to contain the Treeview.
        """

        # Define a function to clear all the items present in Treeview
        for item in self.ls_pretty_table.get_children():
            self.ls_pretty_table.delete(item)

        df['budget'] = df['budget'].apply(lambda x: '€ '+str(x))
        df['quantity'] = df['quantity'].apply(lambda x: str(x)+' g')

        #self.ls_pretty_table = ttk.Treeview(frame, columns=list(df.columns), show="headings")
        self.ls_pretty_table.config(columns=list(df.columns), height=df.shape[0])

        # Add column headings
        for col in df.columns:
            self.ls_pretty_table.heading(col, text=col)
            self.ls_pretty_table.column(col, width=100, anchor=tk.W) # Adjust width as needed.

        # Insert data rows
        for index, row in df.iterrows():
            self.ls_pretty_table.insert("", tk.END, values=list(row))

        self.ls_pretty_table.pack(fill=tk.BOTH, expand=True)


    def add_rows_ls(self):
        font0 = ('Calibri', 12)
        
        self.rm_rows_ls()
        for i in range(len(self.ls_nomi_ing)):
            nome = self.ls_nomi_ing[i]
            qt = self.ls_q_ing[i]
            ct = self.ls_budget_ing[i]
            lab = tk.Label(self.ls_frame, text= f'ingrediente {nome}| totale grammi {qt} | budget € {np.round(ct, 2)}', font=font0)
            lab.pack(side=tk.TOP)
            self.ls_rows.append(lab)
        
        
    def rm_rows_ls(self):
        for i in range(len(self.ls_rows)):
            self.ls_rows[i].destroy()
        self.ls_rows = []




