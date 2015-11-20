#!flask/bin/python
import numpy as np
import os
import sqlite3
from flask import Flask, jsonify, request, make_response, g
from sklearn.externals import joblib


# Configs
DATABASE = 'iris.db'
DEBUG = True
SECRET_KEY = 'my predictive api'
USERNAME = 'admin'
PASSWORD = 'default'


# Create App
app = Flask(__name__)
app.config.from_object(__name__)


# Get champion from pickle and define predict function
__pickle_dir__ = os.path.join(
		os.path.dirname(os.path.abspath(__file__)),
		"pickle/champion.pkl"
	)
champion = joblib.load(__pickle_dir__) 


def predict(sepal_length, sepal_width, petal_length, petal_width):
	"""Receives params and returns the params and predicted value in a json."""
	data = np.array([sepal_length, sepal_width, petal_length, petal_width]).reshape(1,-1)
	pred = champion.predict(data)[0]
	
	prediction = {
			'label': pred,
			'sepal_length': sepal_length,
			'sepal_width' : sepal_width,
			'petal_length' : petal_length,
			'petal_width' : petal_width
		}
	return prediction


# Data Base connection & decorators
def connect_db():
	"""Connect to the database defined in the config variables."""
	rv = sqlite3.connect(app.config['DATABASE'])
	rv.row_factory = sqlite3.Row
	return rv


@app.before_request
def before_request():
	"""Opens the database connection automatically before requests."""
	g.db = connect_db()


@app.teardown_request
def teardown_request(exception):
	"""Closes the database connection automatically after requests."""
	db = getattr(g, 'db', None)
	if db is not None:
		db.close()


def query_db(query, args=(), one=False):
	"""Wrapper of the database query for better handling."""
	cur = g.db.execute(query, args)
	rv = cur.fetchall()
	cur.close()
	return (rv[0] if rv else None) if one else rv


# API Methods
@app.route('/paramspredict', methods=['GET'])
def paramspredict():
	"""
	Predict using the values in the url params.
	Example: 
	http://127.0.0.1:5000/paramspredict?sepal_length=3.14&sepal_width=2&petal_length=0.4&petal_width=4
	"""
	sepal_length = request.args.get('sepal_length') 
	sepal_width = request.args.get('sepal_width')
	petal_length = request.args.get('petal_length')
	petal_width =  request.args.get('petal_width')
	
	pred = predict(sepal_length, sepal_width, petal_length, petal_width)

	return jsonify(pred)


@app.route('/idpredict/<int:id_setosa>')
def idpredict(id_setosa):
	"""
	Predict using the id in the url and getting the values from the database.
	Example: 
	http://127.0.0.1:5000/idpredict/3
	"""
	setosa = query_db('select * from iris_setosa where id = ?', [id_setosa], one=True)
	if setosa is None:
		return not_found("No existe esa planta.")
	else:
		sepal_length = setosa['sepal_length']
		sepal_width = setosa['sepal_width']
		petal_length = setosa['petal_length']
		petal_width =  setosa['petal_width']
	
		pred = predict(sepal_length, sepal_width, petal_length, petal_width)

		return jsonify(pred)


# Error Handle
@app.errorhandler(404)
def not_found(error):
	"""Returns json instead of HTML in case of 404."""
	message = {
            'status': 404,
            'message': 'Not Found: ' + request.url,
            'error': error}
	resp = jsonify(message)
	return resp


if __name__ == '__main__':
    app.run()