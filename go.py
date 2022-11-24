import os
import requests
from urllib.parse import urlparse
from bs4 import BeautifulSoup
from saveFullHtmlPage import saveFullHtmlPage
from dotenv import load_dotenv
import time

load_dotenv()

sitemaps = os.getenv('SITEMAP_URLS').split(',')

outputDir = '/usr/src/app/output'
# Ensure the output directory exists
os.makedirs(outputDir, exist_ok=True)

for sitemap in sitemaps:
    print('Processing sitemap: ' + sitemap)

    wunder = requests.get(sitemap)
    parcala = BeautifulSoup(wunder.content, "xml")
    urls_from_xml = []
    loc_tags = parcala.find_all('loc')
    kwargs = {'bypass_robots': True}

    counter = -1
    for loc in loc_tags:
        counter += 1
        urls_from_xml.append(loc.get_text()) 
        # page = loc.get_text().rsplit('/', 1)[-1]

        path = urlparse(loc.get_text()).path
        
        print('Page: ' + path)
        
        os.makedirs(outputDir + path, exist_ok=True)
        saveFullHtmlPage(loc.get_text(), outputDir + path)

        if counter > int(os.getenv('CRAWLING_PAUSE_EVERY_NTH_REQUEST')) and (counter % int(os.getenv('CRAWLING_PAUSE_EVERY_NTH_REQUEST'))) == 0:
            print('Pausing for ' + os.getenv('CRAWLING_PAUSE_IN_SECONDS') + ' seconds')
            time.sleep(int(os.getenv('CRAWLING_PAUSE_IN_SECONDS')))
