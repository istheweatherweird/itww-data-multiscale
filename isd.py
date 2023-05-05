import sys
import utils

WWW_DIR = sys.argv[1]
OUT_DIR = sys.argv[2]
station_id = sys.argv[3]
old_station_id = utils.get_old_station_id(station_id)

df = utils.read_isd(WWW_DIR, station_id, old_station_id)
summary = utils.get_isd_summary(df)
utils.write_isd_summary(summary, OUT_DIR + "/" + station_id)
