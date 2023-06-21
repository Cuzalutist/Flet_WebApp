import flet as ft

def main(page: ft.Page):    

    # user_code = ft.TextField(label="User", autofocus=True)    
    greetings = ft.Column()
    
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.title = "EMM Mobile"

    #TODO: Call REST API HERE TO LIST THE USERS
    user_code = ft.Dropdown(
        # width=100,
        options=[
            ft.dropdown.Option("Alex"),
            ft.dropdown.Option("Javra"),
            ft.dropdown.Option("Mark"),
        ]
    )
    user_code.value = "Alex"

    def route_change(route):
        page.views.clear()
        page.views.append(
            ft.View(
                "/",
                [
                    ft.AppBar(title=ft.Text("EMM5 App"), bgcolor=ft.colors.SURFACE_VARIANT),
                    ft.Row(alignment=ft.MainAxisAlignment.SPACE_EVENLY,controls=[user_code]),
                    ft.Row(alignment=ft.MainAxisAlignment.SPACE_EVENLY,controls=[ft.ElevatedButton("Login", on_click=lambda _: page.go("/menus"))]),
                    greetings
                ],
            )
        )
        #TODO: CALL REST APP FOR MENUS FROM EMM5 App
        if page.route == "/menus":
            if user_code.value == "Alex":
                page.views.append(
                    ft.View(
                        "/menus",
                        [
                            ft.AppBar(title=ft.Text("Menus"), bgcolor=ft.colors.SURFACE_VARIANT),
                            ft.ElevatedButton("Relocate Coils", width=400, height=50, on_click=lambda _: page.go("/relocate")),
                            ft.ElevatedButton("Inventry Check", width=400, height=50, on_click=lambda _: page.go("/inventrychk")),
                            ft.ElevatedButton("Location Check", width=400, height=50, on_click=lambda _: page.go("/location")),
                            ft.OutlinedButton("Go Home", on_click=lambda _: page.go("/")),
                        ],
                    )
                )
            else:
                page.views.append(
                    ft.View(
                        "/menus",
                        [
                            ft.AppBar(title=ft.Text("Menus"), bgcolor=ft.colors.SURFACE_VARIANT),                            
                            ft.ElevatedButton("Go Home", width=400, height=50, on_click=lambda _: page.go("/")),
                        ],
                    )
                )
        page.update()

    def view_pop(view):
        page.views.pop()
        top_view = page.views[-1]
        page.go(top_view.route)

    page.on_route_change = route_change
    page.on_view_pop = view_pop
    page.go(page.route)

ft.app(target=main)