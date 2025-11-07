-- ====================================================
-- DATABASE CREATION
-- ====================================================
CREATE DATABASE Alumni_Student_ResourceDB;
USE Alumni_Student_ResourceDB;

-- ====================================================
-- 1. STUDENT TABLE
-- ====================================================
CREATE TABLE Student (
    Student_ID      INT AUTO_INCREMENT PRIMARY KEY,
    Name            VARCHAR(100) NOT NULL,
    Gender          ENUM('Male', 'Female', 'Other') NOT NULL,
    DOB             DATE NOT NULL,
    Year_Of_Study   INT CHECK (Year_Of_Study BETWEEN 1 AND 6),
    Previous_Courses TEXT,
    Contact_No      VARCHAR(15) UNIQUE
);

-- ====================================================
-- 2. ADMIN TABLE
-- ====================================================
CREATE TABLE Admin (
    Admin_ID    INT AUTO_INCREMENT PRIMARY KEY,
    Name        VARCHAR(100) NOT NULL,
    Email       VARCHAR(100) UNIQUE NOT NULL,
    Password    VARCHAR(100) NOT NULL
);

-- ====================================================
-- 3. ALUMNI TABLE
-- ====================================================
CREATE TABLE Alumni (
    Alumni_ID       INT AUTO_INCREMENT PRIMARY KEY,
    Name            VARCHAR(100) NOT NULL,
    Expertise_Areas TEXT,
    Contact_Details VARCHAR(100),
    Graduation_Year YEAR,
    Admin_ID        INT,
    FOREIGN KEY (Admin_ID) REFERENCES Admin(Admin_ID)
        ON UPDATE CASCADE ON DELETE SET NULL
);

-- ====================================================
-- 4. RESOURCE TABLE
-- ====================================================
CREATE TABLE Resource (
    Resource_ID        INT AUTO_INCREMENT PRIMARY KEY,
    Type               VARCHAR(50) NOT NULL,
    Condition_Status   ENUM('New','Good','Fair','Poor') DEFAULT 'Good',
    Availability_Status ENUM('Available','Borrowed','Reserved') DEFAULT 'Available',
    Resource_Details   TEXT,
    Tag                VARCHAR(50),
    Admin_ID           INT,
    FOREIGN KEY (Admin_ID) REFERENCES Admin(Admin_ID)
        ON UPDATE CASCADE ON DELETE SET NULL
);

-- ====================================================
-- 5. BORROW_REQUEST TABLE
-- ====================================================
CREATE TABLE Borrow_Request (
    Request_ID     INT AUTO_INCREMENT PRIMARY KEY,
    Request_Date   DATE NOT NULL DEFAULT (CURRENT_DATE),
    Status         ENUM('Pending','Approved','Rejected') DEFAULT 'Pending',
    Student_ID     INT NOT NULL,
    Resource_ID    INT NOT NULL,
    FOREIGN KEY (Student_ID) REFERENCES Student(Student_ID)
        ON UPDATE CASCADE ON DELETE CASCADE,
    FOREIGN KEY (Resource_ID) REFERENCES Resource(Resource_ID)
        ON UPDATE CASCADE ON DELETE CASCADE
);

-- ====================================================
-- 6. LOAN TABLE
-- ====================================================
CREATE TABLE Loan (
    Loan_ID       INT AUTO_INCREMENT PRIMARY KEY,
    Student_ID    INT NOT NULL,
    Resource_ID   INT,
    Issue_Date    DATE NOT NULL DEFAULT (CURRENT_DATE),
    Due_Date      DATE,
    Return_Date   DATE,
    Admin_ID      INT,
    FOREIGN KEY (Student_ID) REFERENCES Student(Student_ID)
        ON UPDATE CASCADE ON DELETE CASCADE,
    FOREIGN KEY (Resource_ID) REFERENCES Resource(Resource_ID)
        ON UPDATE CASCADE ON DELETE SET NULL,
    FOREIGN KEY (Admin_ID) REFERENCES Admin(Admin_ID)
        ON UPDATE CASCADE ON DELETE SET NULL,
    CHECK (Due_Date >= Issue_Date)
);

-- ====================================================
-- 7. MENTORSHIP_SESSION TABLE
-- ====================================================
CREATE TABLE Mentorship_Session (
    Session_ID   INT AUTO_INCREMENT PRIMARY KEY,
    Student_ID   INT NOT NULL,
    Alumni_ID    INT NOT NULL,
    Date         DATE NOT NULL,
    Time         TIME,
    Mode         ENUM('Online','Offline','Hybrid'),
    Duration     INT, -- in minutes
    FOREIGN KEY (Student_ID) REFERENCES Student(Student_ID)
        ON UPDATE CASCADE ON DELETE CASCADE,
    FOREIGN KEY (Alumni_ID) REFERENCES Alumni(Alumni_ID)
        ON UPDATE CASCADE ON DELETE CASCADE
);

