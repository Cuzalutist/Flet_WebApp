import flet as ft
import requests as req
import json


def main(page: ft.Page):    

    # user_code = ft.TextField(label="User", autofocus=True)
    greetings = ft.Column()
    
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.title = "EMM Mobile"
    page.theme_mode = "light"
    page.window_height = 800
    page.window_width = 450
    vHost = "http://192.168.1.78:8980/REST_EMMService/rest/REST_EMMService"

    #Call REST API HERE TO LIST THE USERS
    base_url_usersList     = vHost + "/UsersMenuList"
    base_url_usersPassword = vHost + "/Users"
    base_url_usersEncodedPassword = vHost + "/UsersPassEncoded"
    base_url_usersMenu     = vHost + "/UsersMenu"
    base_url_coilLocation  = vHost + "/Coils/Location"
    base_url_location      = vHost + "/Location"
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
        if coil_value == "":
            coil_value = '~'
        coilURL = ("/" + coil_value)
        response = req.get(base_url_coil + coilURL, headers=headers)
        if response.status_code == 200:
            # print(base_url_coil + coilURL)
            response_json = response.json()
            response_json_obj = response_json['response']['coilRecord']['coilRecord']
            if len(response_json_obj) > 0:
                vCoilRecord = response_json['response']['coilRecord']['coilRecord'][0]
                coil_location.value = vCoilRecord['glocc']
                update_coil_btn.disabled = False
            else:
                coil_location.value = ''
                update_coil_btn.disabled = True
            page.update()
        else:
            print("Request failed with status code:", response.status_code)

    # RELOCATE COIL
    coil_name = ft.TextField(label="Coil", autofocus=True, width=350, hint_text="Scanned Coil Name", on_change=coil_changed)
    coil_location = ft.TextField(label="Old Location", disabled=True)
    coil_location_view = ft.TextField(label="Location", autofocus=True, width=280, hint_text="Scanned Location")
    coil_new_location = ft.TextField(label="New Location", hint_text="New coil location")
    coil_inventory = ft.Text("Inventory under construction !!")
    authMessage = ft.Text(value='', color="red", weight=ft.FontWeight.BOLD, size=20)

    emm_logo = ft.Image(
        src=f"/icons/logo.png",
        width=200,
        height=200,
        fit=ft.ImageFit.CONTAIN,
    )
    
    data_table = []
    coil_table_list = ft.ListView(expand=1, auto_scroll=False)
    coil_table = ft.DataTable(
                    columns=[
                        ft.DataColumn(ft.Text("CoilName")),
                        ft.DataColumn(ft.Text("CoilNum"), numeric=True),
                        ft.DataColumn(ft.Text("Location")),
                    ],
                    rows=data_table,
                    width=380
                )
    coil_table_list.controls.append(coil_table)

    def bs_dismissed(e):
        print("Dismissed!")
    
    coil_info_text = ft.Text("Coil Updated Successfully !!", weight=ft.FontWeight.BOLD, color="green", size=20)

    def update_coil(e):
        #TODO: update the coil location via REST api call
        coilURL = ("/" + coil_name.value)
        locationURL = ("/" + coil_new_location.value)
        response = req.get(base_url_coil + coilURL, headers=headers)
        response_location = req.get(base_url_location + locationURL, headers=headers)
        
        if response.status_code == 200 and response_location.status_code == 200:
            page.overlay.clear()
            response_json = response.json()
            response_location_json = response_location.json()
            isValidLocation = response_location_json['response']['validLocation']

            if eval(isValidLocation) == True:
                response_json['request'] = response_json.pop('response')
                response_json['request']['coilRecord']['coilRecord'][0]['glocc'] = coil_new_location.value
                json_payload = response_json
                request = req.post(base_url_coil + coilURL, json=json_payload, headers=headers)
                if request.status_code == 200:
                    coil_info.visible = True
                    coil_info_text.value = "GG"
                    page.overlay.append(successCoil)
                    successCoil.open = True
                else:
                    page.overlay.append(failedCoil)
                    failedCoil.open = True
            else:
                page.overlay.append(failedCoilLocation)
                failedCoilLocation.open = True
            coil_name.focus()
            coil_location_view.value = coil_new_location.value
            page.update()

    successCoil = ft.BottomSheet(
                ft.Container(
                    ft.Column(
                        [
                            ft.Text("Coil sucessfully updated !", weight=ft.FontWeight.BOLD, color="green", size=20)
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
                            ft.Text("Failed to update the coil !", weight=ft.FontWeight.BOLD, color="red", size=20),
                            ft.Text("", size=20)
                        ],
                        tight=True,
                    ),
                    padding=10
                ),
                open=True,
                on_dismiss=bs_dismissed,
            )
    
    failedCoilLocation = ft.BottomSheet(
                        ft.Container(
                            ft.Column(
                                [
                                    ft.Text("Invalid Location !", weight=ft.FontWeight.BOLD, color="red", size=20),
                                    ft.Text("", size=20)
                                ],
                                tight=True,
                            ),
                            padding=10
                        ),
                        open=True,
                        on_dismiss=bs_dismissed,
                    )
        
    coil_info = ft.Container(
                    ft.Column(
                        [
                            coil_info_text
                        ],
                        tight=True,
                    ),
                    padding=10,
                    visible=False
                )
    
    update_coil_btn = ft.ElevatedButton(content=ft.Container(
                                          content=ft.Column(
                                              [
                                                  ft.Text(value="Update Coil Location", size=20)
                                              ],
                                              alignment=ft.MainAxisAlignment.CENTER,
                                              spacing=5,
                                          ),
                                          padding=ft.padding.all(10),
                                          ),
                                          height=90,
                                          width=415,
                                          disabled=True,
                                          on_click=update_coil
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
                    # ft.Row(alignment=ft.MainAxisAlignment.SPACE_EVENLY,controls=[ft.ElevatedButton("Login", width=300, height=50, on_click=open_user_menus)]),
                    ft.Row(alignment=ft.MainAxisAlignment.SPACE_EVENLY,
                            controls=[ft.ElevatedButton(content=ft.Container
                                                        (
                                                            content=ft.Column(
                                                                [
                                                                    ft.Text(value="Login", size=20)
                                                                ],
                                                                alignment=ft.MainAxisAlignment.CENTER,
                                                                spacing=5,
                                                            ),
                                                            padding=ft.padding.all(10),
                                                        ),
                                                        width=300, 
                                                        height=50, 
                                                        on_click=open_user_menus
                                                        )
                                    ]),
                    ft.Row(alignment=ft.MainAxisAlignment.SPACE_EVENLY,controls=[authMessage])
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
                        # *[ft.ElevatedButton(userMenus, size=20, width=250, height=70, on_click=open_menus) for userMenus in vUserMenus]
                        *[
                            ft.ElevatedButton(userMenus,
                                content=ft.Container(
                                    content=ft.Column(
                                        [
                                            ft.Text(value=userMenus, size=20)                                            
                                        ],
                                        alignment=ft.MainAxisAlignment.CENTER,
                                        spacing=5,
                                    ),
                                    padding=ft.padding.all(10),
                                ),
                                width=500, 
                                height=90,
                                on_click=open_menus
                            ) for userMenus in vUserMenus
                        ]
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
                            ft.Column(controls=[ft.Row(controls=[coil_name,ft.FloatingActionButton(icon=ft.icons.CANCEL_SHARP, on_click=reset_relocation)])]),
                            coil_location,
                            coil_new_location,
                            # ft.OutlinedButton("Update Coil Location", height=50, width=200, on_click=update_coil),
                            update_coil_btn,
                            # ft.OutlinedButton("Log Out", height=50, width=200, on_click=lambda _: page.go("/menu")),
                            ft.ElevatedButton(content=ft.Container(
                                                content=ft.Column(
                                                    [
                                                        ft.Text(value="Log Out", size=20)                                                            
                                                    ],
                                                    alignment=ft.MainAxisAlignment.CENTER,
                                                    spacing=5,
                                                ),
                                                padding=ft.padding.all(10),
                                                ),
                                                height=90,
                                                width=415,
                                                on_click=lambda _: page.go("/menu")
                                            ),
                            coil_info
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
                            coil_table_list
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
        
        if user_passcode.value == "":
            authMessage.value = "Failed to authenticate"
            page.update()

        if response.status_code == 200 and responeEncoded.status_code == 200:
            response_json = response.json()
            response_json_pass = responeEncoded.json()
            vUserRecord = response_json['response']['userRecord']['userRecord'][0]
            vUserPassEncoded = response_json_pass['response']['userPassEncoded']
            if user_code.value == vUserRecord['ttUserCode'] and vUserRecord['ttUserPassword'] == vUserPassEncoded:
                reset_password()
                page.go("/menus")
            else:
                authMessage.value = "Failed to authenticate"
                page.update()
    
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

    def reset_password():
        user_passcode.value = ''
        authMessage.value = ''
    

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

ft.app(target=main, assets_dir="assets")