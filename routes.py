from flask import Flask, render_template, request, abort, jsonify
# from flask.ext.sqlalchemy import SQLAlchemyapp
import pickle
import gzip
from sklearn import linear_model
import numpy as np
import articleparser
import readability
import urllib
import lxml
from bs4 import BeautifulSoup

app  = Flask(__name__)

def getObjFromPklz(infilename):
	"""
	get an object file
	"""
	f = gzip.open(infilename, 'rb')
	try:
	    return pickle.load(f)
	finally:
	    f.close()
# (big_data_full, big_words_full, big_tags_full) = getObjFromPklz('read_training.txt')

def writeToPklz(outfilename, obj):
	"""
	Store an object as a file
	"""
	output = gzip.open(outfilename, 'wb')
	try:
		pickle.dump(obj, output, -1)
	finally:
		output.close()

# @app.route('http://biashtx.azurewebsites.net/')
@app.route('/')
def home():
	return render_template('index.html')

def parse_input(input_string):
	"""
	parse input as string or as url
	"""
	if input_string[0:4] == 'http':
		return articleparser.parseArticles([input_string])
	else:
		return input_string

@app.route('/post_data')
def handle_post_data():

	#Receive data from site 

	data = {
	'input' : request.form['input']
	}# format the records you received into list of dictionaries
	handle_get_vector(data['input'])

@app.route('/get_vector')
def handle_get_vector(stringInput):

	#parse the input into text if url
	textInput = parse_input(stringInput)
	#Get vector with our given input data 
	model = getObjFromPklz("clf_model")
	#run our input through our model
	vect = {'rating': predict(model[0],model[1],model[2], textInput)}

	# return dictionary
	return jsonify(rating=vect)


if __name__ == '__main__':
	app.run(debug=True)