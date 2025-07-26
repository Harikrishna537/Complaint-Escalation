# Complaint Management Web Application

A web-based complaint management system built with Flask and MongoDB. The application allows users to register, log in, submit complaints, view their complaints, and interact with administrators. Admins can manage all complaints, update statuses, and comment on complaints.

---

## Table of Contents
- [Features](#features)
- [Setup Instructions](#setup-instructions)
- [How to Run](#how-to-run)
- [User Stories](#user-stories)
- [Web Application Pages](#web-application-pages)
- [Project Structure](#project-structure)

---

## Features
- User Registration and Login
- User Dashboard to submit/view complaints
- Admin Dashboard to manage all complaints
- Complaint status tracking (Pending, In Progress, Under Review, Resolved, Closed)
- Commenting system for users and admins
- Secure password storage (hashed)
- Session management

---

## Setup Instructions
1. **Clone the repository or copy the project folder to your new system.**
2. **Install Python 3.7+** (if not already installed).
3. **Install MongoDB** and ensure it is running locally on default port `27017`.
4. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
5. **(Optional) Change the Flask secret key in `app.py` for production security.**

---

## How to Run
1. **Start MongoDB** (if not already running):
   - On Windows: Run `mongod` from your command prompt or MongoDB Compass.
2. **Run the Flask app:**
   ```bash
   python app.py
   ```
3. **Open your browser and go to:**
   [http://127.0.0.1:5000/](http://127.0.0.1:5000/)

---

## User Stories
### 1. New User Registration
- A new user visits the site and registers with a username, email, and password.
- The user logs in and is redirected to their dashboard.

### 2. Submit a Complaint
- A logged-in user can submit a complaint by providing a title, selecting a type, and writing a description.
- The complaint is saved with status `Pending`.

### 3. Track Complaint Status
- Users can view all their submitted complaints and see status updates (`Pending`, `In Progress`, etc.).

### 4. Admin Management
- Admin logs in with static credentials (username: `admin`, password: `admin123`).
- Admin can view all complaints, update their status, and add comments.

### 5. Commenting
- Both users and admins can add comments to complaints for discussion or clarification.

---

## Web Application Pages
- **Landing Page**: Welcome page with links to login/register.
- **Register Page**: User registration form.
- **Login Page**: User/admin login form.
- **User Dashboard**: View and submit complaints.
- **Admin Dashboard**: Manage all complaints, update statuses, add comments.
- **Complaint Detail Page**: View complaint details and comments.

---

## Project Structure
```
complaint project-SACET/
├── app.py                  # Main Flask application
├── requirements.txt        # Python dependencies
├── README.md               # Project documentation
└── templates/              # HTML templates
    ├── base.html
    ├── landing.html
    ├── login.html
    ├── register.html
    ├── user_dashboard.html
    ├── admin_dashboard.html
    ├── complaint_detail.html
```

---

## Notes
- **Admin registration is not allowed via the web interface.** Use static credentials.
- **MongoDB must be running locally** for the app to function.
- **For production**, update the `secret_key` in `app.py` and configure MongoDB for secure access.

---

For questions or issues, please contact the project maintainer.
