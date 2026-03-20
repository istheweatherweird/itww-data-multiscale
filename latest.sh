# get the latest weather (and summaries)
# combines a quick mirror of GHCNh (last 2 years) with latest observations from the NOAA API

STATION_IDS=`python3 ./station_ids.py csv/stations.csv`

echo $STATION_IDS

ITWW_LATEST=1 ./mirror_ghcnh.sh www $STATION_IDS

mkdir -p csv/latest

for STATION_ID in $STATION_IDS
do
    echo "Processing station $STATION_ID"
    python3 latest.py www csv/latest $STATION_ID csv/stations.csv
done
