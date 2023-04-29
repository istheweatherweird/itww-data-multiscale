import utils
import sys
import pandas as pd

WWW_DIR = sys.argv[1]
OUT_DIR = sys.argv[2]
station_id = sys.argv[3]
stations = pd.read_csv(sys.argv[4], dtype=str)

df_isd = utils.read_isd(WWW_DIR, station_id)

ICAO = utils.get_ICAO(station_id, stations)
last_isd_timestamp = df_isd.sort_index().index[-1]
df_latest = utils.get_latest(ICAO, last_isd_timestamp - pd.Timedelta(1, "H"))

df = utils.combine_isd_latest(df_isd, df_latest)

summary = utils.get_latest_summary(df)
summary.temp = summary.temp.round(1)

summary.to_csv(OUT_DIR + "/" + station_id + ".csv", index=False)
