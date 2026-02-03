from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from extensions import db, bcrypt, mail
from models.user import User
from flask_mail import Message
from datetime import datetime

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard.home'))  # Redirect if already logged in
        
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        remember = True if request.form.get('remember') else False
        
        user = User.objects(email=email).first()
        
        if user and bcrypt.check_password_hash(user.password_hash, password):
            if not user.is_verified:
                flash('Please verify your email address first.', 'warning')
                return redirect(url_for('auth.login'))
                
            login_user(user, remember=remember)
            user.last_login = datetime.utcnow()
            user.save()
            
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('dashboard.home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
            
    return render_template('auth/login.html')

@auth.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard.home'))
        
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        
        if password != confirm_password:
            flash('Passwords do not match!', 'danger')
            return redirect(url_for('auth.register'))
            
        existing_user = User.objects(email=email).first()
        if existing_user:
            flash('Email already registered! Please login.', 'warning')
            return redirect(url_for('auth.login'))
            
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        user = User(email=email, password_hash=hashed_password)
        token = user.generate_verification_token()
        user.save()
        
        # Send Verification Email (Simplistic)
        msg = Message('Confirm Your Email', sender='noreply@collegematrimony.com', recipients=[email])
        link = url_for('auth.verify_email', token=token, _external=True)
        msg.body = f'Your verification link is: {link}'
        try:
            mail.send(msg)
            flash('Account created! Please check your email to verify your account.', 'success')
        except Exception as e:
            flash(f'Error sending email: {e}', 'danger')
            
        return redirect(url_for('auth.login'))
        
    return render_template('auth/register.html')

@auth.route('/verify-email/<token>')
def verify_email(token):
    user = User.objects(verification_token=token).first()
    if user:
        if user.is_verified:
             flash('Account already verified. Please login.', 'info')
        else:
            user.is_verified = True
            user.verification_token = None  # Consume token
            user.save()
            flash('Your account has been verified! You can now login.', 'success')
    else:
        flash('Invalid or expired verification token.', 'danger')
    return redirect(url_for('auth.login'))

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))
