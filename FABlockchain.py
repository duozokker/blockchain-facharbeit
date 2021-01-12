# Praktischer Teil Facharbeit Informatik

# import aller benötigten Pakete zur erstellung der BLockchain
import hashlib  # für das verhashen der Blocks und der Blockchain
import time  # für den timestamp


# 1. Erstellung der Klasse Block bestehend aus:
#
# INDEX : Gibt an wechlcher Block das wievielte Glied (bzw Kettenstück) in der Blockchain ist
# TX_ROOT : In dieser Variable werden alle Transaktionen inklusive der ausgegebenen Anzahl unserer Währung angegeben
# PREV_HASH : Referiert zu dem Hash des Blocks Index-1 bzw. dem Block Welcher Hinter unserem Aktuellen BLock liegt
# TIMESTAMP: Gibt die Zeit der Erstellung des Blocks und der Betätigten Transaktionen an
# NONCE : Dies ist die Nummer welche bei der Block erstellung (dem Mining) generiert wurde

class Block ( object ):
    def __init__ (self, index, tx_Root, Prev_Hash, Nonce):
        self.index = index
        self.tx_Root = tx_Root
        self.Prev_Hash = Prev_Hash
        self.Timestamp = time.time ()
        self.Nonce = Nonce

    # Diese Funktion Berechnet den Hashwert unseres bzw jedes Blocks
    # Das @property sorgt dasfür dass man "berechne_hashwert" auch als variable aufrufen kann
    # => Das Ergebnis wäre im dem Fall dann immer der Hashwert des jeweiligen Blocks
    @property
    def berechne_hashwert (self):
        # Hier werden alle Werte von der Klasse Block als ein großer String addiert
        alle_werte_string = str ( self.index ) + str ( self.tx_Root ) + str ( self.Prev_Hash ) + str (
            self.Timestamp ) + str ( self.Nonce )

        # Der Oben erstellte String wird nun verrechnet und als sha256 Hash zurückgegeben
        return hashlib.sha256 ( alle_werte_string.encode () ).hexdigest ()

    # durch diese Funktion wird der Wert zurückgegeben der auch oben bei "alle_werte_string" berechnet wird
    def __repr__ (self):
        # return  "index:" + str ( self.index ) + str ( self.tx_Root ) + str ( self.Prev_Hash ) + str ( self.Timestamp ) + str (
        #     self.Nonce )
        return "Index: {} - Transaktionen: {} - Letzer Hash: {} - Zeitpunkt: {} - Nonce: {} !!!!".format(self.index, self.tx_Root,self.Prev_Hash, self.Timestamp,self.Nonce)


# 2. Nachdem wir unseren Block kreirt haben kommen wir jetzt zur Blockchain welche eine Verkettung aus
#   Objekten der Block klasse ist
#
# CHAIN : In dieser Variable werden alle Objekte vom typ Block gespeichert
# AKTUELLE_TRANSAKTIONEN : Speichert alle bestätigten Transaktionen in dem Jeweiligen block
# ERSTELLE_GENESIS_BLOCK : Diese Funktion dient zur erstellung des genesis blocks,
#                          dieser wird benötigt da der erste Block (Block index 1)
#                          keinen Block hat zu welchem er referieren kann (Prev_Hash kann nicht belegt werden)
#                          aufgrund des fehlens einer der Parameter, müssen wir den ersten block welcher auch
#                          Genesis Block genannt wird selbst erstellen und in die Liste einfügen wofür wir die
#                          "erstelle_block" Funktion nutzen
# DIFFICULTY : hier wirf die schwierigkeit des mining prozesses gespeicher welche sich alle 50 blöcke um eine 0 erhöht

