-- ====================================================
-- REVIEW 2 & 3 TEST SCRIPT
-- ====================================================

USE Alumni_Student_ResourceDB;

-- ====================================================
-- INSERT BASE DATA
-- ====================================================

-- Admins
INSERT INTO Admin (Name, Email, Password) VALUES
('Priya Sharma', 'priya@pes.edu', 'admin123'),
('Arjun Patel', 'arjun@pes.edu', 'admin456');

-- Students
INSERT INTO Student (Name, Gender, DOB, Year_Of_Study, Previous_Courses, Contact_No) VALUES
('Ravi Kumar', 'Male', '2002-03-15', 3, 'Python, DBMS', '9876543210'),
('Aditi Mehta', 'Female', '2003-07-10', 2, 'C, Java', '9876501234'),
('Karan Singh', 'Male', '2001-11-21', 4, 'ML, Data Science', '9876598765');

-- Alumni
INSERT INTO Alumni (Name, Expertise_Areas, Contact_Details, Graduation_Year, Admin_ID) VALUES
('Sneha Iyer', 'AI, ML, Cloud', 'sneha@gmail.com', 2020, 1),
('Rahul Verma', 'Cybersecurity, Networks', 'rahul@gmail.com', 2019, 2);

-- Resources
INSERT INTO Resource (Type, Condition_Status, Availability_Status, Resource_Details, Tag, Admin_ID) VALUES
('Book', 'Good', 'Available', 'DBMS Concepts – Korth', 'DBMS', 1),
('Laptop', 'Fair', 'Available', 'Dell Inspiron 15', 'Hardware', 2),
('Project Report', 'New', 'Available', 'Final Year AI Project', 'AI', 1);

-- ====================================================
-- REVIEW 2 — CRUD OPERATIONS
-- ====================================================

-- CREATE (Insert)
INSERT INTO Borrow_Request (Student_ID, Resource_ID) VALUES (1, 1);

-- READ (Select)
SELECT * FROM Student;
SELECT * FROM Resource;
SELECT * FROM Borrow_Request;

-- UPDATE
UPDATE Student
SET Year_Of_Study = 4
WHERE Student_ID = 1;

-- DELETE
DELETE FROM Resource
WHERE Resource_ID = 3;

-- Verify updates
SELECT * FROM Student;
SELECT * FROM Resource;

-- ====================================================
-- REVIEW 3 — TRIGGERS, FUNCTIONS & PROCEDURES
-- ====================================================

-- 1️⃣ Approve a Borrow Request (tests triggers + procedure)
CALL sp_approve_borrow_request(1, 1);

SELECT * FROM Loan;            -- Loan created (Due_Date auto-set)
SELECT * FROM Resource;        -- Availability = 'Borrowed'
SELECT * FROM Borrow_Request;  -- Status = 'Approved'

-- 2️⃣ Return the resource (tests AFTER UPDATE trigger)
UPDATE Loan
SET Return_Date = '2025-10-25'
WHERE Loan_ID = 1;

SELECT * FROM Loan;
SELECT * FROM Resource;        -- Availability = 'Available' again

-- 3️⃣ Test fine calculation function
SELECT fn_calculate_fine('2025-10-10', '2025-10-25') AS Fine_Amount;
-- Expected = 150.00 (15 days × ₹10)

-- 4️⃣ Reject another borrow request
INSERT INTO Borrow_Request (Student_ID, Resource_ID) VALUES (2, 2);
CALL sp_reject_borrow_request(2);
SELECT * FROM Borrow_Request;

-- 5️⃣ Schedule a mentorship session
CALL sp_schedule_mentorship(1, 1, '2025-10-20', '10:30:00', 'Online', 60);
SELECT * FROM Mentorship_Session;

-- 6️⃣ View all sessions for a student
CALL sp_view_student_sessions(1);

-- ====================================================
-- END OF SCRIPT
-- ====================================================

SELECT * FROM Student;

INSERT INTO Loan (Student_ID, Resource_ID, Admin_ID)
VALUES (1, 1, 1);

SELECT * FROM Loan;

SELECT fn_calculate_fine('2025-10-01', '2025-10-05') AS Fine1;

CALL sp_schedule_mentorship(
    1, 1, '2025-10-20', '15:00:00', 'Online', 60
);
SELECT * FROM Mentorship_Session;

CALL sp_view_student_sessions(1);
