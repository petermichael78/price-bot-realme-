from scrapers.csmobiles import obter_preco as csmobiles
from scrapers.darty import obter_preco as darty
from scrapers.movertix import obter_preco as movertix
from scrapers.amazon_de import obter_preco as amazon_deimport os
import requests
import pandas as pd
from bs4 import BeautifulSoup
from datetime import datetime
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# ================= CONFIGURAÇÃO =================
PRECO_LIMITE = 750
PRODUTO = "Realme GT 8 Pro 16GB/512GB Urban Blue"
HISTORICO = "historico_precos.csv"

EMAIL_REMETENTE = os.environ["EMAIL_REMETENTE"]
EMAIL_PASSWORD = os.environ["EMAIL_PASSWORD"]
EMAIL_DESTINO = os.environ["EMAIL_DESTINO"]

HEADERS = {
    "User-Agent": "Mozilla/5.0",
    "Accept-Language": "pt-PT,pt;q=0.9"
}

# ================= EMAIL =================
def enviar_email(preco, loja, link):
    msg = MIMEMultipart()
    msg["From"] = EMAIL_REMETENTE
    msg["To"] = EMAIL_DESTINO
    msg["Subject"] = "📉 NOVO mínimo histórico – Realme GT 8 Pro"

    corpo = f"""
🔔 OPORTUNIDADE DETETADA

📱 Produto: {PRODUTO}
🏬 Loja: {loja}
💰 Preço: {preco:.2f} €
🔗 Link: {link}
📅 Data: {datetime.now().strftime('%d-%m-%Y')}

✔ Novo mínimo histórico
✔ Preço inferior a {PRECO_LIMITE} €
"""

    msg.attach(MIMEText(corpo, "plain"))

    with smtplib.SMTP_SSL("smtp.sapo.pt", 465) as server:
        server.login(EMAIL_REMETENTE, EMAIL_PASSWORD)
        server.send_message(msg)

# ================= UTIL =================
def limpar_preco(texto):
    return float(
        texto.replace("€", "")
             .replace(".", "")
             .replace(",", ".")
             .strip()
    )

def novo_minimo(preco_atual):
    if not os.path.exists(HISTORICO):
        return True
    df = pd.read_csv(HISTORICO)
    return preco_atual < df["preco"].min()

# ================= SCRAPERS =================
def kuantokusta():
    url = "https://www.kuantokusta.pt/p/12028488"
    soup = BeautifulSoup(requests.get(url, headers=HEADERS).text, "html.parser")
    preco = limpar_preco(soup.select_one("span.price").text)
    return {"loja": "KuantoKusta", "preco": preco, "link": url}

def fnac():
    url = "https://www.fnac.pt/realme-GT-8-Pro-512GB-Urban-Blue"
    soup = BeautifulSoup(requests.get(url, headers=HEADERS).text, "html.parser")
    preco = limpar_preco(soup.select_one(".f-productPrice").text)
    return {"loja": "FNAC", "preco": preco, "link": url}

def worten():
    url = "https://www.worten.pt/produtos/gt-8-pro-5g-512gb-16gb"
    soup = BeautifulSoup(requests.get(url, headers=HEADERS).text, "html.parser")
    preco = limpar_preco(soup.select_one("span[data-testid='price']").text)
