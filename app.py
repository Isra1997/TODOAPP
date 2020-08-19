from flask import Flask,render_template,request,jsonify,abort

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
    commpeleted = db.Column(db.Boolean, nullable = False, default = False )
    def reper(self):
        return f'<todo: {self.id}, {self.description}>'



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



@app.route('/')
def index():
    return render_template('index.html',data = Todo.query.all())

