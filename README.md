# Personal Portfolio Website

## Overview

A personal portfolio website built with Flask to showcase my projects. The application features a dark/light theme support, contact form and email notification, and an admin panel for content management.

## Project Structure

```
my_portfolio/
├── app.py                    # Main Flask application
├── models.py                 # Database models and admin views
├── forms.py                  # Contact form implementation
├── config.py                 # Configuration settings
├── database.py               # Database initialisation
├── utils.py                  # Email notification utilities
├── admin.py                  # Admin panel configuration
├── requirements.txt          # Python dependencies
├── Dockerfile                # Container configuration
├── compose.yaml              # Docker Compose setup
├── static/
│   ├── css/
│   │   └── input.css         # Tailwind CSS with custom theme
│   └── images/
│       └── profile.jpg       # Profile image
└── templates/
    ├── base.html             # Base template with navigation
    ├── index.html            # Home page
    ├── about.html            # About page
    ├── projects.html         # Projects page
    ├── contact.html          # Contact page
    ├── login.html            # Admin login page
    └── admin/
        └── index.html        # Admin dashboard
```

## Features

### Core Functionality
- **Responsive Design**: Mobile-first approach with Tailwind CSS
- **Theme Toggle**: Dark and light mode support
- **Contact Form**: Email notifications for incoming messages
- **Admin Panel**: Content management for portfolio updates
- **Database Integration**: PostgreSQL with SQLAlchemy ORM

### Pages
- **Home**: Landing page
- **About**: Detailed information about skills and interests
- **Projects**: Showcase of portfolio projects with links
- **Contact**: Contact form with email integration
  
## Technology Stack

### Backend
- **Python 3.13.2**: Core programming language
- **Flask 3.1.1**: Web framework
- **SQLAlchemy 2.0.41**: Database ORM
- **Flask-Admin 1.6.1**: Admin interface
- **Flask-Login 0.6.3**: User authentication
- **WTForms 3.2.1**: Form handling

### Frontend
- **Tailwind CSS**: Utility-first CSS framework
- **HTML5**: Semantic markup
- **JavaScript**: Theme toggle and interactive features
- **Google Fonts**: Typography using web fonts

### Database & Deployment
- **PostgreSQL**: Primary database
- **Docker**: Containerisation
- **Gunicorn**: WSGI server for production
- **Google Cloud Run**: Serverless Deployment
  
## Customisation

### Styling
The application uses Tailwind CSS with custom CSS variables for theming:
- Primary colour: Purple (#a17be6)
- Dark mode support
- Responsive design for all screen sizes

### Content Management
- Access admin panel at `/admin`
- Update personal information and projects
- Authentication required for admin access
