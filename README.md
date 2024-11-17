# Selwyn Campground Management System
#### Submitted on 12 June 2024

This repository contains my **first web application**, developed during Semester 1 of my Master of Applied Computing studies at Lincoln University. The project was part of the COMP 636: Web App Assessment and demonstrates foundational full-stack web development skills.

## Features
- **Customer Management**: Add, edit, and search customer details with form validation.
- **Booking Management**: Record and manage campsite bookings efficiently.
- **Campers List**: Display a well-formatted list of campers for a selected night using Bootstrap.
- **Reports**: Generate summaries, including customer booking history and average occupancy.

## Technical Details
- **Technologies Used**: Python (Flask), MySQL, Bootstrap.
- **Hosting**: Deployed on PythonAnywhere.
- **Database Integration**: Secure and structured interaction with a MySQL database using parameterized queries.

## Purpose
This project marked the beginning of my journey into web development, showcasing:
- Backend development using Flask and MySQL.
- Designing user-friendly, responsive interfaces with Bootstrap.
- Implementing data-driven functionalities with a focus on usability and scalability.

It reflects my ability to design, build, and deploy a web application from the ground up while integrating best practices in software development.

---

# The Following Part is for the Examiners Evaluation at Lincoln University

# Project Report - Tong Ye 1159668

## Project Report – Part 1:Design Decisions

### Home page

I used Bootstrap containers for the home page,  *div class="container"*. This is to introduce a responsive, fixed-width layout that provides consistent margins on both sides of the page. This ensures that the content is not overly stretched across large screens, which will make it difficult to read and visually unsightly. With these margins, the layout looks more structured, making the interface easier to navigate.

I used Bootstrap navigation components, *ul class="nav nav-tabs"*. This makes a structured, visually appealing, and user-friendly tabbed navigation interface. Background and foreground colours have a sufficient contrast ratio, which makes it easy for most of the users to read.

### Add Booking

This function includes *@app.route("/booking", methods=['GET','POST'])* and *@app.route("/booking/add", methods=['POST'])*, and *datepicker.html*, *bookingform.html* and *booking_confirmation.html*.

Route ***"/booking"*** for rendering the booking form and displaying available options, and route ***"/booking/add"*** for submitting a new booking to the server. Using two routes with different methods allows for a clear separation of concerns and ensures proper handling of different types of requests within the booking functionality.

***"/booking"*** route handles both **GET** and **POST** requests. When accessed via the **GET** method, it renders the ***datepicker.html*** template, allowing users to input booking details. On submitting the form, a **POST** request is sent to the same route *(/booking)* with the first part of the booking details, and it renders the ***bookingform.html*** template, allowing users to input the second part of the booking details.

***/booking/add*** route specifically handles **POST** requests. This route is responsible for processing the form data submitted from the ***bookingform.html*** and adding the booking to the database, then it renders the ***booking_confirmation.html*** template.

Added validation to the **Choose start night of booking form** to the date input to be required, and added **invalid-feedback**. Ensures that a date must be selected before proceeding to the next step. Ensures that there is no Internal Server Error due to proceeding to the next step without selecting a date.

In the **Start Date to be booked** input box, I added **"required"** for validation to make sure there is no Internal Server Error due to clearing the entered date when submitting the booking form.

In **Customer to book for**, I changed the option value from the default first customer name to **"Please select a customer..."** and set it to **selected disabled value**, and added  **"required"** for validation. This ensures that the admin would not select the default first customer by mistake, or miss a customer name when submitting the booking form.

Besides, in the drop-down customer list, I **sorted the customers by first name and family name**, so that it is easier for the admin to find a specific customer.

In **Site to select**, I added **"required"** for validation. This ensures that a site must be selected before submitting the booking form, otherwise, a null value will be inserted into the bookings table.

I also added a **conditional statement** in *bookingform.html*. If there is no site to choose, it will display **No campsite is available**, instead of an empty site list with only the title "Site to select" (which can easily lead the admin to misunderstand that there is a bug in the system). **Bootstrap's "alert-warning" styling** is used here to ensure that the statement is displayed eye-catching.

After submitting the booking form, **a booking confirmation page** will be displayed through *booking_confirmation.html*. This page shows the name, site, check-in date, check-out date, number of days, and number of people. The page uses **Bootstrap's "table-success table-striped" styling** to make the displayed information neat and concise.

### List campers

This function includes *@app.route("/camper", methods=['GET','POST'])*, methods=['POST']), with templates *datepickercamper.html*, *camperlist.html*.

