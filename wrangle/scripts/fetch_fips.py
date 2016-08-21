"""overly complicated script to get FIPS lookups"""
from loggy import loggy
from sys import stdout
import requests

SRC_URL = 'http://data.bls.gov/cew/doc/titles/area/area_titles.csv'
LOGGY = loggy('fetch_fips')

if __name__ == '__main__':
    LOGGY.info("Downloading: %s" % SRC_URL)
    resp = requests.get(SRC_URL)
    stdout.write(resp.text)

