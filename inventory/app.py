"""
This module defines the Flask application for the Inventory Management system.
It includes routes for registration, login, and other functionalities related to the system.
"""

import sqlite3
from flask import Flask, request, render_template, redirect, url_for, flash

app = Flask(__name__)
app.secret_key = "supersecretkey"  # This is used for flashing messages.

DATABASE = 'inventory_management.db'

def get_db():
    """
    Return a new connection to the SQLite3 database.

    Returns:
        sqlite3.Connection: A new connection to the database.
    """
    return sqlite3.connect(DATABASE)

@app.route('/login', methods=['GET', 'POST'])
def login():
    """
    Handle user login and authentication.

    If successful, redirect to the home page.
    If unsuccessful, display an error message.

    Returns:
        str: Success message or error message.
    """
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        con = get_db()
        cur = con.cursor()
        cur.execute(
            "SELECT * FROM users WHERE username = ? AND password = ?", 
            (username, password)
        )
        user = cur.fetchone()
        con.close()

        if user:
            # Redirect to home page after successful login
            flash("Logged in successfully!", "success")
            return redirect(url_for('home'))  # Usually, you'd redirect to a dashboard or homepage.
        else:
            flash("Invalid credentials", "danger")
            return redirect(url_for('login'))

    return render_template('login.html')

@app.route('/home')
def home():
    """
    Display the home page.

    Add any necessary logic or data retrieval for the home page.

    Returns:
        str: Rendered template for the home page.
    """
    return render_template('home.html')

# ... (other imports and code)

@app.route('/register', methods=['GET', 'POST'])
def register():
    """
    Handle user registration and insert new user data into the database.
    If successful, redirects to the login page.
    """
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        confirm_password = request.form['confirm-password']

        if password != confirm_password:
            flash("Passwords do not match!", "danger")
            return redirect(url_for('register'))

        try:
            con = get_db()
            cur = con.cursor()
            cur.execute(
                "INSERT INTO users (username, password) VALUES (?, ?)", 
                (username, password)
            )
            con.commit()
            flash("Registered successfully! Please login.", "success")
            return redirect(url_for('login'))
        except sqlite3.IntegrityError:
            flash("Username already exists", "danger")
            return redirect(url_for('register'))
        finally:
            con.close()

    return render_template('register.html')

if __name__ == '__main__':
    # Initialize the user table (if not present) and start the Flask application.
    with app.app_context():
        db = get_db()
        main_cursor = db.cursor()
        main_cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY,
                username TEXT NOT NULL UNIQUE,
                password TEXT NOT NULL
            )
        ''')
        db.commit()
    app.run(debug=True)
