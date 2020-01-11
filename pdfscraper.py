from urllib import request
from bs4 import BeautifulSoup
import re
import os
import wget


headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.3'}


regex_domain=r'(https?:\/\/(?:www\.|(?!www))[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.[^\s]{2,}|www\.[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.[^\s]{2,}|https?:\/\/(?:www\.|(?!www))[a-zA-Z0-9]+\.[^\s]{2,}|www\.[a-zA-Z0-9]+\.[^\s]{2,})'

urls_file=open('urls.txt').readlines()

def scrap_all(urls_file):
    dict_urls={}
    for url in urls_file:
        dict_urls[url]=scrap_urls(url)
    return dict_urls

def scrap_urls(single_url):
    urls_list=[]
    if(re.match(r'^http[s]?:\/\/',str(single_url))):
        print("\n\n------------ Getting Urls from :  "+single_url)
        request_ok=request.Request(url=single_url, headers=headers) 
        response = request.urlopen(request_ok).read()
        soup= BeautifulSoup(response, "html.parser")
        links_list=soup.find_all('a', href=True)
        for l in links_list:
           urls_list.append(l['href'])
        
        return build_multiple_urls(single_url,urls_list)
    else:
         print('ERROR')
         return []

def build_single_url(domain,url):
    if not str(url).startswith('#'):
        if str(url).startswith('/'):
            return str(str(domain)+str(url))
        if str(url).startswith('https') or str(url).startswith('http'):
            return str(url)

    print('error with : '+str(url))


def build_multiple_urls(domain,urls):
    
    return list(set([build_single_url(domain,url) for url in urls]))

def extract_domain(url):

    domain=re.findall(regex_domain,str(url))

    return domain


def main(urls_file):
    print(scrap_all(urls_file))

main(urls_file)