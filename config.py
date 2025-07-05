import os

PERSONAL_INFO = {
    'name': 'Suah Kim',
    'title': 'Software Engineering Student',
    'bio': "Hi! I'm Suah, a software engineering student at the University of Auckland with a passion for building things that matter. I'm exploring full-stack development, machine learning, and algorithmic trading, working primarily with Python. I love diving into new challenges and turning ideas into code, whether it's optimizing trading algorithms, creating interactive games, or building web applications from scratch.",
    'profile_image': 'profile.jpg', 
    'github': 'https://github.com/mirosgithub',
    'email': os.getenv('EMAIL')
}

PROJECTS_DATA = [
    {
        'title': 'Personal Portfolio Website', 
        'category': 'Web Development',
        'description': "Built this portfolio website using Flask as my first dive into web development. From learning Flask, WTForms, and Jinja templating to implementing SMTP email notifications and handling deployment, this project introduced me to the key aspects of full-stack development. It's not just a showcase, it's a testament to learning by doing.",
        'github_url': 'https://github.com/mirosgithub/my_portfolio', 
        'live_url': 'http://127.0.0.1:5000/'
    }, 
    {
        'title': 'IMC Prosperity 3', 
        'category': 'Algorithmic Trading Competition',
        'description': "Teamed up with fellow engineering and CS students to crack the code on algorithmic trading. We built our trading logic in Python, experimenting with different strategies and fine-tuning our approach through countless iterations. The collaborative coding experience with Git was just as valuable as the trading logic we developed. Proud to have placed 3rd in New Zealand!",
        'github_url': None, 
        'live_url': None, 
    },
    {
        'title': 'Time Crash',
        'category': 'Unity Game Development', 
        'description': "Joined an 8-person team to create a puzzle game for a Game Jam competition. As my first dive into Unity and C#, I contributed to both the coding side, developing parts of the game's puzzle mechanics, and the creative side with game art design. Like many student projects, we ended up doing most of the heavy lifting in the final few days before the deadline! Our collaborative effort earned us a categorical award at the Game Jam.",
        'github_url': None, 
        'live_url': None
    }
]

SECRET_KEY = os.getenv('SECRET_KEY')

SMTP_CONFIG = {
    'SERVER' : "smtp.gmail.com",
    'PORT' : 587,
    'EMAIL' : os.getenv('EMAIL'),
    'PASSWORD' : os.getenv('EMAIL_PASSWORD')
}