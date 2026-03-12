from flask import Flask, render_template, request, redirect, url_for
from models import db, EmailTicket
from ai_service import analyse_email

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

with app.app_context():
    db.create_all()

@app.route('/', methods=["GET","POST"])
def home():
    if request.method=="POST":
        customer_email = request.form["customer_email"]
        subject = request.form["subject"]
        body = request.form["body"]

        ai_result=  analyse_email(body)

        new_ticket= EmailTicket(
            customer_email=customer_email,
            subject=subject,
            body=body,
            intent=ai_result["intent"],
            sentiment=ai_result["sentiment"],
            priority=ai_result["priority"],
            ai_draft_reply=ai_result["draft_reply"]
        )
        db.session.add(new_ticket)
        db.session.commit()
        return redirect(url_for("dashboard"))
    
    return render_template("index.html")

@app.route('/dashboard')
def dashboard():
    query = EmailTicket.query

    priority = request.args.get("priority")
    if priority:
        query = query.filter(EmailTicket.priority.ilike(priority))

    search = request.args.get("search")
    if search:
        query = query.filter(EmailTicket.subject.contains(search))

    tickets = query.order_by(EmailTicket.created_at.desc()).all()

    return render_template("dashboard.html", tickets=tickets)




if __name__ == "__main__":
    app.run(debug=True)