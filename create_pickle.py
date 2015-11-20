from sklearn import svm
from sklearn import datasets
from sklearn.externals import joblib
import os

__dir__ = os.path.abspath(os.path.dirname(__file__))

if __name__ == '__main__':
    clf = svm.SVC()
    iris = datasets.load_iris()
    X, y = iris.data, iris.target
    clf.fit(X, y)
    joblib.dump(clf,
        os.path.join(__dir__, 'model/pickle/champion.pkl')
        )