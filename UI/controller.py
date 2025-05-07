import flet as ft

from UI.view import View
from model.modello import Model


class Controller:
    def __init__(self, view: View, model: Model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model
        # other attributes
        self._mese = 0

    # ----------------------------------------------------------------------------------------------------------------------------------
    def handle_umidita_media(self, e):

        self._view.lst_result.controls.clear()
        mese= self._view.dd_mese.value
        if mese is None:
            self._view.lst_result.controls.append( ft.Text("Attenzione! Inserire un mese"))
            self._view.update_page()
            return

        umidita = self._model.getUmiditaMedia(mese)
        #dict
        self._view.lst_result.controls.append(ft.Text("L'umidità nel mese selezionato è: "))
        for u in umidita:
            self._view.lst_result.controls.append( ft.Text( f" {u["Localita"]}: {u["UmiditaMedia"]}" ))

        self._view.update_page()

    #----------------------------------------------------------------------------------------------------------------------------------
    def handle_sequenza(self, e):

        self._view.lst_result.controls.clear()
        mese = self._view.dd_mese.value

        if mese is None:
            self._view.lst_result.controls.append(ft.Text("Attenzione! Inserire un mese"))
            self._view.update_page()
            return

        #tupla
        (costo, sequenza) = self._model.calcola_sequenza(mese)

        self._view.lst_result.controls.append( ft.Text(f"La sequenza ottima ha costo {costo} ed è:"))
        for s in sequenza:
            self._view.lst_result.controls.append( ft.Text(s))

        self._view.update_page()

    # ----------------------------------------------------------------------------------------------------------------------------------
    def read_mese(self, e):
        self._mese = int(e.control.value)

