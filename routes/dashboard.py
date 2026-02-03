from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from mongoengine.queryset.visitor import Q
from models.confession import Confession
import random
from datetime import datetime

dashboard = Blueprint('dashboard', __name__, url_prefix='/dashboard')

QUOTES = [
    "Love is not about possession. Love is about appreciation.",
    "A successful relationship requires falling in love many times, always with the same person.",
    "True love stories never have endings.",
    "Love looks not with the eyes, but with the mind.",
    "To love and be loved is to feel the sun from both sides."
]

@dashboard.route('/', methods=['GET', 'POST'])
@login_required
def home():
    # Handle Confession Submission
    if request.method == 'POST':
        content = request.form.get('content')
        department_to = request.form.get('department_to')
        
        if content and department_to:
            # Anonymous submission (store sender only for moderation if needed)
            confession = Confession(
                sender_id=current_user.id,
                content=content,
                department_to=department_to
            )
            confession.save()
            flash('Your confession has been posted anonymously!', 'success')
            return redirect(url_for('dashboard.home'))

    # Daily Quote
    quote = random.choice(QUOTES)
    
    # Relationship Importance (Fun Random Metric)
    # Use date + user id to make it stable for the day but random across days
    random.seed(f"{current_user.id}-{datetime.now().date()}")
    relationship_importance = random.randint(70, 100)
    
    # Recent Confessions
    confessions = Confession.objects().order_by('-created_at').limit(10)

    return render_template('dashboard/home.html', 
                         user=current_user,
                         quote=quote,
                         relationship_importance=relationship_importance,
                         confessions=confessions)

@dashboard.route('/suggestions')
@login_required
def suggestions():
    return render_template('dashboard/suggestions.html')

@dashboard.route('/connections')
@login_required
def connections():
    from models.connection import Connection
    # Incoming requests
    requests = Connection.objects(receiver_id=current_user.id, status='pending')
    
    # Accepted connections
    friends = Connection.objects(
        (Q(sender_id=current_user.id) | Q(receiver_id=current_user.id)) & Q(status='accepted')
    )
    
    return render_template('dashboard/connections.html', requests=requests, friends=friends)

@dashboard.route('/messages')
@login_required
def messages():
    return render_template('dashboard/messages.html')
