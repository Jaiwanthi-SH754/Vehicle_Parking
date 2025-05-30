from flask import Flask, render_template, request, flash, redirect, url_for, session
from models import db, User, ParkingLot, ParkingSpot, Reservation
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

# Configure the app (database URI, secret key)
app.config['SECRET_KEY']='jaiwanthi@123'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///parking.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app) #db connected to the app

def initialize_admin():
    with app.app_context():
        if not User.query.filter_by(role='admin').first():
            admin = User(
                full_name='Jaiwanthi',
                email='adminJai@gmail.com',
                password=generate_password_hash('admin123'),
                address='42 Narayana St, Chennai City',
                pin_code='600001',
                phone_number='9876543210',
                role='admin')
            db.session.add(admin)
            db.session.commit()

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/registration', methods=['GET', 'POST'])
def registration():
    if request.method == 'POST':
        full_name = request.form['full_name']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        if password != confirm_password:
            flash('Passwords do not match!', 'danger')
        address = request.form['address']
        pin_code = request.form['pincode']
        phone_number = request.form['phone']
        role = request.form.get('role', 'user')
        
        new_user = User(
            full_name=full_name,
            email=email,
            password=generate_password_hash(password),
            address=address,
            pin_code=pin_code,
            phone_number=phone_number,
            role=role
        )
        
        db.session.add(new_user)
        db.session.commit()

        flash('Registration successful! You can now log in.', 'success')
        return redirect(url_for('login'))
    return render_template('registration.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        user = User.query.filter_by(email=email).first()
        
        if user and check_password_hash(user.password, password):
            session['user_id'] = user.id
            session['role'] = user.role
            flash('Login successful!', 'success')
            return redirect(url_for('user_dashboard'))
        else:
            flash('Invalid email or password', 'danger')
    return render_template('login.html')

@app.route('/admin')
def admin():
    return render_template('admin.html')

#Initialize the database
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    initialize_admin()  
    app.run(debug=True)

