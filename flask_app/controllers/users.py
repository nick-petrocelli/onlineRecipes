from flask import render_template, redirect, session, request, flash
from flask_app import app
from flask_app.models.user import User
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt(app)

# # USER SET UP # #

#Display form
@app.route('/')
def logreg_form():
    return render_template('logreg.html')

#Register Route
@app.route('/register', methods=["POST"])
def register_process():
    if not User.validate_user(request.form):
        return redirect('/')
    pw_hash = bcrypt.generate_password_hash(request.form['password'])
    updated_form =  {
        # **request.form
        "first_name" : request.form['first_name'],
        "last_name" : request.form['last_name'],
        "email" : request.form['email'],
        "password" : pw_hash
    }
    user_id = User.save(updated_form)

    session['user_id'] = user_id
    return redirect('/recipes')

#Login Route
@app.route('/login', methods=['POST'])
def login_process():
    potential_user = User.get_by_email(request.form['email'])

    if not potential_user:
        flash('Invalid email/password', 'login')
        return redirect('/')
    
    if not bcrypt.check_password_hash(potential_user.password, request.form['password']):
        flash('Invalid email/password', 'login')
        return redirect('/')
    
    session['user_id'] = potential_user.id
    
    return redirect('/recipes')


@app.route('/logout')
def clear_session():
    session.clear()
    return redirect('/')
