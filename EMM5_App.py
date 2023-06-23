import flet as ft
import requests as req
import json


def main(page: ft.Page):    

    # user_code = ft.TextField(label="User", autofocus=True)    
    greetings = ft.Column()
    
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.title = "EMM Mobile"
    vHost = "http://192.168.1.78:8980/REST_EMMService/rest/REST_EMMService"

    #Call REST API HERE TO LIST THE USERS
    base_url_usersList     = vHost + "/UsersMenuList"
    base_url_usersPassword = vHost + "/Users"
    base_url_usersMenu     = vHost + "/UsersMenu"
    headers = {
        "Content-Type": "application/json"
    }

    # Make a GET request
    response = req.get(base_url_usersList, headers=headers)
    vUserListJson = []

    if response.status_code == 200:
        response_json = response.json()
        vUserList = response_json['response']['userMenuList']['userMenuList']
        for userList in vUserList:
            vUserListJson.append(userList["ttUserCode"])
    else:
        print("Request failed with status code:", response.status_code)

    user_code = ft.Dropdown(
        # width=100,
        options=[ft.dropdown.Option(userCode) for userCode in vUserListJson],
        autofocus=True
    )
    user_passcode = ft.TextField(label="Password")
    user_code.value = vUserListJson[0]

    # RELOCATE COIL
    coil_name = ft.TextField(label="Coil")
    coil_location = ft.TextField(label="Location", disabled=True)
    coil_location_view = ft.TextField(label="Location", autofocus=True)
    coil_new_location = ft.TextField(label="New Location")
    coil_inventory = ft.Text("Inventory under construction !!")
    
    coil_table = ft.DataTable(
                    columns=[
                        ft.DataColumn(ft.Text("CoilName")),
                        ft.DataColumn(ft.Text("CoilNum"), numeric=True),
                        ft.DataColumn(ft.Text("Location")),
                    ],
                    rows=[
                        ft.DataRow(
                            cells=[
                                ft.DataCell(ft.Text("3725498")),
                                ft.DataCell(ft.Text("3725498")),
                                ft.DataCell(ft.Text("B-000-01")),
                            ],
                        ),
                        ft.DataRow(
                            cells=[
                                ft.DataCell(ft.Text("3725466X0G")),
                                ft.DataCell(ft.Text("3748962")),
                                ft.DataCell(ft.Text("B-000-01")),
                            ],
                        ),
                        ft.DataRow(
                            cells=[
                                ft.DataCell(ft.Text("3709969X01")),
                                ft.DataCell(ft.Text("3753669")),
                                ft.DataCell(ft.Text("B-000-01")),
                            ],
                        ),
                    ],
                )
    

    def route_change(route):
        page.views.clear()
        page.views.append(
            ft.View(
                "/",
                [
                    ft.AppBar(title=ft.Text("EMM5 App"), bgcolor=ft.colors.SURFACE_VARIANT),
                    ft.Row(alignment=ft.MainAxisAlignment.SPACE_EVENLY,controls=[user_code]),
                    ft.Row(alignment=ft.MainAxisAlignment.SPACE_EVENLY,controls=[user_passcode]),
                    ft.Row(alignment=ft.MainAxisAlignment.SPACE_EVENLY,controls=[ft.ElevatedButton("Login", on_click=open_user_menus)]),
                    greetings
                ],
            )
        )
        #Call REST app for Menus from EMM5 App
        if page.route == "/menus" or page.route == "/menus/relocate" or page.route == "/menus/locationCheck" or page.route == "/menus/inventoryCheck":

            if user_code.value == "Alex":
                page.views.append(
                    ft.View(
                        "/menus",
                        [
                            ft.AppBar(title=ft.Text("Menus"), bgcolor=ft.colors.SURFACE_VARIANT),
                            ft.ElevatedButton("Relocate Coils", width=400, height=50, on_click=open_menus_relocate),
                            ft.ElevatedButton("Inventry Check", width=400, height=50, on_click=open_inventoryCheck),
                            ft.ElevatedButton("Location Check", width=400, height=50, on_click=open_menus_locationCheck)
                        ],
                    )
                )
            else:
                page.views.append(
                    ft.View(
                        "/menus",
                        [
                            ft.AppBar(title=ft.Text("Menus"), bgcolor=ft.colors.SURFACE_VARIANT)
                        ],
                    )
                )
        #TODO: Call REST app for POST to coil for EMM5 App
        if page.route == "/menus/relocate":
            page.views.append(
                    ft.View(
                        "/menus/relocate",
                        [
                            ft.AppBar(title=ft.Text("Relocate"), bgcolor=ft.colors.SURFACE_VARIANT),
                            coil_name,
                            coil_location,
                            coil_new_location,
                            ft.OutlinedButton("Log Out", on_click=lambda _: page.go("/menu")),
                        ],
                    )
                )
        if page.route == "/menus/locationCheck":
            page.views.append(
                    ft.View(
                        "/menus/locationCheck",
                        [
                            ft.AppBar(title=ft.Text("Location Check"), bgcolor=ft.colors.SURFACE_VARIANT),
                            coil_location_view,
                            coil_table
                        ],
                    )
                )
        if page.route == "/menus/inventoryCheck":
            page.views.append(
                    ft.View(
                        "/menus/inventoryCheck",
                        [
                            ft.AppBar(title=ft.Text("Inventory Check"), bgcolor=ft.colors.SURFACE_VARIANT),
                            coil_inventory                            
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
    
    def open_user_menus(e):
        # REST call for password verification
        userURL = ("/" + user_code.value)        
        response = req.get(base_url_usersPassword + userURL, headers=headers)

        if response.status_code == 200:
            response_json = response.json()
            vUserRecord = response_json['response']['userRecord']['userRecord'][0]
            if user_code.value == vUserRecord['ttUserCode'] and user_passcode.value == vUserRecord['ttUserPassword']:
                page.go("/menus")
            else:
                print('Failed to authenticate')
    
    def open_menus_relocate(e):
        page.go("/menus/relocate")
    
    def open_menus_locationCheck(e):
        page.go("/menus/locationCheck")
        
    def open_inventoryCheck(e):
        page.go("/menus/inventoryCheck")
    
    page.go(page.route)

ft.app(target=main)