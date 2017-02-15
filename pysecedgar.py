import collections
import re
import requests
import os
import io
import logging
import pandas as pd
from bs4 import BeautifulSoup

logger = logging.getLogger('pysecedgar')
logging.basicConfig(level=logging.INFO)

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
    soup = BeautifulSoup(requests.get(url).content, 'lxml')
    try:
        name = soup.find('name').string
        type = soup.find('type').string
    except:
        return None, None, links
    pagenum = pagecount

    # setting `count` in get_url to some large number doesn't work, this
    # retrieves all the results no matter how many pages there are
    while soup.find('filing') is not None:

        for f in soup.find_all('filing'):
            links[f.find('datefiled').string].append(
                re.sub('-index.*$', '.txt', f.find('filinghref').string)
            )
        url = get_url(cik, formtype, start=pagenum)
        soup = BeautifulSoup(requests.get(url).content, 'lxml')
        pagenum += pagecount

    return name, type, links

def download_filings(cik, formtype, bpath):

    name, type, links = get_linklist(cik, formtype)
    log = []
    nfiles = 0

    for date in links:
        path = bpath + '/' + type + '/' + name + '/' + date
        make_dir(path)
        for url in links[date]:
            response = requests.get(url)
            fpath = path + '/' + os.path.basename(url)
            with io.open(fpath, 'w', encoding='utf-8') as f:
                f.write(response.text)
            logger.info("Retrieved {}".format(fpath))
            log.append([cik, name, date, formtype, fpath])
            nfiles += 1

    logger.info("Retrieved {0} files for CIK: {1}".format(nfiles, cik))

    return pd.DataFrame(log, columns=['cik', 'name', 'date',
                                      'formtype', 'fpath'])

def download_files(cik=None, formtype=None, basedir=os.getcwd()):
    """
    Usage ...

    Parameters
    ----------
        cik : str, list, or tuple
            The CIK key(s)
        formtype : str, list, or tuple
            The form type(s)
        basedir : str, optional
            Path to store downloaded files

    Returns
    ----------
        logdf : DataFrame
            DataFrame with information about everything retrieved

    """
    if cik is not None:
        if not isinstance(cik, (list, tuple)):
            cik = [cik]
        else:
            cik = list(cik)
    else:
        raise ValueError('cik(s) must be provided')

    if formtype is not None:
        if not isinstance(formtype, (list, tuple)):
            formtype = [formtype]
        else:
            formtype = list(formtype)
    else:
        raise ValueError('formtype(s) must be provided')

    logdf = []
    for c in cik:
        for f in formtype:
            logdf.append( download_filings(c, f, basedir) )

    return pd.concat(logdf)

if __name__ == '__main__':
    # Download all N-PX filings for Profunds and Charles Schwab
    ciks = ['0001039803', '0001454889']
    formtype = 'n-px'
    download_files(ciks, formtype)

    # Download all 10-K and 10-Q filings for Apple
    download_files('0000320193', ['10-k', '10-Q'])
