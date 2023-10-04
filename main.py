import os
from datetime import datetime, timedelta

from flask import Flask, render_template, request, session, redirect
import pymysql

conn = pymysql.connect(host="localhost", user="root", password="maheshg@6714", db="DoctorAppointmentBooking")
cursor = conn.cursor()

APP_ROOT = os.path.dirname(os.path.abspath(__file__))
APP_ROOT = APP_ROOT + "/static"

app = Flask(__name__)
app.secret_key = "hijksdzgkjshbn"

status_hospital_accepted = "Request Accepted  By Hospital"
status_hospital_rejected = "Request Rejected By Hospital"
status_doctor_requested = "Doctor Requested"
status_prescription = 'Prescription Written By Doctor'
status_doctor_booking_cancelled = "Booking Cancelled By Doctor"
status_hospital_booking_cancelled = "Booking Cancelled By Hospital"
status_user_cancelled_booking = "Booking Cancelled By User"
@app.route("/")
def index():
    return render_template("index.html")


@app.route("/hLogin")
def hLogin():
    return render_template("hLogin.html")

@app.route("/dLogin")
def dLogin():
    return render_template("dLogin.html")

@app.route("/uLogin")
def uLogin():
    return render_template("uLogin.html")

@app.route("/aLogin")
def aLogin():
    return render_template("aLogin.html")

@app.route("/aLogin1",methods=['post'])
def aLogin1():
    Username = request.form.get("Username")
    Password = request.form.get("Password")
    if Username != 'admin':
        return render_template("msg.html", msg="Invalid  Username  ("+str(Username)+") ", color='text-danger')
    elif Password != 'admin':
        return render_template("msg.html", msg="Invalid  Password", color='text-danger')
    if Username == 'admin' and Password:
        session['role'] = 'admin'
        return render_template("admin.html")

@app.route("/logout")
def logout():
    session.clear()
    return render_template("index.html")

@app.route("/admin")
def admin():
    return render_template("admin.html")

@app.route("/addHospital")
def addHospital():
    return render_template("addHospital.html")

@app.route("/addHospital1",methods=['post'])
def addHospital1():
    hospital_name = request.form.get("hospital_name")
    email = request.form.get("email")
    password = request.form.get("password")
    picture = request.files['picture']
    path = APP_ROOT + "/hospitalPictures/" + picture.filename
    picture.save(path)
    phone = request.form.get("phone")
    speciality = request.form.get("speciality")
    address = request.form.get("address")
    a = cursor.execute("select * from Hospital where email='"+str(email)+"'")
    conn.commit()
    count = cursor.execute("select * from Hospital where phone='" + str(phone) + "'")
    conn.commit()
    print(a)
    if a > 0:
        return render_template("msg.html", msg="Email " + str(email) + " Exists", color='text-danger')
    elif count > 0:
        return render_template("msg.html", msg="Phone Number " + str(phone) + " Exists", color='text-danger')

    try:
        cursor.execute("insert into Hospital (hospital_name,email,phone,picture,password,speciality,address) values('"+str(hospital_name)+"','"+str(email)+"','"+str(phone)+"','"+str(picture.filename)+"','"+str(password)+"','"+str(speciality)+"','"+str(address)+"')")
        conn.commit()
        return render_template("msg.html", msg="Hospital Added Successfully", color='text-success')
    except Exception as e:
        print(e)
        return render_template("msg.html", msg="Something Went Wrong",color='text-danger')


@app.route("/viewHospitals")
def viewHospitals():
    cursor.execute("select * from Hospital")
    hospitals = cursor.fetchall()
    return render_template("viewHospitals.html", hospitals=hospitals)

@app.route("/doctorReg")
def doctorReg():
    return render_template("doctorReg.html")


