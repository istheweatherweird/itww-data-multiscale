import pandas as pd
import sys
import os

stations_in = pd.read_csv(sys.argv[1], dtype=str)

if "ISD_QUICK" in os.environ.keys():
    stations_in = stations_in.head(1)

ids = stations_in.USAF + "-" + stations_in.WBAN

if "ISD_LATEST" not in os.environ.keys():
    ids2 = stations_in.USAF2 + "-" + stations_in.WBAN2
    ids = pd.concat([ids, ids2]).dropna()

print(str.join(" ", ids))
