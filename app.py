from kivy.app import App
from views.main_view import MainView
# from kivy.uix.screenmanager import ScreenManager, Screen
class ShoppingApp(App):
    def build(self):
        return MainView()

if __name__ == "__main__":
    ShoppingApp().run()
