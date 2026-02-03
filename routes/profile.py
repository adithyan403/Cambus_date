from flask import Blueprint, render_template, redirect, url_for, flash, request, abort
from flask_login import login_required, current_user
from models.profile import Profile
from models.user import User
from utils.image_processing import save_profile_picture
from datetime import datetime

profile = Blueprint('profile', __name__, url_prefix='/profile')

@profile.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    if current_user.profile_id:
        return redirect(url_for('profile.view_me'))
        
    if request.method == 'POST':
        try:
            full_name = request.form.get('full_name')
            age = int(request.form.get('age'))
            gender = request.form.get('gender')
            college = request.form.get('college')
            department = request.form.get('department')
            year = int(request.form.get('year'))
            bio = request.form.get('bio')
            interests = request.form.get('interests').split(',') if request.form.get('interests') else []
            interest_list = [i.strip() for i in interests]
            
            # Preferences
            min_age = int(request.form.get('min_age', 18))
            max_age = int(request.form.get('max_age', 25))
            looking_for = request.form.get('looking_for')
            
            profile = Profile(
                user_id=current_user.id,
                full_name=full_name,
                age=age,
                gender=gender,
                college=college,
                department=department,
                year=year,
                bio=bio,
                interests=interest_list,
                looking_for=looking_for,
                preferences={'min_age': min_age, 'max_age': max_age}
            )
            
            if 'profile_picture' in request.files:
                file = request.files['profile_picture']
                if file.filename != '':
                    filename = save_profile_picture(file)
                    profile.profile_picture = filename

            profile.calculate_completeness()
            profile.save()
            
            # Link profile to user
            current_user.profile_id = profile
            current_user.save()
            
            flash('Profile created successfully!', 'success')
            return redirect(url_for('profile.view_me'))
            
        except ValueError as e:
            flash(f'Error creating profile: Invalid data {e}', 'danger')
        except Exception as e:
            flash(f'Error creating profile: {e}', 'danger')

    return render_template('profile/create.html')

@profile.route('/me')
@login_required
def view_me():
    if not current_user.profile_id:
        return redirect(url_for('profile.create'))
    # Fetch fresh to ensure we have the object
    profile_obj = Profile.objects(id=current_user.profile_id.id).first()
    return render_template('profile/view.html', profile=profile_obj, is_own=True)

@profile.route('/<string:user_id>')
@login_required
def view_public(user_id):
    target_user = User.objects(id=user_id).first()
    if not target_user or not target_user.profile_id:
        abort(404)
        
    profile_obj = Profile.objects(id=target_user.profile_id.id).first()
    return render_template('profile/view.html', profile=profile_obj, is_own=(current_user.id == target_user.id))

@profile.route('/edit', methods=['GET', 'POST'])
@login_required
def edit():
    if not current_user.profile_id:
        return redirect(url_for('profile.create'))
        
    profile_obj = Profile.objects(id=current_user.profile_id.id).first()
    
    if request.method == 'POST':
        # Update logic similar to create, but strictly updating fields
        profile_obj.full_name = request.form.get('full_name')
        profile_obj.bio = request.form.get('bio')
        # ... (simplified for now)
        profile_obj.save()
        flash('Profile updated!', 'success')
        return redirect(url_for('profile.view_me'))
        
    return render_template('profile/edit.html', profile=profile_obj)
