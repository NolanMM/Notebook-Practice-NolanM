"""

"""
import numpy as np


class Perceptron:
    def __init__(self, learning_rate=0.01, number_iteration=1000):
        self.learning_rate = learning_rate
        self.number_iteration = number_iteration
        self.activation_func = self.unit_step_func
        self.weights = None
        self.bias = None

    def fit(self, X, y):
        n_samples, n_features = X.shape
        # Initialize weights and bias
        self.weights = np.zeros(n_features)
        self.bias = 0

        # Perceptron learning algorithm
        y_ = np.array([1 if i > 0 else 0 for i in y])   # Convert y to 0 or 1

        for _ in range(self.number_iteration):                          # Iterate over the number of iterations
            for idx, x_i in enumerate(X):
                linear_output = np.dot(x_i, self.weights) + self.bias   # y = w*x + b
                y_predicted = self.activation_func(linear_output)

                update = self.learning_rate * (y_[idx] - y_predicted)   # Update the weights and bias
                self.weights += update * x_i                            # w = w + learning_rate*(y - y_predicted)*x
                self.bias += update                                     # b = b + learning_rate*(y - y_predicted)

    def predict(self, X):
        linear_output = np.dot(X, self.weights) + self.bias
        y_predicted = self.activation_func(linear_output)
        return y_predicted

    def unit_step_func(self, x):
        return np.where(x >= 0, 1, 0)
