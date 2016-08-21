
"""
Extracts data from a file that looks like:

series_id   year    period  value   footnote_codes
LAUCN010010000000003            1990    M01          6.4
LAUCN010010000000003            1990    M02          6.6
"""

import argparse
from csvkit import DictReader, DictWriter
from loggy import loggy
from sys import stdout

LOGGY = loggy('extract_county_unemployment')


if __name__ == '__main__':
    parser = argparse.ArgumentParser("Extracts county-level unemployment data from <infile>")
    parser.add_argument('infile', type=argparse.FileType('r'))
    args = parser.parse_args()
    infile = args.infile
    csvout = DictWriter(stdout, fieldnames=['fips', 'area_type', 'year', 'month', 'unemployment_rate'])

    LOGGY.info("Reading: %s" % infile.name)
    for r in DictReader(infile, delimiter="\t"):
        row = {k: v.strip() for k, v in r.items()}
        seriesid = row['series_id']
        if seriesid[3:5] == 'CN' and seriesid[-2:] == '03':
            newrow = {'fips': seriesid[5:10],
                      'area_type': 'County',
                      'year': row['year'],
                      'month': row['period'][1:], # ignore 'M'
                      'unemployment_rate': row['value'],
                      }
            csvout.writerow(newrow)

