

import os
import requests
from urllib.parse import urlparse
from bs4 import BeautifulSoup
from saveFullHtmlPage import saveFullHtmlPage

sitemap = 'https://w.gitcoin.co/sitemap.xml'
outputDir = '/usr/src/app/tmp'

# Ensure the output directory exists
os.makedirs(outputDir, exist_ok=True)

wunder = requests.get(sitemap)
parcala = BeautifulSoup(wunder.content, "xml")
urls_from_xml = []
loc_tags = parcala.find_all('loc')
kwargs = {'bypass_robots': True}

for loc in loc_tags:
    urls_from_xml.append(loc.get_text()) 
    # page = loc.get_text().rsplit('/', 1)[-1]

    path = urlparse(loc.get_text()).path
    
    print('page: ' + path)
    
    os.makedirs(outputDir + path, exist_ok=True)
    saveFullHtmlPage(loc.get_text(), outputDir + path)


