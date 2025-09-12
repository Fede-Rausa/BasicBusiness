

class testoHelp:
    def __init__(self):
        self.txt = '''
--  CASSA PANINOTECA  --

Copyright : This is a free open source software distributed under REPAX license, ALL RIGHTS RESERVED

Benvenuto! Se stai usando questa applicazione significa che cerchi una comoda cassa per la tua paninoteca personale.

Ci sono due finestre: 
-il registro degli ordini
-il sales manager

Dal menu del Sales Manager puoi selezionare

-CASSA: per inserire un nuovo ordine e calcolare prezzo e sconti (di sotto si spiega come)

-REPORT: per visualizzare rapidamente le statistiche delle vendite nei giorni della settimana e in totale.

-ORDINI: per cambiare lo status degli ordini da fare (TODO), completati (DONE) on in stand by (STBY).
Lo status cambia il colore degli ordini sul registro, in rosso  (DONE), verde (STBY), blu (TODO).

-IMPOSTAZIONI: per fare il setup della tua cassa, decidere quali prodotti vendere, a che prezzo
e come categoria Panino(P), Contorno(C) o Bibita(B)
Dalla categoria scelta dipendono gli sconti (accopiate Panini-contorni) e le colonne in cui vengono esposti.
Per cominciare a settare le impostazioni, scegli il numero di piatti che vuoi vendere.
Dopo averlo confermato, comparirà il form.

-PANNELLO: per controllare il contenuto del registro degli ordini. 
Consente di filtrare gli ordini per status e di cambiarne il font.



COSE IMPORTANTI:

1 - I clienti sono associati a degli id,
con un valore di default che è possibile cambiare manualmente.
ATTENZIONE: possono esservi bug nella generazione di un valore di default, per cui degli id potrebbero 
essere duplicati. 


2 - questo file exe comincia a funzionare da solo, ma archivia i dati che gli serve usare nei file
datiCassa.csv  e impostazioniCassa.csv. 
Se si spostano questi file dalla cartella in cui si trovano, si causerà errore. 
Dalla pagina IMPOSTAZIONI si decide come compilare il file impostazioniCassa.csv,
e quindi i prezzi, i nomi e le categorie dei panini.
In questo modo se si chiude e si riapre l'app, sia i dati registrati sia le impostazioni sono salvi.
Ogni volta che si cambiano le impostazioni si produce anche un backup automatico
del file datiCassa.csv e si rigenererà lo stesso vuoto e con le colonne dei prodotti cambiate.


3 - lo sconto totale è la somma di tre tipologie diverse (tutte personalizzabili in CASSA):
-1: lo sconto arbitario, detto sconto special, che verrà azzerato a ordine concluso
-2: gli sconti unitari per prodotti, che sono fissi e non si azzerano in automatico
-3: gli sconti menu, o sconti per combinazioni, offerti quando un cliente prende una coppia di prodotti di due categorie diverse (anche loro fissi)

in dettaglio:

-1: lo sconto special va specificato per ogni singolo ordine. è un valore che si sottrae direttamente dal prezzo finale.

-2: lo sconto totale per prodotti, o sconto per sconti fissi, è dato da: 
Q = vettore dei prodotti
S = vettore degli sconti fissi unitari
sconto per sconti fissi = prodotto scalare tra Q ed S = somma dei prodotti delle quantità per i relativi sconti
ovvero è uno sconto sulla quantità specifico per prodotto. 

-3: lo sconto menu, o sconto per combinazioni, è più articolato.
L'applicazione prevede che vi siano tre diversi tipi di prodotti: P (panini), C (contorni), B (bibite)
per cui vi sono tre diversi tipi di sconti menu, per le 3 combinazioni delle 3 categorie: P+C, P+B, C+B
per ogni coppia di categorie lo sconto menu si calcola come seque (esempio del caso P+C):
sconto menu P+C = scontoPC *  min(n°panini, n°contorni)
dove scontoPC è un valore che puoi modificare dal form della cassa, accanto alla voce sconto P+C
Quindi, ad esempio, se ordino 3 panini, 5 contorni e pongo scontoPC = € 0.5, 
lo sconto menu associato sarà min(3, 5) * 0.5 = 3*0.5 = € 1.5
(analogo ragionamento vale per gli sconti P+B e C+B)
ATTENZIONE: se capisci questo calcolo, noterai che diversi sconti menu possono sovrapporsi:
ad esempio se ordino 1 panino, 2 contorni, e 3 bibite, e ho scontoPC = 0.5, e scontoPB = 2
lo sconto totale sarà min(1,2)*0.5 + min(1,3)*2 = €2.5
per cui, se prevedi di usare 2 o 3 sconti menu diversi, tienine conto nella scelta dei loro valori


4 - Dalla pagina ORDINI il tasto REMOVE rimuove la riga dal dataset, 
e quindi cancella l'ordine dai registri. Con il tag DONE invece si cambia solo il suo status di completamento.
Dalla pagina PANNELLO puoi filtrare i tipi di ordini per lo status di completamenr


5 - il registro degli ordini è un'app fatta per vedere a schermo intero, di solito su un monitor separato, 
le quantità, le note, lo status e l'id del cliente  degli ordini  più recenti (tipo McDonald).
Dalla sezione PANNELLO puoi filtrare gli ordini per categoria (TODO-da fare, DONE-fatti, STBY-in pausa, ALL-tutti)
e cambiare le dimensioni del font delle scritte.
E' possibile filtrare il dataset in base allo status dal menu a tendina in alto.



6 - se sei arrivato a leggere fino a qui, meriti di sapere che questa pagina è editabile, e puoi scriverci sopra
i tuoi appunti. Ovviamente verrà tutto cancellato alla chiusura.
'''