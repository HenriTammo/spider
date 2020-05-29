import requests#netist kätte saamine
from bs4 import BeautifulSoup#html koodi lugemine

def soupify(url):
    source_code = requests.get(url)#koodi asukoht
    plain_text = source_code.text#muudab tekstiks
    soup = BeautifulSoup(plain_text, 'html.parser')#teeb loetavaks pythoni jaoks
    return soup

def titleFromPage(url):
    new=soupify(url)
    for line in new.find_all("h1"):#toote nimi
        print (line.string)#kuna h1 vahel string väärtus siis loeb sisse stringina

def getPrice(url):
    price = soupify(url)
    priceString = price.find("span", {"class": "price"}) #leiab toote hinna classi järgi
    priceString = priceString.get_text() #muudab tekstiks
    return priceString

def klick_spider(max_pages):
    page = 1 #algne otsingu lehekülg
    breakPage = 0 #otsingu piiramiseks, et ei vaataks tühju lehekülgi
    prevItems = [None] * 100000 #nimekiri toodete kontrolliks, et duplikaate ei oleks
    while page <= max_pages and breakPage == 0:
        counter = 0
        url = "https://www.klick.ee/catalogsearch/result/index/?p=" + str(page) + "&q=" + str(search) #lehekülje URL
        soup=soupify(url) #koodi loetavaks muutmine
        print ("Leheküljel", page, "leiduvad asjad:")
        for link in (soup.find_all("h5", {"class": "product-name"})): #otsib toote classi järgi
            for a in link.find_all('a'): #sorteerib <a> järgi
                if a.get('href'): #kui leiab <a> seest href
                    href = a.get('href') #omistab toote enda lehekülje URL
                    if prevItems[counter] == href: #kui toode eksisteeris varem, siis lõpeta otsimine
                        breakPage = 1
                        print ("Leheküljel ei leidunud midagi, sest viimane lehekülg oli", page-1)
                        break
                    prevItems[counter] = href #lisab toote nimekirja
                    counter += 1 
                    title=a.string #leiab tiitli
                    print(title, ";", getPrice(href), ";", href)
            if breakPage == 1:
                break
        print("\n\n")
        page += 1

search = input("Mida soovite otsida? ")
klick_spider(55)#läbib kuni 55 lehekülge