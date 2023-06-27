from app import app
from flask import render_template
from utils.helpers import send_email, hash_md5,generate_otp,send_email

@app.route('/',methods=['GET', 'POST'])
def index():
    if 'id' in session:
        return redirect(url_for('home'))

    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        if db.get_pass(email):
            if db.get_pass(email) == hash_md5(password):
                session['id'] = db.get_id(email)[0]
                return redirect(url_for('home'))
            else:
                return render_template('index.html', title='Index', custom_css='css/index.css', error='password incorrect')
        else:
            return render_template('index.html', title='Index', custom_css='css/index.css', error='email inavaible')

    return render_template('index.html', title='Index', custom_css='css/index.css')