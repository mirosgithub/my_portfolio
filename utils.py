import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from config import SMTP_CONFIG

def is_spam_message(name, email, message):
    spam_keywords = [
        'seo', 'search engine', 'google search', 'search index', 'search register',
        'instagram growth', 'social media growth', 'follower', 'likes', 'views',
        'website traffic', 'backlink', 'ranking', 'optimization', 'marketing',
        'promote', 'advertise', 'boost', 'increase', 'improve visibility', 'hosting', 'domain'
    ]
    
    text_to_check = f"{name} {email} {message}".lower()
    
    for keyword in spam_keywords:
        if keyword in text_to_check:
            return True, keyword
    
    return False, None

def send_notification_email(name, email, message):
    is_spam, detected_keyword = is_spam_message(name, email, message)
    if is_spam:
        raise ValueError(f"Spam detected: message contains '{detected_keyword}'")
    
    smtp_email = SMTP_CONFIG['EMAIL']
    smtp_server = SMTP_CONFIG['SERVER']
    smtp_port = SMTP_CONFIG['PORT']
    smtp_password = SMTP_CONFIG['PASSWORD']
    
    subject = 'Contact Form Update'
    body = f'From: {name}({email})\nMessage: {message}'
    
    try:
        message_obj = MIMEMultipart()
        message_obj['From'] = smtp_email
        message_obj['To'] = smtp_email
        message_obj['Subject'] = subject
        
        message_obj.attach(MIMEText(body))
        
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(smtp_email, smtp_password)
            server.sendmail(smtp_email, smtp_email, message_obj.as_string())
        
        print('Notification sent')
            
    except Exception as e:
        print(f'Error sending notification: {e}') 