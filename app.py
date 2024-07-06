from flask import Flask, render_template, request, redirect
from flask_scss import Scss
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
# from markupsafe import escape
# initiate flask app
app = Flask(__name__)
Scss(app, static_dir='static', asset_dir='assets') # initiate scss

# initiate database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///task.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# create a class for the database
# data class ~ table
class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(100), nullable=False)
    completed = db.Column(db.Integer, default=0)
    created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self): # primary key of the table
        return f'Task {self.id}'
    
with app.app_context(): 
    db.create_all() # create the database
        
# define app routes or url paths
# home page
@app.route('/')
def hello():
    return render_template('index.html')

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
    
    
# run the app
if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=80)