#!/usr/bin/env python3
import os
import sys
import time
import subprocess
from flask_migrate import upgrade
from app import create_app, db

def wait_for_db():
    """Wait for database to be ready"""
    max_retries = 30
    retry_count = 0
    
    while retry_count < max_retries:
        try:
            # Try to connect to the database
            app = create_app()
            with app.app_context():
                db.engine.execute('SELECT 1')
            print("✓ Database connection successful!")
            return True
        except Exception as e:
            retry_count += 1
            print(f"⚠ Database connection failed (attempt {retry_count}/{max_retries}): {e}")
            time.sleep(2)
    
    print("✗ Failed to connect to database after maximum retries")
    return False

def run_migrations():
    """Run database migrations"""
    try:
        app = create_app()
        with app.app_context():
            print("🔄 Running database migrations...")
            
            # Initialize migrations if not already done
            migrations_dir = os.path.join(os.path.dirname(__file__), 'migrations', 'versions')
            if not os.path.exists(migrations_dir):
                os.makedirs(migrations_dir)
            
            # Run the upgrade
            upgrade()
            print("✓ Database migrations completed successfully!")
            return True
    except Exception as e:
        print(f"✗ Migration failed: {e}")
        return False

def create_initial_migration():
    """Create initial migration if it doesn't exist"""
    try:
        versions_dir = os.path.join(os.path.dirname(__file__), 'migrations', 'versions')
        if not os.path.exists(versions_dir) or len(os.listdir(versions_dir)) == 0:
            print("🔄 Creating initial migration...")
            app = create_app()
            with app.app_context():
                # Initialize migration repository if needed
                try:
                    subprocess.run(['flask', 'db', 'init'], check=True, cwd=os.path.dirname(__file__))
                except subprocess.CalledProcessError:
                    pass  # Directory might already exist
                
                # Create initial migration
                subprocess.run(['flask', 'db', 'migrate', '-m', 'Initial migration'], 
                             check=True, cwd=os.path.dirname(__file__))
                print("✓ Initial migration created!")
    except Exception as e:
        print(f"⚠ Could not create initial migration: {e}")

if __name__ == '__main__':
    print("🚀 Starting PetClinic API Server...")
    
    # Set Flask environment variables
    os.environ['FLASK_APP'] = 'app:create_app'
    os.environ['FLASK_ENV'] = os.environ.get('FLASK_ENV', 'development')
    
    # Wait for database to be ready
    if not wait_for_db():
        sys.exit(1)
    
    # Run migrations
    if not run_migrations():
        print("⚠ Continuing without migrations...")
    
    # Create and run the Flask app
    app = create_app()
    
    print("✓ PetClinic API Server is ready!")
    print("📋 API Documentation available at: http://localhost:5000/apidocs")
    print("❤️  Health check available at: http://localhost:5000/health")
    print("")
    
    # Start the Flask development server
    app.run(
        host='0.0.0.0',
        port=int(os.environ.get('PORT', 5000)),
        debug=os.environ.get('FLASK_DEBUG', '1') == '1'
    )