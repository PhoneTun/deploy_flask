from flask_app import app
from flask import render_template,request, redirect,session, flash
from flask_app.models.skeptic import Skeptic




@app.route('/add_skeptic/<int:sighting_id>', methods=['POST'])
def add_skeptic(sighting_id):
    data = {
        'sighting_id': sighting_id,
        'user_id': session['user_id']
    }
    Skeptic.add_skeptic(data)
    return redirect('/dashboard')

@app.route('/remove_skeptic/<int:sighting_id>', methods=['POST'])
def remove_skeptic(sighting_id):
    data = {
        'sighting_id': sighting_id,
        'user_id': session['user_id']
    }
    Skeptic.remove_skeptic(data)
    return redirect('/dashboard')
