-- Personal Finance Management System Database Schema
CREATE DATABASE IF NOT EXISTS personal_finance;
USE personal_finance;

CREATE TABLE IF NOT EXISTS settings (
    id INT AUTO_INCREMENT PRIMARY KEY,
    password_hash VARCHAR(255) NOT NULL,
    user_name VARCHAR(100) DEFAULT 'User',
    currency VARCHAR(10) DEFAULT 'NPR',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS income (
    id INT AUTO_INCREMENT PRIMARY KEY,
    date_bs VARCHAR(20) NOT NULL,
    date_ad DATE NOT NULL,
    year_bs INT NOT NULL,
    month_bs VARCHAR(20) NOT NULL,
    month_num INT NOT NULL,
    category VARCHAR(50) NOT NULL,
    amount DECIMAL(15,2) NOT NULL DEFAULT 0,
    remarks TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS expenditure (
    id INT AUTO_INCREMENT PRIMARY KEY,
    date_bs VARCHAR(20) NOT NULL,
    date_ad DATE NOT NULL,
    year_bs INT NOT NULL,
    month_bs VARCHAR(20) NOT NULL,
    month_num INT NOT NULL,
    category VARCHAR(50) NOT NULL,
    particular VARCHAR(200),
    quantity DECIMAL(10,3) DEFAULT 1,
    rate DECIMAL(15,2) DEFAULT 0,
    amount DECIMAL(15,2) NOT NULL DEFAULT 0,
    remarks TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS net_worth (
    id INT AUTO_INCREMENT PRIMARY KEY,
    date_bs VARCHAR(20) NOT NULL,
    date_ad DATE NOT NULL,
    bank_balance DECIMAL(15,2) DEFAULT 0,
    cash DECIMAL(15,2) DEFAULT 0,
    share_value DECIMAL(15,2) DEFAULT 0,
    ssf DECIMAL(15,2) DEFAULT 0,
    loan_given DECIMAL(15,2) DEFAULT 0,
    property_value DECIMAL(15,2) DEFAULT 0,
    savings DECIMAL(15,2) DEFAULT 0,
    earned DECIMAL(15,2) DEFAULT 0,
    payout_amount DECIMAL(15,2) DEFAULT 0,
    net_worth DECIMAL(15,2) DEFAULT 0,
    remarks TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS loans (
    id INT AUTO_INCREMENT PRIMARY KEY,
    borrower_name VARCHAR(200) NOT NULL,
    principal DECIMAL(15,2) NOT NULL DEFAULT 0,
    interest_rate DECIMAL(5,2) DEFAULT 0,
    loan_date_bs VARCHAR(20),
    loan_date_ad DATE,
    duration_months INT DEFAULT 0,
    interest_amount DECIMAL(15,2) DEFAULT 0,
    total_payable DECIMAL(15,2) DEFAULT 0,
    status VARCHAR(20) DEFAULT 'active',
    remarks TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS shares (
    id INT AUTO_INCREMENT PRIMARY KEY,
    stock_symbol VARCHAR(20) NOT NULL,
    stock_name VARCHAR(200),
    quantity INT NOT NULL DEFAULT 0,
    purchase_price DECIMAL(10,2) NOT NULL DEFAULT 0,
    current_price DECIMAL(10,2) DEFAULT 0,
    investment DECIMAL(15,2) DEFAULT 0,
    current_value DECIMAL(15,2) DEFAULT 0,
    profit_loss DECIMAL(15,2) DEFAULT 0,
    purchase_date_bs VARCHAR(20),
    purchase_date_ad DATE,
    remarks TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS bikes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    bike_name VARCHAR(100) NOT NULL,
    bike_number VARCHAR(20),
    purchase_price DECIMAL(15,2) DEFAULT 0,
    purchase_date DATE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS bike_expenditure (
    id INT AUTO_INCREMENT PRIMARY KEY,
    bike_id INT,
    bike_name VARCHAR(100),
    bike_number VARCHAR(20),
    date_bs VARCHAR(20),
    date_ad DATE,
    year_bs INT,
    month_bs VARCHAR(20),
    month_num INT,
    particular VARCHAR(200),
    quantity DECIMAL(10,3) DEFAULT 1,
    rate DECIMAL(15,2) DEFAULT 0,
    amount DECIMAL(15,2) NOT NULL DEFAULT 0,
    remarks TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS petrol (
    id INT AUTO_INCREMENT PRIMARY KEY,
    bike_id INT,
    bike_name VARCHAR(100),
    bike_number VARCHAR(20),
    date_bs VARCHAR(20),
    date_ad DATE,
    year_bs INT,
    month_bs VARCHAR(20),
    month_num INT,
    amount_paid DECIMAL(10,2) NOT NULL DEFAULT 0,
    price_per_liter DECIMAL(8,2) NOT NULL DEFAULT 0,
    liters DECIMAL(8,3) DEFAULT 0,
    remaining_fuel DECIMAL(8,3) DEFAULT 0,
    current_km INT DEFAULT 0,
    previous_km INT DEFAULT 0,
    distance INT DEFAULT 0,
    mileage DECIMAL(8,2) DEFAULT 0,
    remarks TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS baby_expenditure (
    id INT AUTO_INCREMENT PRIMARY KEY,
    date_bs VARCHAR(20),
    date_ad DATE,
    year_bs INT,
    month_bs VARCHAR(20),
    month_num INT,
    category VARCHAR(50) NOT NULL,
    particular VARCHAR(200),
    amount DECIMAL(15,2) NOT NULL DEFAULT 0,
    remarks TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS baby_gifts (
    id INT AUTO_INCREMENT PRIMARY KEY,
    person_name VARCHAR(200) NOT NULL,
    amount DECIMAL(15,2) NOT NULL DEFAULT 0,
    date_bs VARCHAR(20),
    date_ad DATE,
    remarks TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO settings (password_hash, user_name) 
VALUES (SHA2('admin123', 256), 'Admin')
ON DUPLICATE KEY UPDATE id=id;
