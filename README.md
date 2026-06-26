# Secure Blog Project

Secure Blog Project is a Flask web application created for secure application programming practice.

The project demonstrates blog functionality while highlighting common security issues and safer implementation patterns. It is useful as a learning project for authentication, sessions, input handling and database-backed Flask routes.

## Tech Stack

- Python
- Flask
- SQLite
- HTML templates
- CSS

## Features

- User registration and login
- Blog post listing and detail pages
- Authenticated post creation
- Comment submission
- Search functionality
- SQLite-backed data storage
- Template-based Flask views

## Security Learning Focus

This project is intentionally useful for reviewing secure and insecure web application patterns, including:

- Password handling
- SQL query safety
- Session management
- Authentication checks
- Route protection
- User-generated content handling

## How to Run Locally

### 1. Create a virtual environment

```bash
python -m venv venv
source venv/bin/activate
```

### 2. Install Flask

```bash
pip install flask
```

### 3. Initialise the database

```bash
python db_init.py
```

### 4. Start the app

```bash
python app.py
```

Open the app:

```text
http://127.0.0.1:5001
```

## Project Status

This is a security-focused learning project. It is kept public to demonstrate Flask fundamentals and secure coding review practice.
