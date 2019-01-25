from builtins import print

import requests
import string
from bs4 import BeautifulSoup




def soupify(url):
    source_code = requests.get(url)
    plain_text = source_code.text
    soup = BeautifulSoup(plain_text, 'html.parser')
    return soup

def titleFromPage(url):
    new=soupify(url)
    for line in new.find_all("h1"):
        print (line.string)

def klick_spider(max_pages):
    page = 1

    breakPage = 0
    prevItems = [None] * 100
    while page <= max_pages and breakPage == 0:
        j= 0
        url = "https://www.klick.ee/catalogsearch/result/index/?p=" + str(page) + "&q=" + str(search)
        soup=soupify(url)
        print ("Leheküljel", page, "leiduvad asjad:")
        for link in (soup.find_all("h5", {"class": "product-name"})):
            for a in link.find_all('a'):
                if a.get('href'):
                    href = a.get('href')
                    if prevItems[j] == href:
                        breakPage = 1
                        print ("Leheküljel ei leidunud midagi, sest viimane lehekülg oli", page-1)
                        break
                    prevItems[j] = href
                    j += 1
                    title=a.string
                    print(title, ";", getPrice(href), ";", href)
                    #print(href)
                    #print(title)
                    #print (getPrice(href))
            if breakPage == 1:
                break
        print("\n\n")
        page += 1


def getPrice(url):
    price = soupify(url)
    priceString = price.find("span", {"class": "price"})
    priceString = priceString.get_text()
    p = str(priceString)
    p = p.replace("-", "00")
    p = float(p)
    return p


search = input("Mida soovite otsida? ")
klick_spider(55)
