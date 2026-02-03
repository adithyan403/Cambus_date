from flask import Blueprint, redirect, url_for, flash, request, render_template
from flask_login import login_required, current_user
from models.connection import Connection
from models.user import User

connection = Blueprint('connection', __name__, url_prefix='/connection')

@connection.route('/send/<string:user_id>')
@login_required
def send_request(user_id):
    target_user = User.objects(id=user_id).first()
    if not target_user:
        flash('User not found.', 'danger')
        return redirect(url_for('dashboard.home'))
        
    # Check existing
    existing = Connection.objects(
        sender_id__in=[current_user.id, target_user.id],
        receiver_id__in=[current_user.id, target_user.id]
    ).first()
    
    if existing:
        flash('Connection already exists or pending.', 'warning')
        return redirect(url_for('match.suggestions'))
        
    conn = Connection(
        sender_id=current_user.id,
        receiver_id=target_user.id,
        status='pending'
    )
    conn.save()
    flash('Connection request sent!', 'success')
    return redirect(url_for('match.suggestions'))

@connection.route('/accept/<string:conn_id>')
@login_required
def accept_request(conn_id):
    conn = Connection.objects(id=conn_id).first()
    if not conn or conn.receiver_id != current_user:
        flash('Invalid request.', 'danger')
        return redirect(url_for('dashboard.home'))
        
    conn.status = 'accepted'
    conn.save()
    flash('Connection accepted!', 'success')
    return redirect(url_for('dashboard.connections')) # Assuming this exists or maps to home

@connection.route('/reject/<string:conn_id>')
@login_required
def reject_request(conn_id):
    conn = Connection.objects(id=conn_id).first()
    if not conn or conn.receiver_id != current_user:
        flash('Invalid request.', 'danger')
        return redirect(url_for('dashboard.home'))
        
    conn.status = 'rejected'
    conn.save()
    flash('Connection rejected.', 'info')
    return redirect(url_for('dashboard.connections'))
