"""

"""

import numpy as np
import matplotlib.pyplot as plt


class NaiveBayes:
    def __init__(self):
        self.mean = None
        self.var = None
        self.priors = None
        self.classes_ = None

    def fit(self, X, y):
        n_samples, n_features = X.shape
        self.classes_ = np.unique(y)
        n_classes = len(self.classes_)

        # init mean, var, priors
        self.mean = np.zeros((n_classes, n_features), dtype=np.float64)
        self.var = np.zeros((n_classes, n_features), dtype=np.float64)
        self.priors = np.zeros(n_classes, dtype=np.float64)

        for c in self.classes_:
            X_c = X[c == y]                                     # get all rows where c == y
            self.mean[c, :] = X_c.mean(axis=0)                  # mean = E[X]
            self.var[c, :] = X_c.var(axis=0)                    # variance = E[(X - E[X])^2]
            self.priors[c] = X_c.shape[0] / float(n_samples)    # P(y)

    def predict(self, X):
        y_pred = [self._predict(x) for x in X]
        return y_pred

    def _predict(self, x):
        # calculate posterior for each class
        posteriors = []

        for idx, c in enumerate(self.classes_):                     # index and classes label
            prior = np.log(self.priors[idx])                        # log(P(y))
            # log(P(x|y)) = log(P(x1|y)) + log(P(x2|y)) + ... + log(P(xn|y)) (sum of all features)
            class_conditional = np.sum(np.log(self._pdf(idx, x)))
            posterior = prior + class_conditional                   # log(P(y)) + log(P(x|y))
            posteriors.append(posterior)                            # store the posterior for each class

        # return the class with the highest posterior probability
        return self.classes_[np.argmax(posteriors)]

    def _pdf(self, class_idx, x):
        mean = self.mean[class_idx]
        var = self.var[class_idx]
        numerator = np.exp(- (x - mean) ** 2 / (2 * var))
        denominator = np.sqrt(2 * np.pi * var)
        return numerator / denominator
