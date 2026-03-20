import utils
import sys
import pandas as pd

WWW_DIR = sys.argv[1]
OUT_DIR = sys.argv[2]
station_id = sys.argv[3]

df_ghcnh = utils.read_ghcnh_parquet(WWW_DIR, station_id)

ICAO = utils.get_ICAO(station_id)
last_ghcnh_timestamp = df_ghcnh.sort_index().index[-1]
df_latest = utils.get_latest(ICAO, last_ghcnh_timestamp - pd.Timedelta(1, "h"))
print(df_latest)

df = utils.combine_ghcnh_latest(df_ghcnh, df_latest)
print(df)

summary = utils.get_latest_summary(df)
summary.temp = summary.temp.round(1)

summary.to_csv(OUT_DIR + "/" + station_id + ".csv", index=False)
