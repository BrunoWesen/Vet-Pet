import json

import requests
from kivy.clock import Clock
from kivy.core.window import Window
from kivymd.app import MDApp
from kivymd.uix.dialog import MDDialog
from kivymd.uix.screen import MDScreen
from akivymd.uix.statusbarcolor import change_statusbar_color
from kivy.utils import get_color_from_hex as ku


class Vet(MDScreen):
    pass


class TelaAtendente(MDScreen):
    counter = 0
    url = "FIREBASE_LINK.json"
    store = MDApp.get_running_app().store

    # def add_att(self, SM):
    #     lista = []
    #
    #     for widget in self.ids.box_att.children[1:]:
    #         lista.append(widget.text)
    #         widget.text = ""
    #
    #     SM.current = "Tela1"

    def add(self, SM, box, wtype, csenha):
        lista = []  # Lista contendo o conteúdo dos textfields

        for widget in box.children[2:]:
            lista.append(widget.text)

        lista.reverse()
        request = requests.get(self.url)

        if request.json()[self.store["entrada"]["user"]]["Senha"] == csenha:

            if lista[4] == lista[5]:
                jsondata = '{"Nome": "%s", "Email": "%s", "ID": "%s", "Telefone": "%s", ' \
                           '"Senha": "%s", "cargo": "%s"}' % (lista[0], lista[1], lista[2], lista[3], lista[4], wtype)
                requests.post(self.url, json=json.loads(jsondata))

            else:
                dialog = MDDialog(
                    text="A confirmação de senha não bate com a senha.",
                    radius=[20, 20, 20, 20])
                dialog.open()
                return
            # print(lista)

        else:
            dialog = MDDialog(
                text="A senha do admin está incorreta.",
                radius=[20, 20, 20, 20])
            dialog.open()
            return

        for widget in box.children[2:]:
            widget.text = ""

        SM.current = "Tela1"

    def rem_func(self, ID, Senha):
        request = requests.get(self.url)

        if Senha.text != request.json()[self.store["entrada"]["user"]]["Senha"]:
            dialog = MDDialog(text='Senha incorreta!', radius=[20, 20, 20, 20])
            dialog.open()
            return

        for i in request.json():

            try:

                if request.json()[i]["ID"] == ID.text:
                    requests.delete(self.url.replace(".json", "") + i + "/" + ".json/")
                    dialog = MDDialog(text='Funcionário removido.', radius=[20, 20, 20, 20])
                    dialog.open()
                    ID.text = ""
                    Senha.text = ""
                    return

            except KeyError:
                continue

        dialog = MDDialog(text='Funcionário inexistente.', radius=[20, 20, 20, 20])
        dialog.open()
        ID.text = ""
        Senha.text = ""

    def rem(self, box):

        for widget in box.children[2:]:
            widget.text = ""

    def manager_changer(self, SM):
        SM.transition.direction = "left"

        def _goto_previous_screen(instance, key, *args):
            if key == 27:
                SM.transition.direction = "right"
                SM.current = "Tela1"
                return True

        Window.bind(on_keyboard=_goto_previous_screen)

    def prevset(self, SM):

        def _goto_previous_screen(instance, key, *args):
            if key == 27:
                SM.current = "TelaAtendente"
                return True

        Window.bind(on_keyboard=_goto_previous_screen)

    def add_vetsc(self, SM):

        if self.counter == 0:

            vet = Vet(name="Vet")
            SM.add_widget(vet)
            del vet
            Clock.schedule_once(self.after_enter, .5)
            self.counter = 1

        else:
            return

    def after_enter(self, *args):
        self.store = MDApp.get_running_app().store
        request = requests.get(self.url)
        # try:
        # print(self.store.keys())
        self.ids.toolbar.title = request.json()[self.store["entrada"]["user"]]["Nome"]
        # except KeyError:
        #     self.ids.toolbar.title = request.json()[self.store["entrada"]["user"]]["Nome"]
        self.parent.get_screen("Vet").ids.toolbar.title = self.ids.toolbar.title

    def transicionar_tela(self, SM, source, nomevet):
        SM.get_screen("Vet").ids.asimg.source = source
        SM.get_screen("Vet").ids.nomevet.text = nomevet
        SM.current = "Vet"

    def on_kv_post(self, base_widget):
        change_statusbar_color(ku("#3E585C"))
        self.store = MDApp.get_running_app().store
