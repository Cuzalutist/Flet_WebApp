import flet as ft

def main(page):    

    # user_code = ft.TextField(label="User", autofocus=True)    
    greetings = ft.Column()

    page.vertical_alignment = ft.MainAxisAlignment.CENTER

    #TODO: Call REST API HERE TO LIST THE USERS
    user_code = ft.Dropdown(
        # width=100,
        options=[
            ft.dropdown.Option("Alex"),
            ft.dropdown.Option("Javra"),
            ft.dropdown.Option("Mark"),
        ]
    )

    def btn_click(e):
        greetings.controls.append(ft.Text(f"Hello, {user_code.value}!"))
        page.update()
        user_code.focus()

    # page.add(
    #     user_code,
    #     user_pass,
    #     ft.ElevatedButton("Say hello!", on_click=btn_click),
    #     greetings,
    # )

    page.add(
        ft.Row(
            alignment=ft.MainAxisAlignment.SPACE_EVENLY,
            controls=[user_code]
        ),        
        ft.Row(
            alignment=ft.MainAxisAlignment.SPACE_EVENLY,
            controls=[ft.ElevatedButton("Login", on_click=btn_click)]
        ),
        greetings
    )

ft.app(target=main)