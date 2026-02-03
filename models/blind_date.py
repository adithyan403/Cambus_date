from extensions import db
from datetime import datetime

class BlindDate(db.Document):
    meta = {'collection': 'blind_dates'}
    
    user1_id = db.ReferenceField('User', required=True)
    user2_id = db.ReferenceField('User', required=True)
    
    user1_interested = db.BooleanField(default=None) # None = Pending, True/False
    user2_interested = db.BooleanField(default=None)
    
    revealed = db.BooleanField(default=False)
    
    date_details = db.DictField()
    # Structure: {'scheduled_date': ..., 'location': '...', 'notes': '...'}
    
    created_at = db.DateTimeField(default=datetime.utcnow)
    revealed_at = db.DateTimeField()
