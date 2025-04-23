import requests

URL = "http://localhost:8000/hello"
RESP = requests.get(URL, auth=("alice@example.com", "alicepass"))
print(RESP.status_code)
