import requests
import json

# Base URL and resource path
base_url = "http://192.168.1.78:8980/REST_EMMService/rest/REST_EMMService"
resource_path = "/UsersMenuList"

# Request headers
headers = {
    "Content-Type": "application/json"
}

# Make a GET request
response = requests.get(base_url + resource_path, headers=headers)

# Check the response status
if response.status_code == 200:
    # try:
        # Extract the output parameter from the response
    response_json = response.json()
    vOut = response_json['response']['userMenuList']['userMenuList'][1]
    print("User Code:", vOut['ttUserCode'])
    print("User Program:", vOut['ttUserName'])
    # except KeyError as e:
    #     print("KeyError:", str(e))
    #     print("Response JSON:", response_json)
else:
    print("Request failed with status code:", response.status_code)