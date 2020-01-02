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
        r = requests.get(self.url, **self.kwargs)
        with p.open('wb') as f:
            f.write(r.content)


def proficient(subject: str, year: int) -> Download:
    years = f'{year - 1}-{year % 100}'
    url = f'https://www2.ed.gov/about/inits/ed/edfacts/data-files/{subject}-achievement-lea-sy{years}.csv'
    # ed.gov does not send the full certificate chain, so I had to build it
    # myself.
    return Download(
        url,
        filename=f'data/{subject}{year}.csv',
        verify='SectigoRSADomainValidationSecureServerCA.pem'
    )


logging.basicConfig(level=logging.INFO)
Path('data').mkdir(exist_ok=True)
math2017 = proficient('math', 2017)
math2017.download()
read2017 = proficient('rla', 2017)
read2017.download()
