class perceptron():
    def __init__(self, X, y, threshold=0.5, learning_rate=0.1, max_epochs=10):
        self.threshold = threshold
        self.learning_rate = learning_rate
        self.X = X
        self.y = y
        self.max_epochs = max_epochs

    def initialize(self, init_type='zeros'):
        if init_type == 'random':
            self.weights = np.random.rand(len(self.X[0])) * 0.05
        if init_type == 'zeros':
            self.weights = np.zeros(len(self.X[0]))

    def train(self):
        epoch = 0
        while True:
            error_count = 0
            epoch += 1
            for (X, y) in zip(self.X, self.y):
                error_count += self.train_observation(X, y, error_count)
            if error_count == 0:
                print("training succesfull")
                break
            if epoch >= self.max_epochs:
                print("reached maximum epochs, no perfect prediction")
                break

    def train_observation(self, X, y, error_count):
        result = np.dot(X, self.weights) > self.threshold
        error = y - result

        if error != 0:
            error_count += 1
            for index, value in enumerate(X):
                self.weights[index] += self.learning_rate * error * value
        return error_count

    def predict(self, X):
        return int(np.dot(X, self.weights) > self.threshold)


X = [(1, 0, 0), (1, 1, 0), (1, 1, 1), (1, 1, 1), (1, 0, 1), (1, 0, 1)]
y = [1, 1, 0, 0, 1, 1]

p = perceptron(X, y)
p.initialize()
p.train()
print(p.predict((1, 1, 1)))
print(p.predict((1, 0, 1)))

import bcolz as bc
import dask.array as da
import numpy as np

n = 1e4

ar = bc.carray(np.arange(n).reshape(n / 2, 2), dtype='float64', rootdir='ar.bcolz', mode='w')
y = bc.carray(np.arange(n / 2), dtype='float64', rootdir='yy.bcolz', mode='w')

dax = da.from_array(ar, chunks=(5, 5))
dy = da.from_array(y, chunks=(5, 5))

XTX = dax.T.dot(dax)
Xy = dax.T.dot(dy)

coefficients = np.linalg.inv(XTX.compute()).dot(Xy.compute())

coef = da.from_array(coefficients, chunks=(5, 5))

ar.flush()
y.flush()

predictions = dax.dot(coef).compute()
print(predictions)
