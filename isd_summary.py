import pandas as pd
import numpy as np
import os
import sys
import pathlib
import gzip

WWW_DIR = sys.argv[1]
OUT_DIR = sys.argv[2]
station_id = sys.argv[3]

def read_isd(basedir, station_id):
    colspecs = [(15,27), (27,28), (87,92), (92,93)]
    colnames = ['timestamp', 'source', 'temp', 'temp_quality']

    path = pathlib.Path(basedir)

    df = pd.concat([pd.read_fwf(gzip.open(gz_file, 'rt', errors='ignore'),
                 colspecs=colspecs, names=colnames, dtype=str)
                 for gz_file in path.glob("*/" + station_id + "*")])

    df['timestamp'] = pd.to_datetime(df.timestamp, format="%Y%m%d%H%M")
    df = df[df.temp != '+9999']
    df['temp'] = df.temp.astype(int)/10
    df = df.groupby('timestamp').first()
    
    return(df)

def get_isd_summary(df):
    hours = pd.date_range(start=df.index.floor('H').min(), 
                  end=df.index.ceil('H').max(), freq="H")
    df2 = df.reindex(df.index.union(hours))
    df2 = df2['temp'].interpolate(limit=1).loc[hours]

    def get_rolling_mean(series, days, prop):
        r = series.rolling(str(days) + "D")
        m = r.mean()
        m.loc[r.count() <= days*24*prop] = np.nan
        return(m)

    rollings = {"D" + str(days): get_rolling_mean(df2.loc[hours], days, 0.99) 
                for days in [1, 7, 30, 365]}

    summary = pd.DataFrame(rollings)
    summary['obs'] = df2.loc[hours]

    
    return(summary)

def write_isd_summary(summary, outdir):
    summary = (summary.round(1)*10).astype(str).replace("(\.0$|nan)", "", regex=True)

    summary['hour'] = summary.index.hour
    summary['year'] = summary.index.year

    summary = summary[['year', 'hour', 'obs', 'D1', 'D7', 'D30', 'D365']]
    
    summary_grouped = summary.groupby(summary.index.strftime('%m%d'))
    for group_name, df_group in summary_grouped:
        df_group.to_csv(outdir + "/" + group_name + ".csv", index=False)

df = read_isd(WWW_DIR, station_id)
summary = get_isd_summary(df)
write_isd_summary(summary, OUT_DIR + "/" + station_id)
