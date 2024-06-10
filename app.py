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
        query = ('''SELECT customers.customer_id, customers.firstname, customers.familyname, customers.email, customers.phone
                    FROM bookings
                    INNER JOIN customers ON bookings.customer = customers.customer_id
                    WHERE bookings.booking_date = %s''')
        connection.execute(query, (campDate,))
        camperList = connection.fetchall()
        return render_template("camperlist.html", camperlist = camperList, campdate=campDate)
    
@app.route("/bookinglist", methods = ['GET'])
def bookinglist():
    connection = getCursor()
    connection.execute("SELECT * FROM bookings;")
    bookingList = connection.fetchall()
    return render_template("currentbooking.html", bookinglist = bookingList)

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

#@app.route("/booking/add", methods=['POST'])
#def makebooking():
    #print(request.form)
    #customerid = request.form.get('customer')
    #siteid = request.form.get('site')
    #bookingdate = request.form.get('bookingdate')
    #cur = getCursor()
    #cur.execute("INSERT INTO bookings (customer, site, booking_date) VALUES(%s,%s,%s);",(customerid, siteid, str(bookingdate)))
    #return redirect("/bookinglist")

@app.route("/booking/add", methods=['POST'])
def makebooking():
    customer = request.form.get('customer')
    site = request.form.get('site')
    booking_date = request.form.get('bookingdate')
    booking_nights = int(request.form.get('bookingnights'))
    occupancy = request.form.get('occupancy')

    first_night = date.fromisoformat(booking_date)
    last_night = first_night + timedelta(days=booking_nights - 1)

    connection = getCursor()
    for n in range(booking_nights):
        booking_day = first_night + timedelta(days=n)
        query = """
        INSERT INTO bookings (customer, site, booking_date, occupancy)
        VALUES (%s, %s, %s, %s)
        """
        connection.execute(query, (customer, site, booking_day, occupancy))

    return render_template('booking_confirmation.html', customer=customer, site=site, start_date=first_night, end_date=last_night, occupancy=occupancy)



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
    
@app.route('/edit_customer/<customer_id>', methods=["GET", "POST"])
def edit_customer(customer_id):
    if request.method == "GET":
        connection = getCursor()
        connection.execute("SELECT * FROM customers WHERE customer_id = %s", (customer_id,))
        customerDetail = connection.fetchone()
        return render_template('edit_customer.html', customerdetail=customerDetail)
    elif request.method == "POST":
        new_firstname = request.form['firstname']
        new_familyname = request.form['familyname']
        new_email = request.form['email']
        new_phone = request.form['phone']

        connection = getCursor()
        query = """
        UPDATE customers
        SET firstname = %s, familyname = %s, email = %s, phone = %s
        WHERE customer_id = %s
        """
        connection.execute(query, (new_firstname, new_familyname, new_email, new_phone, customer_id))

        return redirect("/allcamperlist")