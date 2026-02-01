import requests
from bs4 import BeautifulSoup

def obter_preco():
    url = "https://www.amazon.de/dp/B0FTMGX5ZV"
    headers = {
        "User-Agent": "Mozilla/5.0",
        "Accept-Language": "de-DE,de;q=0.9"
    }

    soup = BeautifulSoup(requests.get(url, headers=headers, timeout=15).text, "html.parser")
    preco = soup.select_one("span.a-offscreen").text
    preco = float(preco.replace("€","").replace(".","").replace(",",".").strip())

    return {"loja": "Amazon DE", "preco": preco, "link": url}
