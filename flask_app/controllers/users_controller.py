# Routing - Mail Sorting room 
from flask_app import app
from flask import render_template, request, redirect, flash, session
from flask_app.models.user_model import User
from flask_app.models.restaurant_model import Restaurant
from flask_bcrypt import Bcrypt        
bcrypt = Bcrypt(app) 



# ============================ Login Page ============================
@app.route("/")
def index():
    return render_template("index.html")

#------------------- REGISTER Method - Action Routes  ------------------------------
@app.route('/users/register', methods=['post'])
def user_reg():
    #  import request, and redirect
    print(f'\n***********\n  {request.form} \n ************* \n')
    if not User.validate(request.form):
        return redirect('/')
    
    #1 hash the password 
    hashed_pw = bcrypt.generate_password_hash(request.form['password'])
    #2 get the data dictionary ready with the hashed Password
    data = {
        # 'first_name': request.form['first_name']
        **request.form,
        'password': hashed_pw
    }
    #3 pass the data dictionary to the User constructor.
    user_id = User.create(data)
    #4 Store user_id in session
    session['user_id'] = user_id
    return redirect('/dashboard')



#--------------------- Dashboard - View Routes -----------------------------
@app.route('/dashboard')
def dash():
    #Route Guard
    if 'user_id' not in session:
        return redirect('/')
    #grab the user
    data = {
        'id' : session['user_id']
    }
    logged_user = User.get_by_id(data)

    #get all the recipes
    all_restaurants = Restaurant.get_all()
    return render_template('dashboard.html', logged_user=logged_user, all_restaurants = all_restaurants)



#--------Log Out ------------------------------------------------------------
@app.route('/logout')
def logout():
    # del session['user_id']
    session.clear()
    return redirect('/')

#--------LOG IN --------------------------------------------------------------
@app.route('/users/login', methods=['post'])
def login():
    data = {
        'email' : request.form['email']
    }
    user_in_db = User.get_by_email(data)
    #if email not found
    if not user_in_db:
        flash('invalid credentials', 'log')
        return redirect('/')
    #Check Password
    if not bcrypt.check_password_hash(user_in_db.password, request.form['password']):
        flash('invalid credentials', 'log')
        return redirect('/')
    
    session['user_id'] = user_in_db.id
    return redirect('/dashboard')

