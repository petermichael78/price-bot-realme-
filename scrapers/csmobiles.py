import requests
from bs4 import BeautifulSoup

def obter_preco():
    url = "https://www.csmobiles.com/realme-gt-8-pro-5g-16gb-512gb"
    headers = {"User-Agent": "Mozilla/5.0"}
    soup = BeautifulSoup(requests.get(url, headers=headers, timeout=15).text, "html.parser")

    preco = soup.select_one("span.price").text
    preco = float(preco.replace("€","").replace(".","").replace(",",".").strip())

    return {"loja": "CSMobiles", "preco": preco, "link": url}
