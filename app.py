import os
import time
from flask import Flask, render_template, request, redirect, url_for, session, jsonify, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from main import run_vector_pipeline, get_relevant_context
from groq_api import get_groq_response
from pyngrok import ngrok
from image_ocr import detect_text_from_image
from ai.medicine_rag import search_medicine_pdf
from groq_api import get_groq_response
from werkzeug.utils import secure_filename
import subprocess
import base64

# Start ngrok tunnel
public_url = ngrok.connect(5000)
print("🔥 Public URL:", public_url)

# Flask app setup
app = Flask(__name__)
app.config['SECRET_KEY'] = 'mysecretkey'
UPLOAD_FOLDER = os.path.join(os.getcwd(), 'uploads')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
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
    start_time = time.time()
    data = request.get_json()
    user_input = data.get("query", "")
    if not user_input:
        return jsonify({"error": "No message provided"}), 400

    # Get context and response
    context = get_relevant_context(user_input)
    reply = get_groq_response(context, user_input, debug=True)
    return jsonify({"reply": reply})

# Image Upload from Chatbot UI
@app.route('/upload-image', methods=['POST'])
def upload_image():
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400

    file = request.files['file']
    caption = request.form.get('caption', '').strip()

    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400

    # Save the image
    filename = secure_filename(file.filename)
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(filepath)

    # OCR the image
    ocr_result = detect_text_from_image(filepath)
    ocr_text = ocr_result.get('raw_text', '').strip()
    medicine = ocr_result.get('medicine', 'Unknown')

    # Extract key features from OCR result (you can customize this further)
    key_features = extract_key_features_from_text(ocr_text)

    # Build prompt
    prompt = f"""The user uploaded an image containing the following visible text:
\"{ocr_text}\"

They also wrote the following caption:
\"{caption}\"

Based on this image and the caption, please:
1. Describe the key features of the object in the image.
2. Answer any questions implied in the message, providing details based on the content from the image and caption."""

    # 🔥 Send prompt directly — no context fetching
    reply = get_groq_response("", prompt, debug=True)

    return jsonify({
        'filename': filename,
        'medicine': medicine,
        'extracted_text': ocr_text,
        'caption': caption,
        'key_features': key_features,
        'response': reply
    })

def extract_key_features_from_text(ocr_text):
    # This is a placeholder function. You can add more sophisticated feature extraction logic.
    # Here, we're simply looking for specific keywords like 'medicine', 'ingredients', 'dosage', etc.
    key_features = []
    
    # Example keywords to look for
    keywords = ['medicine', 'ingredients', 'dosage', 'expiration', 'brand', 'side effects']
    
    # Search for these keywords in the OCR text
    for keyword in keywords:
        if keyword.lower() in ocr_text.lower():
            key_features.append(keyword)

    return key_features


@app.route('/uploaded-image/<filename>')
def uploaded_image(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/upload-pdf', methods=['POST'])
def upload_pdf():
    file = request.files.get('file')
    if file and file.filename.endswith('.pdf'):
        # Save or process PDF
        return jsonify({'response': f"✅ PDF '{file.filename}' uploaded successfully!"})
    return jsonify({'response': "⚠️ Invalid file format."})


# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)
