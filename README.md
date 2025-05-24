# itww-data-multiscale

This repository builds (and hosts) two sets of CSV files, in the `csv` subdirectory:

 - `isd`: historic temperature records. Contains a subdirectory for each weather station. That subdirectory contains a file for each day of the year, e.g. 0101.csv for January 1st.
 - `latest`: latest temperature records. Contains one file for each weather station.

Each dataset is structured with a subdirectory for each station. The isd data has a file for each hour of each day. 
The website www.istheweatherweird.com compares `latest` to `isd` to assess how weird the weather is right now.

The process to build these datasets using GitHub actions is as follows:

1) On one schedule (daily) the ISD data is updated by `isd.sh` which entails:
   - `mirror_isd.sh`: Mirroring NOAA's ISD ftp data for the desired stations (specified by `config/stations_in.csv`)
   - `isd.py`: Process the data associated with each station
2) On another schedule (hourly) the latest temperatures records are updated using `latest.sh` which entails:
   - `mirror_isd.sh`: (with the `ISD_LATEST=1` flag) download just the last two years of ISD data
   - `latest.py`: Process the last two years of ISD data in conjunction with the latest data from the NOAA weather API
  
In both cases we produce data at four resolutions: hourly, daily, weekly, monthly, and yearly.
