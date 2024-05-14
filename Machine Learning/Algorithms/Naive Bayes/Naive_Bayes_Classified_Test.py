"""

"""

import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn import datasets
from Naive_Bayes_Classified import NaiveBayes


def accuracy(y_true, y_pred):
    accuracy_ = np.sum(y_true == y_pred) / len(y_true)
    return accuracy_


def main():
    x, y = datasets.make_classification(n_samples=1000, n_features=10, n_classes=2, random_state=123)
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=123)

    nb = NaiveBayes()
    nb.fit(x_train, y_train)
    predictions = nb.predict(x_test)

    print("Naive Bayes classification accuracy", accuracy(y_test, predictions))


if __name__ == "__main__":
    main()
