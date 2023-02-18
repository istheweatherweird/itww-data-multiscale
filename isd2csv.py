import pandas as pd
import sys

# output dir
OUTPUT_DIR = sys.argv[1]

# read in data
df = pd.read_csv(sys.stdin, dtype=str)

# drop bad temps
df = df[df.temp != "+9999"]

# add month-day column
df['md'] = df.date.str[4:8]

# add year-hour-minute column
df['YHM'] = df.date.str[0:4] + df.date.str[-4:]

# for each monthday
for md in df.md.unique():
    # subset data
    df[df.md == md][["YHM","temp"]].\
            to_csv(OUTPUT_DIR + "/" + md + ".csv", index=False)
