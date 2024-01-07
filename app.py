import flet as fl
import base64

class Persona():
    def __init__(self) -> None:
        self.nombre = None
        self.apellido = None
        self.placa = None
        self.modelo_auto = None
        self.base64_placa = None
        self.base64_persona = None

class Info(fl.UserControl):
    def build(self):
        column = fl.Column()
        card = fl.Card()
        container = fl.Container()
        
        row = fl.Row()
        row.vertical_alignment = fl.CrossAxisAlignment.START
        
        info = fl.Container()
        info.padding = 10
        # info.bgcolor = fl.colors.AMBER
        info.content = fl.Column(
            scroll=fl.ScrollMode.ALWAYS,
            controls=[
                fl.TextField(
                    label="Nombres",
                ),
                fl.TextField(
                    label="Apellidos",
                ),
                fl.TextField(
                    label="Modelo del auto",
                ),
                fl.TextField(
                    label="Color del auto",
                ),
            ],
        )
        
        imgs = fl.Container()
        # imgs.bgcolor = fl.colors.AMBER
        imgs.content = fl.Column(
            horizontal_alignment= fl.CrossAxisAlignment.CENTER,
            controls=[
                fl.Text(
                    value="FOTO",
                    style= fl.TextThemeStyle.DISPLAY_SMALL,
                    weight= fl.FontWeight.BOLD,
                ),
                fl.Image(
                    src="./assets/lustre.png",
                    border_radius=10,
                    fit= fl.ImageFit.COVER,
                    width=200,
                    height=200,
                ),
                fl.Text(
                    value="PLACA",
                    style= fl.TextThemeStyle.DISPLAY_SMALL,
                    weight= fl.FontWeight.BOLD,
                ),
                fl.Image(
                    src="./assets/sample.png",
                    border_radius=10,
                    fit= fl.ImageFit.COVER,
                    width=200,
                ),
            ]
        )
        
        row.controls = [
            imgs
            ,info
        ]
        
        container.content = row 
        container.padding = 10
        
        card.content = container
        column.controls.append(card)
        return column
    
    
    
class Navigation(fl.UserControl):
    def __init__(self, set_page) -> None:
        super().__init__()
        self.set_page = set_page
    
    def build(self):
        rail = fl.NavigationRail(
            selected_index=0
            ,label_type=fl.NavigationRailLabelType.ALL
            ,destinations=[
                fl.NavigationRailDestination(
                    icon=fl.icons.ADD_CIRCLE_OUTLINE_ROUNDED
                    ,label="Agregar"
                ),
                fl.NavigationRailDestination(
                    icon=fl.icons.LIST_ROUNDED
                    ,label="Todos",
                ),
                fl.NavigationRailDestination(
                    icon=fl.icons.REMOVE_RED_EYE_OUTLINED
                    ,label_content=fl.Text("Reconocer")
                ),
            ]
            ,on_change=lambda e: self.set_page(e.control.selected_index)
        )
        return rail

def main(page:fl.Page):
    page.title = "Placas"
    page.theme_mode = fl.ThemeMode.LIGHT
    page.theme = fl.Theme(color_scheme_seed=fl.colors.LIGHT_BLUE_ACCENT)
    def set_page(index):
        row.controls[2] = pages[index]
        page.update()
    
    page1 = Info()
    page2 = fl.Text("page two")
    page3 = Info()
    pages = [page1, page2, page3]
    rail = Navigation(set_page)
    content = pages[0]
    
    row = fl.Row(
        expand=True
        ,controls=[
            rail
            ,fl.VerticalDivider(width=1)
            ,content
        ]
    )
    page.add(row)

fl.app(target=main, assets_dir="assets")