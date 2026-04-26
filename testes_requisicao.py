import requests

headers = {
    "Authorization":"Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI4IiwiZXhwIjoxNzc3MTU4NDQyfQ.ER_ZjTR1XKnWozyw92oYSG4RZhD1CGY4o64Yw8PGS_Y"
}
           

requisicao = requests.get("http://127.0.0.1:8000/auth/refresh", headers=headers)
print(f"Status: {requisicao}")
print(requisicao.json())