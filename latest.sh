# get the latest weather (and summaries)
# combines a quick mirror of ISD (last 2 years) with latest observations from the NOAA API

STATION_IDS=`python3 ./station_ids.py config/stations_in.csv --primary`

echo $STATION_IDS

ISD_LATEST=1 ./mirror_isd.sh www $STATION_IDS

mkdir -p csv/latest

for STATION_ID in $STATION_IDS
do
    python3 latest.py www csv/latest $STATION_ID csv/stations.csv
done
