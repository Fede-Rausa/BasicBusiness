import tkinter as tk
import pandas as pd
import numpy as np
import datetime as dt
import os
from tkcalendar import DateEntry  
#tkcalendar ha problemi con pyinstaller. per risolverli, nell'esportazione usare il comando: 
#pyinstaller --hidden-import "pkg_resources.py2_warn" main_cp05.py
#oppure aggiungere nel file spec il seguente codice:
#hiddenimports=['pkg_resources.py2_warn']
#oppure aggiungere direttamente questa importazione qui
import babel.numbers  #babel è un modulo che permette di formattare i numeri in modo più flessibile

class FinanceManager:
    def __init__(self, parent, root):
        self.parent = parent
        self.root = root
        self.root.title("Finance Manager")
        self.voci_path = 'voci_bilancio.csv'
        self.lg_path = 'libro_giornale.csv'
        self.tipi = ['bifase', 'entrata', 'uscita']

        self.setupMenu()
        self.setupImpoUi()
        self.setupLgUi()
        self.setupBsUi()
        self.show_frame('lg')


    def setupMenu(self):
        self.menubar = tk.Menu(self.root)
        self.root.config(menu=self.menubar)
        self.menubar.add_command(label="VOCI DI BILANCIO", command = lambda: self.show_frame('voci'))
        self.menubar.add_command(label="ENTRATE E USCITE", command = lambda: self.show_frame('lg'))
        self.menubar.add_command(label="BALANCE SHEET", command = lambda: self.show_frame('bs'))
        

    def show_frame(self, fr_name):
        frames = [self.impo_frame, self.lg_frame, self.bs_frame]
        fr_names = np.array(['voci', 'lg', 'bs'])
        id = np.where(fr_names == fr_name)[0] #np.where restituisce l'array degli indici dove è vero, perciò va selezionato [0]
        for i in range(len(frames)):
            if (i != id):
                frames[i].pack_forget()
            else:
                frames[i].pack(expand=True, padx=5, pady=5)


############VOCI DI BILANCIO

    def setupImpoUi(self):
        self.impo_frame = tk.Frame(self.root, bd=2, relief='ridge')
        self.impo_frame.pack(expand=True, fill=tk.BOTH)
        tk.Label(self.impo_frame, text='Piano dei Conti', 
                font = ('Copperplate Gothic Bold', 12)).pack(side=tk.TOP)

        myFont = ('Calibri', 12)

        buttons = tk.Frame(self.impo_frame)
        buttons.pack(side=tk.TOP, padx=10)
        tk.Button(buttons, text='add voice',  command=self.addVoice,
                  font=myFont).pack(side=tk.LEFT)
        tk.Button(buttons, text='remove last',  command=self.rmVoice,
                  font=myFont).pack(side=tk.LEFT)
        tk.Button(buttons, text='reset voices',  command=self.auto_fill_voices, 
                  font=myFont).pack(side=tk.LEFT)
        tk.Button(buttons, text='update voices',  command=self.saveVoices,
                  font=myFont).pack(side=tk.LEFT)

        self.voice_table = tk.Frame(self.impo_frame)
        self.voice_table.pack(side=tk.TOP, padx=10)

        self.voci_ui = []
        self.tipi_ui = []
        self.impo_row_ui = []
        self.auto_fill_voices()

    def addVoice(self, voce=None, tipo=None):
        row = tk.Frame(self.voice_table)
        row.pack(side=tk.TOP, padx=10)

        nome = tk.Entry(row)
        nome.pack(side=tk.LEFT, padx=10)

        selFiltri = self.tipi
        actualStatus = tk.StringVar()
        actualStatus.set(selFiltri[0])
        drop = tk.OptionMenu(row , actualStatus , *selFiltri) # dropdown
        drop.pack(side=tk.LEFT, padx=10)

        self.voci_ui.append(nome)
        self.tipi_ui.append(actualStatus)
        self.impo_row_ui.append(row)

        if (voce!=None):
            nome.delete(0, tk.END)
            nome.insert(0, voce)
            actualStatus.set(tipo)



    def rmVoice(self):
        id = len(self.impo_row_ui) - 1
        if (id >= 0):
            self.impo_row_ui[id].destroy()
            self.impo_row_ui.pop(id)
            self.voci_ui.pop(id)
            self.tipi_ui.pop(id)
        
    def saveVoices(self):
        voci = np.array([ui.get() for ui in self.voci_ui])
        tipi = np.array([ui.get() for ui in self.tipi_ui])
        tipi = tipi[voci != '']
        voci = voci[voci != '']

        self.voci_b = voci
        self.tipi_b = tipi

        df = pd.DataFrame({
            'voci':voci,
            'tipi':tipi
        })
        df.to_csv(self.voci_path, sep=';', index=False)


    def auto_fill_voices(self):
        if (os.path.exists(self.voci_path)):
            df = pd.read_csv(self.voci_path, sep=';')
            voci = df['voci']
            tipi = df['tipi']

            self.voci = np.array(voci)
            self.tipi = np.array(tipi)

            for i in range(len(self.impo_row_ui)):
                self.rmVoice()

            for i in range(df.shape[0]):
                self.addVoice(voci[i], tipi[i])
        else:
            self.voci = np.array(['ricavi', 'costi', 'costi_fissi', 'donazioni_ricevute','cassa', 'credito', 'debito', 'profitto_finale'])
            self.tipi = np.array(['entrata', 'uscita', 'uscita',    'entrata',         'bifase', 'bifase', 'bifase', '   uscita'])
            df = pd.DataFrame({
            'voci':self.voci,
            'tipi':self.tipi
            })
            df.to_csv(self.voci_path, sep=';', index=False)
            self.auto_fill_voices()


