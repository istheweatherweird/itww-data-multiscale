./mirror_isd.sh www `python ./station_ids.py config/stations_in.csv`

#rm -f pipe0
#mkfifo pipe0
#./isd2csv.sh www > pipe0 & psql -1f isd2psql.sql
#rm pipe0
