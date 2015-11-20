import urllib
import json
from random import random


def params_predict():
    """
    Predicts using the paramspredict url.
    """
    sepal_length = round(random() * 7, 3)
    sepal_width = round(random() * 7, 3)
    petal_length = round(random() * 7, 3)
    petal_width = round(random() * 7, 3)
    url = ("http://127.0.0.1:5000/paramspredict?sepal_length={0}"
            "&sepal_width={1}&petal_length={2}&petal_width={3}"
            .format(sepal_length, sepal_width, petal_length, petal_width))
    response = urllib.urlopen(url)
    data = json.loads(response.read())
    return data


def id_predict(id):
    """
    Predicts using the idpredict url.
    """
    url = "http://127.0.0.1:5000/idpredict/{}".format(id)
    response = urllib.urlopen(url)
    data = json.loads(response.read())
    return data


if __name__ == '__main__':
    print "Predicting by passing data in url params"
    for i in range(5):
        print params_predict()
    print "Predicting by passing id on the database"
    for i in range(1, 6):
        print id_predict(i)