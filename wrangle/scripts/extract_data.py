
"""
Extracts data from a file that looks like:

series_id   year    period  value   footnote_codes
LAUCN010010000000003            1990    M01          6.4
LAUCN010010000000003            1990    M02          6.6
LAUCN010010000000006            1990    M02          -
"""

import argparse
from csvkit import DictReader, DictWriter
from loggy import loggy
from sys import stdout

LOGGY = loggy('extract_data')

AREA_TYPES_MAP = {
    'CN': 'County',
    'ST': 'State'
}

if __name__ == '__main__':
    parser = argparse.ArgumentParser("Extracts county/state-level unemployment data from <infile>")
    parser.add_argument('infile', type=argparse.FileType('r'))
    parser.add_argument('--seasonal', action='store_true', help="A flag to set the unemployment_rate header to seasonally_adjusted_unemployment_rate")
    args = parser.parse_args()
    infile = args.infile
    unemp_header = "seasonally_adjusted_unemployment_rate" if args.seasonal else "unemployment_rate"
    LOGGY.info("Reading: %s" % infile.name)
    d = {}
    for r in DictReader(infile, delimiter="\t"):
        row = {k: v.strip() for k, v in r.items()}
        seriesid = row['series_id']
        areatype = AREA_TYPES_MAP.get(seriesid[3:5])
        valtype = seriesid[-2:]
        if areatype and valtype in ['03', '06']:
            fips = seriesid[5:7] if areatype == 'State' else seriesid[5:10]
            year = row['year']
            month = row['period'][1:]
            key = (fips, year, month)
            if not d.get(key):
                d[key] = {
                    'fips': fips,
                    'area_type': areatype,
                    'year': year,
                    'month': month,
                }
            v = unemp_header if valtype == '03' else 'labor_force'
            d[key][v] = None if row['value'] == '-' else row['value']

    csvout = DictWriter(stdout, fieldnames=['fips', 'area_type', 'year', 'month', unemp_header, 'labor_force'])
    csvout.writeheader()
    for k, row in sorted(d.items(), key=lambda x: x[0]):
        csvout.writerow(row)

