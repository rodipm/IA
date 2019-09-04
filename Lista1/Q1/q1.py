""" Questão 1: Naive Bayes:
Teorema: P(Class | X) = P(X | Class) * P(Class)/P(X)
P(Class) = Number of class (target) / Total Observations
P(X) = Number of Similar Observations / Total Observations
p(X | Class) = Number of Similar Observations Among those that are from Class / Total of Class Members  
"""

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

# Import dataset
dataset = pd.read_csv('class01.csv')
X = dataset.iloc[:, 0:100].values
y = dataset.iloc[:, -1].values

"""
Holdout: 35 - 75 
"""
# Split dataset into train and test sets
# 35% para treino e 75% para teste
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.35)

# Feature Scaling
from sklearn.preprocessing import StandardScaler
sc = StandardScaler()
X_train = sc.fit_transform(X_train)
X_test = sc.transform(X_test)


# Gaussian Naive Bayes Classifier
from sklearn.naive_bayes import GaussianNB
classifier = GaussianNB()
classifier.fit(X_train, y_train)

# Prediction Test Sets
y_train_pred = classifier.predict(X_train)
y_pred = classifier.predict(X_test)

# Prediction Visualization
from sklearn.metrics import accuracy_score
acc_train = accuracy_score(y_train, y_train_pred)
acc_test = accuracy_score(y_test, y_pred)

print("==== HOLDOUT =====")
print("Accuracy:")
print("Train Set: ", acc_train, "%")
print("Test Set: ", acc_test, "%")

"""
Leave One Out 
"""
# Split dataset into train and test sets using LeaveOneOut approach
loo = LeaveOneOut()
acc_train_sum = 0
acc_test_sum = 0
counter = 0
for train_index, test_index in loo.split(X):
    counter = counter + 1
    X_train, X_test = X[train_index], X[test_index]
    y_train, y_test = y[train_index], y[test_index]

    # Feature Scaling
    sc = StandardScaler()
    X_train = sc.fit_transform(X_train)
    X_test = sc.transform(X_test)


    # Gaussian Naive Bayes Classifier
    classifier = GaussianNB()
    classifier.fit(X_train, y_train)

    # Prediction Test Sets
    y_train_pred = classifier.predict(X_train)
    y_pred = classifier.predict(X_test)

    # Prediction Visualization
    acc_train = accuracy_score(y_train, y_train_pred)
    acc_test = accuracy_score(y_test, y_pred)

    acc_train_sum = acc_train_sum + acc_train
    acc_test_sum = acc_test_sum + acc_test

acc_train_mean = acc_train_sum / counter 
acc_test_mean = acc_test_sum / counter

print("==== LEAVE ONE OUT =====")
print("Mean Accuracy Accuracy:")
print("Train Set: ", acc_train_mean, "%")
print("Test Set: ", acc_test_mean, "%")