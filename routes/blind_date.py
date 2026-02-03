from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from models.blind_date import BlindDate
from models.profile import Profile
from models.user import User
import random

blind_date = Blueprint('blind_date', __name__, url_prefix='/blind-date')

@blind_date.route('/join')
@login_required
def join_pool():
    # Check if already in a blind date
    existing = BlindDate.objects(
        (Q(user1_id=current_user.id) | Q(user2_id=current_user.id)) & 
        Q(user1_interested__ne=False) & Q(user2_interested__ne=False)
    ).first()
    
    if existing:
        return redirect(url_for('blind_date.current_match'))

    # Find a match (Simplistic random match for now)
    # real logic would query users who also want blind dates
    # For now, just grab a random profile
    potential_matches = Profile.objects(id__ne=current_user.profile_id.id)
    if not potential_matches:
         flash('No profiles available for blind date yet.', 'info')
         return redirect(url_for('dashboard.home'))

    # Randomly pick one
    target_profile = random.choice(potential_matches)
    target_user = User.objects(id=target_profile.user_id.id).first()
    
    # Create Blind Date record
    bd = BlindDate(
        user1_id=current_user.id,
        user2_id=target_user.id
    )
    bd.save()
    
    return redirect(url_for('blind_date.current_match'))

@blind_date.route('/current')
@login_required
def current_match():
    # Find current active blind date
    bd = BlindDate.objects(
        (Q(user1_id=current_user.id) | Q(user2_id=current_user.id)) & 
        Q(user1_interested__ne=False) & Q(user2_interested__ne=False)
    ).first()
    
    if not bd:
        return render_template('blind_date/setup.html')
        
    other_user_id = bd.user2_id if bd.user1_id == current_user else bd.user1_id
    other_profile = Profile.objects(user_id=other_user_id.id).first()
    
    # If not revealed, hide details
    if not bd.revealed:
        # Pass minimal info
        display_profile = {
            'college': other_profile.college,
            'interests': other_profile.interests,
            'gender': other_profile.gender
            # No name, no photo
        }
    else:
        display_profile = other_profile
        
    return render_template('blind_date/matches.html', date=bd, profile=display_profile, revealed=bd.revealed)

@blind_date.route('/respond/<string:bd_id>/<string:response>')
@login_required
def respond(bd_id, response):
    bd = BlindDate.objects(id=bd_id).first()
    if not bd:
        return redirect(url_for('dashboard.home'))
        
    interested = (response == 'yes')
    
    if bd.user1_id == current_user:
        bd.user1_interested = interested
    else:
        bd.user2_interested = interested
        
    bd.save()
    
    # Check if both interested
    if bd.user1_interested and bd.user2_interested:
        bd.revealed = True
        bd.save()
        flash('It\'s a match! Profile details revealed.', 'success')
    elif bd.user1_interested is False or bd.user2_interested is False:
        flash('Match skipped. Searching for new match...', 'info')
        # Here we would logic to find next match, for now just redirect
        # In real app, might want to mark this pair as "failed" to avoid rematch
        
    return redirect(url_for('blind_date.current_match'))
