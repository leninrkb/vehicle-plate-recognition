import flet as fl
import main as recognition_logic
import base64

class Person():
    def __init__(self) -> None:
        self.ci = None
        self.name = None
        self.surname = None
        self.plate = None
        self.model = None
        self.color = None
        self.base64_plate = None
        self.base64_photo = None

class Info(fl.UserControl):
    def __init__(self, entity:Person):
        super().__init__()
        self.entity = entity
        
    def build(self):
        imgs = fl.Column(
            controls = [
                fl.Text(
                    value = "FOTO",
                    style =  fl.TextThemeStyle.DISPLAY_SMALL,
                    weight =  fl.FontWeight.BOLD,
                ),
                fl.Image(
                    src = "./assets/lustre.png",
                    border_radius = 10,
                    fit =  fl.ImageFit.COVER,
                    width = 200,
                ),
                fl.Text(
                    value = "PLACA",
                    style =  fl.TextThemeStyle.DISPLAY_SMALL,
                    weight =  fl.FontWeight.BOLD,
                ),
                fl.Image(
                    src = "./assets/sample.png",
                    border_radius = 10,
                    fit =  fl.ImageFit.COVER,
                    width = 200,
                ),
            ]
        )
        
        self.tf_ci = fl.TextField(label = "C.I.")
        self.tf_ci.value = self.entity.ci
        
        self.tf_name = fl.TextField(label = "Nombres")
        self.tf_name.value = self.entity.name
        
        self.tf_surname = fl.TextField(label = "Apellidos")
        self.tf_surname.value = self.entity.surname
        
        self.tf_model = fl.TextField(label = "Modelo")
        self.tf_model.value = self.entity.model
        
        self.tf_color = fl.TextField(label = "Color")
        self.tf_color.value = self.entity.color
        
        info = fl.Column(
            controls = [
                self.tf_ci
                ,self.tf_name
                ,self.tf_surname
                ,self.tf_model
                ,self.tf_color
            ]
        )
        return fl.Column(
            controls = [
                fl.Card(
                    expand = True
                    ,content = fl.Container(
                        padding = 10
                        ,content = fl.Row(
                            controls = [
                                imgs, info
                            ]
                        )
                    )
                )
            ]
        )
    
    def get_info(self) -> Person:
        self.entity.ci = self.tf_ci.value
        self.entity.name = self.tf_name.value
        self.entity.surname = self.tf_surname.value
        self.entity.model = self.tf_model.value
        self.entity.color = self.tf_color.value
        return self.entity
              
class Create(fl.UserControl):
    def __init__(self, page:fl.Page, entity:Person) -> None:
        super().__init__()
        self.page = page
        self.info = Info(entity)
    
    def build(self):
        options = fl.Card(
            content = fl.Container(
                padding = 10
                ,content = fl.Column(
                    controls = [
                        fl.TextButton(
                            text="Guardar"
                            ,icon = fl.icons.SAVE
                            ,on_click=self.create
                        )
                        ,fl.TextButton(
                            text = "cancelar"
                            ,icon = fl.icons.CANCEL
                        )
                    ]
                )
            )
        )
        return fl.Row(
            controls=[
                options, self.info
            ]
        )
    
    def create(self, e):
        entity = self.info.get_info()
        print(entity.ci)
        print(entity.name)
        print(entity.surname)
        print(entity.color)
        print(entity.model)
          
class Recognition(fl.UserControl):
    def __init__(self, page:fl.Page):
        super().__init__()
        self.started = False
        self.page = page
        self.window_width = self.page.window_width
        
    def build(self):
        return fl.Column(
            controls = [
                fl.Card(
                    expand = True
                    ,content = fl.Container(
                        padding = 10
                        ,content = fl.Column(
                            controls = [
                                fl.TextButton(
                                    text = "Iniciar"
                                    ,icon = fl.icons.REMOVE_RED_EYE_OUTLINED
                                    ,on_click = self.start_recognition
                                )
                                ,fl.TextButton(
                                    text = "Capturar"
                                    ,icon = fl.icons.SCREENSHOT_MONITOR_ROUNDED
                                    ,on_click = self.capture_frame
                                )
                                ,fl.TextButton(
                                    text = "Terminar"
                                    ,icon = fl.icons.CANCEL
                                    ,on_click = self.end_recognition
                                )
                            ]
                        )
                    )
                )
            ]
        )  
    
    def start_recognition(self, e):
        self.started = True
        self.page.window_width = self.window_width * 0.25
        self.page.update()
        recognition_logic.main()  
        self.page.window_width = self.window_width
        self.page.update()
        self.startes = False
        
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
        rail = fl.NavigationRail(
            selected_index = 0
            ,label_type = fl.NavigationRailLabelType.ALL
            ,destinations = [
                fl.NavigationRailDestination(
                    icon = fl.icons.ADD_CIRCLE_OUTLINE_ROUNDED
                    ,label = "Agregar"
                ),
                fl.NavigationRailDestination(
                    icon = fl.icons.LIST_ROUNDED
                    ,label = "Todos",
                ),
                fl.NavigationRailDestination(
                    icon = fl.icons.REMOVE_RED_EYE_OUTLINED
                    ,label_content = fl.Text("Reconocer")
                ),
            ]
            ,on_change = lambda e: self.set_page(e.control.selected_index)
        )
        return rail

def main(page:fl.Page):
    page.title = "Placas"
    page.theme_mode = fl.ThemeMode.SYSTEM
    page.theme = fl.Theme(color_scheme_seed = fl.colors.CYAN)
    # 
    def set_page(index):
        row.controls[2] = pages[index]
        page.update()
    # 
    entity = Person()
    entity.name = "Sana Sunomiya"
    page1 = Create(page, entity)
    page2 = Info(entity)
    page3 = Recognition(page)
    pages = [page1, page2, page3]
    rail = Navigation(set_page)
    content = pages[0]
    row = fl.Row(
        expand = True
        ,controls = [
            rail
            ,fl.VerticalDivider(width = 1)
            ,content
        ]
    )
    page.add(row)

fl.app(target = main, assets_dir = "assets")