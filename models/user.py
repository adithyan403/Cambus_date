from flask_login import UserMixin
from extensions import db, login_manager
from datetime import datetime
import secrets

@login_manager.user_loader
def load_user(user_id):
    return User.objects(pk=user_id).first()

class User(db.Document, UserMixin):
    meta = {
        'collection': 'users',
        'strict': False
    }
    
    user_id = db.StringField(required=True, unique=True, max_length=50)
    email = db.StringField(required=True, unique=True, max_length=150)
    password_hash = db.StringField(required=True)
    is_verified = db.BooleanField(default=True)
    # verification_token = db.StringField() # Removed
    created_at = db.DateTimeField(default=datetime.utcnow)
    last_login = db.DateTimeField()
    
    # Reference to Profile (Lazy reference by string name to avoid circular imports)
    profile_id = db.ReferenceField('Profile')

    # def generate_verification_token(self):
    #     self.verification_token = secrets.token_urlsafe(32)
    #     return self.verification_token
    
    # UserMixin requires a get_id method that returns exact string ID for session
    def get_id(self):
        return str(self.id)
