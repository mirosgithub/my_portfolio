import os
from models import db, PersonalInfo, Projects, User
from werkzeug.security import generate_password_hash

def init_db(app):
    """Initialise the database with tables and initial data"""
    with app.app_context():
        db.create_all()
        
        if not PersonalInfo.query.first():
            initial_personal_info = PersonalInfo(
                name='Suah Kim',
                title='Software Engineering Student',
                bio="Hi! I'm Suah, a pre-penultimate software engineering student at the University of Auckland. I'm exploring full-stack development, machine learning, and algorithmic trading, working primarily with Python. I love diving into new challenges and turning ideas into code, whether it's optimising trading algorithms, creating interactive games, or building web applications from scratch.",
                github='https://github.com/mirosgithub',
                email=os.getenv('EMAIL'),
                profile_image='profile.jpg'
            ) 
            db.session.add(initial_personal_info)
            
        if not Projects.query.first():
            initial_projects = [
                Projects(
                    title='Personal Portfolio Website',
                    category='Web Development',
                    description="Built this portfolio website using Flask as my first dive into web development. From learning Flask, WTForms, and Jinja templating to implementing SMTP email notifications and handling deployment using Docker and Google Cloud, this project introduced me to the key aspects of full-stack development.",
                    github_url='https://github.com/mirosgithub/my_portfolio',
                    live_url=None
                ),
                Projects(
                    title='IMC Prosperity 3',
                    category='Algorithmic Trading Competition',
                    description="Teamed up with fellow engineering and CS students to crack the code on algorithmic trading. We built our trading logic in Python, experimenting with different strategies and fine-tuning our approach through countless iterations. The collaborative coding experience with Git was just as valuable as the trading logic we developed. Proud to have placed 3rd in New Zealand!",
                    github_url=None,
                    live_url=None
                ),
                Projects(
                    title='Time Crash',
                    category='Unity Game Development',
                    description="Joined an 8-person team to create a puzzle game for a Game Jam competition. As my first dive into Unity and C#, I contributed to both the coding side, developing parts of the game's puzzle mechanics, and the creative side with game art design. Like many student projects, we ended up doing most of the heavy lifting in the final few days before the deadline! Our collaborative effort earned us a categorical award at the Game Jam.",
                    github_url=None,
                    live_url=None
                )
            ]
            for project in initial_projects:
                db.session.add(project)
        
        if not User.query.first():
            admin_email = os.getenv('ADMIN_EMAIL')
            admin_password = os.getenv('ADMIN_PASSWORD')
            
            admin_user = User(
                email=admin_email,
                password=generate_password_hash(admin_password)
            )
            db.session.add(admin_user)
        
        db.session.commit()
        print("Database initialised successfully!") 