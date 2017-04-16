import numpy as np
import pandas as pd
from sklearn.neighbors import KNeighborsRegressor
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import train_test_split

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
# DO WE NEED THIS APPROACH TO CODE WEATHER TYPE?
# Encode weather strings into classification numbers
enc = OneHotEncoder()
enc.fit(['vedro', 'umjereno oblačno', 'pretežno oblačno'])
'''

'''
# OR THIS?
weather_types = {'weather_type': ['vedro', 'umjereno oblačno', 'pretežno oblačno', 'potpuno oblačno']}
df_weather_types = pd.DataFrame(weather_types, columns=['weather_type'])
df_weather_codes = pd.get_dummies(df_weather_types['weather_type'])
df_weather_types_codes = pd.concat([df_weather_types, df_weather_codes], axis=1)
'''

df_obs = df_obs.dropna()  # why this works at all?

# OR, MAYBE THIS SIMPLE STRING TO CODE REPLACE IS GOOD ENOUGH?
df_obs.replace('vedro', 1, inplace=True)
df_obs.replace('pretežno vedro', 2, inplace=True)
df_obs.replace('umjereno oblačno', 3, inplace=True)
df_obs.replace('pretežno oblačno', 4, inplace=True)
df_obs.replace('potpuno oblačno', 5, inplace=True)
df_obs.replace('slaba kiša', 6, inplace=True)
df_obs.replace('grmljavina s oborinom', 7, inplace=True)
df_obs.replace('slaba kiša poslije grmlj.', 8, inplace=True)
# print(df_obs)

df_obs_weather = df_obs['weathertype']
df_obs_weather = df_obs_weather.to_frame()
# print(df_obs_weather)

df_merged_temp = df_diff_temp.merge(df_wrf, left_index=True, right_index=True)
df_merged_weather = df_obs_weather.merge(df_wrf, left_index=True, right_index=True)
# print(df_merged_temp)

# Build arrays for regression model (temperature error)
X_train_temp = np.array(df_merged_temp.drop(['tmp2mdiff'], 1))
y_train_temp = np.array(df_merged_temp['tmp2mdiff'])
y_predict_temp = np.array(df_fcst)

# Build arrays for classification model (weather type)
X_train_weather = np.array(df_merged_weather.drop(['weathertype'], 1))
y_train_weather = np.array(df_merged_weather['weathertype'])
y_predict_weather = np.array(df_fcst)


print('Length of X and y arrays:', len(X_train_temp), len(y_train_temp))


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
kneighbor_regression = KNeighborsRegressor(n_neighbors=3)
kneighbor_regression.fit(X_train_temp, y_train_temp)

# example: KNeighborsClassification
kneighbor_classifier = KNeighborsClassifier(n_neighbors=3)
kneighbor_classifier.fit(X_train_weather, y_train_weather)


'''
4) RETURN PREDICTED RESULTS
------------------------------

'''
prediction_temp_err = kneighbor_regression.predict(y_predict_temp)
prediction_temp_err = np.round(prediction_temp_err, 1)
prediction_weather_code = kneighbor_classifier.predict(y_predict_weather)
wrf_t2m = [i[0] for i in y_predict_temp - 273.15]  # y_predict_temp[0] - 273.15
# print(wrf_t2m)
#wrf_t2m = round(wrf_t2m, 1)
corrected_t2m = wrf_t2m - prediction_temp_err

print('--- Results from testing forecast dataset (Maksimir.fcst.csv) ---')
print('Estimated temperature error =', prediction_temp_err)
print('WRF T2m =', wrf_t2m)
print('CORRECTED T2m =', corrected_t2m)
print('Estimated weather code =', prediction_weather_code)

#np.savetxt("data/input/Maksimir_corr_t2m.csv", corrected_t2m, fmt="%.1f", delimiter=",")

df_corr = pd.DataFrame({'timestamp': df_fcst.index.tolist(),
                        'wrf_t2m': np.round(np.array(wrf_t2m).tolist(), decimals=1),
                        'prediction_temp_err': prediction_temp_err.tolist(),
                        'corrected_t2m': np.round(corrected_t2m.tolist(), decimals=1),
                        'prediction_weather_code': prediction_weather_code.tolist()})

df_corr = df_corr[['timestamp',
                   'wrf_t2m',
                   'prediction_temp_err',
                   'corrected_t2m',
                   'prediction_weather_code']]

df_corr.to_csv('data/input/Maksimir.corr.csv', index=False)


'''

5) ACCURACY TESTING
---------------------------------
'''

# Regression accuracy testing
X_train, X_test, y_train, y_test = train_test_split(X_train_temp, y_train_temp, test_size=0.25)
clf = KNeighborsRegressor(n_neighbors=3)
clf.fit(X_train, y_train)
accuracy = clf.score(X_test, y_test)
print('--- Regression accuracy testing from train_test_split ---')
print('Accuracy:', accuracy)

mean_alldata_error = np.sum(abs(y_train_temp)) / len(y_train_temp)
print('All data mean temperature error:', mean_alldata_error)

mean_testdata_error = np.sum(abs(y_test)) / len(y_test)
print('Test data mean temperature error:', mean_testdata_error)

forecast_set = clf.predict(X_test)
mean_forecast_error = np.sum(abs(forecast_set)) / len(forecast_set)
print('Fcst data mean temperature error:', mean_forecast_error)

fcst_to_test_difference = mean_forecast_error - mean_testdata_error
print('Mean forecast error - mean test error =', fcst_to_test_difference)
print('')
