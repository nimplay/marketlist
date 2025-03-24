from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from views.create_list_view import CreateListView
from views.add_list_view import AddListView

class MainView(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.padding = 15
        self.spacing = 15

        # Botón para crear una lista de compra
        create_list_button = Button(text="Crea una lista de compra", size_hint=(1, 0.2))
        create_list_button.bind(on_press=self.show_create_list_view)
        self.add_widget(create_list_button)

        # Botón para añadir una lista de compras
        add_list_button = Button(text="Añade una lista de tus compras", size_hint=(1, 0.2))
        add_list_button.bind(on_press=self.show_add_list_view)
        self.add_widget(add_list_button)

        # Botón para salir
        exit_button = Button(text="Salir", size_hint=(1, 0.2))
        exit_button.bind(on_press=self.exit_app)
        self.add_widget(exit_button)

    def show_create_list_view(self, instance):
        self.clear_widgets()
        self.add_widget(CreateListView(main_container=self))  # Pasar self como contenedor principal

    def show_add_list_view(self, instance):
        self.clear_widgets()
        self.add_widget(AddListView())

    def exit_app(self, instance):
        from kivy.app import App
        App.get_running_app().stop()
