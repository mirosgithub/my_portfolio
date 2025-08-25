from flask_sqlalchemy import SQLAlchemy
from flask_admin.contrib.sqla import ModelView
from flask_login import UserMixin, current_user
from flask import redirect, url_for

db = SQLAlchemy()

class PersonalInfo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))
    title = db.Column(db.String(30))
    bio = db.Column(db.Text)
    github = db.Column(db.String(30))
    linkedin = db.Column(db.String(100))
    email = db.Column(db.String(30))
    profile_image = db.Column(db.String(30))
    
    def __repr__(self):
        return f'<PersonalInfo {self.name}>'

class Projects(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50))
    category = db.Column(db.String(50))
    description = db.Column(db.Text)
    github_url = db.Column(db.String(50))
    live_url = db.Column(db.String(100))
    order = db.Column(db.Integer, default=0)
    
    def __repr__(self):
        return f'<Project {self.title}>'

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(30), unique=True)
    password = db.Column(db.String(200))
    
    def __repr__(self):
        return f'<User {self.email}>'

class PersonalInfoView(ModelView):
    can_delete = False
    can_create = False
    
    def is_accessible(self):
        return current_user.is_authenticated
    
    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('admin.login_view'))

class ProjectsView(ModelView):
    column_list = ['order', 'title', 'category', 'github_url', 'live_url']
    column_default_sort = ('order', False)
    column_sortable_list = ['order', 'title', 'category']
    column_searchable_list = ['title', 'category', 'description']
    form_excluded_columns = ['id']
    
    def is_accessible(self):
        return current_user.is_authenticated
    
    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('admin.login_view')) 