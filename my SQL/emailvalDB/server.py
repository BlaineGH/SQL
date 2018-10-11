from flask import Flask, request, redirect, render_template, session, flash
import re
import md5
from mysqlconnection import MySQLConnector
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
NAME_REGEX = re.compile(r'^[a-zA-Z]+$')
app = Flask(__name__)
mysql = MySQLConnector(app,'emaildb')
app.secret_key = 'thesupersecretthatnoneknowsecretdonttell'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/add', methods=['POST'])
def add():
    if len(request.form['first_name'])< 1 or len(request.form['last_name'])< 1 or len(request.form['email'])< 1 or len(request.form['password']) < 1:
        flash("Dont leave anything blank!")
        return redirect('/')
    if not EMAIL_REGEX.match(request.form['email']):
        flash("Invalid Email Address!")
        return redirect('/')
    if not NAME_REGEX.match(request.form['first_name']) or not NAME_REGEX.match(request.form['last_name']):
        flash('Your not a number!')
        return redirect('/')
    if request.form['password'] != request.form['confirmpassword']:
        flash('Passwords do not match')
        return redirect('/')
    query = "SELECT* FROM user WHERE user.email = :email"
    data = {
             'email': request.form['email'],
           }
    user = mysql.query_db(query, data)
    if len(user) != 0:
        flash('You already have an account.')
        return redirect('/')
    else:
        flash('Success!')
        hashed_password = md5.new(request.form['password']).hexdigest()
        query = "INSERT INTO user (first_name, last_name, email, password, created_at, updated_at) VALUE(:first_name, :last_name, :email, :hashed_password, NOW(), NOW())"
        data = {
                'first_name': request.form['first_name'],
                'last_name': request.form['last_name'],
                'email': request.form['email'],
                'hashed_password': hashed_password,
               }
        mysql.query_db(query, data)
        return redirect('/post')

@app.route('/signin', methods=['POST'])
def signin():
    email = request.form['email']
    password = request.form['password']
    if len(request.form['email'])< 1 or len(request.form['password']) < 1:
        flash("Dont leave anything blank!")
        return redirect('/')
    query = "SELECT* FROM user WHERE user.email = :email"
    data = {
             'email': email,
           }
    user = mysql.query_db(query, data)
    session['email'] = request.form['email']
    if len(user) != 0:
        hashed_pw2 = md5.new(password+user[0]).hexdigest()
        if user[0]['password'] == hashed_pw2:
            session['id'] = user[0]['id']
            session['name'] = user[0]['first_name']
        return redirect('/post')
    else:
        flash("email or password invalid")
        reurn redirect('/')

@app.route('/post')
def post():
	return render_template('post.html')
app.run(debug=True)