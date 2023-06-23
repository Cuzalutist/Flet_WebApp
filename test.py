import json

my_dict = {'coilName': '3735813', 'href': 'http://192.168.1.78:8980/REST_EMMService/rest/REST_EMMService/Coils/3735813'}

# json_str = json.dumps(my_dict)
# data = json.loads(json_str)
coil_name = my_dict['href']

print(coil_name)
