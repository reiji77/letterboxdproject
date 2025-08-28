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
        redirect('/login')
        return "not logged in"
    else: 
        return "currently logged in"


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        # Replace this with actual authentication logic
        user = userData.authenticate_user(username, password, cnx, cursor)
        if user:
            session['logged_in'] = True
            session['id'] = user[0]
            return "Login successful"
        else:
            return "Invalid credentials"
    return '''
        <form method="post">
            Username: <input type="text" name="username"><br>
            Password: <input type="password" name="password"><br>
            <input type="submit" value="Login">
        </form>
    '''

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        email = request.form.get('email')
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            return "Invalid email address"
        userData.insert_user(username, password, email, cnx, cursor)
        return "Registration successful"
    return '''
        <form method="post">
            Username: <input type="text" name="username"><br>
            Password: <input type="password" name="password"><br>
            Email: <input type="text" name="email"><br>
            <input type="submit" value="Register">
        </form>
    '''

    

@app.route('/token', methods=['POST'])
def generate_token():
    username = request.form.get('username')
    password = request.form.get('password')
    if username == 'admin' and password == 'password':
        token = jwt.encode(
            {'username': username, 'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)},
            SECRET_KEY,
            algorithm='HS256'
        )
        return {'token': token}
    return "Invalid credentials", 401

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
    # check if the post request has the file part
    print(request.files)
    if 'file' not in request.files:
        return "no file given"
    file = request.files['file']
    # If the user does not select a file, the browser submits an
    # empty file without a filename.
    if file.filename == '':
        flash('No selected file')
        return "no file given"
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return "file uploaded successfully"
    return "file not allowed"

if __name__ == '__main__':
    cnx, cursor = userData.init_db()
    app.run(host="0.0.0.0", port=5000, debug=True)
