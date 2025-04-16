import os
from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from main import run_vector_pipeline, get_relevant_context
from groq_api import get_groq_response
from pyngrok import ngrok
import subprocess
import base64

# Start ngrok tunnel
public_url = ngrok.connect(5000)
print("🔥 Public URL:", public_url)

# Flask app setup
app = Flask(__name__)
app.config['SECRET_KEY'] = 'mysecretkey'

# SQLite DB config
base_dir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{os.path.join(base_dir, "database", "user.db")}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Init extensions
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

# User model with name
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

# Create tables
with app.app_context():
    db.create_all()

# Route for the homepage
@app.route('/')
def index():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    return render_template('index.html')

# Route for signup
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        # Get form data
        name = request.form['name']
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        # Check if passwords match
        if password != confirm_password:
            return render_template('signup.html', error="Passwords do not match")

        # Hash the password using Bcrypt
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

        # Create a new User object
        new_user = User(name=name, username=username, email=email, password=hashed_password)
        
        # Add the new user to the database
        try:
            db.session.add(new_user)
            db.session.commit()
            return redirect(url_for('login'))
        except Exception as e:
            db.session.rollback()
            return f"Error: {str(e)}"

    return render_template('signup.html')

# Route for login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username_or_email = request.form['username_or_email']
        password = request.form['password']

        # Find the user by username or email
        user = User.query.filter(
            (User.username == username_or_email) | (User.email == username_or_email)
        ).first()

        if user and bcrypt.check_password_hash(user.password, password):
            session['user_id'] = user.id # Store user ID in the session
            return redirect(url_for('index'))# Redirect to home page upon successful login
        else:
            return render_template('login.html', error="Invalid username/email or password")

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
    image_data = image_data.split(',')[1]
    image_binary = base64.b64decode(image_data)

    # Save the image
    img_path = os.path.join('static', 'uploaded_image.png')
    with open(img_path, 'wb') as f:
        f.write(image_binary)
    return jsonify({"message": "Image uploaded successfully!"})

# Logout route to remove user session
@app.route('/profile')
def profile():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    user = User.query.get(session['user_id'])
    return render_template('profile.html', user=user)

# Logout route to remove user session
@app.route('/logout')
def logout():
    session.pop('user_id', None) # Remove user from session
    return redirect(url_for('login'))  # Redirect to login page after logout

@app.route("/groq-response", methods=["POST"])
def groq_response():
    data = request.get_json()
    user_input = data.get("query", "")
    if not user_input:
        return jsonify({"error": "No message provided"}), 400

    # Get context and response
    context = get_relevant_context(user_input)
    reply = get_groq_response(context, user_input, debug=True)
    return jsonify({"reply": reply})

# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)
