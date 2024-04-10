import requests
from flask import Blueprint, render_template, flash, redirect, url_for
from flask_login import login_user, logout_user, login_required, current_user
from models import User
from forms import LoginForm

visualization_bp = Blueprint('visualization', __name__)
creation_bp = Blueprint('creation', __name__)

@visualization_bp.route('/list_ruleset')
def list_ruleset():
    response = requests.get('http://127.0.0.1:8000/list_ruleset')
    result = format_nftables_config(response.json()["ruleset"])
    
    return render_template('ruleset.html', ruleset=result)

@visualization_bp.route('/')
def main_view():
    if current_user.is_authenticated:
        return render_template('main.html', current_user=current_user)
    else:
        form = LoginForm()
        return render_template('login.html', form=form)

@visualization_bp.route('/login', methods=['POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is not None and user.check_password(form.password.data):
            login_user(user)
            flash('Logged in successfully.')
            return redirect('/')
        else:
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

@creation_bp.route('/create_user')
def create_user():
    return render_template('create_user.html')
