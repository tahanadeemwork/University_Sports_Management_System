USE UniversitySportsDB;
GO

-- LAYER 2: Depends on Layer 1
-- Safe to run multiple times

DROP TABLE IF EXISTS Equipment;
DROP TABLE IF EXISTS Team;
DROP TABLE IF EXISTS Coach;
DROP TABLE IF EXISTS Student;
GO

-- Table 5: Student
CREATE TABLE Student (
    StudentID      INT IDENTITY(1,1) PRIMARY KEY,
    RegistrationNo NVARCHAR(20)  NOT NULL UNIQUE,
    FullName       NVARCHAR(100) NOT NULL,
    Gender         NVARCHAR(10)  CHECK (Gender IN ('Male', 'Female', 'Other')),
    DateOfBirth    DATE,
    ContactNo      NVARCHAR(20),
    Email          NVARCHAR(100) UNIQUE,
    Address        NVARCHAR(255),
    EnrollmentYear INT,
    DepartmentID   INT NOT NULL,
    SemesterID     INT NOT NULL,
    CONSTRAINT FK_Student_Department FOREIGN KEY (DepartmentID)
        REFERENCES Department(DepartmentID),
    CONSTRAINT FK_Student_Semester FOREIGN KEY (SemesterID)
        REFERENCES Semester(SemesterID)
);

-- Table 6: Coach
CREATE TABLE Coach (
    CoachID         INT IDENTITY(1,1) PRIMARY KEY,
    FullName        NVARCHAR(100) NOT NULL,
    Gender          NVARCHAR(10)  CHECK (Gender IN ('Male', 'Female', 'Other')),
    ContactNo       NVARCHAR(20),
    Email           NVARCHAR(100) UNIQUE,
    Qualification   NVARCHAR(100),
    ExperienceYears INT,
    DepartmentID    INT NOT NULL,
    SportID         INT NOT NULL,
    CONSTRAINT FK_Coach_Department FOREIGN KEY (DepartmentID)
        REFERENCES Department(DepartmentID),
    CONSTRAINT FK_Coach_Sport FOREIGN KEY (SportID)
        REFERENCES Sport(SportID)
);

-- Table 7: Team
CREATE TABLE Team (
    TeamID        INT IDENTITY(1,1) PRIMARY KEY,
    TeamName      NVARCHAR(100) NOT NULL,
    Gender        NVARCHAR(10)  CHECK (Gender IN ('Male', 'Female', 'Mixed')),
    FormationYear INT,
    DepartmentID  INT NOT NULL,
    SportID       INT NOT NULL,
    CoachID       INT,
    CONSTRAINT FK_Team_Department FOREIGN KEY (DepartmentID)
        REFERENCES Department(DepartmentID),
    CONSTRAINT FK_Team_Sport FOREIGN KEY (SportID)
        REFERENCES Sport(SportID),
    CONSTRAINT FK_Team_Coach FOREIGN KEY (CoachID)
        REFERENCES Coach(CoachID)
);

-- Table 8: Equipment
CREATE TABLE Equipment (
    EquipmentID   INT IDENTITY(1,1) PRIMARY KEY,
    EquipmentName NVARCHAR(100) NOT NULL,
    Category      NVARCHAR(100),
    TotalQuantity INT NOT NULL DEFAULT 0,
    AvailableQty  INT NOT NULL DEFAULT 0,
    Condition     NVARCHAR(50) CHECK (Condition IN ('New', 'Good', 'Fair', 'Poor')),
    PurchaseDate  DATE,
    SportID       INT NOT NULL,
    CONSTRAINT FK_Equipment_Sport FOREIGN KEY (SportID)
        REFERENCES Sport(SportID)
);
GO

-- Verify
SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES
WHERE TABLE_TYPE = 'BASE TABLE'
ORDER BY TABLE_NAME;
-- You should see 8 tables