########## LIBRO GIORNALE


    #costruzione libro giornale
    def setupLgUi(self):
        self.lg_frame = tk.Frame(self.root)
        self.lg_frame.pack(expand=True, fill=tk.BOTH)

        tk.Label(self.lg_frame, text='Libro Giornale', 
                font = ('Copperplate Gothic Bold', 10)).pack(side=tk.TOP)
        
        myFont = ('Calibri', 12)
        myFont0 = ('Calibri', 14)

        self.lista_en_tipi2 = []
        self.lista_en_importi = []
        self.lista_en_date = []
        self.lista_en_descrizioni = []
        self.lista_en_ui = []
        self.lista_us_tipi2 = []
        self.lista_us_importi = []
        self.lista_us_date = []
        self.lista_us_descrizioni = []
        self.lista_us_ui = []

        ## form per aggiungere un'operazione
        lg_form = tk.Frame(self.lg_frame, bd=5, relief='groove')
        lg_form.pack(side=tk.TOP)

        tk.Label(lg_form, text='DATA REGISTRAZIONE:', font=myFont).pack(side=tk.LEFT)
        data_input = DateEntry(lg_form, date_pattern="dd/mm/yyyy", font=myFont)
        data_input.pack(side=tk.LEFT, padx=10)


        tk.Label(lg_form, text='DESCRIZIONE:', font=myFont).pack(side=tk.LEFT)
        descrizione = tk.Text(lg_form, width=40, height=5)
        descrizione.pack(side=tk.LEFT)


        def update_options(new_options, option_menu, selected_option):
            """Updates the OptionMenu with a new list of options."""
            menu = option_menu["menu"]
            menu.delete(0, "end")  # Clear existing options

            for option in new_options:
                menu.add_command(label=option, command=tk._setit(selected_option, option))

            selected_option.set(new_options[0]) # Set the first item of the list as default.

        def change_opt(type):
            selFiltri0 = self.voci[(self.tipi == type)|(self.tipi == 'bifase')]
            update_options(selFiltri0, tag_opt, actualStatus0)
            if (type == 'entrata'):
                importo.config(fg='green')
            else:
                importo.config(fg='red')


        tk.Label(lg_form, text='TIPO DI FLUSSO:', font=myFont).pack(side=tk.LEFT)
        selFiltri = ['entrata', 'uscita']
        actualStatus = tk.StringVar()
        actualStatus.set(selFiltri[0])
        tipo_opt = tk.OptionMenu(lg_form, actualStatus, *selFiltri , command=lambda a: change_opt(a)) # dropdown
        tipo_opt.config(font=myFont)
        tipo_opt.pack(side=tk.LEFT, padx=10)

        tk.Label(lg_form, text='VOCE CONTO:', font=myFont).pack(side=tk.LEFT)
        selFiltri0 = self.voci
        actualStatus0 = tk.StringVar()
        actualStatus0.set(selFiltri0[0])
        tag_opt = tk.OptionMenu(lg_form, actualStatus0, *selFiltri0) # dropdown
        tag_opt.config(font=myFont)
        tag_opt.pack(side=tk.LEFT, padx=10)

        tk.Label(lg_form, text='IMPORTO DI €', font=myFont).pack(side=tk.LEFT)
        importo = tk.Spinbox(lg_form, from_=0, to=9999, increment=0.01, width=10, 
            relief="sunken", repeatdelay=500, repeatinterval=100,
            font=myFont, bg="aliceblue", fg="green")#, command=self.on_spinbox_change)
        importo.pack(side=tk.LEFT)

        change_opt(actualStatus.get()) #all'inizio filtra subito

        tk.Button(lg_form, text='registra flusso di cassa', 
                  command = lambda: add_cashflow(actualStatus.get(), 
                                                 actualStatus0.get(),
                                                 descrizione.get("1.0",tk.END), 
                                                 importo.get(), 
                                                 str(data_input.get_date()),
                                                 checkvar.get()
                                                 ),
                  font=myFont).pack(side=tk.LEFT)

        def scroll_area(main_frame):
            scrollbar = tk.Scrollbar(main_frame)    # Creiamo una barra di scorrimento verticale
            scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

            mat0 = tk.Canvas(main_frame, yscrollcommand=scrollbar.set)  # Creiamo un canvas che conterrà il frame scrollabile
            mat0.pack(side=tk.BOTTOM, expand=True, fill=tk.Y)
            scrollbar.config(command=mat0.yview)

            mat1 = tk.Frame(mat0)    # Creiamo un frame all'interno del canvas
            mat0.create_window((0, 0), window=mat1, anchor="nw")  # Creiamo un window per il canvas, che conterrà il frame scrollabile
            def on_configure(event):  # Funzione per aggiornare la dimensione del canvas al ridimensionamento del frame
                    mat0.configure(scrollregion=mat0.bbox("all"))
            mat1.bind("<Configure>", on_configure)
            return mat1
        


        ## funzioni per il display del libro giornale
        def export_cashflow():
            
            date = np.array(self.lista_en_date)
            impo = np.array(self.lista_en_importi)
            des = np.array(self.lista_en_descrizioni)
            voci = np.array(self.lista_en_tipi2)
            date0 = np.array(self.lista_us_date)
            impo0 = np.array(self.lista_us_importi)
            des0 = np.array(self.lista_us_descrizioni)
            voci0 = np.array(self.lista_us_tipi2)

            tipi = np.concatenate((np.repeat('entrata',date.size), np.repeat('uscita',date0.size)))
            date = np.concatenate((date, date0))
            impo = np.concatenate((impo, impo0))
            voci = np.concatenate((voci, voci0))
            des = np.concatenate((des, des0))

            df = pd.DataFrame({
                'tipi':tipi,
                'voci':voci,
                'importi':impo,
                'date':date,
                'descrizioni':des
            })
            df.to_csv(self.lg_path, sep=';', decimal=',', index=False)
            self.lg_df = df

        def add_cashflow(type, tipo2, des, impo, tempo, showdes=False):
            if (type=='entrata'):
                mother_fr = scroll_en
            else:
                mother_fr = scroll_us

            row = tk.Frame(mother_fr)
            row.pack(side=tk.TOP)
            tk.Label(row, text=tempo, font=myFont).pack(side=tk.LEFT, padx=2)
            tk.Label(row, text=tipo2 + ': €', font=myFont).pack(side=tk.LEFT, padx=2)
            tk.Label(row, text=impo, font=myFont).pack(side=tk.LEFT, padx=2)
            if (showdes):
                tk.Label(row, text=des, font=myFont).pack(side=tk.LEFT, padx=2)

            if (type=='entrata'):
                self.lista_en_tipi2.append(tipo2)
                self.lista_en_importi.append(impo)
                self.lista_en_date.append(tempo)
                self.lista_en_descrizioni.append(des)
                self.lista_en_ui.append(row)
            else:
                self.lista_us_tipi2.append(tipo2)
                self.lista_us_importi.append(impo)
                self.lista_us_date.append(tempo)
                self.lista_us_descrizioni.append(des)
                self.lista_us_ui.append(row)


        def remove_lastflow(type):
            if (type=='entrata'):
                id = len(self.lista_en_ui) - 1
                if (id >= 0):
                    self.lista_en_ui[id].destroy()
                    self.lista_en_ui.pop(id)
                    self.lista_en_date.pop(id)
                    self.lista_en_importi.pop(id)
                    self.lista_en_descrizioni.pop(id)
                    self.lista_en_tipi2.pop(id)
            else:
                id = len(self.lista_us_ui) - 1
                if (id >= 0):
                    self.lista_us_ui[id].destroy()
                    self.lista_us_ui.pop(id)
                    self.lista_us_date.pop(id)
                    self.lista_us_importi.pop(id)
                    self.lista_us_descrizioni.pop(id)
                    self.lista_us_tipi2.pop(id)

        def auto_fill_lg():
            if (os.path.exists(self.lg_path)):
                df = pd.read_csv(self.lg_path, sep=';', decimal=',')
                self.lg_df = df
                tipi = np.array(df['tipi'])
                voci = np.array(df['voci'])
                impo = np.array(df['importi'])
                date = np.array(df['date'])
                des = np.array(df['descrizioni'])

                for i in range(len(self.lista_en_ui)):
                    remove_lastflow('entrata')
                for i in range(len(self.lista_us_ui)):
                    remove_lastflow('uscita')        

                showdes = checkvar.get()
                for i in range(tipi.size):
                    add_cashflow(tipi[i], voci[i], des[i], impo[i], date[i], showdes)
            else:
                self.lg_df = pd.DataFrame({
                    'tipi':['entrata'],
                    'voci':[self.voci[0]],
                    'importi':[0],
                    'date':[dt.datetime.now().year],
                    'descrizioni':['importo vuoto, solo per farlo vedere']
                    })
                self.lg_df.to_csv(self.lg_path, sep=';', decimal=',', index=False)
                auto_fill_lg()
                    

        ##codice per il display del libro giornale

        lg_controls = tk.Frame(self.lg_frame)
        lg_controls.pack(side=tk.TOP)
        checkvar = tk.IntVar()
        check = tk.Checkbutton(lg_controls, text='MOSTRA DESCRIZIONE', variable=checkvar, command = auto_fill_lg)
        check.pack(side=tk.LEFT)
        tk.Button(lg_controls, text='RESET DISPLAY', command=auto_fill_lg).pack(side=tk.LEFT)
        tk.Button(lg_controls, text='AGGIORNA LIBRO GIORNALE', command=export_cashflow).pack(side=tk.LEFT)

        self.lg_table = tk.Frame(self.lg_frame)
        self.lg_table.pack(side=tk.TOP)

        entrate_panel = tk.Frame(self.lg_table, bd=4, relief='groove', bg='green')
        entrate_panel.pack(side=tk.LEFT, padx=10)
        tk.Label(entrate_panel, text='ENTRATE/INPUT/+', font=myFont).pack(side=tk.TOP)
        tk.Button(entrate_panel, text='remove_last', font=myFont, command=lambda: remove_lastflow('entrata')).pack(side=tk.TOP)

        uscite_panel = tk.Frame(self.lg_table, bd=4, relief='groove', bg='red')
        uscite_panel.pack(side=tk.LEFT, padx=10)
        tk.Label(uscite_panel, text='USCITE/OUTPUT/-', font=myFont).pack(side=tk.TOP)
        tk.Button(uscite_panel, text='remove_last', font=myFont, command=lambda: remove_lastflow('uscita')).pack(side=tk.TOP)

        scroll_en = scroll_area(entrate_panel)
        scroll_us = scroll_area(uscite_panel)


        auto_fill_lg()






        ##codice per costruire un'operazione di partita doppia
        '''
        self.lista_entrate_om = []
        self.lista_entrate_sb = []
        self.lista_entrate_ui = []
        self.lista_uscite_om = []
        self.lista_uscite_sb = []
        self.lista_uscite_ui = []

        partita_doppia = tk.Frame(self.lg_form)
        partita_doppia.pack(side=tk.LEFT)
        riga1 = tk.Frame(partita_doppia)
        riga1.pack(side=tk.TOP)
        riga2 = tk.Frame(partita_doppia)
        riga2.pack(side=tk.TOP)
        riga3 = tk.Frame(partita_doppia)
        riga3.pack(side=tk.TOP)
        riga4 = tk.Frame(partita_doppia)
        riga4.pack(side=tk.TOP)

        entrate_fr = tk.Frame(riga4)
        entrate_fr.pack(side=tk.LEFT, padx=10)
        uscite_fr = tk.Frame(riga4)
        uscite_fr.pack(side=tk.LEFT, padx=10)

        def add_voice(type='entrata'):
            if (type=='entrata'):
                cd = True
                row = tk.Frame(entrate_fr)
            else:
                cd = False
                row = tk.Frame(uscite_fr)

            row.pack(side=tk.BOTTOM)

            selFiltri = self.voci[(self.tipi==type) | (self.tipi=='bifase')]
            actualStatus = tk.StringVar()
            actualStatus.set(selFiltri[0])
            drop = tk.OptionMenu(row , actualStatus , *selFiltri) # dropdown
            drop.pack(side=tk.LEFT, padx=10)

            spinImport = tk.Spinbox(row, from_=0, to=9999, increment=0.01, width=10, 
            relief="sunken", repeatdelay=500, repeatinterval=100,
            font=("Arial", 12), bg="aliceblue", fg="green")#, command=self.on_spinbox_change)
            spinImport.pack(side=tk.LEFT)

            if (cd):
                self.lista_entrate_ui.append(row)
                self.lista_entrate_sb.append(spinImport)
                self.lista_entrate_om.append(actualStatus)
            else:
                self.lista_uscite_ui.append(row)
                self.lista_uscite_sb.append(spinImport)
                self.lista_uscite_om.append(actualStatus)

        def rm_voice(type='entrata'):
            if (type=='entrata'):
                id = len(self.lista_entrate_ui) - 1
                if (id >= 0):
                    self.lista_entrate_ui[id].destroy()
                    self.lista_entrate_ui.pop(id)
                    self.lista_entrate_sb.pop(id)
                    self.lista_entrate_om.pop(id)
            else:
                id = len(self.lista_uscite_ui) - 1
                if (id >= 0):
                    self.lista_uscite_ui[id].destroy()
                    self.lista_uscite_ui.pop(id)
                    self.lista_uscite_sb.pop(id)
                    self.lista_uscite_om.pop(id)

        tk.Label(riga1, text ='ENTRATE/INPUT/+').pack(side=tk.LEFT, padx=10)
        tk.Label(riga1, text ='USCITE/OUTPUT/-').pack(side=tk.LEFT, padx=10)
        tk.Button(riga2, text='add', command=lambda: add_voice('entrata')).pack(side=tk.LEFT, padx=10)
        tk.Button(riga2, text='add', command=lambda: add_voice('uscita')).pack(side=tk.LEFT, padx=10)
        tk.Button(riga3, text='remove last', command=lambda: rm_voice('entrata')).pack(side=tk.LEFT, padx=10)
        tk.Button(riga3, text='remove last', command=lambda: rm_voice('uscita')).pack(side=tk.LEFT, padx=10)
        '''

