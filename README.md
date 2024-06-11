# scg

### Project Report – Part 2: Answer Database Question
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

The first change is to add a table called “users” to store their username, password, and user information (first name, family name, phone, email, and corresponding customer_id). Users can log in to their accounts to make a booking or modify their personal information. The customer_id does not need to be displayed and cannot be modified by the user. It is only used to track the corresponding information of the customers table.
  
Because usernames and passwords are involved, a login and authentication system needs to be implemented to verify users before allowing them to make bookings or modify their personal information. 


The second change is to add two columns to the “bookings” table. The first column is “added_by”. “added_by” references the foreign key customer_id in the customers table, which allows administrators to track which user made the booking. The second column is “status”, which is a string data type, including "pending" and "confirmed". All reservations created by users themselves will enter the pending state and will need to be confirmed by the administrator. There is no need to add "canceled". If a user needs to cancel a booking, he/she needs to contact the administrator directly by phone or email, and then the administrator will cancel it directly in the admin system (this will delete the corresponding row in the bookings table).


