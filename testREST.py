import requests as req
import json

vHost = "192.168.1.78"

#Call REST API HERE TO LIST THE USERS
base_url_usersList = "http://" + vHost + ":8980/REST_EMMService/rest/REST_EMMService/UsersMenuList"
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

print(vUserListJson)