@app.route("/doctorReg1",methods=['post'])
def doctorReg1():
    doctor_name = request.form.get("doctor_name")
    email = request.form.get("email")
    password = request.form.get("password")
    picture = request.files['picture']
    path = APP_ROOT + "/DoctorPictures/" + picture.filename
    picture.save(path)
    phone = request.form.get("phone")
    speciality = request.form.get("speciality")
    qualification = request.form.get("qualification")
    designation = request.form.get("designation")
    about = request.form.get("about")
    a = cursor.execute("select * from Doctor where email='" + str(email) + "'")
    conn.commit()
    count = cursor.execute("select * from Doctor where phone='" + str(phone) + "'")
    conn.commit()
    print(a)
    if a > 0:
        return render_template("msg.html", msg="Email " + str(email) + " Exists", color='text-danger')
    elif count > 0:
        return render_template("msg.html", msg="Phone Number " + str(phone) + " Exists", color='text-danger')

    try:
        cursor.execute(
            "insert into Doctor (doctor_name,email,phone,picture,password,speciality,qualification,designation,about) values('" + str(
                doctor_name) + "','" + str(email) + "','" + str(phone) + "','" + str(picture.filename) + "','" + str(
                password) + "','" + str(speciality) + "','" + str(qualification) + "','"+str(designation)+"','"+str(about)+"')")
        conn.commit()
        return render_template("msg.html", msg="Doctor Registered Successfully", color='text-success')
    except Exception as e:
        print(e)
        return render_template("msg.html", msg="Something Went Wrong", color='text-danger')




@app.route("/dLogin1",methods=['post'])
def dLogin1():
    email = request.form.get("email")
    password = request.form.get("password")
    a = cursor.execute("select * from Doctor where email='" + str(email) + "' and password='" + str(password) + "'")
    details = cursor.fetchall()
    if a > 0:
        doctor = details[0]
        session['doctor_id'] = doctor[0]
        session['role'] = 'Doctor'
        return redirect('doctor')
    else:
        return render_template("msg.html", msg='Invalid login details', color="text-danger")


@app.route("/doctor")
def doctor():
    cursor.execute("select * from Doctor where doctor_id='"+str(session['doctor_id'])+"'")
    doctor = cursor.fetchall()
    return render_template("doctor.html",doctor = doctor[0])



@app.route("/hLogin1",methods=['post'])
def hLogin1():
    email = request.form.get("email")
    password = request.form.get("password")
    a = cursor.execute("select * from Hospital where email='" + str(email) + "' and password='" + str(password) + "'")
    details = cursor.fetchall()
    if a > 0:
        Hospital = details[0]
        session['hospital_id'] = Hospital[0]
        session['role'] = 'Hospital'
        return redirect('hospital')
    else:
        return render_template("msg.html", msg='Invalid login details', color="text-danger")

@app.route("/hospital")
def hospital():
    cursor.execute("select * from Hospital where hospital_id='" + str(session['hospital_id']) + "'")
    hospital = cursor.fetchall()
    return render_template("hospital.html",hospital=hospital[0])

@app.route("/userReg")
def userReg():
    return render_template("userReg.html")


@app.route("/userReg1",methods=['post'])
def userReg1():
    name = request.form.get("name")
    email = request.form.get("email")
    password = request.form.get("password")
    phone = request.form.get("phone")
    gender = request.form.get("gender")
    address = request.form.get("address")
    bloodGroup = request.form.get("bloodGroup")
    age = request.form.get("age")
    try:
        cursor.execute("insert into User(name,email,phone,bloodGroup,password,gender,age,address) values('" + str(
                name) + "','" + str(email) + "','" + str(phone) + "','" + str(bloodGroup) + "','" + str(
                password) + "','" + str(gender) + "','" + str(age) + "','" + str(
                address) + "')")
        conn.commit()
        return render_template("msg.html", msg="User Registered Successfully", color='text-success')
    except Exception as e:
        print(e)
        return render_template("msg.html", msg="Something Went Wrong", color='text-danger')



@app.route("/uLogin1",methods=['post'])
def uLogin1():
    email = request.form.get("email")
    password = request.form.get("password")
    a = cursor.execute("select * from User where email='" + str(email) + "' and password='" + str(password) + "'")
    details = cursor.fetchall()
    if a > 0:
        User = details[0]
        session['user_id'] = User[0]
        session['role'] = 'User'
        return redirect('user')
    else:
        return render_template("msg.html", msg='Invalid login details', color="text-danger")

