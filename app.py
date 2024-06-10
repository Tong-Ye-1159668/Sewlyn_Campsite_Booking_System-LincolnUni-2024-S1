from flask import Flask
from flask import render_template
from flask import request
from flask import redirect
from flask import url_for
import re
from datetime import datetime
from datetime import date
from datetime import timedelta
import mysql.connector
from mysql.connector import FieldType
import connect

app = Flask(__name__)

dbconn = None
connection = None

def getCursor():
    global dbconn
    global connection
    connection = mysql.connector.connect(user=connect.dbuser, \
    password=connect.dbpass, host=connect.dbhost, \
    database=connect.dbname, autocommit=True)
    dbconn = connection.cursor()
    return dbconn

@app.route("/")
def home():
    return render_template("base.html")

@app.route("/campers", methods=['GET','POST'])
def campers():
    if request.method == "GET":
        return render_template("datepickercamper.html", currentdate = datetime.now().date())
    else:
        campDate = request.form.get('campdate')
        connection = getCursor()
        connection.execute("SELECT booking_id, site, customer, booking_date, occupancy FROM bookings WHERE booking_date = %s",(campDate,))
        camperList = connection.fetchall()
        return render_template("camperresult.html", camperlist = camperList, campdate=campDate)

@app.route("/booking", methods=['GET','POST'])
def booking():
    if request.method == "GET":
        return render_template("datepicker.html", currentdate = datetime.now().date())
    else:
        bookingNights = request.form.get('bookingnights')
        bookingDate = request.form.get('bookingdate')
        occupancy = request.form.get('occupancy')
        firstNight = date.fromisoformat(bookingDate)

        lastNight = firstNight + timedelta(days=int(bookingNights))
        connection = getCursor()
        connection.execute("SELECT * FROM customers;")
        customerList = connection.fetchall()
        connection.execute("select * from sites where occupancy >= %s AND site_id not in (select site from bookings where booking_date between %s AND %s);",(occupancy,firstNight,lastNight))
        siteList = connection.fetchall()
        return render_template("bookingform.html", customerlist = customerList, bookingdate=bookingDate, sitelist = siteList, bookingnights = bookingNights)    

@app.route("/booking/add", methods=['POST'])
def makebooking():
    print(request.form)
    pass

@app.route("/allcamperlist", methods = ['GET'])
def allcamperlist():
    connection = getCursor()
    connection.execute("SELECT * FROM customers;")
    allcamperList = connection.fetchall()
    return render_template("allcamperlist.html", allcamperlist = allcamperList)

@app.route("/addcustomer", methods=['GET', 'POST'])
def addcustomer():
    new_id = request.form.get('customer_id') 
    firstname = request.form.get('firstname') 
    familyname = request.form.get('familyname') 
    email = request.form.get('email')
    phone = request.form.get('phone')
    if request.method == "GET":
        return render_template("addcustomer.html") 
    else:
        connection = getCursor()
        connection.execute('SELECT MAX(customer_id) FROM customers')
        result = connection.fetchone()
        max_customer_id = result[0] if result[0] is not None else 0
        new_id = max_customer_id + 1
        connection.execute('INSERT INTO customers (customer_id, firstname, familyname, email, phone) VALUES (%s,%s,%s,%s,%s);', (new_id, firstname, familyname, email, phone,))
        return redirect("/allcamperlist")

@app.route('/search',  methods=["GET","POST"])
def search():
    if request.method == "GET":
        return render_template("search.html")
    else:
        search_Name = request.form['search_Name']
        connection = getCursor()
        connection.execute("SELECT * FROM customers WHERE firstname LIKE %s OR familyname LIKE %s;",('%' + search_Name + '%', '%' + search_Name + '%'))
        resultList = connection.fetchall()
        return render_template("search_results.html", resultlist=resultList, search_name=search_Name)