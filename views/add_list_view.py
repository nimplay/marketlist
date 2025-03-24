from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.spinner import Spinner
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivymd.uix.menu import MDDropdownMenu
from kivymd.app import MDApp

import pandas as pd
from utils.listcreator import  create_new_shopping_list

class AddListView(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.padding = 10
        self.spacing = 10
        self.temp_items = []  # Lista temporal para almacenar productos

        # Cargar la lista final de productos una sola vez
        self.final_list = pd.read_csv("data/finallist.csv")

        # Campo para el nombre de la lista
        self.list_name_input = TextInput(hint_text="Nombre de la lista", multiline=False, size_hint=(1, None), height=40)
        self.add_widget(self.list_name_input)

        # Botón para agregar producto
        add_product_button = Button(text="Agregar producto", size_hint=(1, None), height=40)
        add_product_button.bind(on_press=self.show_add_product_popup)
        self.add_widget(add_product_button)

        # ScrollView y GridLayout para mostrar la lista de productos
        self.preview_grid = GridLayout(cols=1, spacing=10, size_hint_y=None)
        self.preview_grid.bind(minimum_height=self.preview_grid.setter('height'))

        self.scroll_view = ScrollView(size_hint=(1, 1))
        self.scroll_view.add_widget(self.preview_grid)
        self.add_widget(self.scroll_view)

        # Botón para guardar la lista
        save_list_button = Button(text="Guardar lista", size_hint=(1, None), height=40)
        save_list_button.bind(on_press=self.save_new_list)
        self.add_widget(save_list_button)

    def show_add_product_popup(self, instance):
        # Crear un popup con el formulario para agregar productos
        popup_layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

        # Barra de búsqueda de productos (TextInput con autocompletado)
        self.product_search_input = TextInput(hint_text="Buscar producto...", multiline=False, size_hint=(1, None), height=40)
        self.product_search_input.bind(text=self.on_search_product)
        popup_layout.add_widget(self.product_search_input)

        # Menú desplegable para mostrar resultados de búsqueda
        self.search_menu = MDDropdownMenu(
            caller=self.product_search_input,
            items=[],  # Los items se actualizan dinámicamente
            width_mult=4,
            callback=self.on_product_selected
        )

        # Campos del formulario
        self.product_weight_input = TextInput(hint_text="Peso (ej: 250)", multiline=False, size_hint=(1, None), height=40)
        self.product_measure_spinner = Spinner(
            text="Selecciona la medida",
            values=("GR", "KG", "LT", "ML"),
            size_hint=(1, None), height=40
        )
        self.product_price_input = TextInput(hint_text="Precio (ej: 4.45)", multiline=False, size_hint=(1, None), height=40)
        self.product_priority_spinner = Spinner(
            text="Selecciona la prioridad",
            values=("Primera necesidad (5)", "Muy importante (4)", "Importante (3)", "Opcional (2)", "Poco frecuente (1)"),
            size_hint=(1, None), height=40
        )
        self.product_type_input = TextInput(hint_text="Tipo (ej: Cafe molido)", multiline=False, size_hint=(1, None), height=40)
        self.product_tag_input = TextInput(hint_text="Etiqueta (ej: CAFE)", multiline=False, size_hint=(1, None), height=40)

        # Agregar campos al popup
        popup_layout.add_widget(self.product_weight_input)
        popup_layout.add_widget(self.product_measure_spinner)
        popup_layout.add_widget(self.product_price_input)
        popup_layout.add_widget(self.product_priority_spinner)
        popup_layout.add_widget(self.product_type_input)
        popup_layout.add_widget(self.product_tag_input)

        # Botón para guardar el producto
        save_product_button = Button(text="Guardar producto", size_hint=(1, None), height=40)
        save_product_button.bind(on_press=self.add_product_to_list)
        popup_layout.add_widget(save_product_button)

        # Crear y abrir el popup
        self.add_product_popup = Popup(title="Agregar producto", content=popup_layout, size_hint=(0.9, 0.9))
        self.add_product_popup.open()

    def on_search_product(self, instance, value):
        # Filtrar productos según el texto ingresado
        if value:
            filtered_products = self.final_list[self.final_list["Nombre"].str.contains(value, case=False)]
            menu_items = [{"text": product["Nombre"]} for _, product in filtered_products.iterrows()]
            self.search_menu.items = menu_items
            self.search_menu.open()
        else:
            self.search_menu.dismiss()

    def on_product_selected(self, instance):
        # Autocompletar campos si el producto existe en finallist.csv
        product_name = instance.text
        product = self.final_list[self.final_list["Nombre"] == product_name].iloc[0]
        self.product_search_input.text = product["Nombre"]
        self.product_weight_input.text = str(product["Peso"])
        self.product_measure_spinner.text = product["Medida"]
        self.product_price_input.text = str(product["Precio"])
        self.product_priority_spinner.text = str(product["Prioridad"])
        self.product_type_input.text = product["Tipo"]
        self.product_tag_input.text = product["Etiqueta"]
        self.search_menu.dismiss()

    def add_product_to_list(self, instance):
        # Validar y agregar el producto a la lista temporal
        try:
            # Obtener la prioridad seleccionada
            priority_text = self.product_priority_spinner.text
            priority_map = {
                "Primera necesidad (5)": 5,
                "Muy importante (4)": 4,
                "Importante (3)": 3,
                "Opcional (2)": 2,
                "Poco frecuente (1)": 1
            }
            priority = priority_map.get(priority_text, 0)  # Si no se selecciona nada, será 0

            product = {
                "Nombre": self.product_search_input.text.strip(),
                "Peso": float(self.product_weight_input.text.strip()),
                "Medida": self.product_measure_spinner.text,
                "Precio": float(self.product_price_input.text.strip()),
                "Prioridad": priority,
                "Tipo": self.product_type_input.text.strip(),
                "Etiqueta": self.product_tag_input.text.strip(),
                "FrecuenciaCompra": 0.5,  # Por defecto
                "Preferencia": 1  # Por defecto
            }
            self.temp_items.append(product)

            # Cerrar el popup
            self.add_product_popup.dismiss()

            # Actualizar el preview de la lista
            self.update_preview()

            self.show_error_popup("Producto agregado correctamente.")
        except ValueError as e:
            self.show_error_popup(f"Error en los datos: {str(e)}")

    def update_preview(self):
        # Limpiar el preview actual
        self.preview_grid.clear_widgets()

        # Agregar los productos al preview
        for item in self.temp_items:
            item_label = Label(
                text=f"{item['Nombre']} - {item['Peso']}{item['Medida']} - ${item['Precio']:.2f} - Prioridad: {item['Prioridad']} - Tipo: {item['Tipo']} - Etiqueta: {item['Etiqueta']}",
                size_hint_y=None, height=40
            )
            self.preview_grid.add_widget(item_label)

    def save_new_list(self, instance):
        list_name = self.list_name_input.text.strip()
        if not list_name:
            self.show_error_popup("El nombre de la lista no puede estar vacío.")
            return

        if not self.temp_items:
            self.show_error_popup("La lista no tiene productos.")
            return

        # Guardar la nueva lista
        create_new_shopping_list(list_name, self.temp_items)
        self.show_error_popup(f"Lista '{list_name}' guardada exitosamente.")

    def show_error_popup(self, message):
        error_popup = Popup(title="Alerta", content=Label(text=message), size_hint=(0.8, 0.4))
        error_popup.open()

class ShoppingApp(MDApp):
    def build(self):
        return AddListView()

if __name__ == "__main__":
    ShoppingApp().run()
