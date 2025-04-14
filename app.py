import os
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

# Initialize Flask app and other extensions
app = Flask(__name__)
app.config['SECRET_KEY'] = 'mysecretkey'

# Define the base directory and configure the SQLite database URI
base_dir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{os.path.join(base_dir, "database", "user.db")}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # To suppress warnings

# Initialize SQLAlchemy and Bcrypt
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

# Define the User model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

# Initialize the database and create tables
with app.app_context():
    db.create_all()

# Route for the homepage
@app.route('/')
def index():
    return render_template('index.html')

# Route for signup
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        # Get form data
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        # Hash the password using Bcrypt
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

        # Create a new User object
        new_user = User(username=username, email=email, password=hashed_password)

        # Add the new user to the database
        try:
            db.session.add(new_user)
            db.session.commit()
            return redirect(url_for('index'))  # Redirect to home page after successful signup
        except Exception as e:
            db.session.rollback()  # Rollback in case of error
            return f"Error: {str(e)}"  # Show the error message
    
    return render_template('signup.html')

# Route for login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username_or_email = request.form['username_or_email']
        password = request.form['password']

        # Find the user by username or email
        user = User.query.filter((User.username == username_or_email) | (User.email == username_or_email)).first()

        if user and bcrypt.check_password_hash(user.password, password):  # Check password hash
            return redirect(url_for('index'))  # Successful login, redirect to the homepage
        else:
            return 'Invalid username/email or password'

    return render_template('login.html')

# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)
