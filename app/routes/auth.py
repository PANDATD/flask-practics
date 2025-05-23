from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, LoginManager, UserMixin
from app.models import users, User
from app.forms import LoginForm, RegisterForm

auth_bp = Blueprint('auth', __name__)

# Dummy session tracking
class SessionUser(UserMixin):
    def __init__(self, username):
        self.id = username

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.username.data in users:
            flash("Username already exists", "warning")
        else:
            users[form.username.data] = User(form.username.data, form.password.data)
            flash("Registered successfully. Please log in.", "success")
            return redirect(url_for('auth.login'))
    return render_template('auth/register.html', form=form)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = users.get(form.username.data)
        if user and user.check_password(form.password.data):
            login_user(SessionUser(user.username))
            flash("Logged in successfully!", "success")
            return redirect(url_for('main.home'))
        else:
            flash("Invalid username or password", "danger")
    return render_template('auth/login.html', form=form)

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash("Logged out.", "info")
    return redirect(url_for('main.home'))
