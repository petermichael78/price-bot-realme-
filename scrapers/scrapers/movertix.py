import requests
from bs4 import BeautifulSoup

def obter_preco():
    url = "https://www.movertix.com/pt/realme-gt-8-pro-16gb-512gb"
    headers = {"User-Agent": "Mozilla/5.0"}
    soup = BeautifulSoup(requests.get(url, headers=headers, timeout=15).text, "html.parser")

    preco = soup.select_one("span.price").text
    preco = float(preco.replace("€","").replace(".","").replace(",",".").strip())

    return {"loja": "Movertix", "preco": preco, "link": url}
