from flask_admin import AdminIndexView, expose
from flask_login import current_user, login_user, logout_user
from flask import redirect, url_for, flash, render_template
from werkzeug.security import check_password_hash
from models import User
from forms import LoginForm

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