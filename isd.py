import sys
import utils

WWW_DIR = sys.argv[1]
OUT_DIR = sys.argv[2]
station_id = sys.argv[3]

df = utils.read_isd(WWW_DIR, station_id)
summary = utils.get_isd_summary(df)
utils.write_isd_summary(summary, OUT_DIR + "/" + station_id)
