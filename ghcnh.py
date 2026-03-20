import sys
import utils

WWW_DIR = sys.argv[1]
OUT_DIR = sys.argv[2]
station_id = sys.argv[3]

df = utils.read_ghcnh_parquet(WWW_DIR, station_id)
summary = utils.get_ghcnh_summary(df)
utils.write_ghcnh_summary(summary, OUT_DIR + "/" + station_id)