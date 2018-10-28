from flask import Flask, render_template, request, make_response
from flask import redirect, url_for, jsonify
from werkzeug.security import generate_password_hash, check_password_hash 
from flask_sqlalchemy import SQLAlchemy 
import uuid, jwt, datetime
from functools import wraps


app = Flask(__name__)

app.config['SECRET_KEY'] = 'thisissecret'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////path/to/our db/tode.db'

db = SQLAlchemy(app)
"""
get all commands at README.md"""
class User(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    public_id = db.Column(db.String(50), unique = True)
    name = db.Column(db.String(50))
    password = db.Column(db.String(80))
    admin = db.Column(db.Boolean)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    text = db.Column(db.String(50))
    complete = db.Column(db.Boolean)
    user_id = db.Column(db.Integer)

@app.route("/users", methods = ["GET"])
def get_all_users():
    users = User.query.all()

    output = []
    for user in users:
        user_data = {}
        user_data['public_id'] = user.public_id
        user_data['name'] = user.name
        user_data['password'] = user.password
        user_data['admin'] = user.admin
        
        output.append(user_data)
    return jsonify({'users': output})

@app.route("/user/<public_id>", methods = ['GET'])
def get_one_user(public_id):
    user = User.query.filter_by(public_id = public_id).first()
    if not user:
        return jsonify({'message': 'No User Found'})
    user_data = {}
    user_data['public_id'] = user.public_id
    user_data['name'] = user.name
    user_data['password'] = user.password
    user_data['admin'] = user.admin

    return jsonify({'user' : user_data})

@app.route("/user", methods = ['POST'])
def create_user():
    data = request.get_json()

    hashed_password = generate_password_hash(data['password'], method = 'sha256')
    new_user = User(public_id = str(uuid.uuid4()), name = data['name'], password = hashed_password, admin = False)

    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message':'new user created'})

app.route("/user/<public_id>", methods = ['PUT'])
def promote_user(public_id):})
        
    user = User.query.filter_by(public_id = public_id).first()
    if not user:
        return jsonify({'message': ' User Not Found'}) 
    
    user.admin = True
    db.session.commit()
    return jsonify({'message': 'User Promoted'})


@app.route("/user/<public_id>", methods = ['DELETE'])
def delete_user(create_user, public_id):
    user = User.query.filter_by(public_id = public_id).first()
    if not user:
        return jsonify({'message': ' User Not Found'}) 
    
    db.session.delete(user)
    db.session.commit()
    return jsonify({'message': 'User Deleted'})

@app.route("/login")
def login():
    if check_password_hash(user.password, auth.password):
        token = jwt.encode({'public_id': user.public_id, 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes = 30)}, app.config['SECRET_KEY'])
        return jsonify({'token': token.decode('UTF-8')})
    
    return make_response({'message': 'Authentifacation error'})    


@app.route("/todo", methods = ['GET'])
def get_all_todos():
    todos = Todo.query.all()
    output = []
    for todo in todos:
        todo_data = {}
        todo_data['id'] = todo.id
        todo_data['text'] = todo.text
        todo_data['complete'] = todo.complete

        output.append(todo_data)
    return jsonify({'todos': output})

@app.route("/todo/<todo_id>", methods = ['GET'])
def get_one_todo(todo_id):
    todo = Todo.query.filter_by(id = todo_id).first()

    if not todo:
        return jsonify({'message': 'No Todo Found'})
    todo_data = {}
    todo_data['id'] = todo.id
    todo_data['text'] = todo.text
    todo_data['complete'] = todo.complete
    
    return jsonify(todo_data) 


@app.route("/todo", methods = ['POST'])
@token_required
def create_todo():
    data = request.get_json()

    new_todo = Todo(text = data['text'], complete = False)
    db.session.add(new_todo)
    db.session.commit()
    
    return jsonify({'message': 'Todo Created'})

@app.route("/todo/<todo_id>", methods = ['PUT'])
def complete_todo(todo_id):
    todo = Todo.query.filter_by(id = todo_id).first()

    if not todo:
        return jsonify({'message': 'No Todo Found'})
    todo.complete = True
    db.session.commit()
    
    return  jsonify({'message': 'todo complted'})

@app.route("/todo/<todo_id>", methods = ['GET'])
def delete_todo(todo_id):
    todo = Todo.query.filter_by(id = todo_id).first()

    if not todo:
        return jsonify({'message': 'No Todo Found'})

    db.session.delete(todo)
    db.session.commit()
    
    return jsonify({'message': 'todo deleted'})

if __name__ == "__main__":
    app.run(debug=True)