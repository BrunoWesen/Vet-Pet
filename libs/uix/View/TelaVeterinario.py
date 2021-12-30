from copy import copy

import requests
from akivymd.uix.statusbarcolor import change_statusbar_color
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.uix.image import Image
from kivymd.app import MDApp
from kivymd.uix.dialog import MDDialog
from kivymd.uix.list import ThreeLineAvatarListItem, ImageLeftWidget
from kivymd.uix.screen import MDScreen
from kivy.utils import get_color_from_hex as ku
from kivymd.uix.tab import MDTabs


# class tabela (MDTabs):
#     def on_tab_switch(self, *args):
#         print(*args)
# from imgur_downloader import ImgurDownloader


class TelaVet(MDScreen):
    overlay_color = ku("#D8588A")
    nomeTab = 'Pacientes'
    url = "FIREBASE_LINK.json"
    store = MDApp.get_running_app().store
    nome = ''

    def procurar(self, filhos, petfilhos):
        self.ids.toolbar.right_action_items = []
        self.ids.float.add_widget(self.procurar_bar)
        self.procurar_bar.focus = True
        self.ids.toolbar.title = ''
        # Window.bind(on_keyboard=self.voltar)
        self.verifcl = Clock.schedule_interval(self.verifvoltar, 1)
        self.listaagenda = copy(filhos)
        self.listapets = copy(petfilhos)

        if self.nomeTab == 'Pacientes':
            self.crias = filhos

        elif self.nomeTab == 'Agenda':
            self.crias = petfilhos

    def verifvoltar(self, *args):

        if not self.procurar_bar.focus:
            self.voltar(28)
            Clock.unschedule(self.verifcl)

    def voltar(self, key, *args):
        if key == 27:
            self.ids.toolbar.title = "Olá, nome do veterinário"
            # self.ids.toolbar.right_action_items = [["magnify", lambda x: self.procurar(self.ids.lista.children,
            #                                                                            self.ids.pets.children) if len(
            #     self.ids.lista.children) > 0 or len(self.ids.pets.children) > 0 else False],
            #                                        ["exit-to-app", lambda x: MDApp.get_running_app().logout()]]
            self.ids.float.remove_widget(self.procurar_bar)
            count = len(self.crias)

            while count > 0:

                if self.nomeTab == 'Pacientes':
                    self.ids.lista.remove_widget(self.crias[count - 1])

                elif self.nomeTab == 'Agenda':
                    self.ids.pets.remove_widget(self.crias[count - 1])
                count -= 1

            if self.nomeTab == 'Pacientes':
                count = len(self.listaagenda)

            elif self.nomeTab == 'Agenda':
                count = len(self.listapets)

            while count > 0:

                if self.nomeTab == 'Pacientes':
                    self.ids.lista.add_widget(self.listaagenda[count - 1])

                elif self.nomeTab == 'Agenda':
                    self.ids.pets.add_widget(self.listapets[count - 1])
                count -= 1

            return True

        if key == 28:
            self.ids.toolbar.title = "Olá, {}".format(self.nome)
            # self.ids.toolbar.right_action_items = [["magnify", lambda x: self.procurar(self.ids.lista.children,
            #                                                                            self.ids.pets.children) if len(
            #     self.ids.lista.children) > 0 or len(self.ids.pets.children) > 0 else False],
            #                                        ["exit-to-app", lambda x: MDApp.get_running_app().logout()]]
            self.ids.float.remove_widget(self.procurar_bar)
            return True

    def get_nome_tab(self):
        # print(self.ids.tab_now.carousel.current_slide.tab_label.text[156:])
        self.nomeTab = self.ids.tab_now.carousel.current_slide.tab_label.text.split(" ")[-1]
        # self.nomeTab = args[2].text.split(" ")[1]
        # print(self.nomeTab)

    def pesquisar(self, texto, search, crias, petcrias):

        if self.nomeTab == 'Pacientes':
            currcrias = crias

        elif self.nomeTab == 'Agenda':
            currcrias = petcrias

        if search:

            count = len(currcrias)
            # print("oi")

            while count > 0:

                if self.nomeTab == 'Pacientes':
                    self.ids.lista.remove_widget(currcrias[count - 1])
                    # print("oi paciente")

                elif self.nomeTab == 'Agenda':
                    self.ids.pets.remove_widget(currcrias[count - 1])
                count -= 1

            if self.nomeTab == 'Pacientes':

                for id, i in enumerate(self.listaagenda):

                    if texto.upper() in self.listaagenda[id].text.upper() or \
                            texto.upper() in self.listaagenda[id].secondary_text.upper() or \
                            texto.upper() in self.listaagenda[id].tertiary_text.upper():
                        self.ids.lista.add_widget(self.listaagenda[id])

            elif self.nomeTab == 'Agenda':
                # self.ids.teste.text = 'THOR'

                for id, i in enumerate(self.listapets):

                    if texto.upper() in self.listapets[id].text.upper() or \
                            texto.upper() in self.listapets[id].secondary_text.upper() or \
                            texto.upper() in self.listapets[id].tertiary_text.upper():
                        self.ids.pets.add_widget(self.listapets[id])

    def show_descricao(self):
        self.dialog = MDDialog(
            text=self.ids.descricao.tertiary_text
        )
        self.dialog.open()

    def on_kv_post(self, base_widget):
        self.procurar_bar = copy(self.ids.procurar)
        self.ids.float.remove_widget(self.ids.procurar)
        change_statusbar_color(ku("#3E585C"))
        Clock.schedule_once(self.after_kv, 1)


    def after_kv(self, *args):
        self.store = MDApp.get_running_app().store

        # nome toolbar
        request = requests.get(self.url)
        self.nome = request.json()[self.store["entrada"]["user"]]["Nome"]
        self.nome = self.nome.split(' ')[0]
        self.ids.toolbar.title = "Olá, {}".format(self.nome)

        def telapet(instancia):
            MDApp.get_running_app().root.set_current('Regis_Pet')
            rpb = MDApp.get_running_app().root.get_screen('Regis_Pet').ids.regis
            rpimg = MDApp.get_running_app().root.get_screen('Regis_Pet').ids.img
            pet = request.json()[instancia.tertiary_text]
            rpimg.source = pet['Imagem']
            contato = request.json()[pet['Dono']]['Email']
            regislist = [contato, pet['Nascimento'], pet['Nome'], pet['Sexo'], pet['Raca'], pet['Espécie']]
            for idx, i in enumerate(rpb.children[::2]):
                i.text = regislist[idx]

        # # lista pets

        for i in request.json():
            try:
                if request.json()[i]['PET'] == 'Sim':
                    pets = request.json()[i]
                    # print(pets['Imagem'])
                    # ImgurDownloader(
                    #     pets["Imagem"],
                    #     delete_dne=True, dir_download="Componentes/Images/"
                    # ).save_images()
                    avatar = ThreeLineAvatarListItem(text="{}".format(pets['Nome']),
                                                     secondary_text="Contato dono: {}".format(
                                                         request.json()[pets['Dono']]['Email']),
                                                     tertiary_text=i
                                                     )
                    img = ImageLeftWidget()
                    img.source = pets['Imagem']
                    avatar.add_widget(img)
                    self.ids.pets.add_widget(avatar)
                    avatar.tertiary_theme_text_color = "Custom"
                    avatar.tertiary_text_color = (0, 0, 0, 0)
                    avatar.bind(on_press=telapet)

            except KeyError:
                continue