@app.route("/user")
def user():
    cursor.execute("select * from User where user_id='" + str(session['user_id']) + "'")
    user = cursor.fetchall()
    return render_template("user.html",user=user[0])


@app.route("/sendHospitalRequest")
def sendHospitalRequest():
    hospital_name = request.args.get("hospital_name")
    if hospital_name is None:
        hospital_name = ''
    cursor.execute("select * from Hospital where hospital_name like '%"+str(hospital_name)+"%'")
    hospitals = cursor.fetchall()
    if len(hospitals) == 0:
        return render_template("msg.html", msg='Hospitals Not Avilable', color='text-primary')
    return render_template("sendHospitalRequest.html",hospitals=hospitals,hospital_name=hospital_name,getSendRequestCount=getSendRequestCount)

@app.route("/sendRequest")
def sendRequest():
    hospital_id = request.args.get("hospital_id")
    return render_template("sendRequest.html",hospital_id=hospital_id)


@app.route("/sendRequest1",methods=['post'])
def sendRequest1():
    week_days = []
    for week_day in ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']:
        week_day = request.form.get(week_day)
        if week_day is not None :
             week_days.append(week_day)
    hospital_id = request.form.get("hospital_id")
    fromTime = request.form.get("fromTime")
    toTime = request.form.get("toTime")
    today = datetime.today().strftime("%Y-%m-%d %H:%M:%S")
    today = datetime.today().strftime('%Y-%m-%d')
    new_from_time = str(today) + " " + (fromTime)
    new_to_time = str(today) + " " + (toTime)
    new_from_time = datetime.today().strptime(new_from_time, "%Y-%m-%d %H:%M")
    new_to_time = datetime.today().strptime(new_to_time, "%Y-%m-%d %H:%M")
    cursor.execute("select * from DoctorRequests where doctor_id='"+str(session['doctor_id'])+"' and status != '"+str(status_hospital_rejected)+"'")
    doctorRequests = cursor.fetchall()
    for doctorRequest in doctorRequests:
        old_from_time = doctorRequest[2]
        old_to_time = doctorRequest[3]
        today = datetime.today().strftime("%Y-%m-%d %H:%M:%S")
        today = datetime.today().strftime('%Y-%m-%d')
        old_from_time = str(today) + " " + (old_from_time)
        old_to_time = str(today) + " " + (old_to_time)
        old_from_time = datetime.today().strptime(old_from_time, "%Y-%m-%d %H:%M")
        old_to_time = datetime.today().strptime(old_to_time, "%Y-%m-%d %H:%M")
        for day in week_days:
            if(day == doctorRequest[1]):
                if (old_from_time >= new_from_time and old_from_time <= new_to_time) and (
                        old_to_time >= new_from_time and old_to_time >= new_to_time):
                    return render_template("msg.html", msg='Time Conflict occurred for this doctor. fails to send the request', color='text-danger')
                elif (old_from_time <= new_from_time and old_from_time <= new_to_time) and (
                        old_to_time >= new_from_time and old_to_time <= new_to_time):
                    return render_template("msg.html", msg='Time Conflict occurred for this doctor. fails to send the request', color='text-danger')
                elif (old_from_time <= new_from_time and old_from_time <= new_to_time) and (
                        old_to_time >= new_from_time and old_to_time >= new_to_time):
                    return render_template("msg.html", msg='Time Conflict occurred for this doctor. fails to send the request', color='text-danger')
                elif (old_from_time >= new_from_time and old_from_time <= new_to_time) and (
                        old_to_time >= new_from_time and old_to_time <= new_to_time):
                    return render_template("msg.html", msg='Time Conflict occurred for this doctor. fails to send the request', color='text-danger')
    for day in week_days:
        cursor.execute("insert into DoctorRequests(day,fromTime,toTime,status,hospital_id,doctor_id) values('"+str(day)+"','"+str(fromTime)+"','"+str(toTime)+"','Doctor Requested','"+str(hospital_id)+"','"+str(session['doctor_id'])+"')")
        conn.commit()
    return render_template("msg.html",msg='Request Sent To Hospital',color='text-primary')


