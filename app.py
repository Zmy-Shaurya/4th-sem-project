from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
db = SQLAlchemy(app)

class EmailTicket(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    customer_email = db.Column(db.String(120))
    subject = db.Column(db.String(255))
    body = db.Column(db.Text)
    intent = db.Column(db.String(100))
    sentiment = db.Column(db.String(50))
    priority = db.Column(db.String(20))
    ai_draft_reply = db.Column(db.Text)
    status = db.Column(db.String(20), default="Draft")

with app.app_context():
    db.create_all()

@app.route('/')
def home():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)