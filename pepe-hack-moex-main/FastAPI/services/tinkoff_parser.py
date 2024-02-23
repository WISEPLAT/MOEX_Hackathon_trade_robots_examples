import time

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup

options = Options()
options.add_argument("--headless")
options.add_argument("--window-size=1980,1020")
browser = webdriver.Chrome(options=options)


def get_company_data_by_ticker(ticker: str):
    url = "https://www.tinkoff.ru/invest/stocks/"
    url += ticker
    browser.get(url)
    time.sleep(2)

    soup = BeautifulSoup(browser.page_source, 'html.parser')

    icon = soup.find("img", class_="InvestLogo__image_rmSHy")["src"]
    icon = "https:" + icon

    description = soup.find("div", {"data-qa-file": "SecurityInfo"}).find_all("p")
    description = "\n".join([p.text for p in description])

    name = soup.find("span", class_="SecurityHeader__showName_iw6qC").text

    bg_div = soup.find("div", class_="SecurityHeader__wrapper_nrfiS")["style"]
    background, text_color = [x.strip() for x in bg_div.split(";")[:2]]

    return icon, description, name, background, text_color


if __name__ == "__main__":
    ticker = input("Input Ticker:")

    for x in get_company_data_by_ticker(ticker):
        print(x)
