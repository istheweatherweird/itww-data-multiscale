# merge custom stations_in.csv with isd-history.csv from noaa ftp and airport codes
import pandas as pd
import sys

stations_in = pd.read_csv(sys.argv[1], dtype='str')
ghcnh_stations = pd.read_csv("https://www.ncei.noaa.gov/oa/global-historical-climatology-network/hourly/doc/ghcnh-station-list.csv", dtype='str')
airports = pd.read_csv(sys.argv[2], dtype='str', header=None)

stations = stations_in.merge(ghcnh_stations, on=['ICAO'])

airports.rename(columns={5:'ICAO', 11:'TZ'}, inplace=True)
stations = stations.merge(airports[['ICAO', 'TZ']],
               how='left', on='ICAO')

stations.to_csv(sys.stdout, index=False)

