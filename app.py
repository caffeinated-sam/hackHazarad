# app.py
import os
from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from main import run_vector_pipeline
import subprocess
import base64
from main import get_relevant_context
from groq_api import get_groq_response  # Import from groq_api instead of main
from pyngrok import ngrok

#starts ngrok
public_url = ngrok.connect(5000)
print("🔥 Public URL:", public_url)

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
    if 'user_id' not in session:  # Check if user is logged in
        return render_template('login.html')  # Render login page directly if not logged in
    return render_template('index.html')  # Render the home page if logged in

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
            session['user_id'] = user.id  # Store user ID in the session
            return redirect(url_for('index'))  # Redirect to home page upon successful login
        else:
            return render_template('login.html', error="Invalid username/email or password")  # Show error message

    return render_template('login.html')

@app.route('/build-vector-db', methods=['POST'])
def build_vector_db():
    result = run_vector_pipeline()
    return render_template('index.html', message=result)

@app.route("/ask", methods=["POST"])
def ask():
    user_input = request.json.get("message")
    
    # STEP 1: Use RAG to get relevant context
    context = get_relevant_context(user_input)

    # STEP 2: Send question + context to GROQ
    reply = get_groq_response(context, user_input)

    # STEP 3: Return reply to frontend
    return jsonify({"reply": reply})

@app.route("/start-camera", methods=["POST"])
def start_camera():
    subprocess.Popen(["python", "detect_objects.py"])
    return '', 204

@app.route('/upload-image', methods=['POST'])
def upload_image():
    data = request.get_json()
    image_data = data.get('image')

    # Convert the base64 string back to image
    image_data = image_data.split(',')[1]  # Remove the metadata part
    image_binary = base64.b64decode(image_data)

    # Save the image
    img_path = os.path.join('static', 'uploaded_image.png')
    with open(img_path, 'wb') as f:
        f.write(image_binary)

    return jsonify({"message": "Image uploaded successfully!"})

# Logout route to remove user session
@app.route('/profile')
def profile():
    if 'user_id' not in session:  # Ensure the user is logged in
        return redirect(url_for('login'))  # Redirect to login if not logged in
    return render_template('profile.html')  # Render the profile page

# Route for Logout
@app.route('/logout')
def logout():
    session.pop('user_id', None)  # Remove user from session
    return redirect(url_for('login'))  # Redirect to login page after logout

@app.route("/groq-response", methods=["POST"])
def groq_response():
    data = request.get_json()
    user_input = data.get("message", "")

    if not user_input:
        return jsonify({"error": "No message provided"}), 400

    # Get context and response
    context = get_relevant_context(user_input)
    reply = get_groq_response(context, user_input, debug=True)  # Turn on debug

    return jsonify({"reply": reply})

# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)
