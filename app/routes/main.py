from flask import Blueprint, render_template, request, flash
from app.forms import ContactForm

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def home():
    return render_template('home.html')

@main_bp.route('/about')
def about():
    return render_template('about.html')

@main_bp.route('/contact', methods=['GET', 'POST'])
def contact():
    form = ContactForm()
    if request.method == 'POST' and form.validate_on_submit():
        flash('Thanks for your message!', 'success')
    return render_template('contact.html', form=form)


@main_bp.route('/dashboard')
def dashboard():
    return render_template('about.html')
