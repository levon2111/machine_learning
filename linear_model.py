import numpy as np
import statsmodels.api as sm

predictors = np.random.random(1000).reshape(500, 2)
target = predictors.dot(np.array([0.4, 0.6])) + np.random.random(500)

lmRegModel = sm.OLS(target, predictors)
result = lmRegModel.fit()
result.summary()

# K nearest neighbor
from sklearn import neighbors, metrics

predictors = np.random.random(1000).reshape(500, 2)
target = np.around(predictors.dot(np.array([0.4, 0.6])) + np.random.random(500))
clf = neighbors.KNeighborsClassifier(n_neighbors=10)
knn = clf.fit(predictors, target)
knn.score(predictors, target)
prediction = knn.predict(predictors)
metrics.confusion_matrix(target, prediction)
