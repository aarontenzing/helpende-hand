from flask import Flask, render_template, request, jsonify, redirect, url_for
import numpy as np
from queue_list import add_queue
from read_json import tijden
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

#Initialize database
db = SQLAlchemy()

app = Flask(__name__)
Bootstrap(app)
app.config['CORS_HEADERS'] = 'Access-Control-Allow-Origin'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///klas.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

class  Klas(db.Model):
    cid = db.Column(db.Integer,primary_key=True,autoincrement=True)
    vak = db.Column(db.String(200),nullable=False)
    name = db.Column(db.String(200),nullable=False)

    def __repr__(self):
        return '<Name %r>' % self.cid 

with app.app_context():
    db.create_all()
 
user_list = []
time_list = []
waitlist= []

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/queue",methods=["GET","POST"])
def queue():
    if request.method == "POST":
        cid = request.form["cid"]
        print(user_list)
        add_queue(cid, user_list, time_list)
        return "succes"
    else:
        return render_template('queue.html')
    
@app.route("/values", methods=["GET"])
def get_values():
    if request.method == "GET":
        data = {'users':user_list, 'time':time_list}
        return jsonify(data)
    else:
        return "Not allowed"

@app.route("/class", methods=["POST","GET"])
def create_class():
    if request.method == "POST":  
        return jsonify()
    else:
        return render_template("class_form.html")
    
@app.route("/stats",methods=["GET"])
def stats():
    if request.method == "GET":
        waitlist=tijden()
        print(waitlist)
        return render_template("statistieken.html",waitlist=waitlist)
    else:
        return "Nothing"
    
@app.route("/databank",methods=["POST","GET"])
def databank():
    klaslijst = "Lijst met Studentnamen"

    if request.method == "POST":
        
        new_student = Klas(name=request.form['name'])
        # Push to Database
        #try:
        db.session.add(new_student)
        db.session.commit()
        return redirect(url_for('databank'))
        #except:
         #   return "Error adding student"
    else:
        studenten = db.session.execute(db.select(Klas).order_by(Klas.name)).scalars()
        return render_template("databank.html",title=klaslijst,klas=studenten)

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')


