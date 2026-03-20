import pandas as pd
import sys

stations = pd.read_csv(sys.argv[1], dtype=str)

print(stations.GHCN_ID.str.cat(sep=" "))
