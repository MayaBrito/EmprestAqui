import json
import requests
import random


def search_image(query):
    query = "%20".join(query.split(' '))
    url = f"https://br.freepik.com/api/regular/search?locale=pt&term={query}"
    headers = {"User-Agent": "Mozilla/5.0"}  # Simular um navegador
    response = requests.get(url, headers=headers)

    items = response.json()["items"]

    return items[random.randint(0, len(items)-1)]["preview"]["url"]


# Carregar a lista de itens (assumindo que está em um arquivo JSON)
with open('tools.json', 'r') as f:
    itens = json.load(f)

# Criar uma lista para armazenar os resultados
resultados = []

# Iterar sobre cada item e buscar a imagem
for i in itens:
    url_imagem = search_image(i["name"])
    i["url"] = url_imagem
    resultados.append(i)
    print(i)

# Salvar os resultados em um novo arquivo JSON
with open('resultados.json', 'w') as f:
    json.dump(resultados, f, indent=4)
