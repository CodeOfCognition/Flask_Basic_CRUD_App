from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
#configure and initialize database: 3 / is relative, 4/ is abolute
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)

#creating a model. It's attributes "id", "content", and "date_created" are accessible throughout
class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True) #creates an integer that references each entry
    content = db.Column(db.String(200), nullable=False) #creates a text column which holds text data (to do tasks). nullable means can't leave blank
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    
    #function that returns a string every time we create a new element (returns task and task id)
    def __repr__(self):
        return '<Task %r>' % self.id

@app.route('/', methods=['POST', 'GET']) #Added methods POST and GET to our route
def index():
    if request.method == 'POST': #if the request that is sent to this route
        task_content = request.form['content'] #content is the id of the input which we want contents of (the form input)
        new_task = Todo(content = task_content) #now we've created a todo object

        try:
            #add task object to database and then redirect back to index page
            db.session.add(new_task)
            db.session.commit()
            return redirect('/') 
        except:
            return 'There was an issue adding your task'
    else:
        tasks = Todo.query.order_by(Todo.date_created).all() # orders all tasks by date created and returns them all; .first() returns first
        return render_template('index.html', tasks=tasks)

@app.route('/delete/<int:id>')
def delete(id):
    task_to_delete = Todo.query.get_or_404(id)

    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return 'There was a problem deleting that item'

@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    task = Todo.query.get_or_404(id)

    if request.method == 'POST':
        task.content = request.form['content'] #sets the content of the task

        try:
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue updating the task'

    else:
        return render_template('update.html', task=task)



if __name__ == "__main__":
    app.run(debug=True)