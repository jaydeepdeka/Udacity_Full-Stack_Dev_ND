from flask import Flask, render_template, request, redirect, url_for, jsonify, abort
from flask_sqlalchemy import SQLAlchemy
import sys
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@localhost:\
    5432/todoapp'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# createdb  -h localhost -p 5432 -U postgres todoapp

class ToDoApp(db.Model):
    __tablename__ = 'todo'
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(), nullable=False)

    def __repr__(self):
        return f'<Todo ID: {self.id}, Description: {self.name}>'

db.create_all()
@app.route('/')
def index():
    return render_template('index.html', data=ToDoApp.query.all())

@app.route('/todos/create', methods=['POST'])
def create_todo():
    error = False
    body = {}
    try:
        # description = request.form.get('description', '')
        description = request.form.get_json()['description']
        todo = ToDoApp(description=description)
        db.session.add(todo)
        db.session.commit()
        body['description'] = todo.description
    except:
        db.session.rollback()
        error = True
        print(sys.exc_info())
    # return redirect(url_for('index'))
    finally:
        db.session.close()
    if not error:
        return jsonify(body)
    else:
        abort (400)

if __name__ == '__main__':
    app.run()