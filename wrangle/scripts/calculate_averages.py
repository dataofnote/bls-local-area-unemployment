import argparse
from loggy import loggy
import pandas as pd
from sys import stdout

LOGGY = loggy('calculate_averages')

if __name__ == '__main__':
    parser = argparse.ArgumentParser("Averages unemployment rate. Expects an `unemployment_rate` (or seasonally adjusted) field")
    parser.add_argument('infile', type=argparse.FileType('r'))
    parser.add_argument('--seasonal', action='store_true', help="A flag to set the unemployment_rate header to seasonally_adjusted_unemployment_rate")
    args = parser.parse_args()
    unemp_header = "seasonally_adjusted_unemployment_rate" if args.seasonal else "unemployment_rate"
    df = pd.read_csv(args.infile, dtype={'fips': str})

    gdf = df.groupby(['fips', 'area_type', 'year']).mean().round(1)

    rdf = gdf.reset_index()[['fips', 'area_type', 'year', unemp_header]]
    rdf.rename(columns = {unemp_header: 'average_' + unemp_header}, inplace=True)
    rdf.sort_values(['fips', 'year'], inplace=True)
    stdout.write(rdf.to_csv(index=False))
