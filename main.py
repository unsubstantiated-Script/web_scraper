import requests
import selectorlib

URL = 'http://programmer100.pythonanywhere.com/tours/'

# Making sure scrape attempt isn't getting blocked.
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}


def scrape(url):
    """SCRAPE THE PAGE SOURCE FROM THE URL"""
    response = requests.get(url, headers=HEADERS)
    source = response.text
    return source


def extract(source):
    extractor = selectorlib.Extractor.from_yaml_file("extract.yaml")
    value = extractor.extract(source)["tours"]
    return value


def send_email(value):
    print("Sending email")


def store(extracted):
    with open('data.txt', 'a') as file:
        file.write(extracted + "\n")

def read(extracted):
    with open('data.txt') as file:
        return file.read()

if __name__ == '__main__':
    extracted = extract(scrape(URL))
    print(extracted)
    content = read(extracted)
    if extracted != "No upcoming tours":
        if extracted not in content:
            store(extracted)
            send_email(extracted)
