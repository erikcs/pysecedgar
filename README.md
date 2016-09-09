Download *all* available files for a given filing type.

##### Installation
`$pip install git+https://github.com/nuffe/pysecedgar.git`

##### Usage
`download_files(cik, formtype, basedir)`

*cik*: CIK key (string)

*formtype*: SEC form type (string), '10-K', '10-Q', '13-F', etc.

*basedir*: base directory for storing downloaded files (string), default: working directory

#### Example
```
from pysecedgar import download_files

# Download all N-PX filings for Profunds and Charles Schwab
# and save them in the current working directory
ciks = ['0001039803', '0001454889']
formtype = 'n-px'
for cik in ciks:
    download_files(cik, formtype)

# Download all 10-K filings for Apple
download_files('0000320193', '10-k')
```
