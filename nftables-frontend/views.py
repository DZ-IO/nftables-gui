import json
import requests
from flask import Blueprint, render_template, flash, redirect, url_for
from flask_login import login_user, logout_user, login_required, current_user
from models import Table, User
from forms.forms import LoginForm, CreateUserForm
from service import db

visualization_bp = Blueprint('visualization', __name__)
creation_bp = Blueprint('creation', __name__)

@visualization_bp.route('/list_ruleset')
def list_ruleset():
    response = requests.get('http://127.0.0.1:8000/tables/list_ruleset')
    result = format_nftables_config(response.json()["ruleset"])
    
    return render_template('ruleset.html', ruleset=result)

@visualization_bp.route('/')
def main_view():
    if current_user.is_authenticated:
        return render_template('main.html', current_user=current_user)
    else:
        form = LoginForm()
        return render_template('login.html', form=form)
    
@visualization_bp.route('/users', methods=['GET'])  
def users():
    users = User.query.all()
    return render_template('users.html', users=users)

@visualization_bp.route('/login')
def login_view():
    form = LoginForm()
    return render_template('login.html', form=form)

@visualization_bp.route('/tables')
def tables():
    response = requests.get('http://127.0.0.1:8000/tables/list_tables')
    result = response.json()["tables"]
    family = []
    names = []
    for line in result.split("table "):
        family.append(line.split(" ")[0])
        variable = line.split(" ")[-1]
        names.append(variable)
    print(names[1])
    for i in range(len(names)):
        if(i != 0):
            Table(name=names[i], family=family[i]).save()
    return render_template('tables.html', names=names, family=family, n=len(names))



@creation_bp.route('/login', methods=['POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        print('Validating login form...')
        user = User.query.filter_by(username=form.username.data).first()
        if user is not None and user.check_password(form.password.data):
            login_user(user)
            flash('Logged in successfully.')
            return redirect('/')
        else:
            form.validate_username(form.username)
            flash('Invalid username or password.')
    else:
        print('Invalid username or password.')
        print(form.errors)
        flash('Invalid username or password.')
    return render_template('login.html', form=form)

def format_nftables_config(config_string):
    # Replace escape sequences with actual characters
    formatted_string = config_string.replace('\\n', '\n').replace('\\t', '\t')

    # Split the string into lines
    lines = formatted_string.split('\n')

    # Remove empty lines
    lines = [line for line in lines if line.strip() != '']

    # Join the lines back together with newline characters
    formatted_string = '\n'.join(lines)
    return formatted_string

@visualization_bp.route('/create_user')
def create_user():
    
    return render_template('create_user.html', form=CreateUserForm())

@creation_bp.route('/create_user', methods=['POST'])
def create_user_post():
    form = CreateUserForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data, password=form.password.data, role=form.role.data, is_active=True)
        db.session.add(user)
        db.session.commit()
        flash('User created successfully.')
        return redirect('/users')
    else:
        flash('Error creating user.')
        print(form.errors)
        return render_template('create_user.html', form=form)

@creation_bp.route("/logout")
def logout():
    '''Cerrar sesión'''
    logout_user()
    return redirect('/')
    