############################ BALANCE SHEET

    def setupBsUi(self):

        def add_row_bs(voce, importo, mat, row_list, col='black'):
            row = tk.Frame(mat)
            row.pack(side=tk.TOP, padx=10)
            tk.Label(row, text=voce, font=item_font, fg=col).pack(side=tk.LEFT, padx=10)
            tk.Label(row, text='€ '+str(importo), font=item_font, fg=col).pack(side=tk.LEFT, padx=10)
            row_list.append(row)

        def remove_rows_bs(rows_list):
            id = len(rows_list) - 1
            if (id >= 0):
                for i in range(len(rows_list)):
                    rows_list[i].destroy()
                rows_list.clear()


        self.bs_frame = tk.Frame(self.root, bd=2, relief='groove')
        self.bs_frame.pack(expand=True, fill=tk.BOTH)
        tk.Label(self.bs_frame, text='BALANCE SHEET', 
                font = ('Copperplate Gothic Bold', 14)).pack(side=tk.TOP)
        
        font0 = ('Terminal', 14)
        item_font = ('Calibri', 14)
        font1 = item_font
        
        first_fr = tk.Frame(self.bs_frame)
        first_fr.pack(side=tk.TOP)

        
        bifase_fr = tk.Frame(first_fr, relief='groove', bd=2)
        bifase_fr.pack(side=tk.LEFT)
        inout_fr = tk.Frame(first_fr, relief='groove', bd=2)
        inout_fr.pack(side=tk.LEFT)
        stime_fr = tk.Frame(first_fr, relief='groove', bd=2)
        stime_fr.pack(side=tk.LEFT)

        
        tk.Label(bifase_fr, text='CONTI DI CONTROLLO',
                 font=font0).pack(side=tk.TOP)
        tk.Label(inout_fr, text='VARIAZIONI DI LIQUIDITÀ',
                 font=font0).pack(side=tk.TOP)
        tk.Label(stime_fr, text='COSTI E RICAVI TEORICI',
                 font=font0).pack(side=tk.TOP)
        
        titles1 = tk.Frame(bifase_fr)
        titles1.pack(side=tk.TOP)
        titles2 = tk.Frame(inout_fr)
        titles2.pack(side=tk.TOP)
        titles3 = tk.Frame(stime_fr)
        titles3.pack(side=tk.TOP)
        tk.Label(titles1, text = 'entrate').pack(side=tk.LEFT, padx=10)
        tk.Label(titles1, text = 'uscite').pack(side=tk.LEFT, padx=10)
        tk.Label(titles2, text = 'entrate').pack(side=tk.LEFT, padx=10)
        tk.Label(titles2, text = 'uscite').pack(side=tk.LEFT, padx=10)
        tk.Label(titles3, text = 'entrate').pack(side=tk.LEFT, padx=10)
        tk.Label(titles3, text = 'uscite').pack(side=tk.LEFT, padx=10)
        controls1 = tk.Frame(bifase_fr)
        controls1.pack(side=tk.TOP)
        controls2 = tk.Frame(inout_fr)
        controls2.pack(side=tk.TOP)
        controls3 = tk.Frame(stime_fr)
        controls3.pack(side=tk.TOP)

        bifase_mat = tk.Frame(bifase_fr)
        bifase_mat.pack(side=tk.TOP)
        inout_mat = tk.Frame(inout_fr)
        inout_mat.pack(side=tk.TOP)
        stime_mat = tk.Frame(stime_fr)
        stime_mat.pack(side=tk.TOP)

        bifase_en = tk.Frame(bifase_mat, relief='groove', bd=2, bg='green')
        bifase_en.pack(side=tk.LEFT)
        bifase_us = tk.Frame(bifase_mat, relief='groove', bd=2, bg='red')
        bifase_us.pack(side=tk.LEFT)

        inout_en = tk.Frame(inout_mat, relief='groove', bd=2, bg='green')
        inout_en.pack(side=tk.LEFT)
        inout_us = tk.Frame(inout_mat, relief='groove', bd=2, bg='red')
        inout_us.pack(side=tk.LEFT)

        stime_en = tk.Frame(stime_mat, relief='groove', bd=2, bg='green')
        stime_en.pack(side=tk.LEFT)
        stime_us = tk.Frame(stime_mat, relief='groove', bd=2, bg='red')
        stime_us.pack(side=tk.LEFT)

        bifase_en_rows = []
        bifase_us_rows = []
        inout_en_rows = []
        inout_us_rows = []
        stime_en_rows = []
        stime_us_rows = []

        def fill_rows_b1():

            tipi = np.array(self.lg_df['tipi'])
            voci = np.array(self.lg_df['voci'])
            impo = np.array(self.lg_df['importi']).astype(float)
            date = np.array(self.lg_df['date'])

            voci_bf = self.voci[self.tipi=='bifase']
            #id_bool_bf = np.isin(voci, voci_bf)

            id_bool_en = (tipi == 'entrata')
            id_bool_us = np.logical_not(id_bool_en)

            remove_rows_bs(bifase_en_rows)
            remove_rows_bs(bifase_us_rows)

            for i in range(len(voci_bf)):
                Voce = voci_bf[i]
                id_bool_voce = (voci == Voce)
                
                Importo_en = np.sum(impo[id_bool_voce & id_bool_en])
                Importo_us = np.sum(impo[id_bool_voce & id_bool_us])
                add_row_bs(Voce, Importo_en, bifase_en, bifase_en_rows)
                add_row_bs(Voce, Importo_us, bifase_us, bifase_us_rows)

        def fill_rows_b2():

            tipi = np.array(self.lg_df['tipi'])
            voci = np.array(self.lg_df['voci'])
            impo = np.array(self.lg_df['importi']).astype(float)
            date = np.array(self.lg_df['date'])

            #voci_en = self.voci[self.tipi=='entrate']
            #voci_us = self.voci[self.tipi=='uscite']
            #id_bool_bf = np.isin(voci, voci_bf)
            
            voci_mf = self.voci[self.tipi != 'bifase']
            voci_bool_tipi_en = (self.tipi == 'entrata')
            
            id_bool_en = (tipi == 'entrata')
            id_bool_us = np.logical_not(id_bool_en)

            remove_rows_bs(inout_en_rows)
            remove_rows_bs(inout_us_rows)

            importi_en = []
            importi_us = []
            for i in range(len(voci_mf)):
                Voce = voci_mf[i]
                id_bool_voce = (voci == Voce)
                if (voci_bool_tipi_en[i]):
                    Importo_en = np.sum(impo[id_bool_voce & id_bool_en])
                    add_row_bs(Voce, Importo_en, inout_en, inout_en_rows)
                    importi_en.append(Importo_en)
                else:
                    Importo_us = np.sum(impo[id_bool_voce & id_bool_us])
                    add_row_bs(Voce, Importo_us, inout_us, inout_us_rows)
                    importi_us.append(Importo_us)

            tot_en = np.sum(np.array(importi_en))
            tot_us = np.sum(np.array(importi_us))
            margine = tot_en - tot_us
            add_row_bs('TOT OUT: ', tot_us, inout_us, inout_us_rows, col='red')
            add_row_bs('TOT IN: ', tot_en, inout_en, inout_en_rows, col='green')
            if (margine >= 0):
                add_row_bs('MARGIN: ', margine, inout_en, inout_en_rows, col='green')
            else:
                add_row_bs('MARGIN: ', margine, inout_en, inout_en_rows, col='red')



        def fill_rows_b3():
            nomi = np.array(self.parent.SM.impo['prodotto'])
            df1 = self.parent.SM.dataset[nomi]
            #to_numeric per convertire le colonne in numeri, ignorando gli errori
            #in questo modo, se ci sono valori non numerici, vengono convertiti in Na
            totali = np.array([pd.to_numeric(df1[prod], errors='coerce').sum() for prod in self.parent.SM.impo['prodotto']])
            #print(totali)
            #print(self.parent.SM.impo['prodotto'])
            prezzi = np.array(self.parent.SM.impo['prezzo'])
            ricavi = totali * prezzi
            tot_ricavi = ricavi.sum()
            tot_sconti = np.array(self.parent.SM.dataset['sconto']).astype(float).sum()

            remove_rows_bs(stime_en_rows)
            remove_rows_bs(stime_us_rows)

            for i in range(len(nomi)):
                add_row_bs(nomi[i], ricavi[i], stime_en, stime_en_rows)
            add_row_bs('TOT RICAVI: ', tot_ricavi, stime_en, stime_en_rows, col='green')

            #codice insicuro per il nome dei percorsi
            if (os.path.exists('prezzi_ingredienti.csv') & os.path.exists('prodotti_ingredienti.csv')):  
                df1 = pd.read_csv('prezzi_ingredienti.csv', sep=';', decimal=',')
                df2 = pd.read_csv('prodotti_ingredienti.csv', sep=';', decimal=',')
                prezzi_ing_kg = dict(zip(df1['ingredienti'], df1['prezziKg']))
                grammi_ing = dict(zip(df2['ingrediente'], df2['grammi'])) 


                ingredienti = np.unique(np.array(df2['ingrediente']))
                costi = []
                for i in range(ingredienti.size):
                    ing = ingredienti[i]
                    id_bool = (df2['ingrediente'] == ing)
                    prods = np.array(df2[id_bool]['prodotto'])
                    tots = np.array([totali[i] for i in range(len(nomi)) if (nomi[i] in prods)])
                    grams = np.array(df2[id_bool]['grammi']).astype(float)
                    prezzo = prezzi_ing_kg[ing]
                    costo = np.sum(grams*tots)*prezzo/1000
                    costi.append(costo)
                    add_row_bs(ing, costo, stime_us, stime_us_rows)
                    print(prods)

                tot_costi = np.sum(np.array(costi))
            else:
                tot_costi = tot_sconti
            
            add_row_bs('TOT SCONTI: ', tot_sconti, stime_us, stime_us_rows)
            add_row_bs('TOT COSTI: ', tot_costi, stime_us, stime_us_rows, col='red')
            margin = tot_ricavi - tot_costi
            col0 = 'green' if (margin >= 0) else 'red'
            add_row_bs('MARGINE: ', margin, stime_en, stime_en_rows, col=col0)
            


        tk.Button(controls1, text='AGGIORNA', command=fill_rows_b1, font=font1,
                  ).pack(side=tk.LEFT)
        tk.Button(controls2, text='AGGIORNA', command=fill_rows_b2, font=font1,
                  ).pack(side=tk.LEFT)
        tk.Button(controls3, text='AGGIORNA', command=fill_rows_b3, font=font1, 
                  ).pack(side=tk.LEFT)

        fill_rows_b1()
        fill_rows_b2()
        fill_rows_b3()

        




                