class Blockchain ( object ):
    def __init__ (self):
        self.chain = []
        self.aktuelle_transaktionen = []
        self.erstelle_genesis_block ()
        self.difficulty = (len ( self.chain ) // 50) + 3

    # Diese Klasse lässt uns einen Block generieren, nach den Oben angegeben Attributen
    # dieser wird daraufhin in die Blockchain klasse in die Variable chain eingefügt
    def erstelle_block (self, Nonce, Prev_Hash):
        self.aktuelle_transaktionen = []

        block = Block (
            index=len ( self.chain ),
            Nonce=Nonce,
            Prev_Hash=Prev_Hash,
            tx_Root=self.aktuelle_transaktionen )  # # TODO: erklärung

        self.chain.append ( block )
        return block

    # Bei dieser Funktion unserer Blockchain Klasse erstellen wir den Oben erwähnten
    # Genesis Block, um dafür zu sorgen, dass unsere Blockchain funktionieren kann
    def erstelle_genesis_block (self):
        self.erstelle_block ( Nonce=0, Prev_Hash=0 )

    # diese Unterfunktion dient zur eigentlichen Erstellung von Trnasaktionen
    # welche daraufhin in die variable "aktuelle_transaktionen" eingefügt wird
    def erstelle_Transaktion (self, sender, empfaenger, menge):
        self.aktuelle_transaktionen.append ( {
            'sender': sender,
            'empfaenger': empfaenger,
            'menge': menge,
            'zeitpunkt': time.time ()
        } )

    # bei der PoW funktion wird ein Hash generiert und geschaut ob dieser mit "0000" anfängt.
    # => sollte dies der Fall sein dann wird wegen staticmethod entweder True oder False zurückgegeben
    @staticmethod
    def PoW (letze_nonce, proof):
        versuch = (str ( letze_nonce ) + str ( proof )).encode ()
        versuch_als_hash = hashlib.sha256 ( versuch ).hexdigest ()

        # menge_an_nullen = ""
        # for i in range(difficulty):
        #     x+="0"
        #
        # #teste ob die ersten "self.difficulty" Stellen 0 sind
        # return versuch_als_hash[:self.difficulty] == menge_an_nullen
        return versuch_als_hash[:4] == "0000"

    # die proof_of_work funktion ist die "PoW" Funktion innerhalb einer schleife welche dafür sorgt, dass
    # die funktion so oft ausgeführt wird bis ein hash generiert wurde welcher mit "0000" anfängt
    @staticmethod
    def proof_of_work (letze_nonce):
        nonce = 0
        while Blockchain.PoW ( letze_nonce=nonce, proof=letze_nonce ) is False:
            nonce += 1

        return nonce

    # 2.1 in dieser Funktion überprüfen wir die Gültigkeit eines bestimmten Blocks
    #       -1- : Als aller erstes untersuchen wir ob der Vorgänger unseres Blocks n
    #             den Block n-1 vor sich hat um zu schauen ob der Index korrekt ist.
    #       -2- : Danach prüfen wir ob der hashwert vom Block n-1 identisch zu dem
    #             unseres Blocks n ist.
    #       -3- : Daraufhin PoW
    #       -4- : Zuletzt wird nur noch der timestamp kontrolliert und es wird geschaut
    #             ob unser Block n-1 auch Zeitlich vor n generiert wurde

    @staticmethod  # Funktionen mit dem parameter staticmethod geben nur bools zurück also immer True oder False
    def pruefe_gueltigkeit (block, letzer_block):

        # ===== -1- =====
        if prev_block.index + 1 != block.index:
            return False

        # ===== -2- =====
        elif prev_block.berechne_hashwert != block.prev_hash:
            return False

        # ===== -3- =====
        elif not BlockChain.verifying_proof ( block.proof_no, prev_block.proof_no ):
            return False

        # ===== -4- =====
        elif block.timestamp <= prev_block.timestamp:
            return False

        # ===== -5- =====
        return True

    # Diese Funktion gibt uns den letzen Block zurück
    @property
    def letzer_block (self):
        return self.chain[-1]

    def getChain (self):
        return self.chain

    def getBlockByID(self,i):
        return self.chain[i]

    def mine (self, adresse):
        # berechnung des Blocks
        aktueller_block = self.letzer_block
        letzte_nonce = aktueller_block.Nonce
        nonce = self.proof_of_work ( letzte_nonce )

        # erstellung des Blocks
        letzer_hash = aktueller_block.berechne_hashwert
        erstellter_block = self.erstelle_block ( nonce, letzer_hash )

        # belohnung für block
        self.erstelle_Transaktion ( sender="root", empfaenger=adresse, menge=10 )

        return vars ( erstellter_block )

    # mit dieser Funktion wird  ausgegeben wie viele coins eine Adresse hat
    def getBalance(self, adresse):
        money_got = 0
        money_spent = 0
        # Hier wird jeder Block durchgegangen
        for i in range(len(self.chain)):
            # Hier wird jede Transaktion von bock i durchgegangen
            for j in range(len(self.chain[i].tx_Root)):
                # Transaktion wird zwischengespeichert und daraufhin auf ausgaben und
                #einnahmen untersucht
                transaction = self.chain[i].tx_Root[j]
                if transaction['empfaenger'] == adresse:
                    money_got += transaction['menge']
                if transaction['sender'] == adresse:
                    money_spent += transaction['menge']
        #ausgaben und einnahmen werden dann von einander abgezogen und übrig bleibt die balance
        balance = money_got - money_spent
        return [balance,money_got, money_spent]

    #mit dieser Funktion werden alle Adressen die je etwas empfangen oder gesendet haben aufgelistet (von Jason)
    def getAllAdressess(self):
        listofppl = []
        for i in range(len(self.chain)):
            for j in range(len(self.chain[i].tx_Root)):
                transaction = self.chain[i].tx_Root[j]
                if transaction['empfaenger'] not in listofppl:
                    listofppl.append(transaction['empfaenger'])
        return listofppl

# Testprogramm
blockchain = Blockchain()
blockchain.mine ( "leo" ) #1
blockchain.erstelle_Transaktion ( "leo", "jason", 5)
blockchain.mine ( "miner" )
blockchain.erstelle_Transaktion ( "jason", "miner", 5)
print(blockchain.getBalance("leo"))
print ( blockchain.chain )
print(blockchain.getAllAdressess())
print(blockchain.getBalance("miner"))
