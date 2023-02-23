from flask import render_template,redirect,session,request, flash
from flask_app import app
from flask_app.models.user import User
from flask_app.models.sighting import Sighting
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

@app.route('/new/sighting')
def new_sighting():
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "id":session['user_id']
    }
    return render_template("report.html",user=User.get_by_id(data))

@app.route('/newreport',methods=['POST'])
def newReport():
    if 'user_id' not in session:
        return redirect('/logout')
    if not Sighting.validate_sighting(request.form):
        return redirect('/new/sighting')
    data = { 
        "location": request.form["location"],
        "happened": request.form["happened"],
        "date": request.form["date"],
        "NumOfSas": int(request.form["NumOfSas"]),
        "user_id": session["user_id"]
    }
    Sighting.save(data)
    return redirect('/dashboard')

@app.route('/edit/sighting/<int:id>')
def edit_sighting(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "id":id
    }
    user_data = {
        "id":session['user_id']
    }
    return render_template("edit.html",edit=Sighting.get_one(data),user=User.get_by_id(user_data))

@app.route('/update/sighting',methods=['POST'])
def update_sighting():
    if 'user_id' not in session:
        return redirect('/logout')
    if not Sighting.validate_sighting(request.form):
        return redirect('/new/sighting')
    data = {
        "location": request.form["location"],
        "happened": request.form["happened"],
        "date": request.form["date"],
        "NumOfSas": int(request.form["NumOfSas"]),
        "user_id": session["user_id"]
    }
    Sighting.update(data)
    return redirect('/dashboard')

@app.route('/sighting/<int:id>')
def show_sighting(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "id":id
    }
    user_data = {
        "id":session['user_id']
    }
    return render_template("show.html",sighting=Sighting.get_one(data),user=User.get_by_id(user_data))

@app.route('/delete/sighting/<int:id>')
def delete_sighting(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "id":id
    }
    Sighting.delete(data)
    return redirect('/dashboard')