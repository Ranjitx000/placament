-- 1. Create Database
CREATE DATABASE IF NOT EXISTS placement_db;
USE placement_db;

-- 2. Students Table (Updated)
CREATE TABLE studentsss (
    id INT AUTO_INCREMENT PRIMARY KEY,
    college_name VARCHAR(255),
    name VARCHAR(255),
    ssc_percentage FLOAT,
    hsc_percentage FLOAT,
    prev_sem_result FLOAT,
    academic_performance VARCHAR(50),
    extra_curricular_activity VARCHAR(50),
    communication VARCHAR(50),
    branch VARCHAR(50),
    year INT,
    skills TEXT,
    cgpa FLOAT,
    expected_salary FLOAT,
    date DATE,
    projects TEXT,
    internship TEXT,
    certifications TEXT,
    company VARCHAR(255),
    resume VARCHAR(255),
    placed VARCHAR(10),
    placement_probability FLOAT
);

-- 3. Admins Table (No Change)
CREATE TABLE IF NOT EXISTS admins (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    college_name VARCHAR(100),
    role VARCHAR(20) DEFAULT 'superadmin',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 4. Companies Table (No Change)
CREATE TABLE IF NOT EXISTS companies (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    job_role VARCHAR(100),
    required_skills TEXT,
    min_cgpa FLOAT,
    package FLOAT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 5. Courses / Certifications Table (No Change)
CREATE TABLE IF NOT EXISTS courses (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    description TEXT,
    skills_covered TEXT,
    link VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 6. Insert default admin
INSERT INTO admins (username, password)
VALUES ('srushti', '$pbkdf2-sha256$29000$Dk3zQfKsm1QfK0sK9k0LFA$JqG13ZKZFT3kxO9swT4gA1K3YgrxE2pRNeI.6wx7Qp8');

-- 7. Optional: Add sample companies
INSERT INTO companies (name, job_role, required_skills, min_cgpa, package)
VALUES 
('Company A', 'Python Developer', 'Python,SQL,Communication', 7.0, 5.0),
('Company B', 'ML Intern', 'Python,Machine Learning,Statistics', 8.0, 6.5);

-- 8. Optional: Add sample courses
INSERT INTO courses (name, description, skills_covered, link)
VALUES 
('Data Science Bootcamp', 'Intro to Data Science and ML', 'Python,Machine Learning,Pandas', 'https://example.com/ds-bootcamp'),
('SQL Mastery', 'Advanced SQL queries', 'SQL,Database Management', 'https://example.com/sql-course');
