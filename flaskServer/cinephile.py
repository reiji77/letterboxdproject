from flask import *
from werkzeug.utils import secure_filename
import os
import jwt
import datetime
import re
import userData


app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
ALLOWED_EXTENSIONS = {'csv'}
SECRET_KEY = "your_secret_key"
app.config['SECRET_KEY'] = SECRET_KEY

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def home():
    if not session.get('logged_in'):
        return jsonify({"status": 200, "message": "Logged in"})
    else: 
        return jsonify({"status": 400, "message": "Not logged in"})


@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')
    user = userData.authenticate_user(username, password, cnx, cursor)
    if user:
        token = jwt.encode(
            {'username': username, 'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)},
            SECRET_KEY,
            algorithm='HS256'
        )
        session['id'] = user[0]
        return jsonify({"status": 200, "message": "Login successful", "token": token})
    else:
        return jsonify({"status": 401, "message": "Invalid credentials"})

@app.route('/register', methods=['POST'])
def register():
    username = request.form.get('username')
    password = request.form.get('password')
    email = request.form.get('email')
    if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
        return jsonify({"status": 400, "message": "Invalid email address"})
    userData.insert_user(username, password, email, cnx, cursor)
    return jsonify({"status": 200, "message": "User registered successfully"})


@app.route('/protected', methods=['GET'])
def protected():
    token = request.headers.get('Authorization')
    if not token:
        return "Token is missing", 401
    try:
        decoded = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        return f"Welcome {decoded['username']}! This is a protected route."
    except jwt.ExpiredSignatureError:
        return "Token has expired", 401
    except jwt.InvalidTokenError:
        return "Invalid token", 401

@app.route('/upload', methods=['POST'])
def upload():
    print(request.files)
    if 'file' not in request.files:
        jsonify({"status": 400, "message": "No file part"})
    file = request.files['file']
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return jsonify({"status": 200, "message": "File uploaded successfully"})
    return jsonify({"status": 400, "message": "Invalid file format"})

@app.route('/friends', methods=['POST'])
def get_friends():
    user_id = session.get('id')
    if not user_id:
        return jsonify({"status": 401, "message": "Unauthorized"})
    
    return jsonify({"status": 400, "message": "Invalid file format"})

if __name__ == '__main__':
    cnx, cursor = userData.init_db()
    app.run(host="0.0.0.0", port=5000, debug=True)
