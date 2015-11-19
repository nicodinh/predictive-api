import urllib, json
from random import random

def predict():
	sepal_length = round(random()*7, 3)
	sepal_width = round(random()*7, 3)
	petal_length = round(random()*7, 3)
	petal_width = round(random()*7, 3)
	url = "http://127.0.0.1:5000/predict?sepal_length={0}&sepal_width={1}&petal_length={2}&petal_width={3}".format(sepal_length,sepal_width,petal_length,petal_width)
	response = urllib.urlopen(url)
	data = json.loads(response.read())
	return data

if __name__ == '__main__':
	for i in range(10):
		print predict()
