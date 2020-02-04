from urllib import request
import  urllib.error
from bs4 import BeautifulSoup
import re
import os
import ssl
from w3lib.url import safe_url_string
from socket import error as SocketError



os.environ['http_proxy']=''


ssl.match_hostname = lambda cert, hostname: True


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
    if(len(urls_file)!=0):
        for url in urls_file:
            url=re.sub(r'\n','',url)
            scrapped=scrap_urls(url)
            if len(scrapped)!=0:
                dict_urls[url]=list(filter(None, scrapped)) 
    return dict_urls

def scrap_urls(url):
    urls_list=[]
    url=re.sub(r'(\/\/)$','/',url)
    if(re.match(r'.+\.pdf',str(url))):
        return []
    if(re.match(r'^http[s]?:\/\/',str(url))):
        print("\n\n------------ Getting Urls from :  "+url)
        url = safe_url_string(url, encoding="utf-8")
        
        try:
            request_ok=request.Request(url=url, headers=headers)
            response = request.urlopen(request_ok).read()
            soup= BeautifulSoup(response, "html.parser")
            links_list=[]
            links_list=soup.find_all('a', href=True)
            if len(links_list)!=0:
                for l in links_list:
                    urls_list.append(l['href'])
            
            return build_multiple_urls(url,list(filter(None, urls_list)))

        except (urllib.error.HTTPError,urllib.error.URLError) as err:
            print(err)
            return []

       
    else:
         print('ERROR')
         return []

 
def build_url(domain,url):
    url=str(url)
    url=re.sub(r'(\/\/)$','/',url)
    domain=re.sub(r'(\/\/)$','/',domain)
    domain=re.sub(r'\n','',domain)
    if not url.startswith('#'):
        if url.startswith('/') or url.startswith('.'):
            if(domain.endswith('/')):
                domain=re.sub(r'(\/)$','',domain)
            url=re.sub(r'(\.)(\/)','/',url)
            return re.sub(r'\n','',str(str(domain)+url))
        if str(url).startswith('https') or str(url).startswith('http'):
            return str(url)


def build_multiple_urls(domain,urls):
    domain2=re.sub(r'(\.\w+)\/.+',r'\g<1>',domain)
    multiple_urls=list(set([build_url(domain,url) for url in urls]))
    multiple_urls2=list(set([build_url(domain2,url) for url in urls]))
    return set(multiple_urls+multiple_urls2)

def download_doc(domain,url):
    exist=0
    url=re.sub(r'(\/\/)$','/',url)
    doc_name=re.sub(r'.+?\/+','',url)
    domain_name=re.sub(r'^http[s]?:\/\/','',domain)
    if(re.match(r'\w+\.\w+\.',str(domain_name))):
        domain_name=re.sub(r'^(.+?\.)','',domain_name)
    domain_name=re.sub(r'\.\w{2,3}.+','',domain_name)
    
    folder_path='download'+'/'+domain_name
    doc_path=folder_path+'/'+doc_name
    
    print("--- Downloading : "+ doc_name)
    try:
        # Create target Directory
        os.mkdir('download')
        print("Directory " , 'download' ,  " Created ") 
    except FileExistsError:
        print("Directory " , 'download' ,  " already exists")
        exist=True      
    try:
        # Create target Directory
        os.mkdir(folder_path)
        print("Directory " , folder_path ,  " Created ") 
    except FileExistsError:
        print("Directory " , folder_path ,  " already exists")
    
    if(not os.path.isfile(doc_path)):
        #http = urllib3.PoolManager()
        print(url)

        
        try:
            url = safe_url_string(url, encoding="utf-8")
            '''with http.request('GET',url, preload_content=False, cert_reqs='CERT_NONE',
                                assert_hostname=False) as resp, open(doc_path, 'wb') as out_file:
                shutil.copyfileobj(resp, out_file)'''
            urllib.request.urlretrieve(url,doc_path)
        #except (urllib3.exceptions.HTTPError,urllib3.exceptions.MaxRetryError) as err:
            #print(err)
        except (urllib.error.HTTPError,urllib.error.URLError,SocketError) as err:
            print(err)


        #resp.release_conn()
    else:
        print(doc_name+' already exists')
            

def downlaod_docs(url,docs):
    if (url.endswith('.pdf')):
        download_doc(url,url)
    else:
        print("\n\n------- Gettings docs from  :  "+url)
        
        for doc in docs:
            #print("\n\n------- Gettings doc from  :  "+doc)
            if (doc.endswith('.pdf')):
                download_doc(url,doc)
            


def main(urls_file,rec=0):
    visited_links=[]
    list_links=scrap_all(urls_file)
    for key,value in list_links.items():
        if key not in visited_links:
            downlaod_docs(key,value)
            visited_links.append(key)
        if rec==1:
            print('---------------- step 2 -----------------------')
            list_links_rec=scrap_all(value)
            for key_rec,value_rec in list_links_rec.items():
                if key_rec not in visited_links:
                    downlaod_docs(key_rec,value_rec)
                    visited_links.append(key_rec)


        
main(urls_file,1)

