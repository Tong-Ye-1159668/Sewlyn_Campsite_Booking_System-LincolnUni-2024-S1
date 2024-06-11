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

# Display a list of campers who are camping on a particular night
@app.route("/campers", methods=['GET','POST'])
def campers():
    if request.method == "GET":
        return render_template("datepickercamper.html", currentdate = datetime.now().date())
    else:
        campDate = request.form.get('campdate')
        connection = getCursor()

        # Retrieve camper information for the particular date
        connection.execute('''SELECT customers.customer_id, customers.firstname, customers.familyname, customers.email, customers.phone, bookings.booking_id
                            FROM bookings INNER JOIN customers ON bookings.customer = customers.customer_id
                            WHERE bookings.booking_date = %s''', (campDate,))
        camperList = connection.fetchall()

        # Render the camper list with the particular camp date
        return render_template("camperlist.html", camperlist = camperList, campdate=campDate)

# Display a booking form to book a site
@app.route("/booking", methods=['GET','POST'])
def booking():
    if request.method == "GET":
        return render_template("datepicker.html", currentdate = datetime.now().date())
    else:
        bookingNights = request.form.get('bookingnights')
        bookingDate = request.form.get('bookingdate')
        occupancy = request.form.get('occupancy')

        # Calculate the last night of the booking
        firstNight = date.fromisoformat(bookingDate)
        lastNight = firstNight + timedelta(days=int(bookingNights))

        connection = getCursor()
        connection.execute("SELECT * FROM customers;")
        customerList = connection.fetchall()

        # Query to retrieve available sites for the specified occupancy and date range
        connection.execute("select * from sites where occupancy >= %s AND site_id not in (select site from bookings where booking_date between %s AND %s);",(occupancy,firstNight,lastNight))
        siteList = connection.fetchall()

        # Render the booking form with all customer list, available sites, and booking details
        return render_template("bookingform.html", customerlist = customerList, bookingdate=bookingDate, sitelist = siteList, bookingnights = bookingNights, occupancy = occupancy)    


# Add a booking to the database
@app.route("/booking/add", methods=['POST'])
def makebooking():
    customerId = request.form.get('customer')
    siteId = request.form.get('site')
    bookingDate = request.form.get('bookingdate')
    bookingNights = request.form.get('bookingnights')
    occupancy = request.form.get('occupancy')

    bookingnights = int(bookingNights)
    firstNight = date.fromisoformat(bookingDate)
    
    connection = getCursor()

    # Insert each night of the booking into the database
    for night in range(bookingnights):
        current_night = firstNight + timedelta(days=night)
        connection.execute("INSERT INTO bookings (site, customer, booking_date, occupancy) VALUES (%s, %s, %s, %s)", (siteId, customerId, current_night, occupancy))

    # Fetch customer details for confirmation
    connection = getCursor()
    connection.execute("SELECT firstname, familyname FROM customers WHERE customer_id = %s", (customerId,))
    customer = connection.fetchone()

    customerName = f"{customer[0]} {customer[1]}"

    # Calculate the check out date of the booking
    lastNight = firstNight + timedelta(days=bookingnights)

    # Render the booking confirmation page with the booking details
    return render_template("booking_confirmation.html", customername=customerName, siteid=siteId, firstnight=firstNight, lastnight=lastNight, bookingnights=bookingNights, occupancy=occupancy)


# Display a list of all campers
@app.route("/allcamperlist", methods = ['GET'])
def allcamperlist():
    connection = getCursor()
    connection.execute("SELECT * FROM customers;")
    allCamperList = connection.fetchall()
    return render_template("allcamperlist.html", allcamperlist = allCamperList)


# Add a new customer to the database
@app.route("/addcustomer", methods=['GET', 'POST'])
def addcustomer():
    newId = request.form.get('customer_id') 
    firstName = request.form.get('firstname') 
    familyName = request.form.get('familyname') 
    email = request.form.get('email')
    phone = request.form.get('phone')
    if request.method == "GET":
        return render_template("addcustomer.html") 
    else:
        connection = getCursor()
        connection.execute("SELECT MAX(customer_id) FROM customers")
        result = connection.fetchone()
        max_customer_id = result[0] if result[0] is not None else 0
        newId = max_customer_id + 1
        # Insert the new customer into the database
        connection.execute("INSERT INTO customers (customer_id, firstname, familyname, email, phone) VALUES (%s,%s,%s,%s,%s);", (newId, firstName, familyName, email, phone,))
        # Fetch the new customer details to the whole customer list
        return redirect("/allcamperlist")


# Search for a customer by name, including partial text matches
@app.route('/search',  methods=["GET","POST"])
def search():
    if request.method == "GET":
        return render_template("search.html")
    else:
        searchName = request.form['searchName']
        connection = getCursor()

        # Query to search for customers by first name or family name
        connection.execute("SELECT * FROM customers WHERE firstname LIKE %s OR familyname LIKE %s;",('%' + searchName + '%', '%' + searchName + '%'))
        resultList = connection.fetchall()

        # Render the search results with the search name and result list
        return render_template("search_results.html", resultlist=resultList, searchname=searchName)


# Edit a customer's details
@app.route('/edit_customer/<customer_id>', methods=["GET", "POST"])
def edit_customer(customer_id):
    # Retrieve the customer details for editing
    if request.method == "GET":
        connection = getCursor()
        connection.execute("SELECT * FROM customers WHERE customer_id = %s", (customer_id,))
        customerDetail = connection.fetchone()
        return render_template('edit_customer.html', customerdetail=customerDetail)
    # Update the customer details in the database
    elif request.method == "POST":
        newFirstName = request.form['firstname']
        newFamilyName = request.form['familyname']
        newEmail = request.form['email']
        newPhone = request.form['phone']

        connection = getCursor()
        # Update the customer details in the database
        query = "UPDATE customers SET firstname = %s, familyname = %s, email = %s, phone = %s WHERE customer_id = %s;"
        connection.execute(query, (newFirstName, newFamilyName, newEmail, newPhone, customer_id))

        # Redirect to the list of all campers after updating the customer details
        return redirect("/allcamperlist")
    
#customer report
@app.route('/customer_report/<int:customer_id>', methods=['GET'])
def customer_report(customer_id):
    connection = getCursor()

    # Retrieve customer first name and family name
    connection.execute("SELECT firstname, familyname FROM customers WHERE customer_id = %s", (customer_id,))
    customerName = connection.fetchone()

    # Retrieve total booking nights of the customer
    connection.execute("SELECT COUNT(*) FROM bookings WHERE customer = %s", (customer_id,))
    totalNights = connection.fetchone()

    # Calculate average occupancy for the customer 
    connection.execute("SELECT AVG(occupancy) FROM bookings WHERE customer = %s", (customer_id,))
    avgOccupancy = connection.fetchone()

    return render_template("customer_report.html", firstname=customerName[0], familyname=customerName[1], totalnights=totalNights[0], avgoccupancy=avgOccupancy[0])

@app.route('/booking/delete/<int:booking_id>', methods=['POST'])
def delete_booking(booking_id):
    connection = getCursor()
    connection.execute("DELETE FROM bookings WHERE booking_id = %s", (booking_id,))
    connection.close()
    return redirect(url_for('campers'))  # Redirect to the camper list page after deletion  