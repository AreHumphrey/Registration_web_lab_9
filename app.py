import re
import hashlib
from datetime import datetime
from flask import Flask, render_template, request, jsonify, url_for, session
import os
from flask_sqlalchemy import SQLAlchemy

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'identifier.db')
db = SQLAlchemy(app)

def hash_password(password):
    return hashlib.sha256(password.encode('utf-8')).hexdigest()

@app.route('/')
def main():
    return render_template('pages/main.html')


@app.route('/registration', methods=['GET'])
def registration_form():
    return render_template('pages/registration.html')


@app.route('/submit_registration', methods=['POST'])
def submit_registration():
    from models import Users, User_details
    data = request.form

    first_name = data.get('first_name')
    session['first_name'] = first_name
    last_name = data.get('last_name')
    middle_name = data.get('middle_name')
    city = data.get('city')
    birthday = datetime.strptime(data.get('birthday'), '%Y-%m-%d').date()
    email = data.get('email')

    password = data.get('password')
    hashed_password = hash_password(password)
    if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
        return False

    phone_number = data.get('phone_number')
    if not re.match(r'^\d{10}$', phone_number):
        return False


    new_user = Users(first_name=first_name, last_name=last_name, middle_name=middle_name, email=email,
                     phone_number=phone_number,  password=hashed_password)

    db.session.add(new_user)
    db.session.commit()

    new_details = User_details(birthday=birthday, city=city, user_id=new_user.id)
    db.session.add(new_details)
    db.session.commit()

    return jsonify({'redirect': url_for('show_result_page')})


@app.route('/result', methods=['GET'])
def show_result_page():
    user_name = session.get('first_name')
    return render_template('pages/result.html', user_name=user_name)


if __name__ == '__main__':
    db.create_all()
    app.run()
