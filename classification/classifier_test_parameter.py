# -*- coding: utf-8 -*-
"""This script should be called with an argument corresponding to the ID of
an MP, and determines the most accurate classifier through parametrization
of classifiers. For the given MP, a host of classifiers are trained on the
dataset and subsequently evaluated through stratisfied crossvalidation.
"""

import os
parentdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.sys.path.insert(0, parentdir)

import classifier_data
from sklearn.cross_validation import StratifiedKFold
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.lda import LDA
from sklearn.qda import QDA
import numpy as np
from sys import argv

_, mp_id = argv


def classifier_score(features, targets, classifier):
    """Performs stratisfied K-fold crossvalidation and for a classifier with a
    specified dataset. Then checks for the event that the trained classifier is
    trivial (all predictions equal to majority class).

    Parameters
    ----------
    features : feature-array
        A data matrix of numpy.array type. See also
        classification.classifier_data.dataset_X_y

    targets : class-array
        A numpy.array class-index. See also
        classification.classifier_data.dataset_X_y
        
    classifier : classifer-like
        A classifier class that takes numpy arrays. Function developed with
        Sci-kit learn classifiers.

    Returns
    -------
    out : accuracy or 'A majority class classifier'
        Accuracy computed by 10-fold statisfied CV, float type, or notification
        of trivial classifier.
    """
    K = 10
    cv = StratifiedKFold(targets, n_folds=K, indices=False)
    accuracies = []

    for train_index, test_index in cv:
        X_train, y_train = np.array(
            features[train_index]), np.array(targets[train_index])
        X_test, y_test = np.array(
            features[test_index]), np.array(targets[test_index])

        classifier.fit(X_train, y_train)
        accuracies.append(classifier.score(X_test, y_test))

    classifier.fit(features, targets)
    pred = classifier.predict(features)

    if np.mean(pred) % 1 == 0:
        return 'A majority class classifier'
    else:
        return np.mean(accuracies)


try:
    X = np.load('../storing/matrices/X_{}.npy'.format(mp_id))
    y = np.load('../storing/matrices/y_{}.npy'.format(mp_id))
except IOError:
    X, y = classifier_data.dataset_X_y(mp_id)

# Initialize different classifiers from sklearns library and test accuracy.
names = ["Nearest Neighbors", "Linear SVM", "RBF SVM", "Decision Tree",
         "Random Forest", "AdaBoost", "Naive Bayes", "LDA", "QDA"]

classifiers = [
    KNeighborsClassifier(3),
    SVC(kernel="linear", C=0.025),
    SVC(gamma=2, C=1),
    DecisionTreeClassifier(max_depth=5),
    RandomForestClassifier(max_depth=5, n_estimators=200),
    AdaBoostClassifier(),
    GaussianNB(),
    LDA(),
    QDA()]

print 'Percentage of "yes"-votes cast in current period of government:',
np.mean(y == 1)
for name, clf in zip(names, classifiers):
    score = classifier_score(X, y, clf)
    print name, ' results are: \n', score
