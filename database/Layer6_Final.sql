USE UniversitySportsDB;
GO

-- LAYER 6: Final tables
-- Safe to run multiple times

DROP TABLE IF EXISTS DepartmentRanking;
DROP TABLE IF EXISTS PlayerRating;
DROP TABLE IF EXISTS InjuryRecord;
DROP TABLE IF EXISTS Expense;
DROP TABLE IF EXISTS Reminder;
GO

-- Table 18: PlayerRating
CREATE TABLE PlayerRating (
    RatingID   INT IDENTITY(1,1) PRIMARY KEY,
    Rating     DECIMAL(3,1) CHECK (Rating BETWEEN 1.0 AND 10.0),
    Review     NVARCHAR(255),
    RatingDate DATE NOT NULL,
    StudentID  INT NOT NULL,
    CoachID    INT NOT NULL,
    SportID    INT NOT NULL,
    CONSTRAINT FK_Rating_Student FOREIGN KEY (StudentID)
        REFERENCES Student(StudentID),
    CONSTRAINT FK_Rating_Coach FOREIGN KEY (CoachID)
        REFERENCES Coach(CoachID),
    CONSTRAINT FK_Rating_Sport FOREIGN KEY (SportID)
        REFERENCES Sport(SportID)
);

-- Table 19: InjuryRecord
CREATE TABLE InjuryRecord (
    InjuryID     INT IDENTITY(1,1) PRIMARY KEY,
    InjuryDate   DATE NOT NULL,
    InjuryType   NVARCHAR(100),
    Severity     NVARCHAR(50) CHECK (Severity IN
                 ('Minor', 'Moderate', 'Severe')),
    Description  NVARCHAR(255),
    RecoveryDays INT,
    IsRecovered  BIT DEFAULT 0,
    StudentID    INT NOT NULL,
    MatchID      INT,
    CONSTRAINT FK_Injury_Student FOREIGN KEY (StudentID)
        REFERENCES Student(StudentID),
    CONSTRAINT FK_Injury_Match FOREIGN KEY (MatchID)
        REFERENCES Match(MatchID)
);

-- Table 20: DepartmentRanking
CREATE TABLE DepartmentRanking (
    RankingID    INT IDENTITY(1,1) PRIMARY KEY,
    RankPosition INT NOT NULL,
    TotalPoints  INT DEFAULT 0,
    TotalWins    INT DEFAULT 0,
    TotalLosses  INT DEFAULT 0,
    Season       NVARCHAR(50),
    DepartmentID INT NOT NULL,
    SportID      INT NOT NULL,
    SemesterID   INT NOT NULL,
    CONSTRAINT FK_Ranking_Department FOREIGN KEY (DepartmentID)
        REFERENCES Department(DepartmentID),
    CONSTRAINT FK_Ranking_Sport FOREIGN KEY (SportID)
        REFERENCES Sport(SportID),
    CONSTRAINT FK_Ranking_Semester FOREIGN KEY (SemesterID)
        REFERENCES Semester(SemesterID),
    CONSTRAINT UQ_Ranking UNIQUE (DepartmentID, SportID, SemesterID)
);

-- Table 21: Expense
CREATE TABLE Expense (
    ExpenseID    INT IDENTITY(1,1) PRIMARY KEY,
    ExpenseTitle NVARCHAR(150) NOT NULL,
    Category     NVARCHAR(100) CHECK (Category IN
                 ('Transport','Food','Equipment','Prize','Venue','Other')),
    Amount       DECIMAL(10,2) NOT NULL CHECK (Amount > 0),
    ExpenseDate  DATE NOT NULL,
    PaidBy       NVARCHAR(100),
    TournamentID INT NOT NULL,
    CONSTRAINT FK_Expense_Tournament FOREIGN KEY (TournamentID)
        REFERENCES Tournament(TournamentID)
);

-- Table 22: Reminder
CREATE TABLE Reminder (
    ReminderID   INT IDENTITY(1,1) PRIMARY KEY,
    Title        NVARCHAR(150) NOT NULL,
    Message      NVARCHAR(500),
    ReminderDate DATETIME NOT NULL,
    IsRead       BIT DEFAULT 0,
    ReminderType NVARCHAR(50) CHECK (ReminderType IN
                 ('Match','Practice','Tournament','General')),
    StudentID    INT,
    CONSTRAINT FK_Reminder_Student FOREIGN KEY (StudentID)
        REFERENCES Student(StudentID)
);
GO

-- Final verification - should show all 22 tables
SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES
WHERE TABLE_TYPE = 'BASE TABLE'
ORDER BY TABLE_NAME;