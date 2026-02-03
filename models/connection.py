from extensions import db
from datetime import datetime

class Connection(db.Document):
    meta = {'collection': 'connections'}
    
    sender_id = db.ReferenceField('User', required=True)
    receiver_id = db.ReferenceField('User', required=True)
    status = db.StringField(required=True, default='pending', choices=('pending', 'accepted', 'rejected'))
    match_percentage = db.FloatField()
    
    created_at = db.DateTimeField(default=datetime.utcnow)
    updated_at = db.DateTimeField(default=datetime.utcnow)
    
    messages = db.ListField(db.DictField()) 
    # Structure: {'sender_id': '...', 'message': '...', 'timestamp': ..., 'read': False}
