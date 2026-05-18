import requests

url = "https://api-xml-scan.vercel.app"

payload = {
    "user": "",
    "senha": "admin",
    "preco": ''
}

response = requests.post(url, json=payload)

print(response.json())