DELIMITER $$
CREATE TRIGGER trg_set_due_date
BEFORE INSERT ON Loan
FOR EACH ROW
BEGIN
    IF NEW.Due_Date IS NULL THEN
        SET NEW.Due_Date = DATE_ADD(NEW.Issue_Date, INTERVAL 15 DAY);
    END IF;
END$$

DELIMITER ;

DELIMITER $$
CREATE TRIGGER trg_update_resource_on_loan
AFTER INSERT ON Loan
FOR EACH ROW
BEGIN
    UPDATE Resource
    SET Availability_Status = 'Borrowed'
    WHERE Resource_ID = NEW.Resource_ID;
END$$

DELIMITER ;

DELIMITER $$
CREATE TRIGGER trg_update_resource_on_return
AFTER UPDATE ON Loan
FOR EACH ROW
BEGIN
    IF NEW.Return_Date IS NOT NULL THEN
        UPDATE Resource
        SET Availability_Status = 'Available'
        WHERE Resource_ID = NEW.Resource_ID;
    END IF;
END$$

DELIMITER ;


DELIMITER $$

CREATE FUNCTION fn_calculate_fine(
    due_date DATE,
    return_date DATE
)
RETURNS DECIMAL(10,2)
DETERMINISTIC
BEGIN
    DECLARE days_late INT DEFAULT 0;
    DECLARE fine DECIMAL(10,2) DEFAULT 0.00;

    -- if no return date, no fine
    IF return_date IS NULL THEN
        RETURN 0.00;
    END IF;

    SET days_late = DATEDIFF(return_date, due_date);

    IF days_late > 0 THEN
        SET fine = days_late * 10; -- ₹10 per day
    ELSE
        SET fine = 0.00;
    END IF;

    RETURN fine;
END$$

DELIMITER ;

DELIMITER $$

CREATE PROCEDURE sp_approve_borrow_request(
    IN p_request_id INT,
    IN p_admin_id INT
)
BEGIN
    DECLARE v_student_id INT;
    DECLARE v_resource_id INT;

    -- Get student and resource linked to request
    SELECT Student_ID, Resource_ID
    INTO v_student_id, v_resource_id
    FROM Borrow_Request
    WHERE Request_ID = p_request_id;

    -- Insert into Loan table
    INSERT INTO Loan (Student_ID, Resource_ID, Admin_ID)
    VALUES (v_student_id, v_resource_id, p_admin_id);

    -- Update request status
    UPDATE Borrow_Request
    SET Status = 'Approved'
    WHERE Request_ID = p_request_id;

    -- Mark resource as borrowed
    UPDATE Resource
    SET Availability_Status = 'Borrowed'
    WHERE Resource_ID = v_resource_id;
END$$

DELIMITER ;

DELIMITER $$
CREATE PROCEDURE sp_reject_borrow_request(
    IN p_request_id INT
)
BEGIN
    UPDATE Borrow_Request
    SET Status = 'Rejected'
    WHERE Request_ID = p_request_id;
END$$

DELIMITER ;

DELIMITER $$
CREATE PROCEDURE sp_schedule_mentorship(
    IN p_student_id INT,
    IN p_alumni_id INT,
    IN p_date DATE,
    IN p_time TIME,
    IN p_mode ENUM('Online','Offline','Hybrid'),
    IN p_duration INT
)
BEGIN
    INSERT INTO Mentorship_Session
        (Student_ID, Alumni_ID, Date, Time, Mode, Duration)
    VALUES
        (p_student_id, p_alumni_id, p_date, p_time, p_mode, p_duration);
END$$

DELIMITER ;

DELIMITER $$
CREATE PROCEDURE sp_view_student_sessions(
    IN p_student_id INT
)
BEGIN
    SELECT 
        s.Session_ID,
        s.Date,
        s.Time,
        s.Mode,
        s.Duration,
        a.Name AS Alumni_Name,
        a.Expertise_Areas
    FROM Mentorship_Session s
    JOIN Alumni a ON s.Alumni_ID = a.Alumni_ID
    WHERE s.Student_ID = p_student_id
    ORDER BY s.Date DESC;
END$$

DELIMITER ;

USE Alumni_Student_ResourceDB;
SHOW TABLES;
SELECT * from Student;

DESCRIBE Student;

USE Alumni_Student_ResourceDB;

-- triggers
SHOW TRIGGERS;

-- procedures and functions
SHOW PROCEDURE STATUS WHERE Db = 'Alumni_Student_ResourceDB';
SHOW FUNCTION STATUS WHERE Db = 'Alumni_Student_ResourceDB';

-- view definition if needed
SHOW CREATE TRIGGER trg_set_due_date;
SHOW CREATE PROCEDURE sp_approve_borrow_request;
SHOW CREATE FUNCTION fn_calculate_fine;



