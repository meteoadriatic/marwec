import numpy as np
import pandas as pd
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

df_wrf = pd.read_csv('data/input/Maksimir.wrf.csv', sep=',', index_col=0)
df_diff = pd.read_csv('data/input/Maksimir.diff.csv', sep=',', index_col=0)

df_merged = df_diff.merge(df_wrf, left_index=True, right_index=True)

#print(df_merged.ix[:, 0])

y_train = np.array(df_merged.ix[:, 0])
df_merged.drop(df_merged.columns[[0]], axis=1, inplace=True)
X_train = np.array(df_merged)

#print(X_train.shape)  # Should return (n1, n2) where n1 = n_samples, n2 = n_features
#print(y_train.shape)  # Should return (m,) where m = n_solutions, and m = n_samples

exit()
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
kneighbor_regression.fit(X_train, y_train)

'''
4) RETURN PREDICTED RESULTS
------------------------------

'''