@app.route("/viewHospitalDoctors")
def viewHospitalDoctors():
    query = "select * from DoctorRequests where hospital_id='" + str(session['hospital_id']) + "' and status='"+str(status_hospital_accepted)+"' group by doctor_id"
    cursor.execute(query)
    doctorRequests = cursor.fetchall()
    if len(doctorRequests) == 0:
        return render_template("msg.html", msg='Doctors  Not Available', color='text-primary')
    return render_template("viewHospitalDoctors.html", get_hospital=get_hospital, getDoctor=getDoctor,doctorRequests=doctorRequests,getDoctorTimings1=getDoctorTimings1)


def get_hospital(hospital_id):
    cursor.execute("select * from hospital where hospital_id='"+str(hospital_id)+"'")
    hospital = cursor.fetchall()
    return hospital[0]

def get_hospital2(hospital_id):
    cursor.execute("select * from hospital where hospital_id='"+str(hospital_id)+"'")
    hospital = cursor.fetchall()
    return hospital[0]


@app.route("/viewDoctorRequests")
def viewDoctorRequests():
    query = ""
    if session['role'] == 'Hospital':
        query = "select * from DoctorRequests where hospital_id='"+str(session['hospital_id'])+"' and status='"+str(status_doctor_requested)+"' group by doctor_id"
        print(query)
    elif session['role'] == 'Doctor':
        query = "select * from DoctorRequests where doctor_id='"+str(session['doctor_id'])+"' and status='"+str(status_doctor_requested)+"' or status = '"+str(status_hospital_accepted)+"' group by doctor_id"
    cursor.execute(query)
    doctorRequests = cursor.fetchall()
    print(doctorRequests)
    if len(doctorRequests) == 0:
        return render_template("msg.html", msg='Doctor Requests Not Available', color='text-primary')
    return render_template("viewDoctorRequests.html",get_hospital2=get_hospital2, getDoctorTimings2=getDoctorTimings2, getHospitalBYDoctorRequest=getHospitalBYDoctorRequest,doctorRequests=doctorRequests,getDoctor=getDoctor,getDoctorTimings=getDoctorTimings)


def getDoctorTimings(doctor_id):
    query = ""
    print(query, "******")
    if session['role'] == 'Hospital':
        query = "select * from DoctorRequests where hospital_id='"+str(session['hospital_id'])+"' and status='"+str(status_doctor_requested)+"' and doctor_id='"+str(doctor_id)+"'"
        print(query,"******")
    elif session['role'] == 'Doctor':
        query = "select * from DoctorRequests where  status='"+str(status_doctor_requested)+"'  and doctor_id='"+str(doctor_id)+"'"
    elif session['role'] == 'User':
        query = "select * from DoctorRequests where  status = '"+str(status_hospital_accepted)+"' and doctor_id='"+str(doctor_id)+"'"
    print(query)
    cursor.execute(query)
    doctor_request_timings = cursor.fetchall()
    return doctor_request_timings




@app.route("/view_my_hospitals")
def view_my_hospitals():
    hospital_id = request.args.get("hospital_id")
    cursor.execute("select * from hospital where hospital_id='"+str(hospital_id)+"'")
    hospital = cursor.fetchall()
    return render_template("view_my_hospitals.html",hospital_id=hospital_id, hospital=hospital[0])


def getDoctor(doctor_id):
    cursor.execute("select * from Doctor where doctor_id='"+str(doctor_id)+"'")
    doctor = cursor.fetchall()
    return doctor[0]


@app.route("/doctorRequestStatus",methods=['post'])
def doctorRequestStatus():
    doctor_id = request.form.get("doctor_id")
    return render_template("doctorRequestStatus1.html",doctor_id=doctor_id)


@app.route("/rejectRequest",methods=['post'])
def rejectRequest():
    doctor_id = request.form.get("doctor_id")
    cursor.execute("update DoctorRequests set status='"+str(status_hospital_rejected)+"' where doctor_id='"+str(doctor_id)+"' and hospital_id='"+str(session['hospital_id'])+"' and status = '"+str(status_doctor_requested)+"'")
    conn.commit()
    return viewDoctorRequests()



