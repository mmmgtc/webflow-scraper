import os, sys, re
import requests
from urllib.parse import urljoin
from bs4 import BeautifulSoup

def saveFullHtmlPage(url, pagepath='page', session=requests.Session(), html=None):
    """Save web page html and supported contents        
        * pagepath : path-to-page   
        It will create a file  `'path-to-page'.html` and a folder `'path-to-page'_files`
    """
    def savenRename(soup, pagefolder, session, url, tag, inner):
        if not os.path.exists(pagefolder): # create only once
            os.mkdir(pagefolder)
        for res in soup.findAll(tag):   # images, css, etc..
            if res.has_attr(inner): # check inner tag (file object) MUST exists  
                try:
                    filename, ext = os.path.splitext(os.path.basename(res[inner])) # get name and extension
                    filename = re.sub('\W+', '', filename) + ext # clean special chars from name
                    fileurl = urljoin(url, res.get(inner))
                    filepath = os.path.join(pagefolder, filename)
                    # rename html ref so can move html and folder of files anywhere
                    res[inner] = os.path.join(os.path.basename(pagefolder), filename)
                    if not os.path.isfile(filepath): # was not downloaded
                        with open(filepath, 'wb') as file:
                            filebin = session.get(fileurl)
                            file.write(filebin.content)
                except Exception as exc:
                    print(exc, file=sys.stderr)
    if not html:
        sessionData = session.get(url)
        sessionData.encoding = 'utf-8'
        html = sessionData.text
    soup = BeautifulSoup(html, "html.parser")
    path, _ = os.path.splitext(pagepath)
    pagefolder = path+'/assets' # page contents folder
    tags_inner = {'img': 'src', 'link': 'href', 'script': 'src'} # tag&inner tags to grab
    for tag, inner in tags_inner.items(): # saves resource files and rename refs
        savenRename(soup, pagefolder, session, url, tag, inner)
    with open(path+'/index.html', 'wb') as file: # saves modified html doc
        file.write(soup.prettify('utf-8'))