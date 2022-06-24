from flask import Flask, redirect, render_template, request, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
app.secret_key = "abc"
class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)

@app.route("/")
def home():
    tasks = Todo.query.order_by(Todo.date).all()
    return render_template("index.html", tasks=tasks)

@app.route("/get_Task", methods=['POST', 'GET'])
def get_Task():
    if request.method == "POST":
        try:
            if len(request.form['task']) > 200: raise Exception("Please do not exceed 200 characters. . .")
            elif not request.form['task']:
                raise Exception("Please provide a task. . .")

            task = Todo(content=request.form['task'])
            db.session.add(task)
            db.session.commit()
            tasks = Todo.query.order_by(Todo.date).all()
            return redirect("/")
        except Exception as e:
            flash(f"{e}")
            return redirect("/")
        

@app.route("/delete/<int:id>")
def delete(id):
    try:
        task_to_delete = Todo.query.get_or_404(id)
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect("/")
    except:
        return redirect("/errorpage")

@app.route("/update/<int:id>", methods=['POST', 'GET'])
def update(id):
    task_to_update = Todo.query.get_or_404(id)
    if request.method == 'POST':
        try:
            if not request.form['content']: raise Exception("You can't input an empty task. . .")
            if len(request.form['content']) > 200: raise Exception("Please do not exceed 200 characters. . .")

            task_to_update.content = request.form['content']
            db.session.commit()
            return redirect("/")
        except Exception as e:
            flash(f"{e}")
            return render_template("update.html", task=task_to_update)
    else:
        return render_template("update.html", task=task_to_update)


if __name__ == "__main__":
    app.run(debug=True)