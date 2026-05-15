USE UniversitySportsDB;
GO

-- LAYER 1: Foundation tables (no foreign keys)
-- Safe to run multiple times

DROP TABLE IF EXISTS Department;
DROP TABLE IF EXISTS Sport;
DROP TABLE IF EXISTS Venue;
DROP TABLE IF EXISTS Semester;
GO

-- Table 1: Department
CREATE TABLE Department (
    DepartmentID    INT IDENTITY(1,1) PRIMARY KEY,
    DepartmentName  NVARCHAR(100) NOT NULL UNIQUE,
    DeanName        NVARCHAR(100),
    ContactEmail    NVARCHAR(100),
    EstablishedYear INT
);

-- Table 2: Sport
CREATE TABLE Sport (
    SportID     INT IDENTITY(1,1) PRIMARY KEY,
    SportName   NVARCHAR(100) NOT NULL UNIQUE,
    SportType   NVARCHAR(50) CHECK (SportType IN ('Individual', 'Team')),
    Description NVARCHAR(255)
);

-- Table 3: Venue
CREATE TABLE Venue (
    VenueID   INT IDENTITY(1,1) PRIMARY KEY,
    VenueName NVARCHAR(100) NOT NULL,
    Location  NVARCHAR(200),
    Capacity  INT,
    VenueType NVARCHAR(50) CHECK (VenueType IN ('Indoor', 'Outdoor'))
);

-- Table 4: Semester
CREATE TABLE Semester (
    SemesterID   INT IDENTITY(1,1) PRIMARY KEY,
    SemesterName NVARCHAR(50) NOT NULL,
    StartDate    DATE NOT NULL,
    EndDate      DATE NOT NULL,
    AcademicYear NVARCHAR(20)
);
GO

-- Verify
SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES
WHERE TABLE_TYPE = 'BASE TABLE'
ORDER BY TABLE_NAME;
-- You should see 4 tables