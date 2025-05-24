# fully mirror the ISD data and generate summary CSVs
STATION_IDS=`python3 ./station_ids.py config/stations_in.csv`

echo "Downloading ISD database"

./mirror_isd.sh www $STATION_IDS

echo "Processing ISD database into day-of-year CSVs"

STATION_IDS=`python3 ./station_ids.py config/stations_in.csv --primary`
for STATION_ID in $STATION_IDS
do
    echo "Processing Station ID" $STATION_ID
    mkdir -p csv/isd/$STATION_ID
    python3 isd.py www csv/isd $STATION_ID
done
