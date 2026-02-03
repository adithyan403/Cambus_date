from extensions import db
from datetime import datetime

class Profile(db.Document):
    meta = {'collection': 'profiles'}
    
    user_id = db.ReferenceField('User', required=True)
    full_name = db.StringField(required=True, max_length=100)
    age = db.IntField(required=True, min_value=18)
    gender = db.StringField(required=True, choices=('Male', 'Female', 'Non-binary', 'Other'))
    college = db.StringField(required=True)
    department = db.StringField(required=True)
    year = db.IntField(required=True)
    bio = db.StringField(max_length=500)
    profile_picture = db.StringField()  # Path to image
    interests = db.ListField(db.StringField())
    
    looking_for = db.StringField(choices=('Friendship', 'Relationship', 'Study Buddy', 'Other'))
    
    # Embedded preferences document could be used, but DictField is flexible for now
    preferences = db.DictField()
    # Structure: {'min_age': 18, 'max_age': 25, 'same_college': False, 'departments': []}

    contact_info = db.DictField()
    # Structure: {'email_public': False, 'social_links': {'instagram': '', 'linkedin': ''}}

    profile_completeness = db.IntField(default=0)
    is_active = db.BooleanField(default=True)
    created_at = db.DateTimeField(default=datetime.utcnow)
    updated_at = db.DateTimeField(default=datetime.utcnow)

    def calculate_completeness(self):
        score = 0
        if self.profile_picture: score += 20
        if self.bio: score += 20
        if self.interests: score += 20
        if self.contact_info: score += 20
        if self.preferences: score += 20
        self.profile_completeness = score
        self.save()
