## SI 364
## Winter 2018
## HW 2 - Part 1

## This homework has 3 parts, all of which should be completed inside this file (and a little bit inside the /templates directory).

## Add view functions and any other necessary code to this Flask application code below so that the routes described in the README exist and render the templates they are supposed to (all templates provided are inside the templates/ directory, where they should stay).

## As part of the homework, you may also need to add templates (new .html files) to the templates directory.

#############################
##### IMPORT STATEMENTS #####
#############################
from flask import Flask, request, render_template, url_for, flash, redirect
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, RadioField, ValidationError
from wtforms.validators import Required
import requests
import json
#####################
##### APP SETUP #####
#####################

app = Flask(__name__)
app.config['SECRET_KEY'] = 'hardtoguessstring'

####################
###### FORMS #######
####################
class ArtistForm(FlaskForm):
	name = StringField('Artist to search for:', validators = [Required()])
	submit = SubmitField('Submit')

class AlbumEntryForm(FlaskForm):
	name = StringField('Enter the name of an album:', validators = [Required()])
	rate = RadioField('How much do you like this album?', choices = [('1', '1 (low)'), ('2', '2'), ('3', '3 (high)')])
	submit = SubmitField('Submit')
####################
###### ROUTES ######
####################

@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/user/<name>')
def hello_user(name):
    return '<h1>Hello {0}<h1>'.format(name)

@app.route('/artist-form')
def artist_form():
	simpleForm = ArtistForm()
	return render_template('artistform.html', form = simpleForm)

@app.route('/artistinfo',  methods = ['GET', 'POST'])
def artist_info():

	print(request.args)
	form = ArtistForm(request.args)
	if request.method == 'GET':
		print(form)
		params = {}
		params['term'] = request.args.get('artist')
		params['entity'] = 'musicTrack'
		print(params)
		response = requests.get('https://itunes.apple.com/search', params = params)
		
		results = json.loads(response.text)['results']
		print(results)
		print('hello')
		return render_template('artist_info.html', objects = results)
	flash('All fields are required!')
	return redirect(url_for('artist_form'))

@app.route('/artistlinks')
def artist_links():
	return render_template('artist_links.html')

@app.route('/specific/song/<artist_name>')
def specific_artist(artist_name):
		params = {}
		params['term'] = artist_name
		params['entity'] = 'musicTrack'
		
		response = requests.get('https://itunes.apple.com/search', params = params)
		
		results = json.loads(response.text)['results']
		print(results)
		print('hello')
		return render_template('specific_artist.html', results = results)

@app.route('/album_entry')
def album_entry():
	simpleForm = AlbumEntryForm()
	return render_template('albumform.html', form = simpleForm)

@app.route('/album_result', methods = ['GET', 'POST'])
def album_result():
	form = AlbumEntryForm(request.form)
	if request.method == 'GET':
		rate = request.args.get('rate')
		album = request.args.get('album')
		return render_template('album_result.html', album = album, stars = rate)
	flash('All fields are required!')
	return redirect(url_for('album_entry'))
if __name__ == '__main__':
    app.run(use_reloader=True,debug=True)