@app.route("/doctorRequestStatus2",methods=['post'])
def doctorRequestStatus2():
    consultant_fee = request.form.get("consultant_fee")
    doctor_id = request.form.get("doctor_id")
    doctorRequest_id = request.form.get("doctorRequest_id")
    cursor.execute("update DoctorRequests set status='"+str(status_hospital_accepted)+"', consultant_fee='"+str(consultant_fee)+"' where doctor_id='" + str(doctor_id) + "' and hospital_id='"+str(session['hospital_id'])+"' and status='"+str(status_doctor_requested)+"'")
    conn.commit()
    cursor.execute("select * from DoctorRequests where doctor_id='" + str(doctor_id) + "' and hospital_id='"+str(session['hospital_id'])+"' and status='"+str(status_hospital_accepted)+"' and doctorRequest_id not in (select doctorRequest_id from Slots)")
    conn.commit()
    results = cursor.fetchall()
    for result in results:
        FromTime = result[2]
        ToTime = result[3]
        dd = datetime.date(datetime.now())
        dd2 = datetime.date(datetime.now())
        date = str(dd) + " " + (FromTime)
        date2 = str(dd2) + " " + (ToTime)
        dt = datetime.strptime(date, '%Y-%m-%d %H:%M')
        dt2 = datetime.strptime(date2, '%Y-%m-%d %H:%M')
        slot_number = 0
        while dt < dt2:
            from_dt = dt
            to_dt = from_dt + timedelta(minutes=20)
            dt = to_dt
            fromTime = from_dt.strftime('%H:%M')
            toTime = to_dt.strftime('%H:%M')
            slot_number = slot_number + 1
            cursor.execute("insert into Slots(fromTime,toTime,slot_number,day,doctorRequest_id) values('"+str(fromTime)+"','"+str(toTime)+"','"+str(slot_number)+"','"+str(result[1])+"','"+str(result[0])+"')")
            conn.commit()
    return render_template("msg.html",msg='Doctor Request Accepted',color='text-success')

def getSendRequestCount(hospital_id):
    count = cursor.execute("select * from DoctorRequests where hospital_id='"+str(hospital_id)+"' and doctor_id='"+str(session['doctor_id'])+"'")
    conn.commit()
    return count


@app.route("/viewDoctors")
def viewDoctors():
    search_name = request.args.get("search_name")
    if search_name is None:
        search_name = ''
    cursor.execute("select * from DoctorRequests where hospital_id in (select hospital_id from hospital where hospital_name like '%"+str(search_name)+"%' or speciality like '%"+str(search_name)+"%') or doctor_id in (select doctor_id from doctor where doctor_name like '%"+str(search_name)+"%' or speciality like '%"+str(search_name)+"%') and status = '"+str(status_hospital_accepted)+"' group by doctor_id")
    doctorRequests = cursor.fetchall()
    return render_template("viewDoctors.html",getDoctorTimings=getDoctorTimings,getDoctorByDoctorRequest=getDoctorByDoctorRequest,doctorRequests=doctorRequests,getHospitalBYDoctorRequest=getHospitalBYDoctorRequest,search_name=search_name, get_hospital=get_hospital)


def getHospitalBYDoctorRequest(hospital_id):
    cursor.execute("select * from Hospital where hospital_id='"+str(hospital_id)+"'")
    hospital = cursor.fetchall()
    return hospital[0]

def getDoctorByDoctorRequest(doctor_id):
    cursor.execute("select * from Doctor where doctor_id='"+str(doctor_id)+"'")
    doctor = cursor.fetchall()
    return doctor[0]