***"/camper"*** route handles both **GET** and **POST** requests. By using a single route to handle both types of requests, the application can keep its routing structure simple and consistent. When accessed via the **GET** method, it renders the ***datepickercamper.html*** template, allowing users to select a specific date. On submitting the form, a **POST** request is sent to the same route *(/camper)* and it renders the ***camperlist.html*** template, allowing users to see all the campers on a particular date and delete bookings.

Displaying a **camper list** in a **separate template** has several benefits. Keeping the camper list display logic in its own template improves code clarity and readability. Developers can easily find and understand the code responsible for rendering the camper list. Using a separate camper list template makes it easier to make changes or updates to the camper list interface without affecting other parts of the application.

On the ***camperlist.html*** page, I **added the selected date to the title**, making it easy for users to know which day the list displayed is for.

The displayed list uses the **Bootstrap's table-hover** styling, making the displayed list neater and more visually appealing.

Placing a **delete button** next to **each customer list** enables users to quickly and directly delete a specific booking without having to navigate to a separate page. This streamlined approach improves the efficiency of booking management tasks. This will redirect to route "/booking/delete/int:booking_id" with method "POST".

### Customer -add

This function includes *@app.route("/addcustomer", methods=['GET','POST'])* and *@app.route("/allcamperlist", methods=['GET'])*, with templates *addcustomer.html*, *allcamperlist.html*.

In the customer adding form (***addcustomer.html***), I used **Bootstrap's form validation**. **Except for the email**, the **first name, family name and phone** are all **required** to be entered, and **invalid feedback** is provided. In the email column, I provided valid feedback to remind users that they can not enter an email. The reason for this design is because **some users (especially the elderly) may not have an email address**. 

Although the database allows the first name to be null, I still set the first name to be required so that when the customer does not provide a first name, the admin can enter other information to indicate it.

After completing the input of the customer information, you will be redirected to a page of **a list of all customers**. This design has several advantages. Redirecting to the whole customer list page provides users with immediate visual confirmation. **Seeing the new customer listed among all other customers reassures them that their action was successful**. Users can easily verify the details of the newly added customer without navigating away from the form. This minimizes the number of steps users need to take to see their input reflected in the system. If there was an error in adding the customer, the user will see it on the list page. This can prompt them to correct any mistakes promptly. **There is an "edit" button for each customer on the whole customer list for users to correct the mistakes promptly.** 

Customer information is displayed **from newest to oldest based on customer ID**, which helps users to **immediately locate newly added customers**.

### Customer -search

This function includes *@app.route("/search", methods=['GET','POST'])*, with templates *search.html*, *search_results.html*.

The title **"Selwyn Campground - Search a Customer to Edit or Show a Report"** at route ***"/search"*** indicates that what the user can do after searching a customer.

The search bar uses **Bootstrap's form validation**. I set it to **required** and provided **invalid-feedback** to ensure that users must enter information to search.

The search results page will redirect to a template ***"search_results.html"***. In this page, I show **what the user just entered in the title**, so that users can more intuitively see what information they entered for the search on the search results page.

For each customer list that matches the search results, I provide an **"edit"** button and a **"Show Smmary Report"** button to facilitate users to **operate on a specific customer individually**.


### Customer -edit

This function includes *@app.route('/edit_customer/customer_id', methods=["GET", "POST"])*, with templates *edit_customer.html*.

In the editing user page, **each input box will display the existing customer information**. The reason for this design is that users do not need to remember or look up a customer’s current details. Pre-filling existing information saves time and effort, as the users only have to change the fields that need to be updated. This design reduces the cognitive load on users by minimizing the amount of information they need to recall or re-enter.

**The customer editing function not placed separately in the navigation bar**, but implemented through the **edit** button after searching for customers or the whole customers list after adding customer information. 

Here are the reasons for this design:

The navigation bar is typically reserved for primary navigation and should not be cluttered with actions that are context-specific, like editing a customer. This helps keep the navigation bar clean and focused on the main sections of the application.

When users see the **edit button next to a customer's information**, it is **immediately clear which customer they are editing**. This reduces confusion and ensures that users are making changes to the correct record.

Keeping related actions (viewing, editing) together minimizes the cognitive load on the user. They don't have to remember where to find the edit function; it’s right where they expect it to be, next to the customer information.

When editing is integrated directly with the customer list, the risk of errors is reduced. Users are less likely to mistakenly edit the wrong customer because they see the customer's details right next to the edit button.

### Summary Report

This function includes *@app.route('/customer_report/int:customer_id', methods=['GET'])*, with templates *customer_report.html*.

