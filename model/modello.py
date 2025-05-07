import copy

from database.meteo_dao import MeteoDao

class Model:
    def __init__(self):
        self.n_soluzioni=0

        #serve per salvare solo la soluzione ottimale:
        self.costo_ottimo=-1
        self.soluzione_ottima = []

    # ----------------------------------------------------------------------------------------------------------------------------------
    def getUmiditaMedia(self, mese):
        return MeteoDao.getUmiditaMedia(mese)

    # ----------------------------------------------------------------------------------------------------------------------------------
    def calcola_sequenza(self, mese):

        self.n_soluzioni=0
        self.costo_ottimo=-1
        self.soluzione_ottima = []

        situazioni = MeteoDao.get_situzioni_mese(mese)
        self._ricorsione([], situazioni)
        return self.costo_ottimo, self.soluzione_ottima

    # ----------------------------------------------------------------------------------------------------------------------------------
    def trova_possibili_step(self, parziale, lista_situazioni):

        giorno = len(parziale)+1
        candidati=[]

        for situazione in lista_situazioni:
            if situazione.data.day == giorno: #controlla se d maiuscolo
                candidati.append(situazione)
        return candidati

    # ----------------------------------------------------------------------------------------------------------------------------------
    def isAmmissibile(self, candidato, parziale):

        #vincolo sui 6 giorni
        cnt=0
        for situazione in parziale:
            if situazione.localita == candidato.localita:
                cnt+=1
        if cnt >= 6:
            return False

        #vincolo su permanenza
        # 1) se è all'inizio
        if len(parziale)==0:
            return True
        if len(parziale)<3:
            if candidato.localita != parziale[0].localita:
                return False

        # 2) vincolo: permanenza minima 3 giorni consecutivi prima di cambiare
        ultima_localita = parziale[-1].localita
        consecutivi = 0

        for s in reversed(parziale):                                  #calcolo consecutivi
            if s.localita == ultima_localita:
                consecutivi +=1
            else:
                break

        if candidato.localita != ultima_localita and consecutivi < 3: #se cambio località prima dei 3 non va bene
            return False
        # else:
        #     if (parziale[0].localita != parziale[1].localita or
        #         parziale[0].localita != parziale[2].localita or
        #         parziale[1].localita != parziale[2].localita):
        #         return False
        #     if (parziale[-3].localita != parziale[-2].localita or
        #         parziale[-2].localita != parziale[-1].localita or
        #         parziale[-1].localita != parziale[-3].localita):
        #         if  candidato.localita != parziale[-1].localita:
        #             return False

        #altrimenti ok
        return True #mettilo subito altrimenti non esegue il isAmmissibile

    # ----------------------------------------------------------------------------------------------------------------------------------
    def calcola_costo(self, parziale):
        costo=0
        # costo umidità
        for situazione in parziale:
            costo += situazione.umidita

        #costo cambio localita
        for i in range(3, len(parziale) ):
            #se i due giorni precedenti non sono stato nella stessa città --> pago 100
            if (parziale[i-1].localita != parziale[i].localita or parziale[i-2].localita != parziale[i].localita):
                costo += 100

        return costo

    # ----------------------------------------------------------------------------------------------------------------------------------
    def _ricorsione(self, parziale, lista_situazioni):
        #condizione terminale
        if len(parziale) == 15:
            #print(parziale)  #serve per capire cosa stai facendo
            self.n_soluzioni += 1 #RICORDAAAA, += non l'inverso
            costo = self.calcola_costo(parziale)

            if self.costo_ottimo == -1 or costo < self.costo_ottimo :
                self.costo_ottimo = costo
                self.soluzione_ottima = copy.deepcopy(parziale)

            return parziale

               # print(f" Costo ottimo: {costo} ")
               # for s in self.soluzione_ottima:
               #     print(s)

            #print( f"{costo} ||| {parziale}")

        #condizione ricorsiva
        else:
            #cercare le città per il giorno che mi serve
            #provo ad aggiungere una di queste città e vado avanti
            candidati = self.trova_possibili_step(parziale, lista_situazioni)
            for c in candidati:
                #verifica vincoli
                if self.isAmmissibile(c, parziale): #attenta a passare c e non candidati. oggetto, non lista
                    parziale.append(c)
                    self._ricorsione(parziale, lista_situazioni)
                    parziale.pop()



if __name__ == '__main__':
    #mi dava errore quando si chiamava model
    m = Model()
    #questa print serve per attivare il metodo _ricorsione che altrimenti non verrebbe mai eseguito, lasciando il num di soluzione sempre a 0
    #print(m.calcola_sequenza(1))
    #print(m.n_soluzioni)
    m.calcola_sequenza(1)
