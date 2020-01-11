from urllib import request
from bs4 import BeautifulSoup
import re
import os
import wget


headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.3'}
single_url='https://www.pdfdrive.com/'

def scrap_urls(single_url):
    urls_list=[]
    if(re.match(r'^http[s]?:\/\/',str(single_url))):
        print("\n\n------------ Scraping :  "+single_url)
        request_ok=request.Request(url=single_url, headers=headers) 
        response = request.urlopen(request_ok).read()
        soup= BeautifulSoup(response, "html.parser")
        links_list=soup.find_all('a', href=True)
        for l in links_list:
           urls_list.append(l['href'])
        return urls_list
    else:
         print('ERROR')

def build_url(url):
    if not str(url).startswith('#'):
        print('--------------ok'+url)

    return 

urls_result=scrap_urls(single_url)

for url in urls_result:
    print(url)
    build_url(url)

