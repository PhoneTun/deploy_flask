from flask_app import app
from flask import render_template,request, redirect,session, flash
from flask_app.models.user import User
from flask_app.models.sighting import Sighting
from flask_app.models.skeptic import Skeptic
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt(app)

@app.route('/')
def index():
    return render_template('login.html')


@app.route('/register', methods=['POST'])
def register():
    if not User.validate_user(request.form):
        print('Fail')
        return redirect('/')
   
    flash('Registration successful!!', 'success')
    pw_hash= bcrypt.generate_password_hash(request.form['password'])
    print(pw_hash)

    data={
        "first_name": request.form['first_name'],
        "last_name": request.form['last_name'],
        "email": request.form['email'],
        "password": pw_hash
    }
    id=User.save(data)
    session['user_id']=id
    return redirect('/')


@app.route('/login', methods=['POST'])
def login():
    user=User.get_by_email(request.form)

    if not user:
        flash("Invalid Email", "login")
        return redirect('/')
    if not bcrypt.check_password_hash(user.password, request.form['password']):
        flash("Invalid Password", "login")
        return redirect('/')
    session['user_id']=user.id
    return redirect('/dashboard')

@app.route('/dashboard')
def welcome():
    if 'user_id' not in session:
        return redirect('/logout')
    data={"id":session['user_id']}
    all_sighting=Sighting.get_all()
    return render_template('wall.html', user=User.get_by_id(data), sightings=all_sighting)


@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')






