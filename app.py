from flask import Flask, render_template, request, redirect, url_for, session, redirect

from flask.helpers import flash
from sqlalchemy import create_engine ,update
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.sql import label
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql.expression import delete, select


app = Flask(__name__)
##postgress

db = SQLAlchemy()
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:0305@localhost:3306/project"
app.config['SECRET_KEY'] = "random string"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config['SQLALCHEMY_ECHO'] = True
db.init_app(app)
class Batch (db.Model):
    __tablename__ = 'batch'
    id = db.Column(db.Integer, primary_key=True)
    batch_title = db.Column(db.String(255), nullable=False)

class Fees (db.Model):
    __tablename__ = 'fees'
    id = db.Column(db.Integer, primary_key=True)
    total_fee = db.Column(db.Integer, nullable=False)
    submitted_fee = db.Column(db.Integer, nullable=False)
    dues_cleared_till = db.Column(db.String(200), nullable=False)
    roll_no = db.Column(db.Integer)
    

class Students (db.Model):
    __tablename__ = 'students'
    ID = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable = False)
    fname = db.Column(db.String(255), nullable = False)
    roll_no = db.Column(db.Integer, primary_key=True)
    batch = db.Column(db.String(200), nullable = False)
    status = db.Column(db.String(20), nullable = False)

@app.route("/", methods=['GET'])
def log():
    return render_template('login.html')

@app.route("/login", methods=['POST','GET'])
def login():
    msg="Login First"
    if request.method == "POST":

        if request.form['username'] == 'admin' and request.form['password'] == 'harry':
            session['logged_in'] = True
            return redirect(url_for('result'))
        else :
            msg = "Incorrect Username and Password"
            return render_template("login.html", msg=msg)
    else:
        return render_template("login.html", msg=msg)

@app.route("/records", methods=['GET'])
def result():
        a = db.session.query(Students.name, Students.fname, Students.roll_no, Students.status, Students.batch, Fees.total_fee, Fees.submitted_fee, Fees.dues_cleared_till,
            label('Remaian', Fees.total_fee - Fees.submitted_fee)).where(Students.roll_no==Fees.roll_no).all()
        return render_template("intro.html", a=a)

@app.route("/insert",methods=['GET','POST'])
def insert():
    if request.method == "POST":

        name = request.form.get("name")
        fname = request.form.get("fname")
        rollno = request.form.get("roll_no")
        batch = request.form.get("batch")
        status = request.form.get("sts")
        # Creat new record
        stud = Students(name = name, fname=fname, roll_no=rollno , batch=batch, status=status)
        db.session.add(stud)
        db.session.commit()
#        a = db.session.query(Students.name, Students.fname, Students.roll_no, Students.status)
#        return render_template("intro.html", a=a)
        return redirect(url_for('insertfee'))

    batch = db.session.query(Batch.batch_title)
    return render_template('insert.html', batch=batch)

@app.route("/student", methods=['GET', 'POST'])
def insertfee():
    if request.method == "POST":
        roll = request.form.get("RN")
        total = request.form.get("TF")
        submit = request.form.get("SF")
        clear = request.form.get("CT")
        stud_exp = Fees(total_fee=total,  submitted_fee=submit, dues_cleared_till=clear, roll_no=roll)
        db.session.add(stud_exp)
        db.session.commit()
        return redirect(url_for('result'))
        

    return render_template("insert_fee.html")


@app.route("/update/<int:roll_no>/", methods=['POST','GET'])
def update(roll_no):
    if request.method == "POST":
        #roll = request.form.get("RN")
        total = request.form.get("TF")
        submit = request.form.get("SF")
        clear = request.form.get("CT")
        a = Fees.query.filter_by(roll_no = roll_no).first()
       # a.roll_2 = roll
        a.total_fee = total
        a.submitted_fee = submit
        a.dues_cleared_till = clear
        db.session.commit()
        return redirect(url_for("result"))
    else:
        a = Fees.query.filter(Fees.roll_no ==roll_no).first()
        return render_template("update.html", a=a , roll_no = roll_no )


             

    

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for('log'))

if __name__ == "__main__":
    app.run(debug=True)