import pandas as pd
import sys

stations_in = pd.read_csv(sys.argv[1], dtype=str)
ids1 = stations_in.USAF + "-" + stations_in.WBAN
ids2 = stations_in.USAF2 + "-" + stations_in.WBAN2
ids = pd.concat([ids1, ids2]).dropna()
print(str.join(" ", ids))
