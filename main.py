import os
import time

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
    with open('data.txt', 'a') as file:
        file.write(extracted + "\n")


def read(extracted):
    with open('data.txt') as file:
        return file.read()


if __name__ == '__main__':
    while True:
        extracted = extract(scrape(URL))
        print(extracted)
        content = read(extracted)
        if extracted != "No upcoming tours":
            if extracted not in content:
                store(extracted)
                send_email(extracted, sender, password, receiver)
        time.sleep(2)
