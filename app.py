import flet as fl
import main as recognition_logic
import base64
import utils as ut
import asyncio
import post_processing

class Storage():
    def __init__(self, page:fl.Page):
        self.data_name = "flet_data"
        self.changed = False
        self.page = page
        self.check_storage()
        
    def check_storage(self):
        try:
            self.load()
        except:
            self.new()
    
    def load(self):
        print("loading data..")
        self.registry = ut.loadData(self.data_name)
    
    def new(self):
        print("new data...")
        self.registry = {}
        self.changed = True
              
    def save(self):
        if self.changed:
            print("saving data...")
            ut.saveData(self.data_name, self.registry)
            self.changed = False
        
class Person:
    def __init__(self) -> None:
        self.name = None
        self.surname = None
        self.plate = None
        self.model = None
        self.color = None
        self.base64_plate = None
        self.base64_photo = None
        
    def show_info(self):
        print("name:",self.name)
        print("surname:",self.surname)
        print("plate:",self.plate)
        print("model:",self.model)
        print("color:",self.color)

class Info(fl.UserControl):
    def __init__(self, entity: Person):
        super().__init__()
        self.entity = entity

    def build(self):
        self.txt_plate = fl.Text(
            value=self.entity.plate
            ,style=fl.TextThemeStyle.TITLE_LARGE
            ,color=fl.colors.INVERSE_PRIMARY
            ,weight=fl.FontWeight.BOLD
        )
        imgs = fl.Column(
            controls=[
                fl.Text(
                    value="FOTO",
                    style=fl.TextThemeStyle.DISPLAY_SMALL,
                    weight=fl.FontWeight.BOLD,
                ),
                fl.Image(
                    src="./assets/lustre.png",
                    border_radius=10,
                    fit=fl.ImageFit.COVER,
                    width=200,
                ),
                fl.Text(
                    value="PLACA",
                    style=fl.TextThemeStyle.DISPLAY_SMALL,
                    weight=fl.FontWeight.BOLD,
                ),
                self.txt_plate
            ]
        )

        self.tf_plate = fl.TextField(label="Placa")
        self.tf_plate.value = self.entity.plate

        self.tf_name = fl.TextField(label="Nombres")
        self.tf_name.value = self.entity.name

        self.tf_surname = fl.TextField(label="Apellidos")
        self.tf_surname.value = self.entity.surname

        self.tf_model = fl.TextField(label="Modelo")
        self.tf_model.value = self.entity.model

        self.tf_color = fl.TextField(label="Color")
        self.tf_color.value = self.entity.color

        info = fl.Column(
            controls=[
                self.tf_plate,
                self.tf_name,
                self.tf_surname,
                self.tf_model,
                self.tf_color,
            ]
        )
        return fl.Column(
            controls=[
                fl.Card(
                    expand=True,
                    content=fl.Container(
                        padding=10, content=fl.Row(controls=[imgs, info])
                    ),
                )
            ]
        )

    def update_fields(self):
        self.tf_plate.value = self.entity.plate
        self.tf_name.value = self.entity.name
        self.tf_surname.value = self.entity.surname
        self.tf_color.value = self.entity.color
        self.tf_model.value = self.entity.model
        self.txt_plate.value = self.entity.plate
        self.update()
        
    def get_info(self) -> Person:
        entity = Person()
        entity.plate = self.tf_plate.value
        entity.name = self.tf_name.value
        entity.surname = self.tf_surname.value
        entity.model = self.tf_model.value
        entity.color = self.tf_color.value
        return entity
    
    def clear(self):
        self.tf_plate.value = ""
        self.tf_name.value = ""
        self.tf_surname.value = ""
        self.tf_color.value = ""
        self.tf_model.value = ""

class Create(fl.UserControl):
    def __init__(self, page: fl.Page, storage: Storage) -> None:
        super().__init__()
        self.page = page
        self.info = Info(Person())
        self.storage = storage

    def build(self):
        options = fl.Card(
            content=fl.Container(
                padding=10,
                content=fl.Column(
                    controls=[
                        fl.TextButton(
                            text="Guardar", icon=fl.icons.SAVE, on_click=self.save
                        ),
                        fl.TextButton(text="cancelar", icon=fl.icons.CANCEL),
                    ]
                ),
            )
        )
        return fl.Row(controls=[options, self.info])

    def save(self, e):
        entity = self.info.get_info()
        self.storage.registry[entity.plate] = entity
        self.storage.changed = True
        display = DisplayInfo(self.page)
        display.show("Guardando...")
        self.info.clear()

