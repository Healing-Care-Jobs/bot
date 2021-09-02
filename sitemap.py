import requests as req
from bs4 import BeautifulSoup
import json
import html
import re
import datetime
import xml.sax.saxutils as saxutils

f = open('sitemap-raw.txt', 'r')
parent = "https://healthcareokay.com"
page_html = f.read()
# print(page_html)
soup = BeautifulSoup(page_html, "lxml")
sitemap = []
for a in soup.find_all('a', href=True):
    link = a['href']
    link = link.replace('&', '&amp;')
    if link.startswith('https://healthcareokay.com') == False:
        link = parent + link
    sitemap.append(link)

# print(len(sitemap))
sitemap = list(dict.fromkeys(sitemap))

map = ['<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.sitemaps.org/schemas/sitemap/0.9 http://www.sitemaps.org/schemas/sitemap/0.9/sitemap.xsd">']

for mp in sitemap:
    dd = datetime.datetime.now().strftime ("%Y-%m-%d")
    dt = datetime.datetime.now().strftime ("%H:%M:%S%z")
    df = str(dd) + 'T' + str(dt)
    entry = '<url><loc>' + mp + '</loc><lastmod>' + df + '</lastmod><priority>0.8</priority></url>'
    map.append(entry)
map.append('</urlset>')
store = open('sitemap.xml', 'w')
store.write(''.join(map))

# print(sitemap)
# print(len(sitemap))



