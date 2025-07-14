-- Initialize PetClinic Database
-- This script creates the database and user if they don't exist

CREATE DATABASE IF NOT EXISTS petclinic CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

CREATE USER IF NOT EXISTS 'petclinic_user'@'%' IDENTIFIED BY 'petclinic_password123';
GRANT ALL PRIVILEGES ON petclinic.* TO 'petclinic_user'@'%';
FLUSH PRIVILEGES;

USE petclinic;

-- The tables will be created by Alembic migrations
-- This script just ensures the database and user exist