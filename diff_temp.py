import pandas as pd
import numpy as np

df_wrf = pd.read_csv('data/input/Maksimir.wrf.csv', sep='\t', index_col=0)
df_obs = pd.read_csv('data/input/Maksimir.obs.csv', sep='\t', index_col=0, header=None, names=['timestamp', 'tmp2m'])

# print(df_obs)

df_wrf_temp = df_wrf['tmp2m']
df_obs_temp = df_obs['tmp2m']

df_diff_temp = df_wrf_temp - df_obs_temp
print(df_diff_temp)

df_diff_temp.to_csv('data/input/Maksimir.diff.csv')
