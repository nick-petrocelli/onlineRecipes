from flask import render_template, redirect, session, request, flash
from flask_app import app
from flask_app.models.user import User
from flask_app.models.recipe import Recipe

@app.route('/recipes')
def dashboard_page():
    if not 'user_id' in session:
        return redirect('/')
    logged_user = User.get_one_by_id(session['user_id'])
    recipe_list = Recipe.get_all_with_owner()
    return render_template('dashboard.html', logged_user = logged_user, recipe_list = recipe_list)



@app.route('/recipes/new')
def create_item_page():
    if not 'user_id' in session:
        return redirect('/')
    logged_user = User.get_one_by_id(session['user_id'])
    return render_template('create_recipe.html', logged_user = logged_user)

@app.route('/recipes/new/process', methods=['POST'])
def create_recipe_process():
    if not 'user_id' in session:
        return redirect('/')
    if not Recipe.validate_recipe(request.form):
        return redirect('/recipes/new')
    
    Recipe.save(request.form)
    return redirect('/recipes')



@app.route('/recipes/<int:id>')
def recipe_details(id):
    if not 'user_id' in session:
        return redirect('/')
    logged_user = User.get_one_by_id(session['user_id'])
    recipe_with_owner = Recipe.get_one_with_owner(id)
    return render_template('recipe_details.html', logged_user = logged_user, recipe_with_owner = recipe_with_owner)



@app.route('/recipes/<int:id>/edit')
def recipe_edit_page(id):
    if not 'user_id' in session:
        return redirect('/')
    logged_user = User.get_one_by_id(session['user_id'])

    recipe = Recipe.get_one_with_owner(id)
    return render_template('recipe_edit.html', logged_user = logged_user, recipe = recipe)

@app.route('/recipes/<int:id>/edit/process', methods=['POST'])
def item_edit_process(id):
    if not 'user_id' in session:
        return redirect('/')
    # logged_user = User.get_one_by_id(session['user_id'])
    if not Recipe.validate_recipe(request.form):
        return redirect(f'/recipes/{id}/edit')
    form_with_id = {
        **request.form,
        'id' : id
    }
    Recipe.edit_one(form_with_id)
    return redirect('/recipes')

@app.route('/recipes/<int:id>/delete')
def delete_recipe(id):
    recipe = Recipe.get_one_with_owner(id)
    if recipe.owner_id != session['user_id']:
        flash("Do not touch someone else's recipe")
        return redirect('/recipes')
    Recipe.delete_recipe(id)
    return redirect('/recipes')