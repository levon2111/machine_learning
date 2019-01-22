import pylab as pl
from sklearn.datasets import load_digits

digits = load_digits()
pl.gray()
pl.matshow(digits.images[0])
pl.show()
print(digits.images[0])

from sklearn.cross_validation import train_test_split
from sklearn.naive_bayes import GaussianNB
from sklearn.metrics import confusion_matrix
import pylab as plt

y = digits.target

n_samples = len(digits.images)
X = digits.images.reshape((n_samples, -1))
print(X)

X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=0)

gnb = GaussianNB()
fit = gnb.fit(X_train, y_train)
predicted = fit.predict(X_test)
confusion_matrix(y_test, predicted)

images_and_predictions = list(zip(digits.images, fit.predict(X)))
for index, (image, prediction) in enumerate(images_and_predictions[:6]):
    plt.subplot(6, 3, index + 5)
    plt.axis('off')
    plt.imshow(image, cmap=plt.cm.gray_r, interpolation='nearest')
    plt.title('Prediction: %i' % prediction)
plt.show()

import pandas as pd
from sklearn.decomposition import PCA
import pylab as plt
from sklearn import preprocessing

url = 'http://archive.ics.uci.edu/ml/machine-learning-databases/wine-quality/winequality-red.csv'
data = pd.read_csv(url, sep=";")

X = data[[u'fixed acidity', u'volatile acidity', u'citric acid',
          u'residual sugar', u'chlorides', u'free sulfur dioxide',
          u'total sulfur dioxide', u'density', u'pH', u'sulphates',
          u'alcohol']]
y = data.quality
X = preprocessing.StandardScaler().fit(X).transform(X)
model = PCA()
results = model.fit(X)
Z = results.transform(X)
plt.plot(results.explained_variance_)
plt.show()
pd.DataFrame(results.components_, columns=list(
    [u'fixed acidity', u'volatile acidity', u'citric acid', u'residual sugar', u'chlorides', u'free sulfur dioxide',
     u'total sulfur dioxide', u'density', u'pH', u'sulphates', u'alcohol']))

from sklearn.naive_bayes import GaussianNB
from sklearn.metrics import confusion_matrix
import pylab as plt

gnb = GaussianNB()
fit = gnb.fit(X, y)
pred = fit.predict(X)
print(confusion_matrix(pred, y))
print(confusion_matrix(pred, y).trace())

predicted_correct = []
for i in range(1, 10):
    model = PCA(n_components=i)
    results = model.fit(X)
    Z = results.transform(X)
    fit = gnb.fit(Z, y)
    pred = fit.predict(Z)
    predicted_correct.append(confusion_matrix(pred, y).trace())
    print(predicted_correct)
plt.plot(predicted_correct)
plt.show()

import sklearn as sklearn
from sklearn import cluster
import pandas as pd

data = sklearn.datasets.load_iris()
X = pd.DataFrame(data.data, columns=list(data.feature_names))
print(X[:5])
model = cluster.KMeans(n_clusters=3, random_state=25)
results = model.fit(X)
X["cluster"] = results.predict(X)
X["target"] = data.target
X["c"] = "lookatmeIamimportant"
print(X[:5])
classification_result = X[["cluster", "target", "c"]].groupby(["cluster", "target"]).agg("count")
print(classification_result)
