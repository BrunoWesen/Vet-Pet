import json

from kivy.storage.jsonstore import JsonStore
from kivy.uix.tabbedpanel import TabbedPanel
from kivymd.uix.dialog import MDDialog
from kivymd.uix.screen import MDScreen
from datetime import datetime
from kivy.utils import get_color_from_hex as ku
import requests


# import firebase_admin
# from firebase_admin import credentials
# from firebase_admin import auth
# from firebase_admin import

# cred = credentials.Certificate("vet_pet_firebase.json")
# firebase_admin.initialize_app(cred)


class Login(MDScreen):
    url = "FIREBASE_LINK.json"

    def linha(self, listtab, currtab):
        if currtab == listtab[0]:
            self.ids.linhaon.pos = 310, 290
        else:
            self.ids.linhaon.pos = 410, 290

    def registerTime(self, SM, ID):
        now = datetime.now()
        dt_string = now.strftime("%d/%m")
        store = JsonStore("meta.json")
        store["entrada"] = {"dia": dt_string, "cliente": SM.root.current, "user": ID}
        SM.store = store

    # def transicionar(self, conta, SM):
    #
    #     from kivy.utils import get_color_from_hex as ku
    #
    #     if conta.upper() == "ATENDENTE":
    #         SM.root.set_current("TelaAtendente")
    #         from akivymd.uix.statusbarcolor import change_statusbar_color
    #         change_statusbar_color(ku("#3E585C"))
    #         self.registerTime(SM, "Atendente")

    # elif conta.upper() == "CLIENTE":
    #     SM.set_current("TelaCliente")
    #     from akivymd.uix.statusbarcolor import change_statusbar_color
    #     change_statusbar_color(ku("#3E585C"))
    #     self.registerTime(SM)

    # elif conta.upper() == "VETERINARIO":
    #     SM.root.set_current("TelaVeterinario")
    #     from akivymd.uix.statusbarcolor import change_statusbar_color
    #     change_statusbar_color(ku("#3E585C"))
    #     self.registerTime(SM, "Veterinario")
    #
    # else:
    #     return -1
    #     print("Usuário Inválido")

    # def inserir_data(self, email, senha):
    #     self.jsondata = '{"Email": "%s", "Senha": "%s"}' % (email, senha)
    #     requests.post(self.url, json=json.loads(self.jsondata))

    def registrar(self, email, senha, csenha):

        def credenciais_corretas():
            # user = auth.create_user(email=email, password=senha)
            # # link = auth.generate_email_verification_link(email, action_code_settings)
            # # send_custom_email(email, link)
            # # print(link)
            # dialog = MDDialog(
            #     text="Email adicionado, agora você já pode logar",
            #     radius=[20, 20, 20, 20])
            #
            # dialog.open()
            jsondata = '{"Email": "%s", "Senha": "%s"}' % (email, senha)
            requests.post(self.url, json=json.loads(jsondata))
            innerdialog = MDDialog(
                text="Cadastro realizado com sucesso!",
                radius=[20, 20, 20, 20])

            innerdialog.open()

        def verificador_de_emails():
            request = requests.get(self.url)
            request.json()

            for i in request.json():

                try:

                    if request.json()[i]["Email"] == email:
                        return True

                except KeyError:
                    continue

        if senha == csenha:

            if len(senha) < 5:
                dialog = MDDialog(
                    text="A senha não pode conter menos de 6 caracteres",
                    radius=[20, 20, 20, 20])
                dialog.open()

            elif senha.find(" ") >= 1 or senha.find("\\") >= 1 or senha.find(",") >= 1 \
                    or senha.find(";") >= 1 or senha.find(":") >= 1 or senha.find(")") >= 1 \
                    or senha.find("(") >= 1:
                dialog = MDDialog(
                    text="A senha não pode conter espaços ou '*\\, *,, *:, *;, *()'",
                    radius=[20, 20, 20, 20])
                dialog.open()

            elif verificador_de_emails():
                dialog = MDDialog(
                    text="Email já cadastrado!",
                    radius=[20, 20, 20, 20])
                dialog.open()

            elif email.count("@") == 1 and email.count("mail.com") == 1:
                credenciais_corretas()

            else:
                dialog = MDDialog(
                    text="As senhas não batem ou email inválido",
                    radius=[20, 20, 20, 20])
                dialog.open()

        else:
            dialog = MDDialog(
                text="As senhas não batem ou email inválido",
                radius=[20, 20, 20, 20])
            dialog.open()

    def pegar_user(self, email, senha, SM):
        request = requests.get(self.url)
        # request_list = list(request.json().keys())

        try:
            int(email)

            for i in request.json():

                try:

                    if request.json()[i]["ID"] == email:

                        if request.json()[i]["Senha"] == senha:

                            if request.json()[i]["cargo"] == "Atendente":
                                SM.root.set_current("TelaAtendente")

                            else:
                                SM.root.set_current("TelaVeterinario")

                            self.ids.texto_email.text = ""
                            self.ids.texto_senha1.text = ""
                            self.registerTime(SM, i)
                            return True
                        break

                except KeyError:
                    continue

        except ValueError:

            for i in request.json():

                try:
                    if request.json()[i]["Email"] == email:

                        if request.json()[i]["Senha"] == senha:
                            SM.root.set_current("TelaCliente")
                            self.ids.texto_email.text = ""
                            self.ids.texto_senha1.text = ""
                            self.registerTime(SM, i)
                            return True
                        break

                except KeyError:
                    continue

        # valemail = False
        # valsenha = False

        # for i in request_list:
        #
        #     for j in request.json()[i].keys():
        #
        #         if email == request.json()[i][j]:
        #             valemail = True
        #
        #         if senha == request.json()[i][j]:
        #             valsenha = True
        #
        # if valemail == True and valsenha == True:
        #     # VAI PRA OUTRA TELA
        #     # self.transicionar(email, SM)
        #     SM.set_current("TelaCliente")
        #     self.registerTime(SM)

        if SM.root.current == "TelaLogin":
            dialog = MDDialog(title='Email ou senha inválidos', md_bg_color=ku('#D8588A'), radius=[20, 20, 20, 20])
            dialog.open()


class Tabbed(TabbedPanel):
    pass
