"""
Logistic Regression Implementation - NolanM - 2024-05-14
"""

import numpy as np
from sklearn.model_selection import train_test_split
from sklearn import datasets
import matplotlib.pyplot as plt
from logistic_regression import LogisticRegression


def accuracy(y_true, y_pred):
    accuracy_ = np.sum(y_true == y_pred) / len(y_true)
    return accuracy_


bc_data_set = datasets.load_breast_cancer()
X, y = bc_data_set.data, bc_data_set.target

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=1234)

regressor = LogisticRegression(learning_rate=0.0001, num_iterations=1000)
regressor.fit(X_train, y_train)
predictions = regressor.predict(X_test, threshold=.8)

print("LR classification accuracy:", accuracy(y_test, predictions))

plt.figure(figsize=(10, 6))
plt.scatter(range(len(y_test)), y_test, color='red', label='True Values')
plt.scatter(range(len(predictions)), predictions, color='blue', label='Predictions')
plt.title('True Values vs Predictions')
plt.xlabel('Data Points')
plt.ylabel('Target Values')
plt.legend()
plt.show()