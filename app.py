from flask import Flask, render_template, request, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(500), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.now)

    def __repr__(self) -> str:
        return f"Todo('{self.title}', '{self.date_created}')"

@app.route("/", methods=['GET', 'POST'])
def hello_world():
    if request.method == "POST":
        todo = Todo(title=request.form['title'], description=request.form['description'])
        db.session.add(todo)
        db.session.commit()
    todos = Todo.query.all()
    return render_template("index.html", allTodo=todos)

@app.route("/delete/<int:id>")
def delete(id):
    todo = Todo.query.get(id)
    if todo:
        db.session.delete(todo)
        db.session.commit()
    return render_template("index.html", allTodo=Todo.query.all())

if __name__ == "__main__":
    app.run(debug=True, port=5000)