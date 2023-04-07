#export ISD_QUICK=1

STATION_IDS=`python3 ./station_ids.py config/stations_in.csv`

./mirror_isd.sh www $STATION_IDS

for STATION_ID in $STATION_IDS
do
    mkdir -p csv/$STATION_ID
    python3 isd_summary.py www csv $STATION_ID
done