class Recognition(fl.UserControl):
    def __init__(self, page: fl.Page, storage: Storage, update_method):
        super().__init__()
        self.started = False
        self.page = page
        self.window_width = self.page.window_width
        self.storage = storage
        self.info = Info(Person())
        self.update_method = update_method
        self.display = DisplayInfo(self.page)

    def build(self):
        options = fl.Column(
            controls=[
                fl.Card(
                    expand=True,
                    content=fl.Container(
                        padding=10,
                        content=fl.Column(
                            controls=[
                                fl.TextButton(
                                    text="Iniciar",
                                    icon=fl.icons.REMOVE_RED_EYE_OUTLINED,
                                    on_click=self.start_recognition,
                                ),
                                fl.TextButton(
                                    text="Capturar",
                                    icon=fl.icons.SCREENSHOT_MONITOR_ROUNDED,
                                    on_click=self.capture_frame,
                                ),
                                fl.TextButton(
                                    text="Terminar",
                                    icon=fl.icons.CANCEL,
                                    on_click=self.end_recognition,
                                )
                                ,fl.TextButton(
                                    text="Reducir",
                                    icon=fl.icons.ARROW_BACK_IOS,
                                    on_click=self.reduce_window,
                                )
                                ,fl.TextButton(
                                    text="Expandir",
                                    icon=fl.icons.ARROW_FORWARD_IOS,
                                    on_click=self.restore_window,
                                )
                                ,fl.OutlinedButton(
                                    text="update"
                                    ,on_click= lambda _: self.find_person("LENIN")
                                )
                            ]
                        ),
                    ),
                )
            ]
        )
        self.menu =  fl.Row(
            controls=[
                options, self.info
            ]
        )
        return self.menu
    
    def find_person(self, plate):
        try:
            entity = self.storage.registry[plate]
            self.info.entity = entity
            self.info.update_fields()
            self.display.show(f"Placa {entity.plate} econtrado!!!")
        except:
            self.info.entity.plate = plate
            self.info.update_fields()
            self.display.show(f"No se encuentra la placa: {plate}")
        
    def restore_window(self, e=None):
        self.page.window_width = self.window_width
        self.page.update()
        
    def reduce_window(self, e=None):
        self.page.window_width = self.window_width * 0.22
        self.page.update()

    def start_recognition(self, e):
        self.started = True
        self.reduce_window()
        recognition_logic.recognition(post_processing.nn, self.find_person)
        self.restore_window()
        self.started = False

    def capture_frame(self, e):
        if self.started:
            recognition_logic.capture_frame()

    def end_recognition(self, e):
        if self.started:
            recognition_logic.end_recognition()
            self.started = False

class Navigation(fl.UserControl):
    def __init__(self, set_page) -> None:
        super().__init__()
        self.set_page = set_page

    def build(self):
        return fl.NavigationRail(
            selected_index=0,
            label_type=fl.NavigationRailLabelType.ALL,
            destinations=[
                fl.NavigationRailDestination(
                    icon=fl.icons.ADD_CIRCLE_OUTLINE_ROUNDED, label="Agregar"
                ),
                fl.NavigationRailDestination(
                    icon=fl.icons.LIST_ROUNDED,
                    label="Todos",
                ),
                fl.NavigationRailDestination(
                    icon=fl.icons.REMOVE_RED_EYE_OUTLINED,
                    label_content=fl.Text("Reconocer"),
                ),
            ],
            on_change=lambda e: self.set_page(e.control.selected_index),
        )

class DisplayInfo(fl.UserControl):
    def __init__(self, page: fl.Page):
        super().__init__()
        self.page = page

    def show(self, message):
        self.page.snack_bar = fl.SnackBar(
            content=fl.Text(
                value=message,
                style=fl.TextThemeStyle.TITLE_LARGE,
                color=fl.colors.INVERSE_PRIMARY,
            )
        )
        self.page.snack_bar.open = True
        self.page.update()

class PersonList(fl.UserControl):
    def __init__(self, page:fl.Page, storage: Storage):
        super().__init__()
        self.storage = storage
        self.page = page

    def build(self):
        grid = fl.GridView(
            expand=1,
            runs_count=5,
            max_extent=200,
            child_aspect_ratio=1.0,
            spacing=5,
            run_spacing=5,
        )
        keys = self.storage.registry.keys()
        for k in keys:
            entity:Person = self.storage.registry[k]
            grid.controls.append(
                fl.Card(
                    content=fl.Container(
                        padding=10
                        ,content=fl.Column(
                            controls=[
                                fl.Text(entity.plate)
                                ,fl.Text(entity.name)
                                ,fl.Image(
                                    src="./assets/lustre.png"
                                    ,fit=fl.ImageFit.FILL
                                    ,width=60
                                    ,border_radius=fl.border_radius.all(5)
                                )
                            ]
                        )
                    )
                )
            )
        return fl.Container(
            padding=10
            ,content=grid
            ,width=500
        )

def main(page: fl.Page):
    def on_close(e):
        if e.data == "close":
            print("cerrando")
            storage.save()
            page.window_destroy()
    def set_page(index):
        row.controls[2] = pages[index]
        page.update()
    def update():
        page.update()
        print("actualizando page")
    # 
    page.title = "Placas"
    page.theme_mode = fl.ThemeMode.SYSTEM
    page.theme = fl.Theme(color_scheme_seed=fl.colors.CYAN)
    page.window_prevent_close = True
    page.on_window_event = on_close
    #
    storage = Storage(page)
    page1 = Create(page, storage)
    page2 = PersonList(page, storage)
    page3 = Recognition(page, storage, update)
    pages = [page1, page2, page3]
    rail = Navigation(set_page)
    content = pages[0]
    row = fl.Row(expand=True, controls=[rail, fl.VerticalDivider(width=1), content])
    page.add(row)


fl.app(target=main, assets_dir="assets")
