# fully mirror the ISD data and generate summary CSVs
STATION_IDS=`python3 ./station_ids.py csv/stations.csv`

echo "Downloading GHCNh parquet database"
./mirror_ghcnh.sh www $STATION_IDS

echo "Processing GHCNh database into day-of-year CSVs"

for STATION_ID in $STATION_IDS
do
     echo "Processing Station ID" $STATION_ID
     mkdir -p csv/ghcnh/$STATION_ID
     python3 ghcnh.py www csv/ghcnh $STATION_ID
done