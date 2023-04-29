# fully mirror the ISD data and generate summary CSVs
STATION_IDS=`python3 ./station_ids.py config/stations_in.csv`

./mirror_isd.sh www $STATION_IDS

for STATION_ID in $STATION_IDS
do
    mkdir -p csv/isd/$STATION_ID
    python3 isd_summary.py www csv/isd $STATION_ID
done
