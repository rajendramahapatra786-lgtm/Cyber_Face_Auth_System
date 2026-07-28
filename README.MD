# 🔐 Cyber Face Authentication System

<div align="center">

![Python](https://img.shields.io/badge/Python-3.10-blue?style=for-the-badge&logo=python)
![Django](https://img.shields.io/badge/Django-4.2-darkgreen?style=for-the-badge&logo=django)
![OpenCV](https://img.shields.io/badge/OpenCV-Computer%20Vision-red?style=for-the-badge&logo=opencv)
![MediaPipe](https://img.shields.io/badge/MediaPipe-Face%20Detection-orange?style=for-the-badge)
![DeepFace](https://img.shields.io/badge/DeepFace-AI%20Recognition-purple?style=for-the-badge)
![SQLite](https://img.shields.io/badge/Database-SQLite-blue?style=for-the-badge&logo=sqlite)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)

### 🚀 AI-Powered Face Authentication & Intruder Detection System

A secure cyber-themed authentication platform built using **Django, OpenCV, MediaPipe, DeepFace, and JavaScript**.

</div>

---

# 📖 Overview

Cyber Face Authentication System is an intelligent biometric authentication platform that replaces traditional username-password login with secure facial recognition.

Instead of remembering passwords, users authenticate themselves using their face. The system captures live webcam images, validates face quality, performs liveness detection, recognizes registered users, records login activities, and detects unknown users attempting unauthorized access.

The project combines Artificial Intelligence, Computer Vision, and Web Technologies into a modern cybersecurity-inspired application that demonstrates real-world biometric authentication.

---

# 🎯 Project Objectives

The primary objectives of this project are:

- Replace traditional authentication with facial recognition.
- Improve security using biometric verification.
- Detect fake login attempts.
- Store login history.
- Detect and capture unknown users.
- Prevent spoofing using liveness detection.
- Build a modern cyber-security themed authentication interface.
- Demonstrate AI integration with Django.

---

## 🚀 Setup Instructions

Open the project in **VS Code**, then open the terminal and run the following commands:

### 1️⃣ Create a Virtual Environment

```bash
python -m venv venv
```

### 2️⃣ Activate the Virtual Environment

**Windows (PowerShell)**

```powershell
.\venv\Scripts\Activate.ps1
```

**Windows (Command Prompt)**

```cmd
venv\Scripts\activate
```

### 3️⃣ Install Project Dependencies

```bash
pip install -r requirements.txt
```

### 4️⃣ Run the Project

```bash
python manage.py runserver
```

The application will be available at:

```text
http://127.0.0.1:8000/
```

----

# ✨ Key Features

## 🔐 Authentication

- Face Registration
- Face Login
- Face Recognition
- User Verification
- Face Encoding Storage

---

## 👁️ AI Features

- Face Detection using OpenCV
- Face Recognition
- Face Validation
- Brightness Checking
- Face Position Validation
- Liveness Detection
- Multiple Face Detection Prevention

---

## 🛡️ Security Features

- Intruder Detection
- Login Activity Tracking
- Unknown Face Logging
- Failed Login Recording
- Security Dashboard
- Login Time Recording
- Logout Time Recording

---

## 🎨 User Interface

- Cyberpunk Theme
- Hacker-style Animations
- Webcam Interface
- Real-time Camera Preview
- Animated Dashboard
- Responsive Layout
- Modern Glassmorphism Design

---

# 🛠 Tech Stack

## Backend

- Python 3.10
- Django 4.2

## Frontend

- HTML5
- CSS3
- JavaScript
- Bootstrap

## AI & Computer Vision

- OpenCV
- DeepFace
- MediaPipe
- NumPy

## Database

- SQLite3

## Additional Libraries

- Pillow
- django-cors-headers

---

# 🚀 Why This Project?

Traditional login systems rely on passwords, which can be:

- Forgotten
- Stolen
- Shared
- Brute-forced

Cyber Face Authentication System eliminates these issues by introducing biometric authentication.

Every login attempt is verified using Artificial Intelligence and Computer Vision before access is granted.

This makes authentication faster, smarter, and significantly more secure.

---

# 🎯 Target Users

- Educational Institutions
- Offices
- Cyber Security Labs
- Attendance Systems
- Research Projects
- AI Learning
- Face Recognition Demonstrations

---

# 🌟 Highlights

✅ Face Recognition

✅ DeepFace Integration

✅ MediaPipe Liveness Detection

✅ Intruder Capture

✅ Login History

✅ Security Dashboard

✅ Cyberpunk UI

✅ AI-based Authentication

---

# 📌 Project Status

🟢 Completed Core Features

🟡 Future Improvements Planned

# 📁 Project Structure

```text
Cyber_Face_Auth_System/
│
├── authapp/                      # Main authentication application
│   ├── migrations/               # Database migration files
│   ├── static/                   # CSS, JavaScript, Images, Audio
│   │
│   ├── css/
│   ├── js/
│   ├── images/
│   ├── sounds/
│   │
│   ├── templates/
│   │   ├── login.html
│   │   ├── register.html
│   │   ├── dashboard.html
│   │   ├── security_monitor.html
│   │   └── ...
│   │
│   ├── face_utils.py             # Face Recognition Logic
│   ├── face_validation.py        # Face Quality Validation
│   ├── liveness.py               # Liveness Detection
│   ├── models.py                 # Database Models
│   ├── views.py                  # Business Logic
│   ├── urls.py                   # URL Routing
│   ├── admin.py
│   └── apps.py
│
├── dashboard/                    # Dashboard Application
│
├── cyber_auth/                   # Django Project Configuration
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
│
├── media/                        # Registered Faces & Intruder Images
│
├── db.sqlite3                    # SQLite Database
├── requirements.txt              # Python Dependencies
├── manage.py                     # Django Management File
└── README.md
```

---

# 🏗 Project Architecture

```text
                     User
                       │
                       ▼
               Web Browser
                       │
         HTML • CSS • JavaScript
                       │
                       ▼
                 Django URLs
                       │
                       ▼
                  Django Views
                       │
      ┌───────────┬──────────────┬─────────────┐
      ▼           ▼              ▼
 Face Utils   Face Validator   Liveness Check
      │           │              │
      └───────────┴──────────────┘
                  │
                  ▼
           OpenCV + DeepFace
                  │
                  ▼
             SQLite Database
                  │
                  ▼
            Dashboard Response
```

---

# 📂 Folder Explanation

## 📁 authapp/

This is the heart of the project.

It contains the authentication logic, AI modules, templates, static resources, URL routing, and Django views responsible for handling face recognition and login.

---

## 📁 cyber_auth/

This folder contains the Django project configuration.

Responsibilities include:

- Project Settings
- Installed Apps
- Database Configuration
- Static Files
- Media Files
- URL Configuration
- Security Settings

---

## 📁 dashboard/

Responsible for displaying authenticated user information after successful login.

It provides the interface where users can access protected pages after verification.

---

## 📁 media/

Stores dynamically generated project data.

Examples include:

- Registered face images
- Captured intruder images
- Uploaded verification files

---

## 📄 manage.py

The main Django management script.

Used to execute commands such as:

```bash
python manage.py runserver
python manage.py migrate
python manage.py makemigrations
python manage.py createsuperuser
```

---

## 📄 requirements.txt

Contains all Python libraries required to run the project.

This allows anyone to recreate the same development environment using:

```bash
pip install -r requirements.txt
```

---

## 📄 db.sqlite3

SQLite database used to store application data.

Examples:

- Registered Users
- Login History
- Authentication Records
- Security Logs
- Face Metadata

# 🔄 Project Workflow

The Cyber Face Authentication System follows a secure multi-stage authentication pipeline. Each login request passes through several validation layers before access is granted.

---

# 📸 Face Registration Workflow

```text
User Opens Registration Page
            │
            ▼
     Enter User Details
            │
            ▼
      Allow Camera Access
            │
            ▼
      Capture Face Images
            │
            ▼
   Face Detection (OpenCV)
            │
            ▼
 Face Quality Validation
            │
            ▼
 Save Face Dataset
            │
            ▼
 Store User Information
            │
            ▼
 Registration Successful
```

### Process

1. User enters registration details.
2. The browser requests webcam permission.
3. Multiple face samples are captured.
4. OpenCV detects the user's face.
5. Face quality is validated.
6. Images are stored inside the project.
7. User information is saved in the database.
8. Registration completes successfully.

---

# 🔐 Face Login Workflow

```text
Open Login Page
        │
        ▼
Allow Camera Access
        │
        ▼
Capture Live Face
        │
        ▼
Face Detection
        │
        ▼
Face Validation
        │
        ▼
Liveness Detection
        │
        ▼
DeepFace Recognition
        │
 ┌──────┴──────────┐
 │                 │
 ▼                 ▼
Matched        Not Matched
 │                 │
 ▼                 ▼
Dashboard     Intruder Detection
```

---

## Login Process

During login the system performs multiple security checks.

### Step 1

The webcam captures a live image.

### Step 2

OpenCV detects whether a face exists.

### Step 3

The system validates:

- Face position
- Face size
- Lighting condition
- Image quality

### Step 4

Liveness detection verifies that the user is physically present.

### Step 5

DeepFace compares the live image with stored face data.

### Step 6

If the similarity score passes the threshold, authentication succeeds.

Otherwise the login attempt is rejected.

---

# 👁 Face Validation Pipeline

```text
Captured Frame
       │
       ▼
Detect Face
       │
       ▼
Check Face Size
       │
       ▼
Check Brightness
       │
       ▼
Check Face Position
       │
       ▼
Single Face?
       │
       ▼
Validation Passed
```

---

## Validation Checks

The system validates every captured frame before recognition.

### ✔ Face Size

Ensures the face is neither too small nor too far from the camera.

---

### ✔ Face Position

Ensures the face remains centered.

---

### ✔ Brightness Detection

Rejects images that are too dark or overexposed.

---

### ✔ Multiple Face Detection

Rejects authentication when more than one face appears.

---

# 👁 Liveness Detection Workflow

```text
Live Camera
      │
      ▼
Detect Face
      │
      ▼
Detect Eyes
      │
      ▼
Eye Movement
      │
      ▼
Blink Detection
      │
      ▼
Live Person Verified
```

---

## Purpose

Liveness detection helps prevent spoofing attacks using:

- Printed photographs
- Mobile phone images
- Screenshots
- Digital displays

Only a real, live user is allowed to continue authentication.

---

# 🤖 Face Recognition Pipeline

```text
Captured Face
        │
        ▼
Image Preprocessing
        │
        ▼
DeepFace Model
        │
        ▼
Extract Face Embeddings
        │
        ▼
Compare with Stored Faces
        │
 ┌──────┴────────┐
 ▼               ▼
Matched      Unknown
 │               │
 ▼               ▼
Grant Access  Reject Login
```

---

## Recognition Engine

DeepFace converts facial features into numerical embeddings.

These embeddings are compared with registered users to determine identity.

Only sufficiently similar embeddings are accepted.

---

# 🚨 Intruder Detection Workflow

```text
Unknown User
        │
        ▼
Capture Face
        │
        ▼
Save Intruder Image
        │
        ▼
Store Login Attempt
        │
        ▼
Security Monitor
```

---

## Intruder Detection

Whenever authentication fails:

- Unknown face image is captured.
- Login attempt is recorded.
- Timestamp is stored.
- Security dashboard is updated.
- Administrator can review suspicious activity.

---

# 📊 Dashboard Workflow

```text
Successful Login
        │
        ▼
Load Dashboard
        │
        ▼
Display User Information
        │
        ▼
Show Login Activity
        │
        ▼
Access Protected Features
```

The dashboard acts as the authenticated user's landing page after successful face verification.

---

# 🛡 Security Layers

The project combines multiple security mechanisms instead of relying on a single face comparison.

✔ Face Detection

✔ Face Validation

✔ Brightness Validation

✔ Position Validation

✔ Liveness Detection

✔ Face Recognition

✔ Login History

✔ Intruder Detection

✔ Authentication Logging

This multi-stage pipeline significantly improves authentication reliability while reducing false acceptance and spoofing attempts.


# ⚙️ Core Modules

The Cyber Face Authentication System is organized into multiple Python modules, each responsible for a specific part of the authentication process.

This modular architecture improves code readability, maintainability, and scalability.

---

# 📄 manage.py

### Purpose

The entry point of the Django project.

It allows developers to execute Django management commands.

### Responsibilities

- Start Development Server
- Database Migration
- Create Superuser
- Execute Custom Commands

### Common Commands

```bash
python manage.py runserver
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
```

---

# 📄 settings.py

### Purpose

Global configuration file of the Django project.

### Responsibilities

- Installed Applications
- Middleware
- Database Configuration
- Static Files
- Media Files
- Security Settings
- Templates
- CORS Configuration

---

# 📄 urls.py

### Purpose

Maps browser requests to Django views.

### Responsibilities

- Route User Requests
- Connect URLs with Views
- Serve Media Files
- API Routing

Example Flow

```
Browser Request
        │
        ▼
urls.py
        │
        ▼
views.py
```

---

# 📄 views.py

### Purpose

Acts as the controller of the application.

Every user request is processed here.

### Responsibilities

- Registration
- Login
- Dashboard
- Logout
- Face Verification
- Intruder Detection
- Login Activity

Request Flow

```
Browser
   │
   ▼
views.py
   │
   ▼
Face Recognition Modules
   │
   ▼
Database
   │
   ▼
HTML Response
```

---

# 📄 models.py

### Purpose

Defines the database structure.

Stores application data securely.

Typical Models

- User Information
- Face Records
- Login Activity
- Intruder Records

Responsibilities

- Store Registered Users
- Login History
- Authentication Logs
- Face Metadata

---

# 📄 face_utils.py

### Purpose

Core Face Recognition Engine.

This module performs facial recognition using OpenCV and DeepFace.

### Responsibilities

- Load Face Images
- Detect Faces
- Extract Facial Features
- Compare Face Embeddings
- Calculate Similarity
- Return Authentication Result

Workflow

```
Captured Image
       │
       ▼
Detect Face
       │
       ▼
Generate Embeddings
       │
       ▼
Compare Stored Faces
       │
       ▼
Authentication Result
```

---

# 📄 face_validation.py

### Purpose

Validates the captured face before recognition.

Poor-quality images are rejected before entering the recognition pipeline.

### Validation Checks

✔ Face Size

✔ Face Position

✔ Image Brightness

✔ Single Face Detection

✔ Face Visibility

Workflow

```
Captured Frame
        │
        ▼
Detect Face
        │
        ▼
Run Validation Rules
        │
        ▼
Pass / Reject
```

---

# 📄 liveness.py

### Purpose

Protects the system from spoofing attacks.

Ensures the camera is looking at a real person rather than a photo or screen.

### Responsibilities

- Eye Detection
- Blink Detection
- Face Movement Analysis
- Live Person Verification

Workflow

```
Camera
   │
   ▼
Detect Face
   │
   ▼
Detect Eyes
   │
   ▼
Blink Verification
   │
   ▼
Live User Confirmed
```

---

# 📄 admin.py

Registers Django models inside the Django Administration Panel.

Allows administrators to manage users, login records, and application data.

---

# 📄 apps.py

Contains application configuration.

Automatically loaded when Django starts.

---

# 📂 templates/

Contains all frontend HTML pages.

Examples

- Home Page
- Login
- Registration
- Dashboard
- Security Monitor
- Error Pages

---

# 📂 static/

Stores all static assets.

Includes

- CSS
- JavaScript
- Images
- Icons
- Sounds
- Videos

---

# 📂 media/

Stores runtime-generated files.

Examples

- Registered Faces
- Intruder Images
- Uploaded Images

---

# 🔄 Complete Request Lifecycle

```
User Opens Website
          │
          ▼
      Django URLs
          │
          ▼
       views.py
          │
          ▼
 Face Validation
          │
          ▼
 Liveness Detection
          │
          ▼
 Face Recognition
          │
          ▼
 Database Lookup
          │
          ▼
 Authentication Decision
          │
     ┌────┴────┐
     ▼         ▼
Dashboard   Reject Login
```

---

# 🧠 Module Interaction

```
Browser
   │
   ▼
urls.py
   │
   ▼
views.py
   │
   ├──────────────┐
   ▼              ▼
face_utils.py   face_validation.py
        │              │
        └──────┬───────┘
               ▼
          liveness.py
               │
               ▼
          models.py
               │
               ▼
          SQLite Database
```

---

# 🎯 Design Principles

The project follows a modular architecture where each file has a single responsibility.

Advantages

- Easy Maintenance
- Better Scalability
- Cleaner Code
- Easier Debugging
- Reusable Components
- Secure Authentication Pipeline