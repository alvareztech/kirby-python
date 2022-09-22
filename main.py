import requests
from bs4 import BeautifulSoup
from datetime import date
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

import datetime
from firebase_admin.firestore import SERVER_TIMESTAMP


def checkFloat(number):
    try:
        return float(number)
    except ValueError:
        return None

# print(results.prettify())


def main():
    print("Hello World!")
    cred = credentials.Certificate("firebase.json")
    firebase_admin.initialize_app(cred)

    db = firestore.client()
    rates = db.collection('rates')

    URL = "https://www.bcb.gob.bo/librerias/indicadores/otras/ultimo.php"
    page = requests.get(URL)

    soup = BeautifulSoup(page.content, "html.parser")

    table = soup.find("table", class_="tablaborde")
    # print(table.prettify())
    rows = table.find_all("tr")

    for i, row in enumerate(rows):
        if i == 0:
            continue
        cols = row.find_all('td')
        country = cols[0].text.strip()
        name = cols[1].text.strip()
        currency = cols[2].text.strip()
        exchange = cols[3].text.strip()
        exchangeME = cols[4].text.strip()
        print("%s %s %s %s %s" %
              (country, name, currency, exchange, exchangeME))
        rates.add({'country': country, 'name': name, 'currency': currency, 'exchange': checkFloat(exchange),
                   'exchangeME': checkFloat(exchangeME), 'source': 'BO', 'date': SERVER_TIMESTAMP})


if __name__ == "__main__":
    main()
