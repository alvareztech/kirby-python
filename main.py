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


def spanishMonthToNumber(month):
    dic = {"enero": 1, "febrero": 2, "marzo": 3, "abril": 4, "mayo": 5, "junio": 6, "julio": 7,
           "agosto": 8, "septiembre": 9, "octubre": 10, "noviembre": 11, "diciembre": 12}
    return dic[month.lower()]


# print(results.prettify())


BO_BCB_URL = "https://www.bcb.gob.bo/librerias/indicadores/otras/ultimo.php"


def main():
    cred = credentials.Certificate("firebase.json")
    firebase_admin.initialize_app(cred)

    db = firestore.client()
    ratesCollection = db.collection('rates')

    page = requests.get(BO_BCB_URL)

    soup = BeautifulSoup(page.content, "html.parser")

    priceDateRaw = soup.select_one(
        "table").select_one("td").select_one("strong").string
    print(priceDateRaw)
    priceDateRaw = priceDateRaw.split()
    priceDateRaw.remove("de")
    priceDate = datetime.datetime(int(priceDateRaw[2]), spanishMonthToNumber(
        priceDateRaw[1]), int(priceDateRaw[0]))
    priceDate = priceDate.strftime("%d-%m-%Y")
    print(priceDate)

    table = soup.find("table", class_="tablaborde")
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
        ratesCollection.add({'country': country, 'name': name, 'currency': currency, 'exchange': checkFloat(exchange),
                             'exchangeME': checkFloat(exchangeME), 'source': 'BO', 'priceDate': priceDate, 'date': SERVER_TIMESTAMP})


if __name__ == "__main__":
    main()
