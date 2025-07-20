#!/usr/bin/env python3

import os
import sqlite3
from flask import Flask
from models import db, PersonalInfo, Projects, User
from dotenv import load_dotenv
from sqlalchemy import text

load_dotenv()

def create_flask_app():
    """Create a Flask app with PostgreSQL"""
    app = Flask(__name__)
    
    database_url = os.getenv('DATABASE_URL')
    if not database_url:
        print("DATABASE_URL environment variable not set")
        return None
    
    if database_url.startswith('postgres://'):
        database_url = database_url.replace('postgres://', 'postgresql://', 1)
    
    app.config['SQLALCHEMY_DATABASE_URI'] = database_url
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    db.init_app(app)
    return app

def fix_postgres_sequences():
    """Fix PostgreSQL sequences after migration"""
    try:
        with db.engine.connect() as conn:
            print("Fixing PostgreSQL sequences...")
            
            result = conn.execute(text("SELECT MAX(id) FROM personal_info"))
            max_personal_info_id = result.scalar() or 0
            
            result = conn.execute(text("SELECT MAX(id) FROM projects"))
            max_projects_id = result.scalar() or 0
            
            result = conn.execute(text('SELECT MAX(id) FROM "user"'))
            max_user_id = result.scalar() or 0
            
            print(f"Max IDs found: personal_info={max_personal_info_id}, projects={max_projects_id}, user={max_user_id}")
            
            if max_personal_info_id > 0:
                conn.execute(text(f"SELECT setval('personal_info_id_seq', {max_personal_info_id})"))
                print(f"Reset personal_info_id_seq to {max_personal_info_id}")
            
            if max_projects_id > 0:
                conn.execute(text(f"SELECT setval('projects_id_seq', {max_projects_id})"))
                print(f"Reset projects_id_seq to {max_projects_id}")
            
            if max_user_id > 0:
                conn.execute(text(f"SELECT setval('user_id_seq', {max_user_id})"))
                print(f"Reset user_id_seq to {max_user_id}")
            
            conn.commit()
            
    except Exception as e:
        print(f"Warning: Could not fix sequences: {e}")

def migrate_data():
    """Migrate data from SQLite to PostgreSQL"""
    
    sqlite_path = './instance/db.sqlite3'
    if not os.path.exists(sqlite_path):
        print(f"SQLite database not found at {sqlite_path}")
        return False
    
    app = create_flask_app()
    if not app:
        return False
    
    with app.app_context():
        try:
            print("Creating PostgreSQL tables...")
            db.create_all()
            print("PostgreSQL tables created successfully!")
            
            sqlite_conn = sqlite3.connect(sqlite_path)
            sqlite_cursor = sqlite_conn.cursor()
            
            print("Starting migration...")
            
            print("Migrating PersonalInfo...")
            sqlite_cursor.execute("SELECT * FROM personal_info")
            personal_info_data = sqlite_cursor.fetchall()
            
            for row in personal_info_data:
                personal_info = PersonalInfo(
                    id=row[0],
                    name=row[1],
                    title=row[2],
                    bio=row[3],
                    github=row[4],
                    email=row[5],
                    profile_image=row[6]
                )
                db.session.merge(personal_info)
            
            print("Migrating Projects...")
            sqlite_cursor.execute("SELECT * FROM projects")
            projects_data = sqlite_cursor.fetchall()
            
            for row in projects_data:
                project = Projects(
                    id=row[0],
                    title=row[1],
                    category=row[2],
                    description=row[3],
                    github_url=row[4],
                    live_url=row[5]
                )
                db.session.merge(project)
            
            print("Migrating Users...")
            sqlite_cursor.execute("SELECT * FROM user")
            users_data = sqlite_cursor.fetchall()
            
            for row in users_data:
                user = User(
                    id=row[0],
                    email=row[1],
                    password=row[2]
                )
                db.session.merge(user)
            
            db.session.commit()
            sqlite_conn.close()
            
            fix_postgres_sequences()
            
            print("Migration completed successfully!")
            return True
            
        except Exception as e:
            print(f"Migration failed: {e}")
            db.session.rollback()
            return False

if __name__ == '__main__':
    migrate_data() 