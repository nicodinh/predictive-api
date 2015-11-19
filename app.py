#!flask/bin/python
import numpy as np
import os
from flask import Flask, jsonify, request, make_response
from sklearn.externals import joblib

__pickle_dir__ = os.path.join(
		os.path.dirname(os.path.abspath(__file__)),
		"pickle/champion.pkl"
	)

champion = joblib.load(__pickle_dir__) 
app = Flask(__name__)

@app.route('/predict', methods=['GET'])
def predict():
	sepal_length = request.args.get('sepal_length') 
	sepal_width = request.args.get('sepal_width')
	petal_length = request.args.get('petal_width')
	petal_width =  request.args.get('petal_width')
	
	data = np.array([sepal_length, sepal_width, petal_length, petal_width]).reshape(1,-1)
	pred = champion.predict(data)[0]
	
	prediction = {
	'scored_label': pred,
	'sepal_length': sepal_length,
	'sepal_width' : sepal_width,
	'petal_length' : petal_length,
	'petal_width' : petal_width
	}
	return jsonify(prediction)

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

if __name__ == '__main__':
    app.run(debug=True)