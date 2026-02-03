from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from models.profile import Profile
from models.user import User
from models.connection import Connection
from utils.matching_algorithm import calculate_match_percentage

match = Blueprint('match', __name__, url_prefix='/match')

@match.route('/suggestions')
@login_required
def suggestions():
    if not current_user.profile_id:
        flash('Please create a profile first!', 'warning')
        return redirect(url_for('profile.create'))
        
    my_profile = Profile.objects(id=current_user.profile_id.id).first()
    
    # Get all other profiles
    # Optimization: exclude already connected users
    # For now, just exclude self
    all_profiles = Profile.objects(id__ne=my_profile.id)
    
    scored_matches = []
    
    for p in all_profiles:
        score = calculate_match_percentage(my_profile, p)
        if score > 0: # Threshold
            scored_matches.append({
                'profile': p,
                'score': score
            })
            
    # Sort by score desc
    scored_matches.sort(key=lambda x: x['score'], reverse=True)
    
    # Limit to top 20
    scored_matches = scored_matches[:20]
    
    return render_template('dashboard/suggestions.html', matches=scored_matches)
