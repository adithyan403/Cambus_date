from extensions import db
from datetime import datetime

class Confession(db.Document):
    meta = {'collection': 'confessions'}
    
    sender_id = db.ReferenceField('User', required=True) # Kept for moderation, but UI will be anonymous
    content = db.StringField(required=True, max_length=500)
    department_to = db.StringField(required=True) # e.g., "Computer Science", "All"
    
    created_at = db.DateTimeField(default=datetime.utcnow)
    likes = db.ListField(db.ReferenceField('User')) # User IDs who liked it
    
    def get_likes_count(self):
        return len(self.likes)
