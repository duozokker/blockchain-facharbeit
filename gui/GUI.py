# Praktischer Teil Facharbeit Informatik 
import sys
import os.path
import tkinter as tk
#Pfad initialisieren um auf Ordner mit scripts zuzugreifen
sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))

from FABlockchain import *

#Testprogramm um die Ersten Adressen, Blocks und Transakti zu erstellen
blockchain = Blockchain ()
blockchain.mine ( "Leo" )
blockchain.erstelle_Transaktion("Leo", "Jason", 5)
blockchain.mine ( "Jason" )

class tkwindow(tk.Frame):
    def __init__(self):
        self.root = None

        if __name__ == "__main__":
            self.root = tk.Tk()
            self.root.title("Blockchain")
            #Lister aller Blöcke
            self.blocklist = tk.Listbox (self.root, height=10)
            self.blocklist.bind("<<ListboxSelect>>", self.getBlock)
            for i in range(len(blockchain.chain)):
                self.blocklist.insert(i,"Block %s"%(str(i)))
                self.blocklistmax=i
            self.blocklist.grid(row=1,column=1,columnspan=2,rowspan=10)

            #knopf um neue Transaktio zu generieren
            transactionbutton= tk.Button(self.root,command=self.transactionwindow,text = "erstelle Transaktion",width=15)
            transactionbutton.grid(row=1,column=3)

            #knopf um einen Block zu minen
            minebutton= tk.Button(self.root,command=self.mine,text = "Mine!",width=15)
            minebutton.grid(row=3,column=3)

            #knopf um alle Adressen zu sehen
            seeAdressesbutton= tk.Button(self.root,command=self.adresses,text = "alle Adressen",width=15)
            seeAdressesbutton.grid(row=5,column=3)


            self.root.mainloop()
    #diese funktion wird durch den mine knopf ausgelöst
    def mine(self):
        blockchain.mine("miner")
        self.blocklist.insert(self.blocklistmax+1,"Block %s"%(str(self.blocklistmax+1)))
        self.blocklistmax= self.blocklistmax+1

    #diese funktion wird ausgeführt, wenn man einen Block anklickt
    def adresses(self):
        #Funktion um angeklickte Adresse zu sehen und Fenster mit Daten anzuzeigen
        def getAdressInfo(dummy):
            name=adresses[(self.adresslist.curselection()[0])]
            print(name,blockchain.getBalance(name))
            adressInfowindow=tk.Tk()
            adressInfowindow.title(name)
            adressInfowindow.configure(background='white')
            title1=tk.Label(adressInfowindow, text="Anzahl auf Adresse",justify="left",bd=15)
            title2=tk.Label(adressInfowindow, text="Anzahl erhalten",justify="left",bd=15)
            title3=tk.Label(adressInfowindow, text="Anzahl versendet",justify="left",bd=15)
            title1.grid(row=1,column=1)
            title2.grid(row=1,column=2)
            title3.grid(row=1,column=3)
            entry1=tk.Label(adressInfowindow,text=blockchain.getBalance(name)[0],relief="flat",justify="center",bd=45,bg="white",height=0,background='white')
            entry1.grid(row=2,column=1)
            entry2=tk.Label(adressInfowindow,text=blockchain.getBalance(name)[1],relief="flat",justify="center",bd=45,bg="white",height=0,background='white')
            entry2.grid(row=2,column=2)
            entry3=tk.Label(adressInfowindow,text=blockchain.getBalance(name)[2],relief="flat",justify="center",bd=45,bg="white",height=0,background='white')
            entry3.grid(row=2,column=3)


        #alle Adresses sammeln
        adresses=blockchain.getAllAdressess()
        adresseswindow=tk.Tk()
        adresseswindow.title("Adressen")
        #Liste mit Adressen anlegen
        self.adresslist = tk.Listbox (adresseswindow, height=10)
        self.adresslist.bind("<<ListboxSelect>>", getAdressInfo)
        for i in range(len(adresses)):
            self.adresslist.insert(i,adresses[i])
        self.adresslist.pack()


    def getBlock(self,clicked=None):
        blockwindow=tk.Tk()

        #schauen, welcher Block ausgewählt ist
        try:
            block=blockchain.getBlockByID(self.blocklist.curselection()[0])
            blockwindow.title("Block %s"%(self.blocklist.curselection()[0]))
        except:
            return
        #In diesem Abschnitt werden alle Werte des Blocks in ein neues tkinter Fenster ausgegebenen
        #zuerst der Index
        Label1 = tk.Label(blockwindow, text="index")
        Label1.grid(row=1,column=1)
        Text1 = tk.Text(blockwindow,relief="flat",selectborderwidth=2, bd =1,height=1)
        Text1.insert("end",block.index)
        Text1.grid(row=1,column=2)
        #wenn es nicht der GenesisBlock ist
        if block.index !=0:
            Label2 = tk.Label(blockwindow, text="Nonce")
            Label2.grid(row=2,column=1)
            Text2 = tk.Text(blockwindow,relief="flat",selectborderwidth=2, bd =1,height=1)
            Text2.insert("end",block.Nonce)
            Text2.grid(row=2,column=2)
            #Hash des vorherigen Blocks
            Label3 = tk.Label(blockwindow, text="Prev_Hash")
            Label3.grid(row=3,column=1)
            Text3 = tk.Text(blockwindow,relief="flat",selectborderwidth=2, bd =1,height=1)
            Text3.insert("end",block.Prev_Hash)
            Text3.grid(row=3,column=2)
            #alle Transaktionen in diesem Block getrennt voneinander
            Label5 = tk.Label(blockwindow, text="tx_Root")
            Label5.grid(row=5,column=1)
            Text5 = tk.Text(blockwindow,relief="flat",selectborderwidth=2, bd =1,height=5)
            #Text5.insert("end",block.tx_Root)
            Text5.insert("end","Sender,Empfänger,Menge,Zeitpunkt\n")
            for i in range(len(block.tx_Root)):
                Text5.insert("end","%s,%s,%s,%s\n"%(block.tx_Root[i]["sender"],block.tx_Root[i]["empfaenger"],block.tx_Root[i]["menge"],block.tx_Root[i]["zeitpunkt"]))
            Text5.grid(row=5,column=2)
        #Zeitstempel
        Label4 = tk.Label(blockwindow, text="Timestamp")
        Label4.grid(row=4,column=1)
        Text4 = tk.Text(blockwindow,relief="flat",selectborderwidth=2, bd =1,height=1)
        Text4.insert("end",block.Timestamp)
        Text4.grid(row=4,column=2)



    #diese Funktion wird ausgelöst, wenn man eine Neue Transaktion erstellen will
    def transactionwindow(self):
        #funktion erstellen um die Werte an die Blockchain zu übertragen
        def doit():
            blockchain.erstelle_Transaktion(Entry1.get(), Entry2.get(), int(Entry3.get()))
            blockchain.mine("Jason")
            print(blockchain.chain)
            twindow.destroy()

        twindow=tk.Tk()
        twindow.title("Transaktion erstellen")
        #Eingabefelder für Sender,Empfänger und Anzahl erstellen
        #Sender
        Label1 = tk.Label(twindow, text="Sender")
        Label1.grid(row=1,column=1)
        Entry1 = tk.Entry(twindow,relief="flat",selectborderwidth=2, bd =5,width=35)
        Entry1.grid(row=1,column=2)
        #Empfänger
        Label2 = tk.Label(twindow, text="Empfänger")
        Label2.grid(row=2,column=1)
        Entry2 = tk.Entry(twindow, bd =5,relief="flat",selectborderwidth=2,width=35)
        Entry2.grid(row=2,column=2)
        #Anzahl
        Label3 = tk.Label(twindow, text="Anzahl")
        Label3.grid(row=3,column=1)
        Entry3 = tk.Entry(twindow, bd =5,relief="flat",selectborderwidth=2,width=35)
        Entry3.grid(row=3,column=2)

        best=tk.Button(twindow, text="Bestätigen", fg="black", command=doit)
        best.grid(row=4,column=2)


        self.root.mainloop()


ui=tkwindow()
ui.getBlock()
