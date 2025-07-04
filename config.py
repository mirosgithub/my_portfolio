import os

PERSONAL_INFO = {
    'name': 'Suah Kim',
    'title': 'Software Engineering Student',
    'bio': "Hi! my name is Suah, and I'm a pre-penultimate software engineering student at the University of Auckland. I'm interested in full stack development, machine learning, and algorithmic trading, with experience in Python, Java, and basic web technologies. I thrive on new challenges and am always eager to learn and apply my technical skills to real-world problems.",
    'profile_image': 'profile.jpg', 
    'github': 'https://github.com/mirosgithub',
    'email': os.getenv('EMAIL')
}

PROJECTS_DATA = [
    {
        'title': 'Personal Portfolio Website', 
        'description': 'description',
        'github_url': None, 
        'live_url': 'http://127.0.0.1:5000/'
    }, 
    {
        'title': 'Project 2', 
        'description': 'description',
        'github_url': None, 
        'live_url': None
    },
    {
        'title': 'Project 3', 
        'description': 'description',
        'github_url': None, 
        'live_url': None
    }
]