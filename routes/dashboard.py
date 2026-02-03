from flask import Blueprint, render_template
from flask_login import login_required, current_user
from mongoengine.queryset.visitor import Q

dashboard = Blueprint('dashboard', __name__, url_prefix='/dashboard')

@dashboard.route('/')
@login_required
def home():
    return render_template('dashboard/home.html', user=current_user)

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
