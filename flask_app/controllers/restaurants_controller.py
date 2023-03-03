from flask_app import app
from flask import render_template, request, redirect, flash, session
from flask_app.models.restaurant_model import Restaurant
from flask_app.models.user_model import User



#=====================Create - page ================================
@app.route('/restaurants/new')
def new_restaurant():
    if 'user_id' not in session:
        return redirect('/')
    return render_template('new.html')


#=====================Create - POST ================================
@app.route('/restaurants/create', methods=['post'])
def create_restaurants():
    if 'user_id' not in session:
        return redirect('/')
    if not Restaurant.validate(request.form):
        return redirect('/restaurants/new')
    
    restaurant_data = {
        **request.form,
        'user_id': session['user_id']
    }
    Restaurant.create(restaurant_data)
    return redirect('/dashboard')

#=====================Edit PAge  ================================
@app.route('/restaurants/<int:id>/edit')
def edit_restaurant(id):
    if 'user_id' not in session:
        return redirect('/')
    data = {
        'id':id,
        **request.form
    }
    this_restaurant = Restaurant.get_by_id(data)
    return render_template('edit.html', this_restaurant=this_restaurant)

#=====================Edit/update - POST ================================
@app.route('/restaurants/<int:id>/update', methods=['post'])
def update_restaurants(id):
    if 'user_id' not in session:
        return redirect('/')
    if not Restaurant.validate(request.form):
        return redirect('/dashboard')
    data = {
        'id' : id,
        **request.form
    }
    Restaurant.update(data)
    return redirect('/dashboard')

#=====================  Read One  ================================
@app.route('/restaurants/<int:id>')
def show_one_restaurant(id):
    if 'user_id' not in session:
        return redirect('/')
    this_restaurant = Restaurant.get_by_id({'id':id})
    return  render_template('one.html', this_restaurant=this_restaurant)


#=====================  DELETE  ================================
@app.route('/restaurants/<int:id>/delete')
def delete_restaurant(id):
    if 'user_id' not in session:
        return redirect('/')
    Restaurant.delete({'id':id})
    return redirect('/dashboard')

