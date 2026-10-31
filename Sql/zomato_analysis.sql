/* =====================================================================
   PROJECT   : Zomato Restaurant Analysis
   FILE      : zomato_analysis.sql
   PURPOSE   : Create the database and table, import the cleaned
               dataset, and validate the import
   DATABASE  : MySQL 8.0+
   SOURCE    : Data/Processed/zomato_cleaned.csv
   AUTHOR    : Khushi Bucha
   ---------------------------------------------------------------------
   CONTENTS
     STEP 1  - Create database
     STEP 2  - Create table
     STEP 3  - Import cleaned CSV
     STEP 4  - Validate the import
   ---------------------------------------------------------------------
   NOTE: Running this whole file again DROPS and re-creates the
         `restaurants` table, then reloads it from the CSV.
   ===================================================================== */


/* =====================================================================
   STEP 1 : CREATE DATABASE
   ===================================================================== */

CREATE DATABASE IF NOT EXISTS zomato_db
    CHARACTER SET utf8mb4
    COLLATE utf8mb4_unicode_ci;

USE zomato_db;


/* =====================================================================
   STEP 2 : CREATE TABLE
   ===================================================================== */

DROP TABLE IF EXISTS restaurants;

CREATE TABLE restaurants (
    id            INT           AUTO_INCREMENT PRIMARY KEY,  -- surrogate key
    address       VARCHAR(500),                              -- full address
    name          VARCHAR(255),                              -- restaurant name
    online_order  VARCHAR(3),                                -- 'Yes' / 'No'
    book_table    VARCHAR(3),                                -- 'Yes' / 'No'
    rate          DECIMAL(2,1),                              -- rating out of 5
    votes         INT,                                       -- number of votes
    phone         VARCHAR(100),                              -- contact number(s)
    location      VARCHAR(100),                              -- neighbourhood
    rest_type     VARCHAR(100),                              -- e.g. Cafe, Casual Dining
    dish_liked    VARCHAR(500),                              -- popular dishes
    cuisines      VARCHAR(255),                              -- cuisines served
    approx_cost   INT,                                       -- cost for two (INR)
    listed_type   VARCHAR(50),                               -- e.g. Buffet, Delivery
    listed_city   VARCHAR(50)                                -- listing area
);


/* =====================================================================
   STEP 3 : IMPORT CLEANED CSV
   ---------------------------------------------------------------------
   One-time setup before running this step in MySQL Workbench:
     a) Run on the server:
          SET GLOBAL local_infile = 1;
     b) Database > Manage Connections > Advanced > "Others" box, add:
          OPT_LOCAL_INFILE=1
        then reconnect.
     c) Update the file path below if the project folder moves.

   Empty values in the CSV are converted to NULL using NULLIF().
   ===================================================================== */

LOAD DATA LOCAL INFILE '/Users/khushibucha/Desktop/Zomato-Restaurant-Analysis/Data/Processed/zomato_cleaned.csv'
INTO TABLE restaurants
CHARACTER SET utf8mb4
FIELDS TERMINATED BY ','
       OPTIONALLY ENCLOSED BY '"'
LINES  TERMINATED BY '\n'
IGNORE 1 LINES                                   -- skip header row
(
    @address, @name, @online_order, @book_table, @rate, @votes, @phone,
    @location, @rest_type, @dish_liked, @cuisines, @approx_cost,
    @listed_type, @listed_city
)
SET
    address      = NULLIF(@address,      ''),
    name         = NULLIF(@name,         ''),
    online_order = NULLIF(@online_order, ''),
    book_table   = NULLIF(@book_table,   ''),
    rate         = NULLIF(@rate,         ''),
    votes        = NULLIF(@votes,        ''),
    phone        = NULLIF(@phone,        ''),
    location     = NULLIF(@location,     ''),
    rest_type    = NULLIF(@rest_type,    ''),
    dish_liked   = NULLIF(@dish_liked,   ''),
    cuisines     = NULLIF(@cuisines,     ''),
    approx_cost  = NULLIF(@approx_cost,  ''),
    listed_type  = NULLIF(@listed_type,  ''),
    listed_city  = NULLIF(TRIM(TRAILING '\r' FROM @listed_city), '');


/* =====================================================================
   STEP 4 : VALIDATE THE IMPORT
   ===================================================================== */

-- 4.1  Total rows loaded                      (expected: 51,632)
SELECT COUNT(*) AS total_rows
FROM restaurants;

-- 4.2  Missing values and value ranges
--      (expected: missing_rate = 10,030 | missing_cost = 344
--                 rate 1.8 - 4.9        | cost 40 - 6000)
SELECT
    SUM(rate IS NULL)        AS missing_rate,
    SUM(approx_cost IS NULL) AS missing_cost,
    MIN(rate)                AS min_rate,
    MAX(rate)                AS max_rate,
    MIN(approx_cost)         AS min_cost,
    MAX(approx_cost)         AS max_cost
FROM restaurants;

-- 4.3  Preview the first 10 records
SELECT *
FROM restaurants
LIMIT 10;

/* ============================ END OF FILE ============================ */
