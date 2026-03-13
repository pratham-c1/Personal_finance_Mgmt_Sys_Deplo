-- ─────────────────────────────────────────────────────────────────────────────
-- Multi-user migration script
-- Run this on your Railway MySQL database (after schema.sql is already applied)
-- ─────────────────────────────────────────────────────────────────────────────
USE railway;

-- ── 1. Rename settings to users and add role column ──────────────────────────
ALTER TABLE settings
    ADD COLUMN username VARCHAR(50) UNIQUE,
    ADD COLUMN role VARCHAR(10) DEFAULT 'user';

-- Set existing admin row's username
UPDATE settings SET username = 'admin', role = 'admin' WHERE id = 1;

-- Make username required after setting existing values
ALTER TABLE settings MODIFY COLUMN username VARCHAR(50) NOT NULL;

-- ── 2. Add user_id to every data table ───────────────────────────────────────
ALTER TABLE income
    ADD COLUMN user_id INT NOT NULL DEFAULT 1,
    ADD INDEX idx_income_user (user_id);

ALTER TABLE expenditure
    ADD COLUMN user_id INT NOT NULL DEFAULT 1,
    ADD INDEX idx_expenditure_user (user_id);

ALTER TABLE net_worth
    ADD COLUMN user_id INT NOT NULL DEFAULT 1,
    ADD INDEX idx_networth_user (user_id);

ALTER TABLE loans
    ADD COLUMN user_id INT NOT NULL DEFAULT 1,
    ADD INDEX idx_loans_user (user_id);

ALTER TABLE shares
    ADD COLUMN user_id INT NOT NULL DEFAULT 1,
    ADD INDEX idx_shares_user (user_id);

ALTER TABLE bikes
    ADD COLUMN user_id INT NOT NULL DEFAULT 1,
    ADD INDEX idx_bikes_user (user_id);

ALTER TABLE bike_expenditure
    ADD COLUMN user_id INT NOT NULL DEFAULT 1,
    ADD INDEX idx_bike_exp_user (user_id);

ALTER TABLE petrol
    ADD COLUMN user_id INT NOT NULL DEFAULT 1,
    ADD INDEX idx_petrol_user (user_id);

ALTER TABLE baby_expenditure
    ADD COLUMN user_id INT NOT NULL DEFAULT 1,
    ADD INDEX idx_baby_exp_user (user_id);

ALTER TABLE baby_gifts
    ADD COLUMN user_id INT NOT NULL DEFAULT 1,
    ADD INDEX idx_baby_gifts_user (user_id);

-- ── Add remaining_fuel column to petrol table ─────────────────────────────────
-- Run this if you already ran the first migration (or include in fresh schema)
ALTER TABLE petrol
    ADD COLUMN remaining_fuel DECIMAL(8,3) DEFAULT 0
    AFTER liters;
