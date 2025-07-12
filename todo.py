from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todos.db'
db = SQLAlchemy(app)


class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    task = db.Column(db.String(200), nullable=False)
    done = db.Column(db.Boolean, default=False)


with app.app_context():
    db.create_all()


@app.route('/api/todos', methods=['GET'])
def get_todos():
    return jsonify([{"id": t.id, "task": t.task, "done": t.done} for t in Todo.query.all()])

@app.route('/api/todos', methods=['POST'])
def create_todo():
    data = request.get_json()
    new_todo = Todo(task=data['task'], done=False)
    db.session.add(new_todo)
    db.session.commit()
    return jsonify({"id": new_todo.id, "task": new_todo.task, "done": new_todo.done}), 201

@app.route('/api/todos/<int:id>', methods=['PUT'])
def update_todo(id):
    data = request.get_json()
    todo = Todo.query.get_or_404(id)
    todo.task = data.get('task', todo.task)
    todo.done = data.get('done', todo.done)
    db.session.commit()
    return jsonify({"id": todo.id, "task": todo.task, "done": todo.done})

@app.route('/api/todos/<int:id>', methods=['DELETE'])
def delete_todo(id):
    todo = Todo.query.get_or_404(id)
    db.session.delete(todo)
    db.session.commit()
    return jsonify({"message": "Deleted"}), 204

if __name__ == '__main__':
    app.run(debug=True)