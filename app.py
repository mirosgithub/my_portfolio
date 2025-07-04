import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from flask import Flask, render_template, flash, redirect, url_for
from config import PERSONAL_INFO, PROJECTS_DATA, SECRET_KEY, SMTP_CONFIG
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
    
def send_notification_email(name, email, message):
    smtp_email = SMTP_CONFIG['EMAIL']
    smtp_server = SMTP_CONFIG['SERVER']
    smtp_port = SMTP_CONFIG['PORT']
    smtp_password = SMTP_CONFIG['PASSWORD']
    
    subject = 'Contact Form Update'
    body = f'From: {name}({email})\nMessage: {message}'
    
    try:
        message = MIMEMultipart()
        message['From'] = smtp_email
        message['To'] = smtp_email
        message['Subject'] = subject
        
        message.attach(MIMEText(body))
        
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(smtp_email, smtp_password)
            server.sendmail(smtp_email, smtp_email, message.as_string())
        
        print('Notification sent')
            
    except Exception as e:
        print(f'Error sending notification: {e}')

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
        name = form.name.data
        email = form.email.data
        message = form.message.data
        
        send_notification_email(name, email, message)
        flash(f"Thanks for reaching out, {name.split()[0]}! I'll be in touch with you soon.")

        return redirect(url_for('contact'))
    
    return render_template('contact.html', title='Contact', form=form)