from flask import Flask, render_template
from config import PERSONAL_INFO, PROJECTS_DATA

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html', personal_info=PERSONAL_INFO)

@app.route('/about')
def about():
    return render_template('about.html', personal_info=PERSONAL_INFO)

@app.route('/projects')
def projects():
    return render_template('projects.html', projects=PROJECTS_DATA, personal_info=PERSONAL_INFO)