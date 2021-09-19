import requests
import json

url = "https://141b0828.eu-gb.apigw.appdomain.cloud/api/add-review"

json_payload = json.dumps({'review': {'dealership': 1, 'review': 'Some test text'}})

headers = {"Content-Type": "application/json", "X-Debug-Mode":"true"}

response = requests.request("POST", url, data=json_payload, headers=headers)

print('response:', response)