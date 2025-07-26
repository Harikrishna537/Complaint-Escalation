from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from pymongo import MongoClient
from werkzeug.security import generate_password_hash, check_password_hash
from bson.objectid import ObjectId
from datetime import datetime
import os

app = Flask(__name__)
app.secret_key = 'your-secret-key-change-this-in-production'

# MongoDB connection
client = MongoClient('mongodb+srv://harikrishna:hari537@complaintcluster.o4n1v6k.mongodb.net/')
db = client['complaint_portal']
users_collection = db['users']
complaints_collection = db['complaints']

# Complaint types
COMPLAINT_TYPES = [
    'Technical Issue',
    'Service Quality',
    'Billing Issue',
    'Product Defect',
    'Customer Service',
    'Delivery Problem',
    'Other'
]

# Complaint statuses
COMPLAINT_STATUSES = [
    'Pending',
    'In Progress',
    'Under Review',
    'Resolved',
    'Closed'
]

@app.route('/')
def landing():
    return render_template('landing.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        user_type = request.form.get('user_type', 'user')
        
        # Prevent admin registration
        if user_type == 'admin':
            flash('Admin registration is not allowed.', 'error')
            return render_template('register.html')

        # Check if user already exists
        if users_collection.find_one({'$or': [{'username': username}, {'email': email}]}):
            flash('Username or email already exists', 'error')
            return render_template('register.html')
        
        # Create new user (only user_type 'user')
        user_data = {
            'username': username,
            'email': email,
            'password': generate_password_hash(password),
            'user_type': user_type,
            'created_at': datetime.now()
        }
        
        users_collection.insert_one(user_data)
        flash('Registration successful! Please login.', 'success')
        return redirect(url_for('login'))
    
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        # Static admin credentials
        if username == 'admin' and password == 'admin123':
            session['user_id'] = 'admin_static_id'
            session['username'] = 'admin'
            session['user_type'] = 'admin'
            return redirect(url_for('admin_dashboard'))

        user = users_collection.find_one({'username': username})
        
        if user and check_password_hash(user['password'], password):
            session['user_id'] = str(user['_id'])
            session['username'] = user['username']
            session['user_type'] = user['user_type']
            return redirect(url_for('user_dashboard'))
        else:
            flash('Invalid username or password', 'error')
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    flash('Logged out successfully', 'success')
    return redirect(url_for('landing'))

@app.route('/dashboard')
def user_dashboard():
    if 'user_id' not in session or session['user_type'] != 'user':
        return redirect(url_for('login'))
    
    # Get user's complaints
    complaints = list(complaints_collection.find({'user_id': session['user_id']}).sort('created_at', -1))
    
    return render_template('user_dashboard.html', 
                         complaints=complaints, 
                         complaint_types=COMPLAINT_TYPES,
                         complaint_statuses=COMPLAINT_STATUSES)

@app.route('/admin')
def admin_dashboard():
    if 'user_id' not in session or session['user_type'] != 'admin':
        return redirect(url_for('login'))
    
    # Get all complaints with user information
    pipeline = [
        {
            '$lookup': {
                'from': 'users',
                'localField': 'user_id',
                'foreignField': '_id',
                'as': 'user_info'
            }
        },
        {'$sort': {'created_at': -1}}
    ]
    
    complaints = list(complaints_collection.aggregate(pipeline))
    
    return render_template('admin_dashboard.html', 
                         complaints=complaints,
                         complaint_statuses=COMPLAINT_STATUSES)

@app.route('/submit_complaint', methods=['POST'])
def submit_complaint():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    complaint_data = {
        'user_id': session['user_id'],
        'title': request.form['title'],
        'type': request.form['type'],
        'description': request.form['description'],
        'status': 'Pending',
        'created_at': datetime.now(),
        'updated_at': datetime.now(),
        'comments': []
    }
    
    complaints_collection.insert_one(complaint_data)
    flash('Complaint submitted successfully!', 'success')
    return redirect(url_for('user_dashboard'))

@app.route('/update_status', methods=['POST'])
def update_status():
    if 'user_id' not in session or session['user_type'] != 'admin':
        return redirect(url_for('login'))
    
    complaint_id = request.form['complaint_id']
    new_status = request.form['status']
    
    complaints_collection.update_one(
        {'_id': ObjectId(complaint_id)},
        {
            '$set': {
                'status': new_status,
                'updated_at': datetime.now()
            }
        }
    )
    
    flash('Status updated successfully!', 'success')
    return redirect(url_for('admin_dashboard'))

@app.route('/complaint/<complaint_id>')
def view_complaint(complaint_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    complaint = complaints_collection.find_one({'_id': ObjectId(complaint_id)})
    
    if not complaint:
        flash('Complaint not found', 'error')
        return redirect(url_for('user_dashboard'))
    
    # Check if user owns this complaint or is admin
    if session['user_type'] != 'admin' and complaint['user_id'] != session['user_id']:
        flash('Access denied', 'error')
        return redirect(url_for('user_dashboard'))
    
    # Get user info for the complaint
    user = users_collection.find_one({'_id': ObjectId(complaint['user_id'])})
    
    return render_template('complaint_detail.html', 
                         complaint=complaint, 
                         user=user,
                         complaint_statuses=COMPLAINT_STATUSES)

@app.route('/add_comment', methods=['POST'])
def add_comment():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    complaint_id = request.form['complaint_id']
    comment_text = request.form['comment']
    
    complaint = complaints_collection.find_one({'_id': ObjectId(complaint_id)})
    
    if not complaint:
        flash('Complaint not found', 'error')
        return redirect(url_for('user_dashboard'))
    
    # Check access rights
    if session['user_type'] != 'admin' and complaint['user_id'] != session['user_id']:
        flash('Access denied', 'error')
        return redirect(url_for('user_dashboard'))
    
    comment = {
        'user_id': session['user_id'],
        'username': session['username'],
        'user_type': session['user_type'],
        'comment': comment_text,
        'created_at': datetime.now()
    }
    
    complaints_collection.update_one(
        {'_id': ObjectId(complaint_id)},
        {
            '$push': {'comments': comment},
            '$set': {'updated_at': datetime.now()}
        }
    )
    
    flash('Comment added successfully!', 'success')
    return redirect(url_for('view_complaint', complaint_id=complaint_id))

if __name__ == '__main__':
    app.run(debug=True)