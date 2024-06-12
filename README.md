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

This function includes *@app.route("/camper", methods=['GET','POST'])*, with templates *datepickercamper.html*, *camperlist.html*.

***"/camper"*** route handles both **GET** and **POST** requests. By using a single route to handle both types of requests, the application can keep its routing structure simple and consistent. When accessed via the **GET** method, it renders the ***datepickercamper.html*** template, allowing users to select a specific date. On submitting the form, a **POST** request is sent to the same route *(/camper)* and it renders the ***camperlist.html*** template, allowing users to see all the campers on a particular date and delete bookings.

Displaying a **camper list** in a **separate template** has several benefits. Keeping the camper list display logic in its own template improves code clarity and readability. Developers can easily find and understand the code responsible for rendering the camper list. Using a separate camper list template makes it easier to make changes or updates to the camper list interface without affecting other parts of the application.

On the ***camperlist.html*** page, I **added the selected date to the title**, making it easy for users to know which day the list displayed is for.

The displayed list uses the **Bootstrap's table-hover** styling, making the displayed list neater and more visually appealing.

Placing a **delete button** next to **each customer list** enables users to quickly and directly delete a specific booking without having to navigate to a separate page. This streamlined approach improves the efficiency of booking management tasks.

### Customer -add

In the customer adding form (***addcustomer.html***), I used **Bootstrap's form validation**. **Except for the email**, the **first name, family name and phone** are all **required** to be entered, and **invalid feedback** is provided. In the email column, I provided valid feedback to remind users that they can not enter an email. The reason for this design is because **some users (especially the elderly) may not have an email address**. 

Although the database allows the first name to be null, I still set the first name to be required so that when the customer does not provide a first name, the admin can enter other information to indicate it.

After completing the input of the customer information, you will be redirected to a page of **a list of all customers**. This design has several advantages. Redirecting to the whole customer list page provides users with immediate visual confirmation. **Seeing the new customer listed among all other customers reassures them that their action was successful**. Users can easily verify the details of the newly added customer without navigating away from the form. This minimizes the number of steps users need to take to see their input reflected in the system. If there was an error in adding the customer, the user will see it on the list page. This can prompt them to correct any mistakes promptly. **There is an "edit" button for each customer on the whole customer list for users to correct the mistakes promptly.** 

Customer information is displayed **from newest to oldest based on customer ID**, which helps users to **immediately locate newly added customers**.



### Styling

The selections of **number of nights** and **number of people** are changed to **Bootstrap CSS "select"** to make the interface look more user-friendly.


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
