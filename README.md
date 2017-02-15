Download *all* available files for a given filing type (for a company identified by its CIK code)

##### Installation
`$ pip install git+https://github.com/nuffe/pysecedgar.git`

##### Usage
`download_files(cik, formtype, basedir)`

`cik`: CIK key(s) (string, list, or tuple)

`formtype`: SEC form type(s) (string, list, or tuple). For example: `'10-K'`, `'10-Q'`, `'13-F'`, etc.

`basedir`: base directory for storing downloaded files (string), default: working directory

Files are stored as `basedir/formtype/company name/cik/date/`

#### Example
```python
from pysecedgar import download_files

# Download all N-PX filings for Profunds and Charles Schwab
# and save them in the current working directory
ciks = ['0001039803', '0001454889']
formtype = 'n-px'
download_files(ciks, formtype)

# Download all 10-K and 10-Q filings for Apple
download_files('0000320193', ['10-k', '10-Q'])
```

#### Misc
On [WRDS](https://wrds-web.wharton.upenn.edu/wrds/index.cfm?) the `FUNDA` table in the Compustat library (`COMP`) contains some handy identifiers (`CIK`, `Ticker`, `gvkey`, etc)

```SQL
SELECT DISTINCT(conm), cik, cusip, tic, gvkey, fyear from COMP.FUNDA
```

downloads a [table](https://www.dropbox.com/s/6ahl8h4u39nhdi7/keys.csv?dl=0) of these identifiers.

#### How
Works by constructing the appropriate `https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany` "query", then using Beautiful Soup to find each filing's link on the resulting page. Inspiration from various sources on the internet.

#### Todo
Specify date range
