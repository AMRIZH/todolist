from flask import Flask, render_template, request, redirect, session, url_for
from flask_scss import Scss
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

# initiate flask app
app = Flask(__name__)
app.secret_key = 'yoursecretkey' # secret key for session
Scss(app, static_dir='static', asset_dir='assets') # initiate scss

# initiate database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mylist.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False # turn off the modification tracker
db = SQLAlchemy(app)

# set up class for the database
# data class ~ table
class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(100), nullable=False)
    completed = db.Column(db.Integer, default=0)
    created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self): # primary key of the table
        return f'Task {self.id}'

class Items(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(100), nullable=False)
    completed = db.Column(db.Integer, default=0)
    created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self): # primary key of the table
        return f'Item {self.id}'

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    password_hash = db.Column(db.String(200), nullable=False)

    def __repr__(self):
        return f'User {self.id}'

    def set_password(self, password): # hash the password
        self.password_hash = generate_password_hash(password)

    def check_password(self, password): # check the password
        return check_password_hash(self.password_hash, password)

with app.app_context(): 
    db.create_all() # create the database
        
# define app routes or url paths
# task page
@app.route('/task', methods=['GET', 'POST'])
def taskpage():
    # add task
    if request.method == 'POST':
        task_content = request.form['content'] # get the content from the form
        new_task = Task(content=task_content) # create a new task

        try:
            db.session.add(new_task) # establish connection with database and add the new task
            db.session.commit() # commit the changes
            return redirect('/task') # redirect to the task page
        except Exception as e:
            print(f"Error: {e}")
            return 'There was an issue adding your task'
    # see all current task
    else:
        tasks = Task.query.order_by(Task.created).all() # get all the tasks from the database
        return render_template('task.html', tasks=tasks) # render the task page with the tasks 
    # return render_template('task.html')

# delete task
@app.route('/delete/<int:id>')
def delete(id: int):
    delete_task = Task.query.get_or_404(id) # get the task to delete
    try:
        db.session.delete(delete_task) # delete the task
        db.session.commit() # commit the changes
        return redirect('/task') # redirect to the task page
    except Exception as e:
        print(f"Error: {e}")
        return 'There was a problem deleting that task'
    
# update task
@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id: int):
    task = Task.query.get_or_404(id) # get the task to update
    if request.method == 'POST':
        task.content = request.form['content'] # get the new content
        try:
            db.session.commit() # commit the changes
            return redirect('/task') # redirect to the task page
        except Exception as e:
            print(f"Error: {e}")
            return 'There was an issue updating your task'
    else:
        return render_template('update.html', task=task)

# ===============================================
# To buy list
@app.route('/buy', methods=['GET', 'POST'])
def buyPage():
    # add item
    if request.method == 'POST':
        item_content = request.form['content'] # get the content from the form
        new_item = Items(content=item_content) # create a new buy

        try:
            db.session.add(new_item) # establish connection with database and add the new buy
            db.session.commit() # commit the changes
            return redirect('/buy') # redirect to the buy page
        except Exception as e:
            print(f"Error: {e}")
            return 'There was an issue adding the item'
    # see all current item
    else:
        items = Items.query.order_by(Items.created).all() # get all the items from the database
        return render_template('buy.html', items=items) # render the buy page with the items 

# delete task
@app.route('/deleteitem/<int:id>')
def deleteitem(id: int):
    delete_item = Items.query.get_or_404(id) # get the item to delete
    try:
        db.session.delete(delete_item) # delete the item
        db.session.commit() # commit the changes
        return redirect('/buy') # redirect to the buy page
    except Exception as e:
        print(f"Error: {e}")
        return 'There was a problem deleting that item'
    

# edit item
@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id: int):
    item = Items.query.get_or_404(id) # get the item to edit
    if request.method == 'POST':
        item.content = request.form['content'] # get the new content
        try:
            db.session.commit() # commit the changes
            return redirect('/buy') # redirect to the buy page
        except Exception as e:
            print(f"Error: {e}")
            return 'There was an issue editing your item'
    else:
        return render_template('edit.html', item=item)

# ===============================================
# auth page
@app.route('/')
def home():
    if 'username' in session:
        print(f'You are logged in as {session["username"]}')
        return redirect(url_for('dashboard'))
    return render_template('index.html')

# login and register
@app.route('/login', methods=['GET', 'POST'])
def login_register():
    if request.method == 'POST': # check if the form is submitted
        action = request.form['action']
        username = request.form['username']
        password = request.form['password']

        if action == 'login': # check if the action is login
            # check if the user exists and the password is correct
            user = User.query.filter_by(username=username).first()
            if user and user.check_password(password): 
                session['username'] = username
                session['user_id'] = user.id
                return redirect(url_for('dashboard'))
            return render_template('login.html', message='Invalid username or password')
        elif action == 'register': # check if the action is register
            # check if the username already exists
            user = User.query.filter_by(username=username).first()
            if user:
                return render_template('login.html', message='Username already exists')
            else: # create a new user
                new_user = User(username=username)
                new_user.set_password(password)
                db.session.add(new_user)
                db.session.commit()
                session['username'] = username # add the username to the session
                session['user_id'] = new_user.id # add the user_id to the session
                return redirect(url_for('dashboard'))
    return render_template('login.html') # render the login page

# dashboard
@app.route('/dashboard')
def dashboard():
    if 'username' in session: # check if the user is logged in
        return render_template('dashboard.html', username=session['username']) # render the dashboard
    return redirect(url_for('home')) # redirect to the index page

# logout
@app.route('/logout')
def logout():
    session.pop('username', None) # remove the username from the session
    session.pop('user_id', None) # remove the user_id from the session
    return redirect(url_for('home')) # redirect to the index page

# run the app
if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=80)
