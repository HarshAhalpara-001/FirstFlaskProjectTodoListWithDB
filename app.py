from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    task = db.Column(db.String(100), nullable=False)
    desc = db.Column(db.String(100), nullable=False)
    date = db.Column(db.Date, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return f"Task('{self.task}', '{self.desc}', '{self.date}')"

@app.route("/", methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        task_content = request.form['task']
        task_desc = request.form['desc']
        new_task = Task(task=task_content, desc=task_desc)
        db.session.add(new_task)
        db.session.commit()
        return redirect(url_for('home'))
    
    tasks = Task.query.all()
    return render_template('index.html', tasks=tasks)

@app.route("/delete/<int:id>", methods=['POST'])
def delete(id):
    task_to_delete = Task.query.get_or_404(id)
    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect(url_for('home'))
    except:
        return "There was a problem deleting that task."

if __name__ == "__main__":
    app.run(debug=True)
