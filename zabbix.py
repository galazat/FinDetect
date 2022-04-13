

import requests
import json

ZABBIX_API_URL = "https://example.com/zabbix/api_jsonrpc.php"
UNAME = "Admin"
PWORD = "password"

r = requests.post(ZABBIX_API_URL,
                  json={
                      "jsonrpc": "2.0",
                      "method": "user.login",
                      "params": {
                          "user": UNAME,
                          "password": PWORD},
                      "id": 1
                  })

print(json.dumps(r.json(), indent=4, sort_keys=True))

AUTHTOKEN = r.json()["result"]

# Retrieve a list of problems
print("\nRetrieve a list of problems")
r = requests.post(ZABBIX_API_URL,
                  json={
                      "jsonrpc": "2.0",
                      "method": "problem.get",
                      "params": {
                          "output": "extend",
                          "selectAcknowledges": "extend",
                          "recent": "true",
                          "sortfield": ["eventid"],
                          "sortorder": "DESC"
                      },
                      "id": 2,
                      "auth": AUTHTOKEN
                  })

print(json.dumps(r.json(), indent=4, sort_keys=True))

#Logout user
print("\nLogout user")
r = requests.post(ZABBIX_API_URL,
                  json={
                      "jsonrpc": "2.0",
                      "method": "user.logout",
                      "params": {},
                      "id": 2,
                      "auth": AUTHTOKEN
                  })

print(json.dumps(r.json(), indent=4, sort_keys=True))