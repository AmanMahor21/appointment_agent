DROP TABLE IF EXISTS Appointments;
DROP TABLE IF EXISTS Patients;

CREATE TABLE Patients (
    id INTEGER PRIMARY KEY,
    name TEXT,
    dob TEXT,
    gender TEXT,
    contact TEXT
);

CREATE TABLE Appointments (
    id INTEGER PRIMARY KEY,
    patient_id INTEGER,
    appointment_date TEXT,
    appointment_time TEXT,
    FOREIGN KEY(patient_id) REFERENCES Patients(id)
);

-- Seed data
INSERT INTO Patients (name, dob, gender, contact) VALUES
    ('John Doe', '1985-02-14', 'Male', '555-1234'),
    ('Mary Smith', '1990-07-22', 'Female', '555-5678');

INSERT INTO Appointments (patient_id, appointment_date, appointment_time) VALUES
    (1, '2025-07-15', '10:00'),
    (2, '2025-07-16', '11:00'),
    (2, '2025-07-20', '11:30');
