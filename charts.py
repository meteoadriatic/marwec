import matplotlib.pyplot as plt
import pandas as pd
import matplotlib
import datetime as dt

matplotlib.style.use('ggplot')

df_obs = pd.read_csv('data/input/Maksimir.diff.csv', sep=',')
#df_obs = df_obs.sort_values(by='timestamp', ascending=1)
df_obs = df_obs.reset_index(drop=True)

#df_obs_timestamp = (df_obs['timestamp'] - 1490774400) / 60 / 60 / 24
#df_obs_timestamp = (df_obs['timestamp'] - 1490774400)
df_obs_timestamp = df_obs['timestamp']
df_obs_time = pd.to_datetime(df_obs_timestamp, unit='s')
#df_obs_time = df_obs_time.dt.strftime('%Y-%m-%d')

df_obs_tmp2mdiff = df_obs['tmp2mdiff']  # - 273.15

print(df_obs_time)

#plt.scatter(df_obs.index.values, df_obs_timestamp)
plt.bar(df_obs_time.tolist(), df_obs_tmp2mdiff, width=0.02)
# plt.axis([0.0,600.0,1000000.0,2000000.0])
datemin = dt.date(2017, 3, 29)
datemax = dt.date(2017, 4, 3)
plt.xlim(datemin, datemax)
plt.title('Model temperature error')
plt.xlabel('Date')
plt.ylabel('Error (K)')
plt.show()
