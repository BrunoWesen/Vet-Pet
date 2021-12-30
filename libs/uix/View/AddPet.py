import json
from copy import copy

import requests
from kivy.metrics import dp
from kivy.clock import Clock
from kivymd.uix.dialog import MDDialog
from kivymd.uix.label import MDLabel
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.screen import MDScreen
from kivymd.uix.textfield import MDTextField
from plyer import filechooser
import os


class Texto(MDLabel):  # MDLabel que eu adaptei pra ter a animação do keyboard_up do Android
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.assis = 0

    def on_focus(self, focus):
        if self.assis == 0:
            self.posin = copy(self.pos)
            self.assis += 1

        if focus == True:
            self.event = Clock.schedule_interval(self.campotexto_anim, 1 / 60)
            Clock.schedule_once(self.campotexto_animfim, 1 / 3)

        if focus == False:
            self.pos_hint = {}
            self.pos[1] = self.posin[1]

    def campotexto_animfim(self, *args):
        Clock.unschedule(self.event)

    def campotexto_anim(self, *args):
        pos = self.pos
        pos[1] = pos[1] * 1.028
        self.pos_hint = {}
        self.pos[1] = pos[1]


class CampoTexto(MDTextField):  # MDTextField que eu adaptei pra ter a animação do keyboard_up do Android
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.count = 0

    def on_focus(self, *args):
        super().on_focus(*args)

        if self.focus == True:

            if self.count == 1:
                self.posp = copy(self.pos)
                self.parent.children[-1].on_focus(self.focus)
                self.event = Clock.schedule_interval(self.campotexto_anim, 1 / 60)
                Clock.schedule_once(self.campotexto_animfim, 1 / 3)

        if self.focus == False and self.count > 0:
            self.parent.children[-1].on_focus(self.focus)
            self.pos_hint = {}
            self.pos[1] = self.posp[1]
            self.count = 0

        self.count += 1

    def campotexto_animfim(self, *args):
        Clock.unschedule(self.event)

    def campotexto_anim(self, *args):
        pos = self.pos
        pos[1] = pos[1] * 1.02
        self.pos_hint = {}
        self.pos[1] = pos[1]


class AddPet(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.path = os.getcwd()
        self.url = "FIREBASE_LINK.json"
        # print(self.path)

    def on_kv_post(self, base_widget):
        menu_items = [
            {
                "viewclass": "OneLineListItem",
                "text": "F",
                "height": dp(56),
                "on_release": lambda x="F": self.set_item(x),
            }, {
                "viewclass": "OneLineListItem",
                "text": "M",
                "height": dp(56),
                "on_release": lambda x="M": self.set_item(x),
            }
        ]
        self.menu = MDDropdownMenu(
            caller=self.ids.drop_item,
            items=menu_items,
            position="center",
            width_mult=4,
        )
        self.menu.bind()

    def set_item(self, text_item):
        self.ids.drop_item.set_item(text_item)
        self.menu.dismiss()

    def take_item(self, SM, salvar):
        lista = [self.ids.ct1.text, self.ids.ct2.text, self.ids.drop_item.current_item, self.ids.ct3.text, self.ids.ct32.text,
                 self.ids.ct4.text]

        from imagebox import ImgSender
        imgsender = ImgSender(self.selection[0])
        self.imglink = imgsender.send()

        if salvar:
            user = SM.store["entrada"]["user"]
            jsondata = '{"Dono": "%s", "Espécie": "%s", "Nome": "%s", "Sexo": "%s", "Nascimento": "%s", ' \
                       '"Peso": "%s", "Raca": "%s", "Imagem": "%s", "PET": "Sim"}' % (
                           user, lista[0], lista[1], lista[2], lista[3],
                           lista[4], lista[5], self.imglink)
            requests.post(self.url, json=json.loads(jsondata))
            SM.root.get_screen("TelaCliente").salvar(json.loads(jsondata))


        if SM.root.current != "Adicionar_Pets":
            self.ids.ct1.text = ""
            self.ids.ct2.text = ""
            self.ids.ct3.text = ""
            self.ids.ct32.text = ""
            self.ids.ct4.text = ""

    def file_chooser(self):
        filechooser.open_file(on_selection=self.selected)

    def selected(self, selection):

        # try:    # Android / Linux
        #     img = selection[0].split("/")
        #
        #     if img[-1].split(".")[-1].upper() == "JPG" or img[-1].split(".")[-1].upper() == "PNG" \
        #             or img[-1].split(".")[-1].upper() == "JPEG" or img[-1].split(".")[-1].upper() == "GIF"\
        #             or img[-1].split(".")[-1].upper() == "WEBP":
        #         shutil.copy(selection[0], self.path + "/Componentes/UserImages", follow_symlinks=True)
        #         self.img = img
        #         Clock.schedule_once(self.changebuttoncolor, 1.5)
        #
        #     else:
        #         return
        #
        # except IndexError:
        #     return

        try:  # Windows
            img = selection[0].split("/")

            if img[-1].split(".")[-1].upper() == "JPG" or img[-1].split(".")[-1].upper() == "PNG" \
                    or img[-1].split(".")[-1].upper() == "JPEG" or img[-1].split(".")[-1].upper() == "GIF" \
                    or img[-1].split(".")[-1].upper() == "WEBP":

                if os.path.getsize(selection[0]) > 1_048_576:
                    dialog = MDDialog(
                        text="A imagem não pode ser maior que 1MB.",
                        radius=[20, 20, 20, 20])
                    dialog.open()
                    return

                else:
                    self.ids.btimg.background_normal = selection[0]
                    self.ids.btimg.background_down = selection[0]
                    self.selection = selection
                os.chdir(self.path)

            else:
                return

        except IndexError:
            return
