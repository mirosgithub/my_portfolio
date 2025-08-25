from flask import Flask, render_template, flash, redirect, send_from_directory, url_for, jsonify
from flask_login import LoginManager
from flask_admin import Admin
from flask_migrate import Migrate
from config import SECRET_KEY
from models import db, PersonalInfo, Projects, User, PersonalInfoView, ProjectsView
from forms import ContactForm
from utils import send_notification_email
from admin import MyAdminIndexView
import os
import logging
from sqlalchemy import text

app = Flask(__name__)
app.config['SECRET_KEY'] = SECRET_KEY

logging.basicConfig(level=logging.INFO)
app.logger.setLevel(logging.INFO)

DATABASE_URL = os.getenv('DATABASE_URL')
if not DATABASE_URL:
    raise ValueError("DATABASE_URL environment variable is required")

app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
    'pool_size': 5,
    'pool_timeout': 30,
    'pool_recycle': 1800,
    'pool_pre_ping': True,
    'max_overflow': 0
}
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
migrate = Migrate(app, db)

login = LoginManager()
login.login_view = 'login'
login.init_app(app)

@login.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

admin = Admin(app, index_view=MyAdminIndexView())
admin.add_view(PersonalInfoView(PersonalInfo, db.session))
admin.add_view(ProjectsView(Projects, db.session))

@app.route('/health')
def health_check():
    try:
        db.session.execute(text('SELECT 1'))
        return jsonify({'status': 'healthy', 'database': 'connected'}), 200
    except Exception as e:
        app.logger.error(f"Health check failed: {str(e)}")
        return jsonify({'status': 'unhealthy', 'database': 'disconnected', 'error': str(e)}), 503

@app.route('/')
def home():
    try:
        personal_info = PersonalInfo.query.first()
    except Exception as e:
        app.logger.error(f"Database error in home route: {str(e)}")
        personal_info = None
    return render_template('index.html', personal_info=personal_info)

@app.route('/about')
def about():
    try:
        personal_info = PersonalInfo.query.first()
    except Exception as e:
        app.logger.error(f"Database error in about route: {str(e)}")
        personal_info = None
    return render_template('about.html', personal_info=personal_info)

@app.route('/projects')
def projects():
    try:
        projects_list = Projects.query.order_by(Projects.order.asc()).all()
        personal_info = PersonalInfo.query.first()
    except Exception as e:
        app.logger.error(f"Database error in projects route: {str(e)}")
        projects_list = []
        personal_info = None
    return render_template('projects.html', projects=projects_list, personal_info=personal_info)

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    form = ContactForm()
    
    if form.validate_on_submit():
        name = form.name.data
        email = form.email.data
        message = form.message.data
        
        try:
            send_notification_email(name, email, message)
            flash(f"Thanks for reaching out, {name.split()[0]}! I'll be in touch with you soon.")
        except Exception as e:
            app.logger.error(f"Email sending failed: {str(e)}")
            flash("Sorry, there was an error sending your message. Please try again later.")

        return redirect(url_for('contact'))
    
    try:
        personal_info = PersonalInfo.query.first()
    except Exception as e:
        app.logger.error(f"Database error in contact route: {str(e)}")
        personal_info = None
    
    return render_template('contact.html', title='Contact', form=form, personal_info=personal_info)

@app.route('/cv')
def cv():
    return send_from_directory('static/pdfs', 'Suah_Kim_CV.pdf')

@app.route('/transcript')
def transcript():
    return send_from_directory('static/pdfs', 'Suah_Kim_Transcript.pdf')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)