
from flask import Flask, render_template, request, redirect, url_for, session, jsonify

from chat import get_response

app = Flask(__name__)
app.secret_key = "your_secret_key"  # Required for session management

@app.get("/")
def index():
    return render_template('base.html')

@app.post("/predict")
def predict():
    text=request.get_json().get("message")
    #TODO: check if text is valid
    response = get_response(text)
    message = {"answer": response}
    return jsonify(message)

@app.route("/sign_in", methods=['GET', 'POST'])
def sign_in():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        # TODO: Replace with actual authentication logic
        if username == "admin" and password == "password":  
            session['user'] = username  # Store user in session
            return redirect(url_for('dashboard'))
        else:
            return render_template('sign_in.html', error="Invalid credentials")
    
    return render_template('sign_in.html')

@app.route("/sign_up")
def sign_up():
    return render_template('sign_up.html')

@app.route("/dashboard")
def dashboard():
    if 'user' not in session:  # Redirect if not logged in
        return redirect(url_for('sign_in'))
    return render_template('dashboard.html')

@app.route("/logout")
def logout():
    session.pop('user', None)  # Remove user session
    return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(debug=True)
