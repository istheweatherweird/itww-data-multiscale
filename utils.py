import pandas as pd
import numpy as np
import pathlib
import gzip
import requests

def read_ghcnh_por_psv(basedir, GHCN_ID):
    columns = ['DATE', 'temperature']
    
    path = pathlib.Path(basedir)
    df = pd.read_csv(basedir + "/" + GHCN_ID + ".psv",
                    sep="|", usecols=columns, dtype=str)

    df['timestamp'] = pd.to_datetime(df.DATE, utc=True)
    df['temp'] = df['temperature'].astype(float)

    return df[['timestamp', 'temp']].groupby('timestamp').first()

def read_ghcnh_parquet(basedir, GHCN_ID):
    columns = ['DATE', 'temperature']
    
    path = pathlib.Path(basedir)
    parquet_files = list(path.glob("GHCNh_" + GHCN_ID + "_*.parquet"))

    if len(parquet_files) > 0:
        dfs = []
        for parquet_file in parquet_files:
            try:
                dfs.append(pd.read_parquet(parquet_file, columns=columns))
            except Exception as e:
                raise ValueError(f"Error: failed to parse {parquet_file}: {e}")
        df = pd.concat(dfs, ignore_index=True)

        df['timestamp'] = pd.to_datetime(df.DATE, utc=True)
        df['temp'] = df['temperature'].astype(float)
        df = df[df.temp.notna()]

        return df[['timestamp', 'temp']].groupby('timestamp').first()
    else:
        raise ValueError("No parquet files found for this station")

def get_ghcnh_summary(df):
    hours = pd.date_range(start=df.index.min().floor('h'), 
                          end=df.index.max().ceil('h'), freq="h")
    df2 = df.reindex(df.index.union(hours))
    df2 = df2['temp'].interpolate(limit=1).loc[hours]

    def get_rolling_mean(series, days, prop):
        r = series.rolling(str(days) + "D")
        m = r.mean()
        m.loc[r.count() <= days*24*prop] = np.nan
        return(m)

    rollings = {"D" + str(days): get_rolling_mean(df2.loc[hours], days, 0.95)
                for days in [1, 7, 30, 365]}

    summary = pd.DataFrame(rollings)
    summary['obs'] = df2.loc[hours]

    
    return(summary)

def write_ghcnh_summary(summary, outdir):
    summary = (summary.round(1)*10).astype(str).replace("(\\.0$|nan)", "", regex=True)

    summary['hour'] = summary.index.hour
    summary['year'] = summary.index.year

    summary = summary[['year', 'hour', 'obs', 'D1', 'D7', 'D30', 'D365']]
    
    summary_grouped = summary.groupby(summary.index.strftime('%m%d'))
    for group_name, df_group in summary_grouped:
        df_group.to_csv(outdir + "/" + group_name + ".csv", index=False)

def get_GHCN_ID(ICAO):
    stations = get_stations()
    GHCN_ID = stations[stations.ICAO == ICAO].iloc[0].GHCN_ID
    return(GHCN_ID)

def get_ICAO(GHCN_ID):
    stations = get_stations()
    ICAO = stations[stations.GHCN_ID == GHCN_ID].iloc[0].ICAO
    return(ICAO)

def get_latest(ICAO, start_time, end_time=None):
    nws_request_url = 'https://api.weather.gov/stations/{}/observations'.format(
        ICAO
    )

    params = {'start': start_time.floor("s").isoformat().replace('+00:00', 'Z')}
    if end_time is not None:
        params['end'] = end_time.ceil("s").isoformat().replace('+00:00', 'Z')

    response_json = requests.get(nws_request_url, params=params).json()

    try:
        timestamps = [obs['properties']['timestamp']
                      for obs in response_json['features']
                      if obs['properties']['temperature']['value']
                      ]
        temps = [obs['properties']['temperature']['value']
                 for obs in response_json['features']
                 if obs['properties']['temperature']['value']
                 ]
        observations = pd.Series(temps, index=pd.DatetimeIndex(timestamps))
    except KeyError:
        observations = pd.Series()

    return observations

def combine_ghcnh_latest(df_ghcnh, df_latest):
    df = pd.concat((
        df_ghcnh.reset_index(), 
        df_latest.to_frame('temp').reset_index().rename(
            columns={"index":"timestamp"})))

    df = df.groupby('timestamp').first() # in case GHCNh and NOAA have an overlap
    return df

def get_latest_summary(df):
    summary = (get_ghcnh_summary(df)
			   # drop the obs from here so that our obs is not interpolated/rounded
               .drop("obs", axis=1) 
               .stack())
    summary.name = 'temp'
    summary.index.names = ['timestamp', 'timescale']

    # get the most recent non-missing for each timescale
    latest = summary.reset_index().groupby("timescale").last().reset_index() 
	
    # add back in the most recent obs
    latest_obs = df.temp.dropna().tail(1).reset_index() 
    latest_obs['timescale'] = 'obs'
    latest = pd.concat((latest, latest_obs))

    return latest

def get_stations():
    return pd.read_csv("csv/stations.csv", dtype=str)
