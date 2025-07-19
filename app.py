import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from flask import Flask, render_template, flash, redirect, url_for
from config import SECRET_KEY, SMTP_CONFIG
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, EmailField, PasswordField, BooleanField
from wtforms.validators import InputRequired
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin, AdminIndexView, expose
from flask_admin.contrib.sqla import ModelView
from flask_login import UserMixin, LoginManager, current_user, login_user, logout_user
from werkzeug.security import check_password_hash

app = Flask(__name__)
app.config['SECRET_KEY'] = SECRET_KEY
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'

db = SQLAlchemy()
db.init_app(app)

login = LoginManager()
login.login_view = 'login'
login.init_app(app)

@login.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class PersonalInfo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))
    title = db.Column(db.String(30))
    bio = db.Column(db.Text)
    github = db.Column(db.String(30))
    email = db.Column(db.String(30))
    profile_image = db.Column(db.String(30))
    
class PersonalInfoView(ModelView):
    can_delete = False
    can_create = False
    
    def is_accessible(self):
        return current_user.is_authenticated
    
    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('admin.login_view'))
    
class Projects(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50))
    category = db.Column(db.String(50))
    description = db.Column(db.Text)
    github_url = db.Column(db.String(50))
    live_url = db.Column(db.String(50))
    
class ProjectsView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated
    
    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('admin.login_view'))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(30), unique=True)
    password = db.Column(db.String(30))
    
class MyAdminIndexView(AdminIndexView):
    @expose('/')
    def index(self):
        if not current_user.is_authenticated:
            return redirect(url_for('.login_view'))
        return super().index()

    @expose('/login/', methods=['GET', 'POST'])
    def login_view(self):
        form = LoginForm()
    
        if form.validate_on_submit():
            email = form.email.data
            password = form.password.data
            remember = True if form.remember.data else False
        
            user = User.query.filter_by(email=email).first()
        
            if not user or not check_password_hash(user.password, password):
                flash('Please check your login details and try again.')
                return redirect(url_for('.login_view'))
        
            login_user(user, remember=remember)
            return redirect(url_for('.index'))
    
        return render_template('login.html', form=form)
    
    @expose('/logout/')
    def logout_view(self):
        logout_user()
        return redirect(url_for('home'))
    
admin = Admin(app, index_view=MyAdminIndexView())
admin.add_view(PersonalInfoView(PersonalInfo, db.session))
admin.add_view(ProjectsView(Projects, db.session))

class ContactForm(FlaskForm):
    name = StringField('Name', validators=[InputRequired()])
    email = EmailField('Email', validators=[InputRequired()])
    message = TextAreaField('Message', validators=[InputRequired()])
    submit = SubmitField('Send')

class LoginForm(FlaskForm):
    email = EmailField('Email', validators=[InputRequired()])
    password = PasswordField('Password', validators=[InputRequired()])
    remember = BooleanField('Remember me')
    submit = SubmitField('Login')
    
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
    return render_template('index.html', personal_info=PersonalInfo.query.first())

@app.route('/about')
def about():
    return render_template('about.html', personal_info=PersonalInfo.query.first())

@app.route('/projects')
def projects():
    return render_template('projects.html', projects=Projects.query.all(), personal_info=PersonalInfo.query.first())

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
    
    return render_template('contact.html', title='Contact', form=form, personal_info=PersonalInfo.query.first())