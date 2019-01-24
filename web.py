from builtins import print

import requests
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
        prices = []
        url = "https://www.klick.ee/catalogsearch/result/index/?p=" + str(page) + "&q=" + str(search)
        soup=soupify(url)
        print ("Leheküljel", page, "leiduvad asjad:")
        prices = getPrice(url, prices)
        #for price in prices.find_all:

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
                    print(href)
                    #titleFromPage(href)
                    print(title)
                    print (prices[j])
                    #print ( 'href="%s">%s' % (href.encode('UTF8', 'replace'), title.encode('UTF8', 'replace')))
            if breakPage == 1:
                break
        print("\n\n")
        page += 1


def getPrice(url, prices):
    price = soupify(url)
    p = 0
    for line in price.find_all("span", {"class": "price"}):
        print (line)
        p = line.string
        p = p.strip("€")
        p = p.strip(" ")
        p = p.strip("\xa0")
        p = p.replace(",", ".")
        print (p)
        #for letter in 'qwertyuiopasdfghjklzxcvbnm/':
            #p = p.replace(letter, '')
        #p.replace(u'\xa0', ' ').encode('utf-8')
        p = float(p)
        prices.append(p)

search = input("Mida soovite otsida?")
klick_spider(55)
