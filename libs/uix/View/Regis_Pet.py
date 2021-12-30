from kivy.properties import ColorProperty
from kivy.uix.widget import Widget
from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
import requests



class Box(Widget):
    cor = ColorProperty([1, 1, 1, 1])

class Regis_Pet(MDScreen):
    url = "FIREBASE_LINK.json"
    store = MDApp.get_running_app().store
    nome = ''

    def voltar(self, SM):
        SM.transition.direction = "right"
        SM.current = 'TelaVeterinario'

    def on_kv_post(self, base_widget):
        self.store = MDApp.get_running_app().store

        request = requests.get(self.url)
        self.nome = request.json()[self.store["entrada"]["user"]]["Nome"]
        self.nome = self.nome.split(' ')[0]
        self.ids.toolbar.title = "Olá, {}".format(self.nome)


