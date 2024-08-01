from flask import Flask, render_template, url_for, redirect,request, flash, send_from_directory,Response, session,jsonify
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Integer, String, Time,Date,Boolean, Column, Text, ForeignKey
from sqlalchemy.orm import relationship
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from flask_login import login_user, logout_user,current_user, login_required,LoginManager, UserMixin
import logging
import os
from datetime import datetime
import json
import cv2
from ultralytics import YOLO
from ultralytics.data.explorer.explorer import Explorer

app = Flask(__name__)

bootstrap = Bootstrap()
bootstrap.init_app(app)

# Set the Login Manager to remember user is loged in 
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'  # Redirect to login if unauthorized
@login_manager.user_loader
def load_user(user_id):
    user = Users.query.get(int(user_id))
    return user

# Set the databae configuration and secret key
app.config["SECRET_KEY"] = 'noor_2024'
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///SPS.db"
db = SQLAlchemy()
db.init_app(app)

# set the YOLO Model
model = YOLO('best.pt')
camera = None
def gen_live_frames():
    global camera   
    while True:
        if not camera or not camera.isOpened():
            break
        success, frame = camera.read()
        if not success:
            break
        else:
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
def gen_yolo_frames():
    global camera
    while True:
        if not camera or not camera.isOpened():
            break
        success, frame = camera.read()
        if not success:
            break
        else:
            results = model.predict(source=frame)
            for result in results:
                boxes = result.boxes.xyxy
                scores = result.boxes.conf
                classes = result.boxes.cls
                for box, score, cls in zip(boxes, scores, classes):
                    x1, y1, x2, y2 = map(int, box[:4])
                    conf = score.item()
                    class_id = int(cls.item())
                    class_name = model.names[class_id]
                    if class_name == 'Occupied':
                        color = (0, 0, 255)  # Red for 'Occupied'
                    elif class_name == 'Empty':
                        color = (0, 255, 0)  # Green for 'Empty'
                    else:
                        color = (255, 255, 255)  # Default color (white)
                    label = f'{class_name} {conf:.2f}'
                    # Draw the bounding box and label on the frame
                    cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
                    cv2.putText(frame, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
@app.route('/video_live')
def video_live():
    return Response(gen_live_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')
@app.route('/video_yolo')
def video_yolo():
    return Response(gen_yolo_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')
@app.route('/start_stream')
def start_stream():
    global camera
    # 0 ivcam
    # 1 webcam
    # 2 iriun
    camera = cv2.VideoCapture(0)
    session['streaming'] = True
    return redirect(url_for('dashboard'))
@app.route('/stop_stream')
def stop_stream():
    global camera
    if camera:
        camera.release()
    camera = None
    session['streaming'] = False
    return redirect(url_for('dashboard'))
'''****************************** Users Table ******************************'''
class Users(db.Model, UserMixin):
    id = Column(Integer, primary_key=True)
    name =Column(String(80), nullable=False)
    email = Column(String(120), unique=True, nullable=False) # it should be unique
    password = Column(String(128), nullable=False)
    phone_number = Column(String(15), nullable=True)
    gender = Column(String(10), nullable=True)
    date_of_birth = Column(Date, nullable=True)
    nationality = Column(String(), nullable=True)
    about = Column(Text, nullable=True)
    profile_picture  = Column(String(50), nullable=True)
    cover_photo  = Column(String(50), nullable=True)
    contacts = relationship('Contacts', backref='users')  # One-to-Many relationship with contacts
    bookings = relationship('Bookings', backref='users')  # One-to-Many relationship with Booking
    is_admin = Column(Boolean, default=False)  # Flag to distinguish user type
    def set_password(self, password):
        self.password = generate_password_hash(password)
    def check_password(self, password):
        return check_password_hash(self.password, password)
'''****************************** End of Users Table ******************************'''
def get_user_counts_by_gender():
    males = count(Users.query.filter_by(gender='Male').all()) 
    females = count(Users.query.filter_by(gender='Female').all())
    return {
        "male":males,
        "female":females
    }
def count(a):
    counter = 0
    for i in a:
        counter = counter + 1
    return counter
'''****************************** Contact/Feedback Table ******************************'''
class Contacts(db.Model, UserMixin):
    id = Column(Integer, primary_key = True)
    name = Column(String(50), nullable=False)
    email = Column(String(120), nullable=False)
    phone = Column(String(15), nullable=True)
    company = Column(String(100), nullable=True)
    note =Column(Text, nullable=False)
    subject = Column(String(50), nullable=True)
    type_of_feedback = Column(String(50), nullable=True)
    user_id = Column(Integer, ForeignKey('users.id'))  # Foreign key to user model
'''****************************** End of Contact/Feedback Table ******************************'''
'''****************************** Booking Table ******************************'''
class Bookings(db.Model, UserMixin):
    id = Column(Integer, primary_key = True)
    user_id = Column(Integer, ForeignKey('users.id'))  # Foreign key to user model
    number_plate = Column(String(50), nullable=False)
    vihicle_type = Column(String(50), nullable=True)
    arrival_date = Column(Date, nullable=False)
    arrival_time = db.Column(String(10), nullable=False)
    departure_date = Column(Date, nullable=False)
    departure_time = db.Column(String(10), nullable=False)
    time_duration = Column(Integer, nullable=True)
    cost_per_hour = Column(Integer, nullable=False, default=20)
    total_ammount = Column(Integer, nullable=True)
    slot_number = Column(Integer, nullable=False)
with app.app_context():
    db.create_all()
'''****************************** All Routes  ******************************'''
@app.route("/")
@app.route('/home')
def index():
    return render_template("index.html")


    
@app.errorhandler(404)
def page_404(e):
    return render_template("404.html"), 404



video_path = 'static\images\carPark.mp4'
video_path_yolo = 'static\images\carPark.avi'
def generate_frames():
    cap = cv2.VideoCapture(video_path)
    while True:
        success, frame = cap.read()
        if not success:
            break
        else:
            # Encode the frame in JPEG format
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()

            # Yield the frame as a byte stream
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
def generate_frames_yolo():
    cap = cv2.VideoCapture(video_path_yolo)
    while True:
        success, frame = cap.read()
        if not success:
            break
        else:
            # Encode the frame in JPEG format
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()

            # Yield the frame as a byte stream
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
@app.route("/demo")
def demo():
    return render_template("demo.html")

# a route to show the video or frams generates from gnenerate_frames to web page
@app.route('/video_feed_demo')
def video_feed_demo():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

# a route to show the video or frams generates from gnenerate_frames to web page
@app.route('/video_feed_yolo_demo')
def video_feed_yolo_demo():
    return Response(generate_frames_yolo(), mimetype='multipart/x-mixed-replace; boundary=frame')

   
'''****************************** FOR CONTACTS AND RELATED PAGES AND ROUTES ******************************'''
@app.route("/contact", methods=['GET', 'POST'])
@login_required
def contact():
    user = current_user
    if request.method == 'POST':
        subject = request.form.get("subject")
        type_of_feedback = request.form.get("type")
        name = request.form.get("name")
        email = request.form.get("email")
        phone = request.form.get("phone")
        company = request.form.get("company")
        note = request.form.get("note")
        new_contact = Contacts(name=name,email=email,phone=phone,company=company,
        note=note, subject=subject, type_of_feedback=type_of_feedback, user_id=user.id)
        db.session.add(new_contact)
        db.session.commit()
        if current_user.is_admin:
            flash("Feedback or Contact added", category="success")
            return redirect(url_for("contact_details"))
        else:
            flash("Feedback or Contact Recieved", category="success")
            return redirect(url_for("index"))
    else:
        return render_template("contact.html")
@app.route('/contact_details')
@login_required
def contact_details():
    return render_template('contact_details.html', contacts = Contacts.query.all())
@app.route("/update_contact/<int:id>", methods=['GET', 'POST'])
@login_required
def update_contact(id):
    contact_to_update = Contacts.query.get_or_404(id)
    if request.method == 'POST':
        contact_to_update.subject = request.form.get("subject")
        contact_to_update.type_of_feedback = request.form.get("type")
        contact_to_update.name = request.form.get("name")
        contact_to_update.email = request.form.get("email")
        contact_to_update.phone = request.form.get("phone")
        contact_to_update.company = request.form.get("company")
        contact_to_update.note = request.form.get("note")
        db.session.commit()
        if current_user.is_admin:
            flash("Feedback or Contact Updated Successfully", category="success")
            return redirect(url_for("contact_details"))
        else:
            flash("Feedback or Contact Recieved", category="success")
            return redirect(url_for("index"))
    else:
        return render_template('update_contact.html', contact=contact_to_update)
@app.route("/delete_contact/<int:id>")
@login_required
def delete_contact(id):
    contact_to_delete = Contacts.query.get_or_404(id)
    db.session.delete(contact_to_delete)
    db.session.commit()
    flash("Contact Deleted Successfully", category='success')
    return redirect(url_for('contact_details'))
@app.route('/about')
def about():
    return render_template('about.html')

@app.route("/services")
def services():
    return render_template("services.html")
@app.route("/terms")
def terms():
    return render_template('terms.html')
@app.route("/detail")
def detail():
    return render_template("detail.html")
@app.route("/article_details")
def article_details():
    return render_template("article-details.html")
'''****************************** Authentication  ******************************'''
@app.route("/signup", methods=['GET','POST'])
def signup():
    if request.method =="POST":
        # get the form values
        name = request.form.get("name")
        email = request.form.get("email")
        password = request.form.get("password")
        # Check for existing email
        existing_user = Users.query.filter_by(email=email).first()
        if existing_user:
            flash('Email already exists!', category='error')
            return render_template('signup.html')
        # Create new user
        user = Users(name=name, email=email)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        flash('Signup successful!', category='success')
        return redirect(url_for('login'))
    else:
        # for GET method
        return render_template("signup.html")


@app.route("/login", methods=['GET','POST'])
def login():
    # check fot POST requist
    if request.method == "POST":
        # get the email and password
        email = request.form.get('email')
        password = request.form.get('password')
        terms_condition = True if request.form.get('check') else False
        
        user = Users.query.filter_by(email=email).first()
        if user and user.check_password(password):
            login_user(user, remember=terms_condition)
            flash('Logged In Successfully.', category='success')
            if user.is_admin:
                return redirect(url_for('dashboard'))
            else:
                return redirect(url_for('profile'))
        else:
            flash('Invalid email or password', category='error')
            return render_template('login.html')
    else:
        return render_template("login.html")
# route for logout
@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash('Logged Out Successfully', 'success')
    return redirect(url_for('index'))
'''****************************** Profile and Action related to profile page ******************************'''
@app.route('/profile')
@login_required  # Add login protection (replace with your implementation)
def profile():
    user = Users.query.get(current_user.id)
    return render_template('profile.html', user=user)
# Define allowed image extensions
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
# Configure upload folder path for profile picture
app.config['PROFILE_PICTURE_FOLDER'] = 'static/uploads/profile_pictures/'
# Configure upload folder path for cover photo
app.config['COVER_PHOTO_FOLDER'] = 'static/uploads/cover_photos/'
# maximam upload size 16MB
app.config["MAX_CONTENT_LENGHT"] = 16 * 1024 * 1024
@app.route('/uploads_profile', methods=['POST'])
@login_required
def uploads_profile():
    # get the current user to update
    user = current_user
    # check if the post request has the file part
    if 'profile_picture' not in request.files:
        flash('No file part', category='error')
        return redirect(url_for('profile', user=user))
    file = request.files['profile_picture'] 
    # If the user does not select a file, the browser submits an
    # empty file without a filename.
    if file.filename == '':
        flash('No selected file', category='error')
        return redirect(url_for('profile', user=user))
    # Handle image uploa
    if  file and allowed_file(file.filename):
        unique_file_name = secure_filename(str(str(user.id)+file.filename))
        file.save(os.path.join(app.config['PROFILE_PICTURE_FOLDER'], unique_file_name))
        # Update user profile picture in database
        user.profile_picture = unique_file_name  # Update user model with filename
        #user.profile_picture_data = file.rea
        db.session.commit()
        flash('Profile picture updated Successfully', category='success')
        return redirect(url_for('profile', user=user))
        #return unique_file_name
    else:
        flash('Invalid image format. Allowed formats: JPEG, PNG, GIF', category='error')
        return redirect(url_for('profile'))
@app.route("/uploads_cover", methods=['POST'])
@login_required
def uploads_cover():
    # get the current user to update
    user = current_user
    # check if the post request has the file part
    if 'cover_photo' not in request.files:
        flash('No file part', category='error')
        return redirect(url_for('profile', user=user))
    file = request.files['cover_photo']
    # If the user does not select a file, the browser submits an
    # empty file without a filename.
    if file.filename == '':
        flash('No selected file', category='error')
        return redirect(url_for('profile', user=user))
    # Handle image uploa
    if  file and allowed_file(file.filename):
        unique_file_name = secure_filename(str(str(user.id)+file.filename))
        file.save(os.path.join(app.config['COVER_PHOTO_FOLDER'], unique_file_name))
        # Update user profile picture in database
        user.cover_photo = unique_file_name  # Update user model with filename
        db.session.commit()
        flash('Cover Photo updated Successfully', category='success')
        return redirect(url_for('profile', user=user))
        #return unique_file_name
    else:
        flash('Invalid image format. Allowed formats: JPG, JPEG, PNG, GIF', category='error')
        return redirect(url_for('profile')) 
@app.route('/uploads_profile/<filename>')
def uploaded_profile(filename):
    return send_from_directory(app.config['PROFILE_PICTURE_FOLDER'], filename)
@app.route('/uploads_cover/<filename>')
def uploaded_cover(filename):
    return send_from_directory(app.config['COVER_PHOTO_FOLDER'], filename)
@app.route("/profile_details" , methods=['POST'])
@login_required
def profile_details():
    # get current user
    user = current_user
    # get form details
    gender = request.form.get('gender')
    date_of_birth = request.form.get('date')
    nationality = request.form.get('nationality')
    phone_number =  request.form.get('mobile')
    # add details 
    user.gender = gender
    user.phone_number = phone_number
    date_string = str(date_of_birth)  # Corrected date string
    date_object = datetime.date
    try:
        date_object = datetime.strptime(date_string, '%Y-%m-%d').date()
        print("Converted date:", date_object)
        user.date_of_birth = date_object
    except ValueError:
        print("Invalid date format. Please use YYYY-MM-DD.")
        
    user.nationality = nationality
    db.session.commit()
    flash('Profile Details updated successfully!', category='success')
    return redirect(url_for('profile',user=user))
@app.route("/profile_about", methods=['POST'])
@login_required
def profile_about():
    user = current_user # Get current user details
    about = request.form.get('about')
    user.about = about
    db.session.commit()
    flash('About updated successfully!', category='success')
    return redirect(url_for('profile', about=about))
'''****************************** Viewing User and actions related to this page ******************************'''
@app.route('/add_user', methods=['GET','POST'])
@login_required
def add_user():
    if request.method == 'POST':
        name = request.form.get("name")
        email = request.form.get("email")
        password = request.form.get("password")
        role = request.form.get("role")
        if role == 'admin':
            is_admin = True
        else:
            is_admin = False
        gender = request.form.get("gender")
        # create a new User 
        new_user = Users(name=name, email=email,gender=gender, is_admin=is_admin)
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()
        flash("User Addedd Successfully!!", category='success')
        return redirect(url_for('user_details'))
    else:
        return render_template('user_details.html')
@app.route('/update_user/<int:id>', methods=['GET','POST'])
@login_required
def update_user(id):
    user_to_update = Users.query.get_or_404(id)
    if request.method == 'POST':
        # get all infromation from rquest Form
        try:
            role = request.form.get("role")
            if role == 'admin':
                is_admin = True
            else:
                is_admin = False           
            # update the user with recieved id
            user_to_update.name = request.form.get("name")
            user_to_update.email =request.form.get("email")
            user_to_update.set_password(request.form.get("password"))
            user_to_update.is_admin = is_admin
            db.session.commit()
            flash("User Updated Successfully!!", category='success')
            return redirect(url_for('user_details'))
        except:
            flash("Woops There was a problem during user Updating try again", category='danger')
            return redirect(url_for('user_details'))
    else:
        return render_template('update_user.html', user=user_to_update)
@app.route('/delete_user/<int:id>')
@login_required
def delete_user(id):
    user_to_delete = Users.query.get_or_404(id)
    try:
        db.session.delete(user_to_delete)
        db.session.commit()
        flash("User deleted Successfully!!", category='success')
        return redirect(url_for("user_details"))
    except:
        flash("Woops There was a problem during user deleting try again", category='danger')
        return redirect(url_for("user_details"))
@app.route('/delete_user_profile', methods=['POST'])
@login_required
def delete_user_profile():
    user =current_user
    db.session.delete(user)
    db.session.commit()
    flash('Your account has been deleted successfully.', category='info')
    return redirect(url_for('logout'))      
@app.route("/dashboard", methods=['GET', 'POST'])
@login_required
def dashboard():
    user = current_user
    # Prepare chart data for engagements chart Users (bar)
    chart_values_users = [db.session.query(Users).count(), db.session.query(Contacts).count(), db.session.query(Bookings).count()]
     # Prepare chart data for engagements chart Users (pie)
    user_counts = get_user_counts_by_gender()
    chart_values_male_female = [user_counts["male"], user_counts["female"]]
    return render_template('dashboard.html',
    chart_values_users=json.dumps(chart_values_users), chart_values_male_female=json.dumps(chart_values_male_female))
@app.route("/user_details")
@login_required
def user_details():
    users = Users.query.all()
    return render_template("user_details.html", users=users)
@app.route("/parking_cost", methods=['GET', 'POST'])
@login_required
def parking_cost():
    if request.method == "POST":
        cost_value = request.form.get('cost')
        return render_template("parking_cost.html", cost_value=cost_value)

    else:
        cost_value = 20
        return render_template("parking_cost.html", cost_value=cost_value)
'''****************************** Bookings and related actions ******************************'''
@app.route("/book", methods=['GET', 'POST'])
@login_required
def book():
    if request.method =='POST':
        user = current_user
        bookings = Bookings()
        bookings.cost_per_hour = 20
        plate = request.form.get('plate')
        vihile_type = request.form.get('vihicle_type')
        arrival_date = request.form.get('arival_date')
        arrival_time = request.form.get('arival_time')
        departure_date = request.form.get('departure_date')
        departure_time = request.form.get('departure_time')
        time_duration = int(request.form.get("duration"))
        slot_number = request.form.get('slot_number')
        # conert time 
        at = convertTime(arrival_time)
        dt = convertTime(departure_time)
        # calculate the total ammount
        total_ammount = time_duration * int(bookings.cost_per_hour)         
        new_booking = Bookings(
            user_id=user.id,
            number_plate=plate,
            vihicle_type=vihile_type,
            arrival_date=convertDate(arrival_date),
            arrival_time=at,
            departure_date=convertDate(departure_date),
            departure_time=dt,
            slot_number = slot_number,
            time_duration=time_duration,
            cost_per_hour = bookings.cost_per_hour,
            total_ammount= total_ammount)
        db.session.add(new_booking)
        db.session.commit()
        flash("Slot Booked Successfully", category='success')
        if current_user.is_admin:
            return redirect(url_for("view_booking"))
        else:
            return redirect(url_for("index"))
    else:
        return render_template("book_slot.html")
@app.route("/view_booking", methods=['GET'])
@login_required
def view_booking():
    bookings = Bookings.query.all()
    if request.method == "GET":
        return render_template("view_booking.html", bookings = bookings)
def convertDate(date_str):
    date_object = datetime.date
    date_object = datetime.strptime(str(date_str), '%Y-%m-%d').date()
    return date_object
def convertTime(time_str):
    T = time_str.split(":")
    hh = T[0]
    mm = T[1]
    am_pm = ''
    if hh>= "00" and hh <= "11":
        am_pm = 'AM'
    else:
        hh = "0" + str(int(hh) % 12)
        am_pm = 'PM'
    # return the formated time
    return f'{hh}:{mm} {am_pm}'
@app.route("/delete_booking/<int:id>")
@login_required
def delete_booking(id):
    booking_to_delete = Bookings.query.get_or_404(id)
    try:
        db.session.delete(booking_to_delete)
        db.session.commit()
        flash("Booking deleted Successfully!!", category='success')
        return redirect(url_for("view_booking"))
    except:
        flash("Woops There was a problem during Booking deleting try again", category='danger')
        return redirect(url_for("view_booking"))
@app.route("/update_booking/<int:id>", methods = ['GET', 'POST'])
@login_required
def update_booking(id):
    booking_to_update = Bookings.query.get_or_404(id)
    if request.method == 'POST':
        try:
            cost_per_hour = 20
            time_duration = int(request.form.get("duration"))
            # conert time 
            at = convertTime(request.form.get('arival_time'))
            dt = convertTime(request.form.get('departure_time'))
            # calculate the total ammount
            total_ammount = time_duration * int(cost_per_hour)
            booking_to_update.number_plate = request.form.get('plate')
            booking_to_update.vihicle_type = request.form.get('vihicle_type')
            booking_to_update.arrival_date = convertDate(request.form.get('arival_date'))
            booking_to_update.arrival_time = at
            booking_to_update.departure_date =convertDate(request.form.get('departure_date'))
            booking_to_update.departure_time = dt
            booking_to_update.time_duration = time_duration
            booking_to_update.cost_per_hour = cost_per_hour
            booking_to_update.total_ammount = total_ammount
            db.session.commit()
            flash("Bookings Update successfully", category='success')
            if current_user.is_admin:
                return redirect(url_for("view_booking"))
            else:
                return redirect(url_for("index"))
        except:
            flash("Woops There was a problem during Booking updaing try again", category='danger')
            return redirect(url_for("view_booking"))
    else:
         return render_template('update_booking.html', booking = booking_to_update)
# run the application the debuger is true
if __name__ == '__main__':
    app.run(threaded=True, debug=True)
