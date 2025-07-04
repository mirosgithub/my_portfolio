from flask import Flask, render_template, flash, redirect, url_for
from config import PERSONAL_INFO, PROJECTS_DATA, SECRET_KEY
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, EmailField
from wtforms.validators import InputRequired

app = Flask(__name__)
app.config['SECRET_KEY'] = SECRET_KEY

class ContactForm(FlaskForm):
    name = StringField('Name', validators=[InputRequired()])
    email = EmailField('Email', validators=[InputRequired()])
    message = TextAreaField('Message', validators=[InputRequired()])
    submit = SubmitField('Send')

@app.route('/')
def home():
    return render_template('index.html', personal_info=PERSONAL_INFO)

@app.route('/about')
def about():
    return render_template('about.html', personal_info=PERSONAL_INFO)

@app.route('/projects')
def projects():
    return render_template('projects.html', projects=PROJECTS_DATA, personal_info=PERSONAL_INFO)

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    form = ContactForm()
    if form.validate_on_submit():
        first_name = form.name.data.split()[0]
        flash(f"Thanks for reaching out, {first_name}! I'll be in touch with you soon.")
        return redirect(url_for('contact'))
    return render_template('contact.html', title='Contact', form=form)