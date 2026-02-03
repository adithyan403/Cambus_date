import sys
import os

# Add parent directory to path to import app
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app
from models.user import User

def init_db():
    app = create_app()
    with app.app_context():
        print("Connecting to database...")
        # Accessing the collection triggers creation/index building in MongoEngine
        User.ensure_indexes()
        print("User collection indexes ensured.")
        print("Database initialization complete.")

if __name__ == "__main__":
    init_db()
