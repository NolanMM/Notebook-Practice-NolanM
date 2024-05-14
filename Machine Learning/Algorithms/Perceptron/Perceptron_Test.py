"""

"""
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn import datasets
import matplotlib.pyplot as plt
from Perceptron import Perceptron


def accuracy(y_true, y_pred):
    accuracy_ = np.sum(y_true == y_pred) / len(y_true)
    return accuracy_


def main():
    # Using sk_learn's make_blobs to generate a dataset with 2 classes  (0 and 1) and 2 features (x1 and x2)
    # and 100 samples in total (50 samples per class) with a cluster_std of 1.05
    x, y = datasets.make_blobs(n_samples=100, n_features=2, centers=2, cluster_std=1.05, random_state=2)
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=123)

    p = Perceptron(learning_rate=0.01, number_iteration=1000)
    p.fit(x_train, y_train)
    predictions = p.predict(x_test)

    print("Perceptron classification accuracy", accuracy(y_test, predictions))

    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    plt.scatter(x_train[:, 0], x_train[:, 1], marker='o', c=y_train)

    # Decision Boundary
    x0_1 = np.amin(x_train[:, 0])
    x0_2 = np.amax(x_train[:, 0])

    # w1*x1 + w2*x2 + b = 0 => x2 = (-w1*x1 - b)/w2 (where x1 is the feature on x-axis and x2 is the feature on y-axis)
    x1_1 = (-p.weights[0] * x0_1 - p.bias) / p.weights[1]
    x1_2 = (-p.weights[0] * x0_2 - p.bias) / p.weights[1]

    ax.plot([x0_1, x0_2], [x1_1, x1_2], 'k')

    # x-axis and y-axis limits of the plot
    y_min = np.amin(x_train[:, 1])
    y_max = np.amax(x_train[:, 1])

    ax.set_ylim([y_min-3, y_max+3])

    plt.show()


if __name__ == "__main__":
    main()
