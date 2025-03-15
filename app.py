from kivy.app import App
from views.main_view import MainView

class ShoppingApp(App):
    def build(self):
        return MainView()

if __name__ == "__main__":
    ShoppingApp().run()
