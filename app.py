from flask import Flask,render_template,request,jsonify,abort, redirect ,url_for

from flask_sqlalchemy import SQLAlchemy
import sys
from flask_migrate import Migrate

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://israragheb@localhost:5432/todoapp'
db = SQLAlchemy(app)
mirgrate = Migrate(app,db)

class Todo(db.Model):
    __tablename__ = 'todos'
    id = db.Column(db.Integer, primary_key = True)
    description = db.Column(db.String(), nullable = False)
    completed = db.Column(db.Boolean, nullable = False, default = False)
    list_id = db.Column(db.Integer, db.ForeignKey('todolists.id'),nullable=False)
    def reper(self):
        return f'<todo: {self.id}, {self.description}>'

class TodoLists(db.Model):
    __tablename__ = 'todolists'
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(), nullable = False)
    todo = db.relationship('Todo',backref='list',lazy=True)



@app.route('/todos/create',methods=['post'])
def create_todo():
    error = False
    body = {}
    try:
        descr = request.get_json()['description']
        item = Todo(description=descr)
        db.session.add(item)
        db.session.commit()
        body['description'] = item.description
    except:
        error = True
        db.session.rollback()
        print(sys.exc_info())
    finally:
        db.session.close()
    if error:
        abort(400)
    else:
        return jsonify(body)

@app.route('/todos/<todo_id>/update_completed', methods= ['post'])
def update_completed(todo_id):
    try:
        completed = request.get_json()['completed']
        item = Todo.query.get(todo_id)
        item.completed = completed
        db.session.commit()
    except:
        db.session.rollback()
    finally:
        db.session.close()

    return redirect(url_for('index'))

@app.route('/todos/<todo_id>/delete_todo', methods = ['DELETE'])
def delete_todo(todo_id):
    try:
        todo = Todo.query.filter_by(id=todo_id).delete()
        db.session.commit()
    except:
        db.session.rollback()
    finally:
        db.session.close()

    return jsonify({ 'success': "True" })


@app.route('/lists/<list_id>')
def get_list_id(list_id):
    return render_template('index.html',
    lists=TodoLists.query.all(),
    active_list=TodoLists.query.get(list_id),
    todos = Todo.query.filter_by(list_id=list_id).order_by('id').all())

@app.route('/')
def index():
    return redirect(url_for('get_list_id',  list_id=1))

