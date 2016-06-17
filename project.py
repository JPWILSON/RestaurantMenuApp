import sys 
import os 
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem

from flask import Flask, render_template, url_for, request, redirect, flash, jsonify

engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind = engine)
session = DBSession()

app = Flask(__name__)

@app.route("/restaurants/<int:rest_id>/menu/JSON/")
def menuJSON(rest_id):
	restaurant = session.query(Restaurant).filter_by(id = rest_id).one()
	items = session.query(MenuItem).filter_by(restaurant_id = rest_id).all()
	return jsonify(MenuItems = [i.serialize for i in items])

@app.route("/restaurants/<int:rest_id>/menu/<int:item_id>/JSON/")
def itemJSON(rest_id, item_id):
	menuItem = session.query(MenuItem).filter_by(id = item_id).one()
	return jsonify(MenuItem = menuItem.serialize)

@app.route("/")
@app.route("/restaurants/")
def restaurants():
	restaurants = session.query(Restaurant).all()
	return render_template('restaurants.html', restaurants = restaurants)

@app.route("/restaurants/<int:rest_id>/menu")
def menu(rest_id):
	restaurant = session.query(Restaurant).filter_by(id= rest_id).one()
	items = session.query(MenuItem).filter_by(restaurant_id = rest_id).all()
	return render_template('menu.html', restaurant = restaurant, items = items)

@app.route("/restaurants/<int:rest_id>/newItem/", methods = ['GET', 'POST'])
def newItem(rest_id):
	restaurantery = session.query(Restaurant).filter_by(id = rest_id).one()
	if request.method == 'POST':
		newItem = MenuItem(name = request.form['name'], price = request.form['price'], 
			description = request.form['description'], restaurant_id = rest_id)
		session.add(newItem)
		session.commit()
		flash("New menu item: '%s' created!" % newItem.name)
		return redirect(url_for('menu', rest_id = rest_id))
	else:
		return render_template('newItem.html', restaurant = restaurantery)
@app.route("/restaurants/<int:rest_id>/<int:item_id>/editItem/", methods = ['GET', 'POST'])
def editItem(rest_id, item_id):
	restaurant = session.query(Restaurant).filter_by(id = rest_id).one()
	itemToEdit = session.query(MenuItem).filter_by(id = item_id).one()
	if request.method == 'POST':
		if request.form['name']:
			itemToEdit.name = request.form['name']
			itemToEdit.price = request.form['price']
			itemToEdit.description = request.form['description']
			session.add(itemToEdit)
			session.commit()
			flash("Menu item '%s' was edited" %itemToEdit.name)
			return redirect(url_for('menu', rest_id = rest_id))
	else:
		return render_template('editItem.html', rest = restaurant, item = itemToEdit)

@app.route("/restaurants/<int:rest_id>/<int:item_id>/deleteItem/", methods = ['GET', 'POST'])
def deleteItem(rest_id, item_id):
	restaurant = session.query(Restaurant).filter_by(id = rest_id).one()
	itemToDelete = session.query(MenuItem).filter_by(id = item_id).one()
	if request.method == 'POST':
		session.delete(itemToDelete)
		session.commit()
		flash("'%s' was deleted from the menu!" % itemToDelete.name)
		return redirect(url_for('menu', rest_id = rest_id))
	else:
		return render_template('deleteItem.html', rest = restaurant, item = itemToDelete)


if __name__ == '__main__':
	app.secret_key = 'super_secret_key'
	app.debug = True
	app.run(host = '0.0.0.0', port= 5000)

#flash("insert message to flash here")
#get_flashed_messages()