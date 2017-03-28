import numpy as np
import pandas as pd
from sklearn.preprocessing import OneHotEncoder
from sklearn.neighbors import KNeighborsRegressor

'''
1) COLLECTING AND PREPARING DATA
---------------------------------
We need to load input data into numpy arrays.

Training data consists of training data (X_train)
and training solutions (y_train):

X_train = training data matrix consisting of n_samples in rows
and n_features in columns. In our case, samples (rows) will be
a big set of WRF forecast times indexed with unix timestamp
and features (columns) will be meteorological variables at particular
geographical points within WRF domain.

y_train = training solutions for the model. For training solutions we will
use WRF errors at exact forecast time indexed by unix timestamp that
corresponds to the same time in training data, y_train array will be calculated
as diffrence bewteen forecasted data by WRF and observed data at synoptic station.

'''

# Read input files
df_obs = pd.read_csv('data/input/Maksimir.obs.csv', sep=',', index_col=0)
df_wrf = pd.read_csv('data/input/Maksimir.wrf.csv', sep=',', index_col=0)
df_diff = pd.read_csv('data/input/Maksimir.diff.csv', sep=',', index_col=0)
df_fcst = pd.read_csv('data/input/Maksimir.fcst.csv', sep=',', index_col=0)

# Separate weather type for classification model
df_obs_weather = df_obs['weathertype']


# Encode weather strings into classification numbers
#enc = OneHotEncoder()
#enc.fit(['vedro', 'umjereno oblačno', 'pretežno oblačno'])

weather_types = {'weather_type': ['vedro', 'umjereno oblačno', 'pretežno oblačno', 'potpuno oblačno']}
df_weather_types = pd.DataFrame(weather_types, columns=['weather_type'])
df_weather_codes = pd.get_dummies(df_weather_types['weather_type'])
df_weather_types_codes = pd.concat([df_weather_types, df_weather_codes], axis=1)

# what now with that?!

#print(df_weather_types_codes)
#exit()

# Create new dataframe that has same timestamp in both wrf and temp. diff dataframes
df_merged_temp = df_diff.merge(df_wrf, left_index=True, right_index=True)

# Create new dataframe that has same timestamp in both wrf and obs. weather dataframes
df_merged_weather = df_obs_weather.merge(df_wrf, left_index=True, right_index=True)

print(df_merged_temp)
#print(df_merged_temp.ix[:, 0])

# Build arrays for regression model (temperature error)
y_train_temp = np.array(df_merged_temp.ix[:, 0])
df_merged_temp.drop(df_merged_temp.columns[[0]], axis=1, inplace=True)
X_train_temp = np.array(df_merged_temp)
y_predict_temp = np.array(df_fcst)

# print(X_train.shape)  # Should return (n1, n2) where n1 = n_samples, n2 = n_features
# print(y_train.shape)  # Should return (m,) where m = n_solutions, and m = n_samples

# Build arrays for classification model (weather type)
y_train_weather = np.array(df_merged_weather.ix[:, 0])
df_merged_weather.drop(df_merged_weather.columns[[0]], axis=1, inplace=True)
X_train_weather = np.array(df_merged_weather)
y_predict_weather = np.array(df_fcst)


# exit()
'''
2) PREPROCESSING DATA
--------------------------------
Preprocessing of data consists of normalizing feature values in order to
set influence magnitude on the predicted results

'''

# Preprocessing statements here


'''
3) RUNNING MODEL
------------------------------
When data is ready and correctly preprocessed we want to chose
regression model and feed it with our X_train and y_train numpy arrays
'''

# example: KNeighborsRegression
kneighbor_regression = KNeighborsRegressor(n_neighbors=1)
kneighbor_regression.fit(X_train_temp, y_train_temp)

'''
4) RETURN PREDICTED RESULTS
------------------------------


'''
# exit()
prediction = kneighbor_regression.predict(y_predict_temp)

print(prediction)