Similarly, **the customer report function is not placed separately in the navigation bar**, but implemented through the **Show Summary Report** button after searching for customers. The reason for this design is the same as the one of the customer edit.

The customer summary report page will redirect to a template ***"customer_report.html"***. On this page, I show **the customer's full name** at the title so that users can more intuitively see which customer the summary report is for.

### Navigation and Styling

Most of the tables on the website use **Bootstrap's table-hover** styling. Table hover styles provide users with visual feedback as they interact with a list by highlighting rows when they hover over them. This interactive behaviour improves the overall user experience by making the interface more responsive and engaging. Users can quickly identify and focus on individual rows in a list, which is particularly helpful when browsing large data sets or looking for specific information.

Most buttons (for example, submit, edit, save changes) use the **btn-primary button** styling. **Delete** button uses the **btn-danger** style, and **Show Summary Report** uses the **btn-info style**. This design helps users distinguish. 

Navigation links are added at the bottom of most pages to help users return to the previous page to re-operations.




## Project Report – Part 2: Answer Database Question
#### 1. What SQL statement creates the customer table and defines its fields/columns?

CREATE TABLE IF NOT EXISTS `customers` (

  `customer_id` INT NOT NULL AUTO_INCREMENT,
  
  `firstname` VARCHAR(45) NULL,
  
  `familyname` VARCHAR(60) NOT NULL,
  
  `email` VARCHAR(255) NULL,
  
  `phone` VARCHAR(12) NULL,
  
  PRIMARY KEY (`customer_id`));


#### 2. Which line of SQL code sets up the relationship between the customer and booking tables?

CONSTRAINT `customer`

  FOREIGN KEY (`customer`)
  
  REFERENCES `scg`.`customers` (`customer_id`)
  
  ON DELETE NO ACTION
  
  ON UPDATE NO ACTION)

  
#### 3. Which lines of SQL code insert details into the sites table?

INSERT INTO `sites` (`site_id`, `occupancy`) VALUES ('P1', '5');

INSERT INTO `sites` (`site_id`, `occupancy`) VALUES ('P4', '2');

INSERT INTO `sites` (`site_id`, `occupancy`) VALUES ('P2', '3');

INSERT INTO `sites` (`site_id`, `occupancy`) VALUES ('P5', '8');

INSERT INTO `sites` (`site_id`, `occupancy`) VALUES ('P3', '2');

INSERT INTO `sites` (`site_id`, `occupancy`) VALUES ('U1', '6');

INSERT INTO `sites` (`site_id`, `occupancy`) VALUES ('U2', '2');

INSERT INTO `sites` (`site_id`, `occupancy`) VALUES ('U3', '4');

INSERT INTO `sites` (`site_id`, `occupancy`) VALUES ('U4', '4');

INSERT INTO `sites` (`site_id`, `occupancy`) VALUES ('U5', '2');


#### 4. Suppose that as part of an audit trail, the time and date a booking was added to the database needed to be recorded. What fields/columns would you need to add to which tables? Provide the table name, new column name and the data type.

I will add a new column to the **bookings** table. The new column should store both the date and time information in a single column. I will use the **DATETIME** data type. I will use DEFAULT CURRENT_TIMESTAMP to automatically add the current date and time when a new booking record is inserted. 

**Table name: bookings**

**New column name: added_datetime**

**Data type: DATETIME**


ALTER TABLE `bookings`

ADD COLUMN `added_datetime` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP;


#### 5. Suppose the ability for customers to make their own bookings was added. Describe two different changes that would be needed to the data model to implement this. 

The first change is to add a new table called **"users"** to store their username, password, and user information (first name, family name, phone, email, and corresponding customer_id). Users can log in to their accounts to make a booking or modify their personal information. The customer_id does not need to be displayed and cannot be modified by the user. It is only used to track the corresponding information of the customers table.
  
Because usernames and passwords are involved, a login and authentication system needs to be implemented to verify users before allowing them to make bookings or modify their personal information. 


The second change is to add two new columns to the **“bookings”** table. The first column is **“added_by”**. **“added_by”** references the foreign key customer_id in the customers table, which allows administrators to track which user made the booking. The second column is **“status”**, which is a string data type, including "pending" and "confirmed". All reservations created by users themselves will enter the pending state and will need to be confirmed by the administrator. There is no need to add "canceled". If a user needs to cancel a booking, he/she needs to contact the administrator directly by phone or email, and then the administrator will cancel it directly in the admin system (this will delete the corresponding row in the bookings table).
