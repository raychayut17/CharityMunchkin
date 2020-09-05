from flask import Flask, redirect, url_for, render_template, request, session, flash, jsonify
from datetime import timedelta
import stripe
import os
from dotenv import load_dotenv, find_dotenv
from flask_sqlalchemy import SQLAlchemy

# Init
app = Flask(__name__)
app.secret_key = "ILoveMyLittleSister"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.sqlite3'	#users is table name
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.permanent_session_lifetime = timedelta(days=30)	# Dictates how long a session stays

load_dotenv(find_dotenv())
# Set your secret key. Remember to switch to your live secret key in production.
# See your keys here: https://dashboard.stripe.com/account/apikeys
stripe.api_key = 'sk_test_51HO2oqD7FF1qp64AlhHD6g4KbhjYtO49Z819Si5v6u4pOgJO1cdVGREIOfE0fVHhMq6suQoFPzocILy5B3JBE80J00KsLvbaOM'

@app.route('/create-checkout-session', methods=['POST', 'GET'])
def create_checkout_session():
	session = stripe.checkout.Session.create(
		payment_method_types=['card'],
		line_items=[{
			'price_data': {
				'currency': 'usd',
					'product_data': {
						'name': 'Donate $1',
					},
				'unit_amount': 100,
			},
		'quantity': 1,
		}],
		mode='payment',
		success_url='https://example.com/success',
		cancel_url='https://example.com/cancel',
	)
	return jsonify(id=session.id)

@app.route('/create-checkout-session5', methods=['POST', 'GET'])
def create_checkout_session5():
	session = stripe.checkout.Session.create(
		payment_method_types=['card'],
		line_items=[{
			'price_data': {
				'currency': 'usd',
					'product_data': {
						'name': 'Donate $1',
					},
				'unit_amount': 500,
			},
		'quantity': 1,
		}],
		mode='payment',
		success_url='https://example.com/success',
		cancel_url='https://example.com/cancel',
	)
	return jsonify(id=session.id)

@app.route('/create-checkout-session10', methods=['POST', 'GET'])
def create_checkout_session10():
	session = stripe.checkout.Session.create(
		payment_method_types=['card'],
		line_items=[{
			'price_data': {
				'currency': 'usd',
					'product_data': {
						'name': 'Donate $1',
					},
				'unit_amount': 1000,
			},
		'quantity': 1,
		}],
		mode='payment',
		success_url='https://example.com/success',
		cancel_url='https://example.com/cancel',
	)
	return jsonify(id=session.id)

db = SQLAlchemy(app)
class users(db.Model):
	_id = db.Column("id", db.Integer, primary_key=True)
	name = db.Column(db.String(100))
	score = db.Column(db.Integer)

	def __init__(self, name, score):
		self.name = name
		self.score = score

# Page Connections
@app.route("/index")
@app.route("/")
def home():
	return render_template("index.html")

@app.route("/ad", methods=["POST", "GET"])
def ad():
	if request.method == "POST":
		session.permanent = True	# Will last as long as we dictates
		user = request.form["nm"]
		session["user"] = user

		found_user = users.query.filter_by(name=user).first()	# to delete, use .delete() instead of .first()
		if found_user:
			session["user"] = found_user.name
		else:
			'''if "user" in session:
				found_user.name = session["user"]
				db.session.commit()'''
			'''else:'''
			usr = users(user, 0)
			db.session.add(usr)
			db.session.commit()

		flash("Login Successful")
		return redirect(url_for("ad"))
	else:
		if "user" in session:
			found_user = users.query.filter_by(name=session["user"]).first()
			flash("Already Logged in")
			print(found_user.name, found_user.score)
			return render_template("ad.html", user=session["user"], score=found_user.score)
		return render_template("ad.html")

@app.route("/about")
def about():
	return render_template("about.html")

if __name__ == "__main__":
	db.create_all()
	app.run(debug=True)