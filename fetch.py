"""A script to fetch all the data for this analysis."""

import logging
from pathlib import Path
import urllib.parse

import requests


class Download:

    def __init__(
        self, url: str, directory: str = '.', filename=None, **kwargs
    ) -> None:
        # Throw if URL is invalid.
        purl = urllib.parse.urlparse(url)
        if filename is None:
            filename = Path(purl.path).name
        self.url = url
        self.directory = directory
        self.filename = filename
        self.kwargs = kwargs

    def download(self, force: bool = False):
        p = Path(self.directory, self.filename)
        if not force and p.is_file():
            logging.info(f'file exists: {self.filename}')
            return
        logging.info(f'download: {self.url}')
        r = requests.get(self.url, **self.kwargs)
        with p.open('wb') as f:
            f.write(r.content)


class Data:

    def __init__(self, directory='data'):
        self.directory = directory

    def proficient(self, subject: str, year: int) -> Download:
        years = f'{year - 1}-{year % 100}'
        url = f'https://www2.ed.gov/about/inits/ed/edfacts/data-files/{subject}-achievement-lea-sy{years}.csv'
        # ed.gov does not send the full certificate chain, so I had to build it
        # myself.
        return Download(
            url,
            filename=f'{self.directory}/{subject}{year}.csv',
            verify='SectigoRSADomainValidationSecureServerCA.pem'
        )

    def graduation(self, year: int) -> Download:
        years = f'{year - 1}-{year % 100}'
        url = f'https://nces.ed.gov/ccd/tables/xls/ACGR_RE_Characteristics_{years}.xlsx'
        # TODO: Convert XLS to CSV.
        return Download(url, filename=f'{self.directory}/grad{year}.csv')

    # College Admissions Test
    def cat_tx(self, test: str, year: int) -> Download:
        url = f'https://tea.texas.gov/acctres/{test}_district_data_class_{year}'
        return Download(url, filename=f'{self.directory}/{test}-{year}-tx.csv')

    def download(self):
        Path(self.directory).mkdir(exist_ok=True)
        math2017 = self.proficient('math', 2017)
        math2017.download()
        read2017 = self.proficient('rla', 2017)
        read2017.download()
        grad2017 = self.graduation(2017)
        grad2017.download()
        sat2017tx = self.cat_tx('sat', 2017)
        sat2017tx.download()
        act2017tx = self.cat_tx('act', 2017)
        act2017tx.download()


logging.basicConfig(level=logging.INFO)
data = Data()
data.download()
