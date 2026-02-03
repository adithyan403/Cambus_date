import sys
import os

# Add parent directory to path to import app
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app
from models.user import User
from models.profile import Profile
from models.blind_date import BlindDate
from models.connection import Connection
from models.confession import Confession

def init_db():
    app = create_app()
    with app.app_context():
        print("Connecting to database...")
        
        # Accessing the collection triggers creation/index building in MongoEngine
        print("Ensuring indexes for User...")
        User.ensure_indexes()
        
        print("Ensuring indexes for Profile...")
        Profile.ensure_indexes()
        
        print("Ensuring indexes for BlindDate...")
        BlindDate.ensure_indexes()
        
        print("Ensuring indexes for Connection...")
        Connection.ensure_indexes()
        
        print("Ensuring indexes for Confession...")
        Confession.ensure_indexes()
        
        print("Database initialization complete.")

if __name__ == "__main__":
    init_db()
