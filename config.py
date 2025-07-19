import os

SECRET_KEY = os.getenv('SECRET_KEY')

SMTP_CONFIG = {
    'SERVER' : "smtp.gmail.com",
    'PORT' : 587,
    'EMAIL' : os.getenv('EMAIL'),
    'PASSWORD' : os.getenv('EMAIL_PASSWORD')
}