@app.route("/viewAvailableTimings")
def viewAvailableTimings():
    week_days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    booking_date = request.args.get('booking_date')
    doctor_id = request.args.get('doctor_id')
    if booking_date == None:
        date_time = datetime.today()
        print(date_time)
        day = date_time.weekday()
        print(day)
        booking_date = str(date_time.strftime('%Y-%m-%d'))
        booking_date2 = datetime.today().date()
        print(booking_date2)
    else:
        booking_date2 = booking_date
        booking_date = datetime.strptime(booking_date, '%Y-%m-%d')
        print(booking_date)
        day = booking_date.weekday()
        print(day)
        booking_date = str(booking_date)
        print(booking_date,"hhhh")
    day = week_days[day]
    cursor.execute("select * from DoctorRequests where doctor_id='"+str(doctor_id)+"' and status= '"+str(status_hospital_accepted)+"' and day='"+str(day)+"'")
    conn.commit()
    doctorRequests = cursor.fetchall()
    doctorRequests2 = []
    for doctorRequest in doctorRequests:
        doctorRequest = list(doctorRequest)
        query = "select * from Slots where doctorRequest_id='"+str(doctorRequest[0])+"'"
        cursor.execute(query)
        slots = cursor.fetchall()
        doctorRequest.append(slots)
        doctorRequests2.append(doctorRequest)
    print(doctorRequests2)
    return render_template("viewAvailableTimings.html",doctorRequests=doctorRequests2, doctor_id=doctor_id, booking_date2=booking_date2, booking_date=booking_date, day=day, isSlotBooked=isSlotBooked, getHospital_by_doctor_request_id=getHospital_by_doctor_request_id)


def getHospital_by_doctor_request_id(hospital_id):
    cursor.execute("select * from Hospital where hospital_id='"+str(hospital_id)+"'")
    hospital = cursor.fetchall()
    return hospital[0]



def isSlotBooked(slot_id,booking_date):
    a = cursor.execute("select * from Bookings where booking_date='"+str(booking_date)+"' and status='Doctor Appointment Booked' and slot_id='"+str(slot_id)+"'")
    conn.commit()
    if a == 0:
        return False
    else:
        return True


@app.route("/bookAppointment",methods=['post'])
def bookAppointment():
    booking_date = request.form.get("booking_date")
    slot_id = request.form.get("slot_id")
    cursor.execute("select * from DoctorRequests where doctorRequest_id in (select doctorRequest_id from slots where slot_id='"+str(slot_id)+"')")
    doctorRequests = cursor.fetchall()
    consultant_fee = doctorRequests[0][7]
    return render_template("bookAppointment.html",consultant_fee=consultant_fee,booking_date=booking_date,slot_id=slot_id)


@app.route("/bookAppointment1",methods=['post'])
def bookAppointment1():
    slot_id = request.form.get("slot_id")
    booking_date = request.form.get("booking_date")
    cause = request.form.get("cause")
    cursor.execute("select * from Slots where slot_id='"+str(slot_id)+"'")
    conn.commit()
    slots = cursor.fetchall()
    slot = slots[0]
    fromTime = slot[1]
    toTime = slot[2]
    cursor.execute("insert into Bookings(cause,booking_date,status,slot_id,user_id) values('"+str(cause)+"','"+str(booking_date)+"','Doctor Appointment Booked','"+str(slot_id)+"','"+str(session['user_id'])+"')")
    conn.commit()
    return render_template("msg.html", msg='Your Appointment Booked On '" " +str(booking_date)+"   "+str(fromTime) + " - " + str(toTime),color='text-primary ')


@app.route("/viewBookings")
def viewBookings():
    query = ""
    if session['role'] == 'User':
        query = "select * from Bookings where user_id='"+str(session['user_id'])+"'"
    elif session['role'] == 'Doctor':
        query = "select * from bookings where slot_id in (select slot_id from slots where doctorRequest_id in (select doctorRequest_id from doctorrequests where doctor_id in (select doctor_id from Doctor where doctor_id='" + str(
            session['doctor_id']) + "'))) "
    elif session['role'] == 'Hospital':
        query = "select * from bookings where slot_id in (select slot_id from slots where doctorRequest_id in (select doctorRequest_id from doctorrequests where hospital_id in (select hospital_id from hospital where hospital_id='"+str(session['hospital_id'])+"'))) "
    cursor.execute(query)
    bookings = cursor.fetchall()
    if len(bookings) == 0:
        return render_template("msg.html", msg='No Bookings', color='text-primary')
    return render_template("viewBookings.html",isHospitalRated=isHospitalRated, isDoctorRated=isDoctorRated, getHospitalBYBookings=getHospitalBYBookings,bookings=bookings,getDoctorBYBookings=getDoctorBYBookings,getSlot_idByBookings=getSlot_idByBookings,getUser_idByBookings=getUser_idByBookings)


