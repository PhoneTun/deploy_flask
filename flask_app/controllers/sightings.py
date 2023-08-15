from flask_app import app
from flask import render_template,request, redirect,session, flash
from flask_app.models.sighting import Sighting
from flask_app.models.user import User
from flask_app.models.skeptic import Skeptic


@app.route('/new/sighting')
def create():
    if 'user_id'  in session:
        data={"id":session['user_id']}
    # all_posts=Post.get_all()
        return render_template('create.html', user=User.get_by_id(data))
    

@app.route('/sightings/new', methods=['POST'])
def add_sights():
    if not Sighting.validate_sighting(request.form):
        print ("fail")
        return redirect("/new/sighting")
    print(request.form)
    Sighting.save(request.form)
    return redirect('/dashboard')

@app.route('/new/edit/<sighting_id>')
def edit(sighting_id):
    if 'user_id'  in session:
        data={"id":session['user_id']}
    return render_template('update.html', user=User.get_by_id(data), sight=Sighting.get_one(sighting_id))

@app.route('/sightings/update', methods=['POST'])
def edit_recipe():
    print("Form data received:", request.form)
    if not Sighting.validate_sighting(request.form):
        print ("fail")
        return redirect (f"/new/edit/{request.form['id']}")
    print(request.form)
    Sighting.update(request.form)
    return redirect('/dashboard')

@app.route('/show/<sighting_id>')
def view_recipe(sighting_id):
    print(">>>>>>>>>>>>>>>>>>>>>"+sighting_id)
    if 'user_id'  in session:
        data={"id":session['user_id']}
    skeptics = Skeptic.get_skeptics_for_sighting(sighting_id)
    skeptic_ids = [skeptic['id'] for skeptic in skeptics]
    return render_template('view.html', user=User.get_by_id(data), sight=Sighting.get_one(sighting_id), skeptics=skeptics, skeptic_ids=skeptic_ids)

@app.route ('/sight/delete/<sighting_id>')
def delete_post(sighting_id):
    print("Deleting post-", sighting_id)
    Sighting.delete(sighting_id)
    return redirect ("/dashboard") 

    

