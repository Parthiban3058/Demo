from flask import Flask, render_template, request, redirect, url_for, flash,session
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///authentication.db'
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(50), nullable=False)


    # Sample questions
questions = [
   
        "1.Does your child make eye contact with others?",
        "2.Does your child respond when their name is called?",
        "3.Does your child enjoy playing with other children?",
        "4.Does your child engage in repetitive behaviors, such as hand-flapping or rocking?",
        "5.Does your child show interest in sharing their experiences or achievements with others?",
        "6.Does your child have difficulty understanding or using nonverbal cues, such as facial expressions or gestures?",
        "7.Does your child become upset by changes in routine?",
        "8.Does your child exhibit sensitivity to certain sensory stimuli, such as loud noises or bright lights?",
        "9.Does your child use language appropriately to communicate their needs and desires?",
        "10.Does your child exhibit intense interests in specific topics or objects?",
        "11.Does your child have difficulty understanding jokes or sarcasm?",
        "12.Does your child engage in repetitive play patterns?",
        "13.Does your child prefer to play alone rather than with others?",
        "14.Does your child have difficulty understanding social rules or expectations?",
        "15.Does your child have difficulty empathizing with others emotions?"
]

# Scoring algorithm (just a simple example)
def calculate_score(responses):
    
    valid_responses = [int(response) for response in responses if response is not None]
    # Calculate the score
    score = sum(valid_responses)
    return score




@app.route('/')
def index():
    return render_template('index.html')

@app.route('/home')
def home():
    return render_template('index.html')
@app.route('/about')
def about():
     username = session.get('username')  # Retrieve the username from the session
     return render_template('about.html', username=username)

@app.route('/blog')
def blog():
    
     return render_template('blog.html')

@app.route('/user',methods=['GET','POST'])
def user():
    return redirect('login')
   
@app.route('/logout')
def logout():
    session.pop('username', None)  # Remove username from session
    flash('You have been logged out.', 'info')
    return redirect(url_for('home'))


@app.route( '/login', methods=['GET', 'POST'])
def login():
    if 'username' in session:
        return redirect(url_for('assessment'))
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username, password=password).first()

        if user:
            session['username'] = username
            return redirect(url_for('assessment'))
        else:
            flash('Invalid username or password.', 'error')
    return render_template('login.html')



@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            flash('Username already exists. Please choose a different one.', 'error')
        else:
            new_user = User(username=username, password=password)
            db.session.add(new_user)
            db.session.commit()
            flash('Registration successful! Please log in.', 'success')
            return redirect(url_for('login'))

    return render_template('register.html')

@app.route('/assessment', )
def assessment():
   username = session.get('username')  # Retrieve the username from the session
   return render_template('assessment.html', username=username, questions=questions)
   
@app.route('/result', methods=['POST'])
def result():
    responses = [request.form.get(f"response{i+1}") for i in range(len(questions))]
    # Ensure all responses are None or "0" or "1"
    for response in responses:
        if response not in [None, "0", "1"]:
            return "Invalid response submitted"
    score = calculate_score(responses)
    
    # Determine likelihood based on score
    if score == 0:
        return  "You doesn't answer any questions"
    elif score < 8:
        return redirect(url_for('low_autism'))
    elif 8 <= score < 12:
        return redirect(url_for('moderate_autism'))
    else:
        return redirect(url_for('high_autism'))
    
@app.route('/low_autism')
def low_autism():
     username = session.get('username')  # Retrieve the username from the session
     return render_template('low_autism.html', username=username)
    
@app.route('/moderate_autism')
def moderate_autism():
     username = session.get('username')  # Retrieve the username from the session
     return render_template('moderate_autism.html', username=username)

@app.route('/high_autism')
def high_autism():
    username = session.get('username')  # Retrieve the username from the session
    return render_template('high_autism.html', username=username)
    


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
