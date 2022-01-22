import os
import functools
import json
import requests
from flask import Flask, render_template, redirect, url_for, request, session, flash, g
from flask_migrate import Migrate
from werkzeug.security import generate_password_hash, check_password_hash


def create_app(test_config=None):
	app = Flask(__name__)
	app.config.from_mapping(
		SECRET_KEY=os.environ.get('SECRET_KEY', default='dev'),
	)

	if test_config is None:
		app.config.from_pyfile('config.py', silent=True)
	else:
		app.config.from_mapping(test_config)

	from .models import db, User, Team, Player

	db.init_app(app)
	migrate = Migrate(app,db)

	def require_login(view):
		@functools.wraps(view)
		def wrapped_view(**kwargs):
			if not g.user:
				return redirect(url_for('log_in'))
			return view(**kwargs)
		return wrapped_view

	@app.errorhandler(404)
	def page_not_found(e):
		return render_template('404.html'),404

	@app.before_request
	def load_user():
		user_id = session.get('user_id')
		if user_id:
			g.user = User.query.get(user_id)
		else:
			g.user = None

	@app.route('/sign_up', methods=('GET', 'POST'))
	def sign_up():
		if request.method == 'POST':
			username = request.form['username']
			password = request.form['password']
			error = None

			if not username:
				error = 'Username is required.'
			elif not password:
				error = 'Password is required.'
			elif User.query.filter_by(username=username).first():
				error = 'Username is already taken.'

			if error is None:
				user = User(username=username, password=generate_password_hash(password))
				db.session.add(user)
				db.session.commit()
				flash("Successfully signed up! Please log in.", 'success')
				return redirect(url_for('log_in'))

			flash(error, 'error')
		return render_template('sign_up.html')

	@app.route('/log_in', methods=('GET', 'POST'))
	def log_in():
		if request.method == 'POST':
			username = request.form['username']
			password = request.form['password']
			error = None
			user = User.query.filter_by(username=username).first()
			
			if not user or not check_password_hash(user.password, password):
				error = 'Username or password are incorrect'

			if error is None:
				session.clear()
				session['user_id'] = user.id
				return redirect(url_for('index'))

			flash(error, category='error')
		return render_template('log_in.html')

	@app.route('/log_out', methods=('GET', 'DELETE'))
	def log_out():
		session.clear()
		flash('Successfully logged out.', 'success')
		return redirect(url_for('log_in'))

	@app.route('/')
	def index():
		return redirect(url_for('team_index'))

	@app.route('/teams')
	def team_index():
		return render_template('team_index.html', teams=db.session.query(Team).all())

	@app.route('/teams/<team_id>/edit', methods=('GET', 'POST', 'PATCH'))
	def team_view(team_id):
		return render_template('team_view.html', players=db.session.query(Player).filter_by(team_id=team_id))

	
	@app.route('/teams/<team_id>/delete', methods=('GET', 'DELETE'))
	@require_login
	def team_delete(team_id):
		team = Team.query.filter_by(id=team_id).first_or_404()
		db.session.delete(team)
		db.session.commit()
		flash(f"Successfully deleted team: '{team.name}'", 'success')
		return redirect(url_for('team_index'))
	
	@app.route('/sync', methods=('GET','POST'))
	@require_login
	def sync_data():
		error = None
		if request.method == 'POST':
			if request.form['submit_button'] == 'Teams':
				url = "https://api-nba-v1.p.rapidapi.com/teams/league/standard?season=2021"
				headers = {
					'x-rapidapi-host': "api-nba-v1.p.rapidapi.com",
					'x-rapidapi-key': "4c35093009mshbfaeb92ef632ff8p108b6ejsnbce105f84548"
					}

				response = requests.get(url, headers=headers)
				jsonResponse = response.json()
				for team in jsonResponse["api"]["teams"]:
					if team["nbaFranchise"] == '1' and team["allStar"] == '0':
						id = int(team["teamId"])
						full_name = team["fullName"]
						abbreviation = team["shortName"]
						nickname = team["nickname"]
						city = team["city"]
						logo = team["logo"]
						conf_name = team["leagues"]["standard"]["confName"]
						div_name = team["leagues"]["standard"]["divName"]
						team = Team(id=id, full_name=full_name, abbreviation=abbreviation, nickname=nickname, city=city, logo=logo, conf_name=conf_name, div_name=div_name)
						db.session.add(team)
						db.session.commit()

						
				flash(f"Successfully synced teams", 'success')
				return redirect(url_for('team_index'))
			
			if request.form['submit_button'] == 'Players':
				url = "https://api-nba-v1.p.rapidapi.com/players/league/standard"

				headers = {
					'x-rapidapi-host': "api-nba-v1.p.rapidapi.com",
					'x-rapidapi-key': "4c35093009mshbfaeb92ef632ff8p108b6ejsnbce105f84548"
					}
				response = requests.get(url, headers=headers)
				jsonResponse = response.json()

				for player in jsonResponse["api"]["players"]:
					if player["teamId"] != None and player["dateOfBirth"] >= '1977-01-01' and player["yearsPro"] >= '1' and player["leagues"]["standard"]["active"]=='1':
						firstName = player["firstName"]
						lastName = player["lastName"]
						db_player_obj=db.session.query(Player).filter(Player.firstName==firstName, Player.lastName==lastName).first()
						h_float = float(player["heightInMeters"])
						h_us = h_float * 3.28084
						height = str(h_us)
						db_player_obj.h = height
						flash(db_player_obj.h, 'error')

						'''
						firstName = player["firstName"]
						lastName = player["lastName"]
						height = int(float(player["heightInMeters"]) * 3.28084)
						weight = int(float(player["weightInKilograms"]) * 2.20462)
						country = player["country"]
						college = player["collegeName"]
						years_pro = player["yearsPro"]
						position = player["leagues"]["standard"]["pos"]
						jersey = player["leagues"]["standard"]["jersey"]
						team_id = int(player["teamId"])
						player = Player(firstName=firstName, lastName=lastName, height=height, weight=weight, country=country, college=college, years_pro=years_pro, position=position, jersey=jersey, team_id=team_id)
						db.session.add(player)
						'''
						db.session.commit()
						flash(db_player_obj.h, 'error')

			flash(error, 'error')
		return render_template('sync.html')

	return app
