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
    base_url_usersEncodedPassword = vHost + "/UsersPassEncoded"
    base_url_usersMenu     = vHost + "/UsersMenu"
    base_url_coilLocation  = vHost + "/Coils/Location"
    base_url_coil          = vHost + "/Coils"
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

    def coil_changed(e):
        coil_value = e.control.value
        coilURL = ("/" + coil_value)
        response = req.get(base_url_coil + coilURL, headers=headers)
        if response.status_code == 200:
            try:
                response_json = response.json()
                vCoilRecord = response_json['response']['coilRecord']['coilRecord'][0]
                coil_location.value = vCoilRecord['glocc']
            except IndexError:
                print("Index out of range error !")
            except KeyError:
                print("KeyError: 'coilRecord' key not found in the response.")
            page.update()
        else:
            print("Request failed with status code:", response.status_code)

    # RELOCATE COIL
    coil_name = ft.TextField(label="Coil", autofocus=True, width=200, hint_text="Scanned Coil Name", on_change=coil_changed)
    coil_location = ft.TextField(label="Old Location", width=200, disabled=True)
    coil_location_view = ft.TextField(label="Location", autofocus=True, width=200, hint_text="Scanned Location")
    coil_new_location = ft.TextField(label="New Location", width=200, hint_text="New coil location")
    coil_inventory = ft.Text("Inventory under construction !!")

    emm_logo = ft.Image(
        src=f"./icons/logo.png",
        width=100,
        height=100,
        fit=ft.ImageFit.CONTAIN,
    )
    
    data_table = []
    coil_table = ft.DataTable(
                    columns=[
                        ft.DataColumn(ft.Text("CoilName")),
                        ft.DataColumn(ft.Text("CoilNum"), numeric=True),
                        ft.DataColumn(ft.Text("Location")),
                    ],
                    rows=data_table
                )

    def bs_dismissed(e):
        print("Dismissed!")

    successCoil = ft.BottomSheet(
                ft.Container(
                    ft.Column(
                        [
                            ft.Text("Coil sucessfully updated !")
                        ],
                        tight=True,
                    ),
                    padding=10,
                ),
                open=True,
                on_dismiss=bs_dismissed,
            )

    failedCoil = ft.BottomSheet(
                ft.Container(
                    ft.Column(
                        [
                            ft.Text("Failed to update the coil !")
                        ],
                        tight=True,
                    ),
                    padding=10,
                ),
                open=True,
                on_dismiss=bs_dismissed,
            )
    
    def route_change(route):
        page.views.clear()
        page.views.append(
            ft.View(
                "/",
                [
                    ft.AppBar(title=ft.Text("EMM5 App"), bgcolor=ft.colors.SURFACE_VARIANT),
                    ft.Row(alignment=ft.MainAxisAlignment.SPACE_EVENLY,controls=[emm_logo]),
                    ft.Row(alignment=ft.MainAxisAlignment.SPACE_EVENLY,controls=[user_code]),
                    ft.Row(alignment=ft.MainAxisAlignment.SPACE_EVENLY,controls=[user_passcode]),
                    ft.Row(alignment=ft.MainAxisAlignment.SPACE_EVENLY,controls=[ft.ElevatedButton("Login", on_click=open_user_menus)]),
                    greetings
                ],
            )
        )
        #Call REST app for Menus from EMM5 App
        if page.route == "/menus" or page.route == "/menus/relocate" or page.route == "/menus/locationCheck" or page.route == "/menus/inventoryCheck":
            vUser = ('/' + user_code.value)
            response = req.get(base_url_usersMenu + vUser, headers=headers)
            vUserMenus = []
            if response.status_code == 200:
                response_json = response.json()
                vUserMenusDict = response_json['response']['userMenu']['userMenu']
                for menuList in vUserMenusDict:
                    vUserMenus.append(menuList['ttMenuProgram'])
            else:
                print("Request failed with status code:", response.status_code)
            
            page.views.append(
                ft.View(
                    "/menus",
                    [
                        ft.AppBar(title=ft.Text("Menus"), bgcolor=ft.colors.SURFACE_VARIANT),
                        *[ft.ElevatedButton(userMenus, width=400, height=50, on_click=open_menus) for userMenus in vUserMenus]
                    ],
                )
            )
        #Call REST app for POST to coil for EMM5 App
        if page.route == "/menus/relocate":
            page.views.append(
                    ft.View(
                        "/menus/relocate",
                        [
                            ft.AppBar(title=ft.Text("Relocate"), bgcolor=ft.colors.SURFACE_VARIANT),
                            ft.Column(controls=[ft.Row(controls=[coil_name,ft.FloatingActionButton(icon=ft.icons.CHECK, on_click=update_coil),ft.FloatingActionButton(icon=ft.icons.CANCEL_SHARP, on_click=reset_relocation)])]),
                            coil_location,
                            coil_new_location,
                            ft.OutlinedButton("Log Out", on_click=lambda _: page.go("/menu")),
                        ],
                    )
                )
        if page.route == "/menus/locationCheck":
            reset_coil_location()
            page.views.append(
                    ft.View(
                        "/menus/locationCheck",
                        [
                            ft.AppBar(title=ft.Text("Location Check"), bgcolor=ft.colors.SURFACE_VARIANT),
                            ft.Column(controls=[ft.Row(controls=[coil_location_view,ft.FloatingActionButton(icon=ft.icons.CHECK, on_click=add_dataTable),ft.FloatingActionButton(icon=ft.icons.CANCEL_SHARP, on_click=reset_dataTable)])]),
                            coil_table
                        ]
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
        userPassCodeURL = ("/" + user_passcode.value)
        response = req.get(base_url_usersPassword + userURL, headers=headers)
        responeEncoded = req.get(base_url_usersEncodedPassword + userPassCodeURL, headers=headers)

        if response.status_code == 200 and responeEncoded.status_code == 200:
            response_json = response.json()
            response_json_pass = responeEncoded.json()
            vUserRecord = response_json['response']['userRecord']['userRecord'][0]
            vUserPassEncoded = response_json_pass['response']['userPassEncoded']
            if user_code.value == vUserRecord['ttUserCode'] and vUserRecord['ttUserPassword'] == vUserPassEncoded:
                page.go("/menus")
            else:
                print('Failed to authenticate')
    
    # Check coils and fill the table
    def add_dataTable(e):
        locationURL = ("/" + coil_location_view.value)
        response = req.get(base_url_coilLocation + locationURL, headers=headers)
        if coil_location_view.value == '':
            data_table.clear()
        else:
            if response.status_code == 200:
                response_json = response.json()
                vCoilRecords = response_json['response']['ttCoilLocation']['ttCoilLocation']
                data_table.clear()
                for vCoilRecord in vCoilRecords:
                    # print(vCoilRecord['coilName'])
                    data_table.append(ft.DataRow(
                                      cells=[
                                        ft.DataCell(ft.Text(vCoilRecord['coilName'])),
                                        ft.DataCell(ft.Text(vCoilRecord['coilNum'])),
                                        ft.DataCell(ft.Text(vCoilRecord['coilLocation'])),
                                    ],
                            ))
        coil_location_view.focus()
        page.update()

    def reset_coil_location():
        coil_location_view.value = ''
        data_table.clear()

    def update_coil(e):
        #TODO: update the coil location via REST api call
        
        abp = False
        page.overlay.clear()
        if abp == True:
            page.overlay.append(successCoil)
            successCoil.open = True
        else:
            page.overlay.append(failedCoil)
            failedCoil.open = True
        coil_name.focus()
        page.update()        

    # Reset the screen location check
    def reset_dataTable(e):
        reset_coil_location()
        coil_location_view.focus()
        page.update()
    
    def reset_relocation(e):
        coil_name.value = ''
        coil_location.value = ''
        coil_new_location.value = ''
        coil_name.focus()
        page.update()

    def open_menus(e):
        userMenu = e.control.text
        if userMenu == "Relocate Coils":
            page.go("/menus/relocate")
        elif userMenu == "Inventory Check":
            page.go("/menus/inventoryCheck")
        elif userMenu == "Location Check":
            page.go("/menus/locationCheck")
        else:
            print("No menus")

    page.go(page.route)

ft.app(target=main)