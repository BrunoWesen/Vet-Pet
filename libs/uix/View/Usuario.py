# import os
# import json
# from kivy.clock import Clock
import requests
from kivy.clock import Clock
from kivy.properties import ColorProperty
from kivy.uix.widget import Widget
# from kivymd.app import MDApp
from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from akivymd.uix.statusbarcolor import change_statusbar_color
from kivy.utils import get_color_from_hex as ku

from imgur_downloader.imgurdownloader import ImgurDownloader


class Lista(MDScreen):  # Widget que criei para representar um widget de seleção de pets
    def __init__(self, src, nome, **kwargs):
        self.src = src
        self.nome = nome
        super().__init__(**kwargs)


class TelaCliente(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Clock.schedule_once(self.after_kv, .5)

    url = "FIREBASE_LINK.json"

    def after_kv(self, *args):
        change_statusbar_color(ku("#3E585C"))
        lista = []
        request = requests.get(self.url)

        for i in request.json():

            try:
                # print("entrei")
                # print(request.json()[i]["Dono"])
                # print(MDApp.get_running_app().store["entrada"]["user"])
                if request.json()[i]["Dono"] == MDApp.get_running_app().store["entrada"]["user"]:
                    # print("cheguei")
                    # print(request.json()[i]["Imagem"])
                    lista.append(request.json()[i])
                    ImgurDownloader(
                        request.json()[i]["Imagem"], delete_dne=True, dir_download="Componentes/UserImages/"
                    ).save_images()

            except KeyError:
                continue

        # print(lista)
        self.i = 0
        for j in lista:
            # print(j)
            src = "Componentes/UserImages/" + j["Imagem"].split("/")[-1]
            # print(src)
            self.ids.Ger_sec.add_widget(Lista(src, j["Nome"], name=str(self.i)))
            self.i += 1
            # print(self.ids.Ger_sec.children)

    def salvar(self, widget):
        ImgurDownloader(
            widget["Imagem"],
            delete_dne=True, dir_download="Componentes/UserImages/"
        ).save_images()

        src = "Componentes/UserImages/" + widget["Imagem"].split("/")[-1]
        self.ids.Ger_sec.add_widget(Lista(src, widget["Nome"], name=str(self.i)))
        self.i += 1

    def selecionar(self, SM, direction):

        if direction == "direita":
            SM.current = SM.next()

        else:
            SM.current = SM.previous()
