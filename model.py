import numpy as np
import pandas as pd
from sklearn.preprocessing import OneHotEncoder
from sklearn.neighbors import KNeighborsRegressor
from sklearn.neighbors import KNeighborsClassifier

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
df_diff_temp = pd.read_csv('data/input/Maksimir.diff.csv', sep=',', index_col=0)
df_fcst = pd.read_csv('data/input/Maksimir.fcst.csv', sep=',', index_col=0)

'''
# Encode weather strings into classification numbers
enc = OneHotEncoder()
enc.fit(['vedro', 'umjereno oblačno', 'pretežno oblačno'])
'''

'''
weather_types = {'weather_type': ['vedro', 'umjereno oblačno', 'pretežno oblačno', 'potpuno oblačno']}
df_weather_types = pd.DataFrame(weather_types, columns=['weather_type'])
df_weather_codes = pd.get_dummies(df_weather_types['weather_type'])
df_weather_types_codes = pd.concat([df_weather_types, df_weather_codes], axis=1)
'''

df_obs = df_obs.dropna()  # why this works at all?

df_obs.replace('vedro', 1, inplace=True)
df_obs.replace('umjereno oblačno', 2, inplace=True)
df_obs.replace('pretežno oblačno', 3, inplace=True)
df_obs.replace('potpuno oblačno', 4, inplace=True)
# print(df_obs)

df_obs_weather = df_obs['weathertype']
df_obs_weather = df_obs_weather.to_frame()
# print(df_obs_weather)

df_merged_temp = df_diff_temp.merge(df_wrf, left_index=True, right_index=True)
df_merged_weather = df_obs_weather.merge(df_wrf, left_index=True, right_index=True)
# print(df_merged_weather)
# exit()

# Build arrays for regression model (temperature error)
y_train_temp = np.array(df_merged_temp.ix[:, 0])
df_merged_temp.drop(df_merged_temp.columns[[0]], axis=1, inplace=True)
X_train_temp = np.array(df_merged_temp)
y_predict_temp = np.array(df_fcst)
# print(X_train.shape)  # Should return (n1, n2) where n1 = n_samples, n2 = n_features
# print(y_train.shape)  # Should return (m,) where m = n_solutions, and m = n_samples

# Build arrays for classification model (weather type)
X_train_weather = np.array(df_merged_weather.drop(['weathertype'], 1))
y_train_weather = np.array(df_merged_weather['weathertype'])
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

# example: KNeighborsClassification
kneighbor_classifier = KNeighborsClassifier(n_neighbors=1)
kneighbor_classifier.fit(X_train_weather, y_train_weather)

'''
4) RETURN PREDICTED RESULTS
------------------------------


'''
# exit()
prediction_temp = kneighbor_regression.predict(y_predict_temp)
prediction_weather = kneighbor_classifier.predict(y_predict_weather)

print('Estimated temperature error =', prediction_temp)
print('Estimated weather code =', prediction_weather)
