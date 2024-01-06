import flet as ft


class Info(ft.UserControl):
    def build(self):
        column = ft.Column()
        card = ft.Card()
        
        container = ft.Container()
        
        row = ft.Row()
        row.wrap = 0
        row.alignment = ft.MainAxisAlignment.SPACE_AROUND
        
        info = ft.Container()
        # info.width = 100
        # info.height = 100
        # info.expand = True
        info.padding = 10
        info.bgcolor = ft.colors.AMBER
        info.content = ft.Column(
            scroll=ft.ScrollMode.ALWAYS,
            controls=[
                ft.TextField(
                    label="Holaa",
                    value= "holap",
                ),
                ft.TextField(
                    label="Holaa",
                    value= "holap",
                ),
                ft.TextField(
                    label="Holaa",
                    value= "holap",
                ),
            ],
        )
        
        imgs = ft.Container()
        imgs.bgcolor = ft.colors.AMBER
        imgs.content = ft.Column(
            horizontal_alignment= ft.CrossAxisAlignment.CENTER,
            controls=[
                ft.Text(
                    value="PROPIETARIO",
                    style= ft.TextThemeStyle.DISPLAY_SMALL,
                    weight= ft.FontWeight.BOLD,
                ),
                ft.Image(
                    src="./assets/lustre.png",
                    border_radius=10,
                    fit= ft.ImageFit.COVER,
                    width=200,
                    height=200,
                ),
                ft.Text(
                    value="PLACA",
                    style= ft.TextThemeStyle.DISPLAY_SMALL,
                    weight= ft.FontWeight.BOLD,
                ),
                ft.Image(
                    src="./assets/sample.png",
                    border_radius=10,
                    fit= ft.ImageFit.COVER,
                    width=200,
                ),
            ]
        )
        
        row.controls = [
            info,
            imgs
        ]
        
        container.content = row 
        container.padding = 10
        
        card.content = container
        column.controls = [card]
        return column

def main(page:ft.Page):
    page.theme_mode = ft.ThemeMode.LIGHT
    page.theme = ft.Theme(color_scheme_seed=ft.colors.LIGHT_BLUE_ACCENT)
    info = Info()
    column = ft.Column()
    column.controls.append(info)
    page.add(column)

ft.app(target=main, assets_dir="assets")