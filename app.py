from flask import Flask, render_template, flash, redirect, url_for
from flask_login import LoginManager
from flask_admin import Admin
from config import SECRET_KEY
from models import db, PersonalInfo, Projects, User, PersonalInfoView, ProjectsView
from forms import ContactForm
from utils import send_notification_email
from admin import MyAdminIndexView
from database import init_db
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = SECRET_KEY

DATABASE_URL = os.getenv('DATABASE_URL')
if not DATABASE_URL:
    raise ValueError("DATABASE_URL environment variable is required")

app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL

db.init_app(app)

login = LoginManager()
login.login_view = 'login'
login.init_app(app)

@login.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

admin = Admin(app, index_view=MyAdminIndexView())
admin.add_view(PersonalInfoView(PersonalInfo, db.session))
admin.add_view(ProjectsView(Projects, db.session))

init_db(app)

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

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)