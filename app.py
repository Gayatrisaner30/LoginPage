from flask import Flask, render_template, request, redirect, url_for
from flask_dance.contrib.google import make_google_blueprint, google

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key_here'

# Replace this with a proper database in a production environment
users = []

# Flask-Dance Google configuration
blueprint = make_google_blueprint(
    client_id='your_google_client_id_here',
    client_secret='your_google_client_secret_here',
    scope=['profile', 'email'],
)
app.register_blueprint(blueprint, url_prefix='/login')

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email = request.form['email']
        username = request.form['username']
        password = request.form['password']
        users.append({'email': email, 'username': username, 'password': password})
        return redirect('/')
    return render_template('signup.html')

@app.route('/google-login')
def google_login():
    if not google.authorized:
        return redirect(url_for('google.login'))
    resp = google.get('/oauth2/v1/userinfo')
    if resp.ok:
        user_info = resp.json()
        # You can handle the Google login response here
        # For simplicity, we'll just display the user info on the page
        return f"<h2>Logged in with Google</h2><p>Email: {user_info['email']}</p>"
    return "Google login failed."

if __name__ == '__main__':
    app.run(debug=True)
