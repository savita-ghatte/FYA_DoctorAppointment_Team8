-- ===========================================
-- HOSPITAL MANAGEMENT SYSTEM DATABASE
-- Doctor Appointment Booking System
-- ===========================================

DROP DATABASE IF EXISTS AppointmentBookingSystem;
CREATE DATABASE AppointmentBookingSystem;
USE AppointmentBookingSystem;

-- ===========================================
-- DEPARTMENTS TABLE
-- ===========================================

CREATE TABLE Departments (
    Department_ID INT AUTO_INCREMENT PRIMARY KEY,
    Department_Name VARCHAR(100) NOT NULL UNIQUE,
    Description TEXT
);

-- ===========================================
-- PATIENT TABLE
-- ===========================================

CREATE TABLE Patients (
    Patient_ID INT AUTO_INCREMENT PRIMARY KEY,
    Name VARCHAR(100) NOT NULL,
    Age INT,
    Gender ENUM('Male','Female','Other'),
    Email VARCHAR(100) NOT NULL UNIQUE,
    Phone VARCHAR(15),
    Address TEXT,
    Password VARCHAR(255) NOT NULL
);

-- ===========================================
-- DOCTOR TABLE
-- ===========================================

CREATE TABLE Doctors (
    Doctor_ID INT AUTO_INCREMENT PRIMARY KEY,
    Department_ID INT,

    Name VARCHAR(100) NOT NULL,
    Qualification VARCHAR(100),
    Specialization VARCHAR(100),
    Experience INT,

    Hospital VARCHAR(100),

    Fees DECIMAL(10,2),

    Available_Days VARCHAR(100),

    Available_Time VARCHAR(100),

    Email VARCHAR(100) UNIQUE,

    Phone VARCHAR(15),

    Password VARCHAR(255),

    FOREIGN KEY (Department_ID)
    REFERENCES Departments(Department_ID)
);

-- ===========================================
-- APPOINTMENT TABLE
-- ===========================================

CREATE TABLE Appointments (

    Appointment_ID INT AUTO_INCREMENT PRIMARY KEY,

    Patient_ID INT NOT NULL,

    Doctor_ID INT NOT NULL,

    Appointment_Date DATE,

    Appointment_Time TIME,

    Reason TEXT,

    Status ENUM(
        'Pending',
        'Approved',
        'Rejected',
        'Completed',
        'Cancelled'
    ) DEFAULT 'Pending',

    FOREIGN KEY (Patient_ID)
        REFERENCES Patients(Patient_ID),

    FOREIGN KEY (Doctor_ID)
        REFERENCES Doctors(Doctor_ID)
);

-- ===========================================
-- PRESCRIPTION TABLE
-- ===========================================

CREATE TABLE Prescriptions (

    Prescription_ID INT AUTO_INCREMENT PRIMARY KEY,

    Appointment_ID INT NOT NULL,

    Diagnosis TEXT,

    Medicine VARCHAR(255),

    Dosage VARCHAR(100),

    Instructions TEXT,

    FOREIGN KEY (Appointment_ID)
        REFERENCES Appointments(Appointment_ID)
);

-- ===========================================
-- ADMIN TABLE
-- ===========================================

CREATE TABLE Admins (

    Admin_ID INT AUTO_INCREMENT PRIMARY KEY,

    Username VARCHAR(50) UNIQUE NOT NULL,

    Email VARCHAR(100) UNIQUE,

    Password VARCHAR(255) NOT NULL
);

-- ===========================================
-- INSERT DEFAULT DEPARTMENTS
-- ===========================================

INSERT INTO Departments
(Department_Name, Description)
VALUES
('Cardiology','Heart Specialist'),
('Neurology','Brain and Nervous System'),
('Orthopedics','Bones and Joints'),
('Dermatology','Skin Specialist'),
('Pediatrics','Child Specialist'),
('ENT','Ear, Nose and Throat'),
('Gynecology','Women Health');

-- ===========================================
-- INSERT DEFAULT ADMIN
-- ===========================================

INSERT INTO Admins
(Username, Email, Password)
VALUES
('admin','admin@hospital.com','admin123');

-- ===========================================
-- DATABASE CREATED SUCCESSFULLY
-- ===========================================