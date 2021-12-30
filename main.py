import os

from kivymd.app import MDApp
from kivy.core.window import Window
from kivy.storage.jsonstore import JsonStore
from datetime import datetime
from libs.uix.root import Root


class MainApp(MDApp):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Window.keyboard_anim_args = {"d": 0.2, "t": "linear"}
        Window.softinput_mode = "below_target"
        self.store = JsonStore("meta.json")

    def logout(self):
        os.remove("meta.json")
        self.root.set_current("TelaLogin")
        Window.bind(on_keyboard=self.exit)

    def exit(self, instance, key, *args):
        if key == 27:
            self.stop()
            return True


    def build(self):
        self.root = Root()
        # store["entrada"] = {"hora": "agora"}
        now = datetime.now()
        dt_string = now.strftime("%d/%m")
        mes = str(int(dt_string[3:5]) + 1)

        if mes == "13":
            mes = "01"

        try:
            user = self.store["entrada"]["user"]

            if self.store["entrada"]["dia"][3:5] == dt_string[3:5]:
                self.root.set_current(self.store["entrada"]["cliente"])
                self.store["entrada"] = {"dia": dt_string, "cliente": self.root.current, "user": user}

            elif self.store["entrada"]["dia"][3:5] == mes:

                if dt_string[:2] > self.store["entrada"]["dia"][:2]:
                    raise KeyError

                else:
                    self.root.set_current(self.store["entrada"]["cliente"])
                    self.store["entrada"] = {"dia": dt_string, "cliente": self.root.current, "user": user}

        except KeyError:
            self.root.set_current("TelaLogin")


        # print(dt_string)


if __name__ == "__main__":
    # Window.size = (420, 840)
    MainApp().run()
