# itww-data-multiscale

This repository builds (and hosts) two sets of CSV files, in the `csv` subdirectory:

 - `ghcnh`: historic temperature records. Contains a subdirectory for each weather station. That subdirectory contains a file for each day of the year, e.g. 0101.csv for January 1st.
 - `latest`: latest temperature records. Contains one file for each weather station.

The website www.istheweatherweird.com compares `latest` to `isd` to assess how weird the weather is right now.

The process to build these datasets using GitHub actions is as follows:

1) On one schedule (daily) the GHCNh data is updated by `ghcnh.sh` which entails:
   - `mirror_ghnch.sh`: Mirroring NOAA's GHCNh http data for the desired stations (specified by `config/stations_in.csv`)
   - `ghcnh.py`: Process the data associated with each station
2) On another schedule (hourly) the latest temperatures records are updated using `latest.sh` which entails:
   - `mirror_ghcnh.sh`: (with the `ITWW_LATEST=1` flag) download just the last two years of GHCNh data
   - `latest.py`: Process the last two years of GHCNh data in conjunction with the latest data from the NOAA weather API
  
In both cases we produce data at four resolutions: hourly, daily, weekly, monthly, and yearly.
