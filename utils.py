import pandas as pd
import numpy as np
import pathlib
import gzip
import requests

def read_isd_helper(basedir, station_id):
    colspecs = [(15,27), (27,28), (87,92), (92,93)]
    colnames = ['timestamp', 'source', 'temp', 'temp_quality']

    path = pathlib.Path(basedir)

    df = pd.concat([pd.read_fwf(gzip.open(gz_file, 'rt', errors='ignore'),
                 colspecs=colspecs, names=colnames, dtype=str)
                 for gz_file in path.glob("*/" + station_id + "*")])

    df['timestamp'] = pd.to_datetime(df.timestamp, format="%Y%m%d%H%M", utc=True)
    df = df[df.temp != '+9999']
    df['temp'] = df.temp.astype(int)/10

    return df

def read_isd(basedir, station_id, station_id2=None):
    df = read_isd_helper(basedir, station_id)

    if station_id2 is not None:
        df2 = read_isd_helper(basedir, station_id2)
        df = pd.concat((df, df2))

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

def get_ICAO(station_id):
    stations = get_stations()
    ICAO = stations[(stations.USAF + "-" + stations.WBAN) == station_id].ICAO.iloc[0]
    return(ICAO)

def get_latest(ICAO, start_time, end_time=None):
    nws_request_url = 'https://api.weather.gov/stations/{}/observations'.format(
        ICAO
    )

    params = {'start': start_time.floor("S").isoformat().replace('+00:00', 'Z')}
    if end_time is not None:
        params['end'] = end_time.ceil("S").isoformat().replace('+00:00', 'Z')

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

def combine_isd_latest(df_isd, df_latest):
    df = pd.concat((
        df_isd.reset_index(), 
        df_latest.to_frame('temp').reset_index().rename(
            columns={"index":"timestamp"})))

    df = df.groupby('timestamp').first() # in case ISD and NOAA have an overlap
    return df

def get_latest_summary(df):
    summary = (get_isd_summary(df)
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

def get_old_station_id(station_id):
    stations = get_stations()
    row = stations[(stations.USAF.astype(str) + "-" + stations.WBAN.astype(str)) == station_id].iloc[0]
    if pd.isnull(row.USAF2):
        return None
    else:
        return row.USAF2 + "-" + row.WBAN2

def get_stations():
    return pd.read_csv("csv/stations.csv", dtype=str)
