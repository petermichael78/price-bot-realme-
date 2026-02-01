import requests
from bs4 import BeautifulSoup

def obter_preco():
    url = "https://www.darty.pt/products/realme-gt-8-pro-512gb"
    headers = {"User-Agent": "Mozilla/5.0"}
    soup = BeautifulSoup(requests.get(url, headers=headers, timeout=15).text, "html.parser")

    preco = soup.select_one("span.product-price").text
    preco = float(preco.replace("€","").replace(".","").replace(",",".").strip())

    return {"loja": "Darty", "preco": preco, "link": url}
