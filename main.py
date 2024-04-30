import os
import time
import sqlite3
import requests
import selectorlib

from send_email import send_email

URL = 'http://programmer100.pythonanywhere.com/tours/'

# Making sure scrape attempt isn't getting blocked.
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

password = os.getenv("GMAIL_PASSWORD")
sender = os.getenv("SENDER")
receiver = os.getenv("RECEIVER")

connection = sqlite3.connect('data.db')


def scrape(url):
    """SCRAPE THE PAGE SOURCE FROM THE URL"""
    response = requests.get(url, headers=HEADERS)
    source = response.text
    return source


def extract(source):
    extractor = selectorlib.Extractor.from_yaml_file("extract.yaml")
    value = extractor.extract(source)["tours"]
    return value


def store(extracted):
    # with open('data.txt', 'a') as file:
    #     file.write(extracted + "\n")
    row = extracted.split(",")
    row = [item.strip() for item in row]
    cursor = connection.cursor()
    cursor.execute("INSERT INTO events VALUES(?,?,?)", row)
    connection.commit()


def read(extracted):
    # with open('data.txt') as file:
    #     return file.read()
    row = extracted.split(",")
    row = [item.strip() for item in row]
    band, city, date = row
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM events WHERE band=? AND city=? AND date=?", (band, city, date))
    rows = cursor.fetchall()
    print(rows)
    return rows


if __name__ == '__main__':
    while True:
        extracted = extract(scrape(URL))
        print(extracted)

        if extracted != "No upcoming tours":
            row = read(extracted)
            if not row:
                store(extracted)
                send_email(extracted, sender, password, receiver)
        time.sleep(2)
