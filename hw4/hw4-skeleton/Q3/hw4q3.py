## Data and Visual Analytics - Homework 4
## Georgia Institute of Technology
## Applying ML algorithms to detect eye state

import numpy as np
import pandas as pd
import time

from sklearn.model_selection import cross_val_score, GridSearchCV, cross_validate, train_test_split
from sklearn.metrics import accuracy_score, classification_report
from sklearn.svm import SVC
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler, normalize
from sklearn.decomposition import PCA

######################################### Reading and Splitting the Data ###############################################
# XXX
# TODO: Read in all the data. Replace the 'xxx' with the path to the data set.
# XXX
data = pd.read_csv('eeg_dataset.csv')

# Separate out the x_data and y_data.
x_data = data.loc[:, data.columns != "y"]
y_data = data.loc[:, "y"]

# The random state to use while splitting the data.
random_state = 100

# XXX
# TODO: Split 70% of the data into training and 30% into test sets. Call them x_train, x_test, y_train and y_test.
# Use the train_test_split method in sklearn with the parameter 'shuffle' set to true and the 'random_state' set to 100.
# XXX
x_train, x_test, y_train, y_test = train_test_split(x_data,y_data,train_size=0.7,random_state = 100,shuffle = True)

# ############################################### Linear Regression ###################################################
# XXX
# TODO: Create a LinearRegression classifier and train it.
# XXX
learner_regr = LinearRegression()
learner_regr.fit(x_train,y_train)
# XXX
# TODO: Test its accuracy (on the training set) using the accuracy_score method.
# TODO: Test its accuracy (on the testing set) using the accuracy_score method.
# Note: Round the output values greater than or equal to 0.5 to 1 and those less than 0.5 to 0. You can use y_predict.round() or any other method.
# XXX
train_y_pred = learner_regr.predict(x_train)
test_y_pred = learner_regr.predict(x_test)
train_accuracy = accuracy_score(np.floor(train_y_pred + 0.5).astype(int),y_train.tolist())
test_accuracy = accuracy_score(np.floor(test_y_pred + 0.5).astype(int),y_test.tolist())
# ############################################### Random Forest Classifier ##############################################
# XXX
# TODO: Create a RandomForestClassifier and train it.
# XXX
learner_rf = RandomForestClassifier()
learner_rf.fit(x_train,y_train)

# XXX
# TODO: Test its accuracy on the training set using the accuracy_score method.
# TODO: Test its accuracy on the test set using the accuracy_score method.
# XXX
train_y_pred = learner_rf.predict(x_train)
test_y_pred = learner_rf.predict(x_test)
train_accuracy = accuracy_score(train_y_pred,y_train)
test_accuracy = accuracy_score(test_y_pred,y_test)
# XXX
# TODO: Determine the feature importance as evaluated by the Random Forest Classifier.
#       Sort them in the descending order and print the feature numbers. The report the most important and the least important feature.
#       Mention the features with the exact names, e.g. X11, X1, etc.
#       Hint: There is a direct function available in sklearn to achieve this. Also checkout argsort() function in Python.
# XXX
feature_importance = learner_rf.feature_importances_
feature_sorted = np.argsort(feature_importance)
print(['X'+str(feature+1) for feature in feature_sorted[::-1]])
# XXX
# TODO: Tune the hyper-parameters 'n_estimators' and 'max_depth'.
#       Print the best params, using .best_params_, and print the best score, using .best_score_.
# XXX
rf_classifier = RandomForestClassifier()
estimator_range = np.insert(np.arange(99,500,100), 0, 9, axis=0)
depth_range = np.insert(np.arange(50,202,50), 0, 10, axis=0)
param_grid = dict(n_estimators=estimator_range, max_depth=depth_range)
rf_grid = GridSearchCV(rf_classifier, 
                                        param_grid=param_grid,
                                        scoring='accuracy',
                                        cv=10,
                                        n_jobs=-1
                                       )
rf_grid.fit(x_train, y_train)
print(rf_grid.best_params_)
print(rf_grid.best_score_)

# ############################################ Support Vector Machine ###################################################
# XXX
# TODO: Pre-process the data to standardize or normalize it, otherwise the grid search will take much longer
# TODO: Create a SVC classifier and train it.
# XXX
scaler = StandardScaler()
scaler.fit(x_train)
x_train_scaled = scaler.transform(x_train)
x_test_scaled = scaler.transform(x_test)

learner_svm = SVC()
learner_svm.fit(x_train_scaled,y_train)
# XXX
# TODO: Test its accuracy on the training set using the accuracy_score method.
# TODO: Test its accuracy on the test set using the accuracy_score method.
# XXX
train_y_pred = learner_svm.predict(x_train_scaled)
test_y_pred = learner_svm.predict(x_test_scaled)
train_accuracy = accuracy_score(train_y_pred,y_train)
test_accuracy = accuracy_score(test_y_pred,y_test)
# XXX
# TODO: Tune the hyper-parameters 'C' and 'kernel' (use rbf and linear).
#       Print the best params, using .best_params_, and print the best score, using .best_score_.
# XXX
svm_classifier = SVC(max_iter=100000)
kernels = ["linear","rbf"]
C_range = np.logspace(-3, 2, 6)
param_grid = dict(kernel=kernels, C=C_range)
svm_grid = GridSearchCV(svm_classifier, 
                                        param_grid=param_grid,
                                        scoring='accuracy',
                                        cv=10,
                                        n_jobs=-1
                                       )
svm_grid.fit(x_train_scaled, y_train)
print(svm_grid.best_params_)
print(svm_grid.best_score_)
# ######################################### Principal Component Analysis #################################################
# XXX
# TODO: Perform dimensionality reduction of the data using PCA.
#       Set parameters n_component to 10 and svd_solver to 'full'. Keep other parameters at their default value.
#       Print the following arrays:
#       - Percentage of variance explained by each of the selected components
#       - The singular values corresponding to each of the selected components.
# XXX
pca=PCA(n_components=10,svd_solver='full')
pca.fit(x_data)
print(pca.explained_variance_ratio_)
print(pca.singular_values_)