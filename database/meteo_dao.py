from database.DB_connect import DBConnect
from model.situazione import Situazione

class MeteoDao():

    @staticmethod
    def get_all_situazioni():
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """SELECT s.Localita, s.Data, s.Umidita
                       FROM situazione s 
                       ORDER BY s.Data ASC"""
            cursor.execute(query)
            for row in cursor:
                result.append(Situazione(row["Localita"],
                                         row["Data"],
                                         row["Umidita"]))
            cursor.close()
            cnx.close()
        return result

    # ----------------------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def getUmiditaMedia(mese):
        #Se avessi avuto il nome del mese e non i numeri avrei fatto cosi:
        #dictMesi = { "gennaio": 1, "febbraio": 2, "marzo": 3, "aprile": 4, "maggio": 5, "giugno": 6, "luglio": 7, "agosto": 8, "settembre": 9, "ottobre": 10, "novembre": 11, "dicembre": 12 }
        #intMesi = dictMesi.get(nomeMese.lower())

        cnx = DBConnect.get_connection()
        ris=[]
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query="""select s.Localita, AVG(s.Umidita) as UmiditaMedia 
                     from situazione s
                     where MONTH(s.Data)=%s
                     group by Localita """
            cursor.execute(query, (mese, ))
            for row in cursor:
                #lista di dizionari
                ris.append( {"Localita": row["Localita"], "UmiditaMedia": row["UmiditaMedia"] })

                #oggetti Situazione
                #ris.append( Situazione( row["Localita"], row["UmiditaMedia"]) )
            cursor.close()
            cnx.close()
            return ris

    #----------------------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def get_situzioni_mese(mese):

        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """select s.Localita, s.Umidita, s.Data 
                       from situazione s
                       where MONTH(s.Data)=%s 
                       and DAY(s.Data) <=15
                       order by s.Data ASC """

            cursor.execute(query, (mese,))
            for row in cursor:
                result.append(Situazione(row["Localita"],
                                         row["Data"],
                                         row["Umidita"]))
            cursor.close()
            cnx.close()
        return result

if __name__ == "__main__":
    meteo = MeteoDao()
    umidita = meteo.getUmiditaMedia("febbraio")
    print(umidita)