def getDoctorBYBookings(booking_id):
     cursor.execute("select * from Doctor where doctor_id in (select doctor_id from DoctorRequests where doctorRequest_id in (select doctorRequest_id from slots where slot_id in (select slot_id from bookings where booking_id='"+str(booking_id)+"'))) ")
     doctors = cursor.fetchall()
     doctor = doctors[0]
     print(doctor)
     return doctor

def getSlot_idByBookings(slot_id):
    cursor.execute("select * from Slots where slot_id='"+str(slot_id)+"'")
    slots = cursor.fetchall()
    slot = slots[0]
    print(slot)
    return slot


def getUser_idByBookings(user_id):
    cursor.execute("select * from User where user_id='"+str(user_id)+"'")
    users = cursor.fetchall()
    user = users[0]
    return user

def getHospitalBYBookings(booking_id):
    cursor.execute(
        "select * from hospital where hospital_id in (select hospital_id from DoctorRequests where doctorRequest_id in (select doctorRequest_id from slots where slot_id in (select slot_id from bookings where booking_id='" + str(
            booking_id) + "'))) ")
    hospitals = cursor.fetchall()
    hospital = hospitals[0]
    return hospital


@app.route("/BookingStatus",methods=['post'])
def BookingStatus():
    booking_id = request.form.get("booking_id")
    cursor.execute("update Bookings set status = '"+str(status_hospital_booking_cancelled)+"' where booking_id = '"+str(booking_id)+"' ")
    conn.commit()
    return render_template("msg.html", msg='Booking Cancelled',color='text-danger')



@app.route("/BookingStatus2",methods=['post'])
def BookingStatus2():
    booking_id = request.form.get("booking_id")
    cursor.execute("update Bookings set status = '"+str(status_user_cancelled_booking)+"' where booking_id = '"+str(booking_id)+"' ")
    conn.commit()
    return render_template("msg.html", msg='Booking Cancelled',color='text-danger')





@app.route("/BookingStatus1",methods=['post'])
def BookingStatus1():
    booking_id = request.form.get("booking_id")
    cursor.execute("update Bookings set status = '"+str(status_doctor_booking_cancelled)+"' where booking_id = '"+str(booking_id)+"' ")
    conn.commit()
    return render_template("msg.html", msg='Booking Cancelled',color='text-danger')


@app.route("/acceptRequest",methods=['post'])
def acceptRequest():
    booking_id = request.form.get("booking_id")
    cursor.execute("update Bookings set status = 'User Booking Accepted' where booking_id = '" + str(booking_id) + "' ")
    conn.commit()
    return viewBookings()


@app.route("/writePrescription",methods=['post'])
def writePrescription():
    booking_id = request.form.get("booking_id")
    return render_template("writePrescription.html",booking_id=booking_id)

@app.route("/writePrescription1",methods=['post'])
def writePrescription1():
    booking_id = request.form.get("booking_id")
    prescription = request.form.get("prescription")
    cursor.execute("update Bookings set status = '"+str(status_prescription)+"', prescription= '"+str(prescription)+"' where booking_id='"+str(booking_id)+"'")
    conn.commit()
    return viewBookings()

def isDoctorRated(booking_id,review_for):
    isRated = cursor.execute("select * from Reviews where booking_id='"+str(booking_id)+"' and review_for = 'Doctor'")
    return isRated

def isHospitalRated(booking_id,review_for):
    isRated1 = cursor.execute(
        "select * from Reviews where booking_id='" + str(booking_id) + "' and review_for = 'Hospital'")
    return isRated1

@app.route("/RatingForDoctor",methods=['post'])
def RatingForDoctor():
    booking_id = request.form.get("booking_id")
    return render_template("RatingForDoctor.html",booking_id=booking_id)


@app.route("/RatingForDoctor1",methods=['post'])
def RatingForDoctor1():
    booking_id = request.form.get("booking_id")
    rating = request.form.get("rating")
    review = request.form.get("review")
    cursor.execute("insert into Reviews (rating,review,review_for,booking_id) values('"+str(rating)+"','"+str(review)+"','Doctor','"+str(booking_id)+"')")
    conn.commit()
    return viewBookings()


