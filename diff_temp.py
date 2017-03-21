import pandas as pd

df_wrf = pd.read_csv('data/input/Maksimir.wrf.csv', sep=',', index_col=0)
df_obs = pd.read_csv('data/input/Maksimir.obs.csv', sep=',', index_col=0)

df_wrf_temp = df_wrf['tmp2m']
df_obs_temp = df_obs['tmp2m']
df_obs_temp = df_obs_temp.drop_duplicates()
df_wrf_temp = df_wrf_temp.drop_duplicates()

df_diff_temp = df_wrf_temp - df_obs_temp
df_diff_temp = df_diff_temp.dropna()
print(df_diff_temp)

df_diff_temp.to_csv('data/input/Maksimir.diff.csv')