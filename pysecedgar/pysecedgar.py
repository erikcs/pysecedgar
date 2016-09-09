from __future__ import print_function
import collections
import re
import requests
import os
import io
from bs4 import BeautifulSoup
from urllib2 import urlopen

def make_dir(path):
    if not os.path.exists(path):
        os.makedirs(path)

def get_url(cik, formtype, start=0, count=40):

    url = ('https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany'
            '&CIK={}'
            '&type={}' 
            '&start={}'
            '&count={}'
            '&output=xml')
    
    return url.format(cik, formtype, start, count)

def get_linklist(cik, formtype, pagecount=40):

    links = collections.defaultdict(list)
    url = get_url(cik, formtype)
    soup = BeautifulSoup(urlopen(url), 'lxml')
    try:
        name = soup.find('name').string
        type = soup.find('type').string
    except:
        return None, None, links
    pagenum = pagecount

    while soup.find('filing') is not None:

        for f in soup.find_all('filing'):
            links[f.find('datefiled').string].append(
                re.sub('-index.*$', '.txt', f.find('filinghref').string)
            )
        url = get_url(cik, formtype, start=pagenum)
        soup = BeautifulSoup(urlopen(url), 'lxml')
        pagenum += pagecount
    
    return name, type, links

def download_files(cik, formtype, bpath=os.getcwd()):

    name, type, links = get_linklist(cik, formtype)
    nfiles = 0

    for date in links:
        path = bpath + '/' + type + '/' + name + '/' + date
        make_dir(path)
        for url in links[date]:
            filing = requests.get(url).text
            fpath = path + '/' + os.path.basename(url)
            with io.open(fpath, 'w', encoding='utf-8') as f:
                f.write(filing)
            print("Retrieved", fpath) 
            nfiles += 1

    print("Retrieved ", nfiles, " files for CIK: ",  cik)
    
if __name__ == '__main__':
    # Download all N-PX filings for Profunds and Charles Schwab
    ciks = ['0001039803', '0001454889'] 
    formtype = 'n-px' 
    for cik in ciks:
        download_files(cik, formtype)

    # Download all 10-K filings for Apple
    download_files('0000320193', '10-k')

