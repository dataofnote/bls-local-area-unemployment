from lxml import html as htmlparse
from datetime import datetime
from pathlib import Path
from pytz import timezone
from sys import argv
from urllib.parse import urljoin
import re
import requests

from loggy import loggy
myloggy = loggy('fetch_data.py')

SRC_TIME_ZONE = timezone('US/Eastern')
SRC_TIMESTAMP_FMT = '%m/%d/%Y %I:%M %p'
LANDING_PAGE_URL = 'http://download.bls.gov/pub/time.series/la/'


def gather_directory_listing():
    resp = requests.get(LANDING_PAGE_URL)
    doc = htmlparse.fromstring(resp.text)

    # <pre>
    #  8/19/2016 10:25 AM    136552044  <a href="...">la.data.0.CurrentU00-04</a>
    # </pre>
    texts = doc.xpath('//pre/text()')
    hrefs =  doc.xpath('//pre/a/@href')[1:] # skip the link for [To Parent Directory]

    rows = []
    for txt, href in zip(texts, hrefs):
        if re.search('\d+ *$', txt):
            ts, filesize = re.search(r'(.+? [AP]M) +(\d+) *$', txt.strip()).groups()
            timestamp = datetime.strptime(re.sub(r'\s+', ' ', ts).strip(), SRC_TIMESTAMP_FMT)
            url = urljoin(LANDING_PAGE_URL, href)
            rows.append((url, SRC_TIME_ZONE.localize(timestamp)))

    return rows


def check_filestamp(dest_path, timestamp):
    """
    Returns none if dest_path does not exist
    Positive number if dest_path's modtime is newer than timestamp
    Negative number otherwise

    # because of how ******* ridiculously complicated it is
    # to get timezone of current machine, we'll just pretend we
    # live in Greenwich. No big harm
    """
    if not dest_path.exists():
        return None

    else:
        return dest_path.stat().st_mtime - timestamp


if __name__ == '__main__':
    dest_dir = Path(argv[1])
    if not dest_dir.is_dir():
        raise IOError("First argument must be a valid directory name.")

    myloggy.info("Fetching: %s" % LANDING_PAGE_URL)
    for url, ts in gather_directory_listing():
        dest_path = dest_dir / Path(url).name
        xc = check_filestamp(dest_path, ts.timestamp())
        if xc is None or xc < 0:
            if xc is None:
                myloggy.info("Downloading (first time): %s" % url)
            else:
                myloggy.info("Downloading (%s hours out-of-date): %s" % (round(abs(xc) / (3600), 1), url))
            resp = requests.get(url)
            if resp.status_code == 200:
                dest_path.write_text(resp.text)
            else:
                raise RuntimeError("Received status code %s" % resp.status_code)
        else:
            myloggy.info("Up-to-date (last updated: %s): %s" % (ts.isoformat(), url))
