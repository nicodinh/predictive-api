import os
from sklearn.externals import joblib

__pickle_dir__ = os.path.join(
		os.path.dirname(os.path.abspath(__file__)),
		"pickle/champion.pkl"
	)

champion = joblib.load(__pickle_dir__) 

