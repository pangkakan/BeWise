import mechanicalsoup
from bs4 import BeautifulSoup
from urllib.request import urlopen
browser = mechanicalsoup.Browser()

url = "https://schema.mau.se/setup/jsp/Schema.jsp?startDatum=idag&intervallTyp=m&intervallAntal=6&sprak=SV&sokMedAND=true&forklaringar=true&resurser=p.TGSYA23h"
page = browser.get(url)
html = page.soup
tags = html.find_all("b")
print(tags)