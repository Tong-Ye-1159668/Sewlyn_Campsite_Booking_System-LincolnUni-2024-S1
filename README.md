# scg

### Project Report – Part 2: Answer Database Question
#### 1. What SQL statement creates the customer table and defines its fields/columns?

```sql
CREATE TABLE IF NOT EXISTS `customers` (
  `customer_id` INT NOT NULL AUTO_INCREMENT,
  `firstname` VARCHAR(45) NULL,
  `familyname` VARCHAR(60) NOT NULL,
  `email` VARCHAR(255) NULL,
  `phone` VARCHAR(12) NULL,
  PRIMARY KEY (`customer_id`));
```

#### 2. Which line of SQL code sets up the relationship between the customer and booking tables?

```sql
CONSTRAINT `customer`
  FOREIGN KEY (`customer`)
  REFERENCES `scg`.`customers` (`customer_id`)
  ON DELETE NO ACTION
  ON UPDATE NO ACTION)
```

#### 3. Which lines of SQL code insert details into the sites table?

```sql
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
```

#### 4. Suppose that as part of an audit trail, the time and date a booking was added to the database needed to be recorded. What fields/columns would you need to add to which tables? Provide the table name, new column name and the data type.

I will add a new column to the **bookings** table. The new column should be the data type that can store date and time. I will use the **DATETIME** data type.

**Table name: bookings**

**New column name: added_datetime**

**Data type: DATETIME**

```sql
ALTER TABLE `bookings`
ADD COLUMN `added_datetime` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP;
```

#### 5. Suppose the ability for customers to make their own bookings was added. Describe two different changes that would be needed to the data model to implement this. 

1. The first change is to add a column named "added_by" at the **bookings** table to show who made this booking, customer or admin.

   **Table name: bookings**

   **New column name: added_by**

   **Data type: VARCHAR(255)**

```sql
ALTER TABLE `bookings`
ADD COLUMN `added_by` VARCHAR(255) NOT NULL;
```

