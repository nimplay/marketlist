from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.popup import Popup
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
import pandas as pd
from utils.listmanager import generate_shopping_list_logic

class CreateListView(BoxLayout):
    def __init__(self, main_container, **kwargs):
        super().__init__(**kwargs)
        self.main_container = main_container  # Guardar referencia al contenedor principal
        self.orientation = 'vertical'
        self.padding = 10
        self.spacing = 10

        # Fila para el input y el botón "Generar lista"
        input_button_layout = BoxLayout(orientation='horizontal', spacing=10, size_hint=(1, None), height=50)

        # Campo para ingresar el presupuesto (3/4 del ancho)
        self.budget_input = TextInput(hint_text="Ingresa tu presupuesto", multiline=False, size_hint_x=0.75)
        input_button_layout.add_widget(self.budget_input)

        # Botón para generar la lista (1/4 del ancho)
        generate_button = Button(text="Generar lista", size_hint_x=0.25)
        generate_button.bind(on_press=self.generate_shopping_list)
        input_button_layout.add_widget(generate_button)

        self.add_widget(input_button_layout)

        # Botón para volver a la vista principal
        back_button = Button(text="Volver", size_hint=(1, None), height=40)
        back_button.bind(on_press=self.go_back)
        self.add_widget(back_button)

        # ScrollView y GridLayout para mostrar la lista de compras generada
        self.scroll_view = ScrollView(size_hint=(1, 1))
        self.list_grid = GridLayout(cols=1, spacing=10, size_hint_y=None)
        self.list_grid.bind(minimum_height=self.list_grid.setter('height'))
        self.scroll_view.add_widget(self.list_grid)
        self.add_widget(self.scroll_view)

    def generate_shopping_list(self, instance):
        try:
            budget = float(self.budget_input.text)
            if budget <= 0:
                raise ValueError("El presupuesto debe ser mayor que 0.")
        except ValueError as e:
            self.show_error_popup(str(e))
            return

        # Cargar la lista final de productos
        df = pd.read_csv("data/finallist.csv")

        # Generar la lista de compras usando listmanager
        shopping_list, remaining_budget = generate_shopping_list_logic(df, budget)

        # Mostrar la lista generada en el ScrollView
        self.show_shopping_list(shopping_list, remaining_budget)

    def show_shopping_list(self, shopping_list, remaining_budget):
        # Limpiar la lista anterior
        self.list_grid.clear_widgets()

        # Agregar los productos a la lista
        for item in shopping_list:
            item_label = Label(
                text=f"{item['Nombre']}-{item['Peso']}{item['Medida']} - Cantidad: {item['Cantidad']} - Precio Total: {item['PrecioTotal']:.2f}",
                size_hint_y=None, height=40
            )
            self.list_grid.add_widget(item_label)

        # Agregar el presupuesto restante
        remaining_budget_label = Label(
            text=f"Presupuesto restante: {remaining_budget:.2f}",
            size_hint_y=None, height=40
        )
        self.list_grid.add_widget(remaining_budget_label)

    def show_error_popup(self, message):
        error_popup = Popup(title="Error", content=Label(text=message), size_hint=(0.8, 0.4))
        error_popup.open()

    def go_back(self, instance):
        # Lógica para volver a la vista principal
        if self.main_container:
            self.main_container.clear_widgets()
            from views.main_view import MainView
            self.main_container.add_widget(MainView())
