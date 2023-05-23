from flask_bootstrap import Bootstrap
from flask import Flask, render_template, request, jsonify, redirect, url_for
import numpy as np
from queue_list import add_queue
from read_json import tijden
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
    cid = db.Column(db.Integer,primary_key=True)
    vak = db.Column(db.String(200),primary_key=True,nullable=False)
    name = db.Column(db.String(200), nullable=False)

    def __repr__(self):
        return '<Name %r>' % self.cid 

with app.app_context():
    db.create_all()
 
user_list = []
time_list = []
waitlist= []

filtervak = [""]

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/queue",methods=["GET","POST"])
def queue():
    if request.method == "POST":
        
        if (filtervak[0] == ""): # check of er een vak geselecteerd is
            return "geen vak geselecteerd"
            
        cid = request.form["cid"]
        name_query = db.session.execute(db.select(Klas.name).where(Klas.vak == filtervak[0] and Klas.cid == cid)).scalar()
        
        if (not(name_query)): # check of er een naam in databank staat
            return "geen databank entry"
        
        pressed = int(request.form["button"])
        subject = filtervak[0]
        add_queue(cid, pressed, user_list, time_list, subject)
        return "succes"
    else:
        return render_template('queue.html', subject=filtervak[0])
    
@app.route("/values", methods=["GET"])
def get_values():
    if request.method == "GET":
        names = []
        for i in user_list:
            names.append(Klas.query.filter_by(cid=i, vak=filtervak[0]).with_entities(Klas.name).scalar())
        print(names)
        #querying student name from the database, if no entry NULL
        data = {'users':user_list, 'time':time_list, 'names':names}
        return jsonify(data)
    else:
        return "Not allowed"
    
@app.route("/stats",methods=["GET"])
def stats():
    if request.method == "GET":
        waitlist=[]
        names = []
        return render_template("statistieken2.html",waitlist=waitlist, names=names)
    else:
        return "Nothing"
    
@app.route('/update',methods=["POST","GET"])
def update():
    if request.method == "GET":
        table_klas = db.session.execute(db.select(Klas).order_by(Klas.vak,Klas.cid)).scalars()
        print('tabel: ',table_klas)
        return render_template('update.html',title='Update databank',klas=table_klas)

    if request.method == "POST":
        update_student_cid = request.form.getlist('cid')
        update_student_vak= request.form.getlist('vak')
        update_student_naam = request.form.getlist('naam')

        print("lijst met cids:" ,update_student_cid)
        print("lijst met vak:" ,update_student_vak)
        print("lijst met naam:" ,update_student_naam)

        #db.session.drop(Klas)
        Klas.__table__.drop(db.engine)
        Klas.__table__.create(db.engine)
        for i in range(len(update_student_cid)):
            if(update_student_cid[i] == '' or update_student_vak[i] == '' or update_student_naam[i] == ''):
                print('Index {} Overslaan'.format(i))
                pass
            else:
                new_student = Klas(cid=int(update_student_cid[i]), name=str(update_student_naam[i]), vak = str(update_student_vak[i]))
                db.session.add(new_student)
                db.session.commit()
                print('succes')
       
        return redirect(url_for('databank'))

@app.route("/databank",methods=["POST","GET"])
def databank():
    klaslijst = "Lijst met Studentnamen"

    if request.method == "POST":
        if(request.form['subject']!='Kies een vak'):
            
            # Bekijk laatste id 
            last_id = db.session.execute(db.select(Klas.cid).where(Klas.vak == request.form['subject'] ).order_by(Klas.cid.desc())).scalar()
            #print("laatste id: ", last_id)
            if last_id == None:
                curr_id = 1
            else:
                curr_id = last_id + 1
            new_student = Klas(cid=curr_id, name=request.form['name'], vak = request.form['subject'])
            db.session.add(new_student)
            db.session.commit()
            
        else:
            print("leeg")
        return redirect(url_for('databank'))
    else:
        studenten = db.session.execute(db.select(Klas).order_by(Klas.vak,Klas.cid)).scalars()
        return render_template("databank.html",title=klaslijst,klas=studenten)

@app.route("/selvak",methods=["POST"])
def selectvak():
    if request.method == "POST":
        if request.form['vak'] == "Vakken":
            filtervak[0] = ""
        else:
            filtervak[0] = str(request.form['vak'])
            
        #print(filtervak)
        # Not working trying to select class en putting it in global var. (so /value can query right class)
        # Need to fix when creating< table -> different tables for every subject
        return render_template('queue.html', subject=filtervak[0])
    
@app.route("/selvak2",methods=["POST"])
def selectvak2():
    if request.method == "POST":

        if request.form['vak'] == "Vakken":
            filtervak[0] = ""
        else:
            filtervak[0] = str(request.form['vak'])
        
        waitlist = tijden(filtervak[0]) # gaat entries halen die het juist vak bevatten
        
        distinct_cid = []
        names = []
    
        distinct_cid= list(set(unique['cid'] for unique in waitlist))
        
        for i in distinct_cid:
            #print("uniek cid: ", i)
            names.append(Klas.query.filter_by(cid=int(i), vak=filtervak[0]).with_entities(Klas.name).scalar())
            #print("names: ", names) 
            #print("finaal_names: ", names) 
        
        if (len(waitlist) == 0): # waneer er geen data is geen subject title
            filtervak[0] = ""
            
        return render_template("statistieken2.html",waitlist=waitlist, names=names, subject=filtervak[0])
        
        # Not working trying to select class en putting it in global var. (so /value can query right class)
        # Need to fix when creating< table -> different tables for every subject

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')