@app.route("/RatingForHospital",methods=['post'])
def RatingForHospital():
    booking_id = request.form.get("booking_id")
    return render_template("RatingForHospital.html",booking_id=booking_id)


@app.route("/RatingForHospital1",methods=['post'])
def RatingForHospital1():
    booking_id = request.form.get("booking_id")
    rating = request.form.get("rating")
    review = request.form.get("review")
    cursor.execute("insert into Reviews (rating,review,review_for,booking_id) values('"+str(rating)+"','"+str(review)+"','Hospital','"+str(booking_id)+"')")
    conn.commit()
    return viewBookings()


@app.route("/hospitalRatings")
def hospitalRatings():
    hospital_id = request.args.get("hospital_id")
    cursor.execute("select  avg(rating)   from reviews where review_for='Hospital' and booking_id in (select booking_id from bookings where slot_id in (select slot_id from slots where doctorRequest_id in (select doctorRequest_id from doctorrequests where hospital_id = '"+str(hospital_id)+"')))")
    conn.commit()
    avg_rating = cursor.fetchall()
    avg_rating = avg_rating[0][0]
    print(avg_rating)
    cursor.execute("select * from reviews where review_for='Hospital' and booking_id in (select booking_id from bookings where slot_id in (select slot_id from slots where doctorRequest_id in (select doctorRequest_id from doctorrequests where hospital_id = '"+str(hospital_id)+"')))")
    reviews = cursor.fetchall()
    print(reviews)
    if len(reviews) == 0:
        return render_template("msg.html",msg= 'No Rating and Reviews',color='text-primary')
    return render_template("hospitalRatings.html", reviews=reviews, avg_rating=avg_rating,getUserbyReview=getUserbyReview)


def getUserbyReview(booking_id):
    cursor.execute("select * from User where user_id in (select user_id from bookings where booking_id='"+str(booking_id)+"')")
    user = cursor.fetchall()
    return user[0]


@app.route("/doctorRatings")
def doctorRatings():
    doctor_id = request.args.get("doctor_id")
    cursor.execute("select  avg(rating)  from reviews where review_for='Doctor' and booking_id in (select booking_id from bookings where slot_id in (select slot_id from slots where doctorRequest_id in (select doctorRequest_id from doctorrequests where doctor_id = '" + str(doctor_id) + "')))")
    conn.commit()
    avg_rating = cursor.fetchall()
    avg_rating = avg_rating[0][0]
    print(avg_rating)
    cursor.execute("select * from reviews where review_for='Doctor' and booking_id in (select booking_id from bookings where slot_id in (select slot_id from slots where doctorRequest_id in (select doctorRequest_id from doctorrequests where doctor_id = '" + str(doctor_id) + "')))")
    reviews = cursor.fetchall()
    print(reviews)
    if len(reviews) == 0:
        return render_template("msg.html", msg='No Rating and Reviews', color='text-primary')
    return render_template("doctorRatings.html",reviews=reviews,avg_rating=avg_rating,getUsers=getUsers)


def getUsers(booking_id):
    cursor.execute("select * from User where user_id in (select user_id from bookings where booking_id='" + str(booking_id) + "')")
    user = cursor.fetchall()
    return user[0]


def getDoctorTimings1(doctor_id):
    query = "select * from DoctorRequests where hospital_id='" + str(session['hospital_id']) + "' and status='" + str(status_hospital_accepted) + "' and doctor_id='" + str(doctor_id) + "'"
    print(query, "******")
    cursor.execute(query)
    doctor_request_timings = cursor.fetchall()
    print(doctor_request_timings)
    return doctor_request_timings




def getDoctorTimings2(doctor_id):
    query = "select * from DoctorRequests where  status='" + str(status_hospital_accepted) + "' or status='" + str(status_doctor_requested) + "'  and doctor_id='" + str(doctor_id) + "'"
    cursor.execute(query)
    doctor_request_timings2 = cursor.fetchall()
    print(doctor_request_timings2)
    return doctor_request_timings2




app.run(debug=True)