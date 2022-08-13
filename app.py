from crypt import methods
from random import random
from flask import Flask, render_template, request, session, url_for , redirect
from twilio.rest import Client
import random
from bson.objectid import ObjectId
import smtplib
from flask_uploads import configure_uploads, patch_request_class
import math
from fpdf import FPDF
from forms import UploadForm , photos
import os
import pickle
from resnet import ResNet
import joblib,os
from db_config import mongo
from datetime import datetime
from schemas.detectionHistory import validate_detectionHistory
from forms import RegistrationForm_ID , LoginForm_ID
import bcrypt

app=Flask(__name__)
app.config['SECRET_KEY'] = 'ec9439cfc6c796ae2029594d'
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['UPLOADED_PHOTOS_DEST'] = os.path.join(basedir, 'uploads') # you'll need to create a folder named uploads
UPLOAD_PATH=os.path.join(basedir, 'uploads')
app.config["MONGO_URI"] = "mongodb+srv://karthik:karthik@cluster0.rctxccl.mongodb.net/Fasal-Mithra"

mongo.init_app(app)


resnet = ResNet()

configure_uploads(app, photos)
patch_request_class(app)  # set maximum file size, default is 16MB

@app.route("/signup")
def login():
    form=RegistrationForm_ID()
    return render_template("signup.html",form=form)

@app.route("/verify", methods=['POST', 'GET'])
def verify():
    message = ''
    #if method post in index
    if "email" in session:
        return redirect(url_for("logged_in"))
    if request.method == "POST":
        Firstname = request.form.get("firstname")
        Lastname = request.form.get("lastname")
        Mobilenumber = request.form.get("mobile_number")
        EmailId = request.form.get("email_address")
        Password1=request.form.get("password1")
        Password2=request.form.get("password2")
        City=request.form.get("city")
        State=request.form.get("state")
        Zip=request.form.get("zip")
        
        email_found = mongo.db.users.find_one({"email": EmailId})
        if email_found:
            message = 'This email already exists in database'
            return render_template('index.html', message=message)
        if Password1 != Password2:
            message = 'Passwords should match!'
            return render_template('signup.html', message=message)
        else:
            hashed = bcrypt.hashpw(Password2.encode('utf-8'), bcrypt.gensalt())
            user_input = {'firstName': Firstname, 'lastName': Lastname, 'phone': Mobilenumber , 'password': Password2 , 'email': EmailId ,'city' : City , 'state' : State}
            #insert it in the record collection
            mongo.db.users.insert_one(user_input)
            #find the new created account and its email
            user_data = mongo.db.users.find_one({"email": EmailId})
            #if registered redirect to logged in as the registered user
            return render_template('verify_mobile.html', email=EmailId)
    return render_template('verify_mobile.html')

@app.route("/verify/mobile",methods=['POST','GET'])
def getotp():

    number=request.form['m_number']
    number="+91"+number
    val=getotpapi(number)
    if val:
        return render_template('enterotp_number.html')

def generateotp():
    return random.randrange(100000,999999)

def getotpapi(number):
    account_sid="AC9e190d819b63357ccf38543d018e2e2c"
    auth_token="ffb47bdd9eb5baee9b43caeea08bc440"
    client=Client(account_sid,auth_token)
    otp=generateotp()
    session['response']=str(otp)
    body='Your OTP is ' + str(otp)
    message=client.messages.create(
                            from_='+19854667072',
                            body=body,
                            to=number
    )
    if message.sid:
        return True 
    else:
        return False

@app.route('/verify/mobile/validate',methods=['POST'])
def validate():
    otp=request.form['otp']
    if 'response' in session:
        s=session['response']
        session.pop('response',None)
        if s==otp:
            return render_template('success_number.html')
        else:
            return 'You are not authorized, Sorry!!'
    return render_template('validateotp.html')

@app.route('/email',methods=['POST'])
def emailid_v():
    return render_template('verify_email.html')



@app.route("/verify/email",methods=['POST','GET'])
def verify_email():
    emailid = request.form['emailid']
    val=getotpapi_email(emailid)
    if val:
        return render_template('enterotp_email.html')

def generateotp_email():
    digits = "0123456789"
    OTP = ""
    for i in range(6):
        OTP += digits[math.floor(random.random() * 10)]
    otp = OTP #+ " is your OTP"
    return otp


def getotpapi_email(emailid):
    s = smtplib.SMTP('smtp.gmail.com', 587)
    s.starttls()
    s.login("seesawsofficial@gmail.com", "pinpekzdqvrcscqq")
    otp=generateotp_email()
    msg=otp + " is your OTP"
    s.sendmail('&&&&&&&&&&&&&&&&', emailid, msg)
    session['response']=str(otp)
    return True

@app.route('/verify/email/validate',methods=['POST'])
def validate_email():
    form=LoginForm_ID()
    otp=request.form['otp']
    if 'response' in session:
        s=session['response']
        session.pop('response',None)
        if s==otp:
            return render_template("login.html",form=form)
        else:
            return 'You are not authorized, Sorry!!'
    return render_template('/validateotp.html')



@app.route('/logged_in',methods=['POST'])
def logged_in():
    if request.method == "POST":
        EmailId = request.form.get("email_address")
        Password = request.form.get("password")
        p1 = mongo.db.users.find_one({"email": EmailId})
        if Password==p1["password"]:
            return render_template('index.html')
        else:
            return redirect(url_for("login"))

@app.route("/logout", methods=["POST", "GET"])
def logout():
    if "email" in session:
        session.pop("email", None)
        return render_template("signout.html")
    else:
        return render_template('index.html')




@app.route("/")
@app.route("/home")
def home():
    return render_template("index.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/contact") 
def contact():
    return render_template("contact.html")

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    form = UploadForm()
    return render_template('uploadimage.html', form=form)

@app.route("/predict", methods=['GET', 'POST']) 
def Predict():
    uid = '124352414'
    city = 'Hyderabad'
    ip = '13143536'
    district = 'Ranga Reddy'
    state = 'Telangana'
    lat = 11.4652
    lon = 242.24

    form = UploadForm()
    if request.method == 'POST':
        if form.photo.data:
            filename = photos.save(form.photo.data)
            file_url = photos.url(filename)
            imageurl= 'uploads/'+filename
            #image="uploads/AppleCedarRust2_1.jpg"
            detection = resnet.predict_image(imageurl)
            print(detection)
            detection_split = detection.split('___')
            plant, disease = detection_split[0], detection_split[1]
            disease_info = mongo.db.disease.find_one({"name": detection})
            plant_info = mongo.db.plants.find_one({"commonName": plant})
            print(plant_info)
            detectionHistory = {
            "createdAt": str(datetime.now()),
            "ip": ip,
            "city": city,
            "district": district,
            "state": state,
            "location": {
                "lat": lat,
                "lon": lon
                },
            "detected_class": detection,
            "plantId": plant_info['_id'],
            "diseaseId":ObjectId('507f191e810c19729de860ea') if disease_info == None  else disease_info['_id'],
            "rating": 5
            }
            validated_detectionHistory = validate_detectionHistory(detectionHistory)
            done = mongo.db.detectionhistory.insert_one(validated_detectionHistory['data'])

        return render_template('predict.html',plant_info=plant_info,disease_info=disease_info,img=imageurl)
    return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True)