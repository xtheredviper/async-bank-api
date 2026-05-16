import requests

url = "http://127.0.0.1:8000/auth/login"

data = {
    "email": "carol@email.com",
    "password": "123456"
}

response = requests.post(url, json=data)

print(response.json())