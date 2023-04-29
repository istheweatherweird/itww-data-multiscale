# merge custom stations_in.csv with isd-history.csv from noaa ftp and airport codes
import pandas as pd
import sys

stations_in = pd.read_csv(sys.argv[1], dtype='str')
isd_history = pd.read_csv("ftp://ftp.ncdc.noaa.gov/pub/data/noaa/isd-history.csv", dtype='str')
airports = pd.read_csv(sys.argv[2], dtype='str', header=None)

stations = stations_in.merge(isd_history, on=['USAF','WBAN'])

airports.rename(columns={5:'ICAO', 11:'TZ'}, inplace=True)
stations = stations.merge(airports[['ICAO', 'TZ']],
               how='left', on='ICAO')

stations.to_csv(sys.stdout, index=False)

