import os
import sys
import subprocess

def run_migrations():
    print("Running migrations...")
    subprocess.run([sys.executable, "manage.py", "migrate"])

def create_superuser():
    print("Creating superuser...")
    username = input("Enter superuser username: ")
    email = input("Enter superuser email: ")
    subprocess.run([
        sys.executable,
        "manage.py",
        "createsuperuser",
        "--username", username,
        "--email", email
    ])

def train_model():
    print("Training sentiment analysis model...")
    subprocess.run([sys.executable, "train_model.py"])

def initialize_database():
    print("Initializing database with sample data...")
    subprocess.run([sys.executable, "initialize_db.py"])

def run_server():
    print("Starting development server...")
    subprocess.run([sys.executable, "manage.py", "runserver"])

def main():
    # Set up Django environment
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sentiment_platform.settings')
    
    # Run migrations
    run_migrations()
    
    # Create superuser if needed
    create_super = input("Do you want to create a superuser? (y/n): ")
    if create_super.lower() == 'y':
        create_superuser()
    
    # Train model
    train_model()
    
    # Initialize database
    init_db = input("Do you want to initialize the database with sample data? (y/n): ")
    if init_db.lower() == 'y':
        initialize_database()
    
    # Run server
    run_server()

if __name__ == '__main__':
    main() 