from urllib import request
from bs4 import BeautifulSoup
import re
import os
import wget
import urllib3
import shutil




headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) ' 
                      'AppleWebKit/537.11 (KHTML, like Gecko) '
                      'Chrome/23.0.1271.64 Safari/537.11',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
        'Accept-Encoding': 'none',
        'Accept-Language': 'en-US,en;q=0.8',
        'Connection': 'keep-alive'}


regex_domain=r'(https?:\/\/(?:www\.|(?!www))[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.[^\s]{2,}|www\.[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.[^\s]{2,}|https?:\/\/(?:www\.|(?!www))[a-zA-Z0-9]+\.[^\s]{2,}|www\.[a-zA-Z0-9]+\.[^\s]{2,})'

urls_file=open('urls.txt').readlines()

def scrap_all(urls_file):
    dict_urls={}
    for url in urls_file:
        url=re.sub(r'\n','',url)
        dict_urls[url]=list(filter(None, scrap_urls(url))) 
    return dict_urls

def scrap_urls(url):
    urls_list=[]
    if(re.match(r'^http[s]?:\/\/',str(url))):
        print("\n\n------------ Getting Urls from :  "+url)
        request_ok=request.Request(url=url, headers=headers)
        response = request.urlopen(request_ok).read()
        soup= BeautifulSoup(response, "html.parser")
        links_list=soup.find_all('a', href=True)
        for l in links_list:
           urls_list.append(l['href'])
        
        return build_multiple_urls(url,list(filter(None, urls_list)))
    else:
         print('ERROR')
         return []

 
def build_url(domain,url):
    url=str(url)
    if not url.startswith('#'):
        if url.startswith('/'):
            if(domain.endswith(r'\/')):
                url=re.sub(r'\/','',url)
            return re.sub(r'\n','',str(str(domain)+url))
        if str(url).startswith('https') or str(url).startswith('http'):
            return str(url)


def build_multiple_urls(domain,urls):
    
    return list(set([build_url(domain,url) for url in urls]))

def download_doc(domain,url):
  
    doc_name=re.sub(r'.+?\/+','',url)
    domain_name=re.sub(r'.+?\/+','',domain)
    print("--- Downloading : "+ doc_name)
    try:
        # Create target Directory
        os.mkdir('download')
        print("Directory " , 'download' ,  " Created ") 
    except FileExistsError:
        print("Directory " , 'download' ,  " already exists")      
    try:
        # Create target Directory
        os.mkdir('download'+'/'+domain_name)
        print("Directory " , 'download'+'/'+domain_name ,  " Created ") 
    except FileExistsError:
        print("Directory " , 'download'+'/'+domain_name ,  " already exists")
    http = urllib3.PoolManager()

    with http.request('GET',url, preload_content=False) as resp, open('download'+'/'+domain_name+'/'+doc_name, 'wb') as out_file:
        shutil.copyfileobj(resp, out_file)

    resp.release_conn()
    #request.urlretrieve(url, domain_name+'/'+doc_name)
    #wget.download(url,out=domain_name)


def downlaod_docs(url,docs):
    
    if (url.endswith('.pdf')):
        download_doc(url,url)
    else:
        print("\n\n------- Gettings doc from  :  "+url)
        for doc in docs:
            #print("\n\n------- Gettings doc from  :  "+doc)
            if (doc.endswith('.pdf')):
                print('okokok')
                download_doc(url,doc)
            


def main(urls_file,rec=0):
    list_links=scrap_all(urls_file)
    for key,value in list_links.items():
        downlaod_docs(key,value)
        if rec==1:
            print('---------------- 2 eme couche -----------------------')
            list_links_rec=scrap_all(value)
            for key_rec,value_rec in list_links_rec.items():
                downlaod_docs(key_rec,value_rec)


        
main(urls_file,1)
