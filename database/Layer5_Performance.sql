USE UniversitySportsDB;
GO

-- LAYER 5: Depends on Layer 4
-- Safe to run multiple times

DROP TABLE IF EXISTS MatchPerformance;
DROP TABLE IF EXISTS EquipmentIssue;
DROP TABLE IF EXISTS PointsTable;
GO

-- Table 15: MatchPerformance
CREATE TABLE MatchPerformance (
    PerformanceID   INT IDENTITY(1,1) PRIMARY KEY,
    MatchID         INT NOT NULL,
    StudentID       INT NOT NULL,
    TeamID          INT NOT NULL,
    GoalsScored     INT DEFAULT 0,
    Assists         INT DEFAULT 0,
    YellowCards     INT DEFAULT 0,
    RedCards        INT DEFAULT 0,
    MinutesPlayed   INT DEFAULT 0,
    PerformanceNote NVARCHAR(255),
    CONSTRAINT FK_Perf_Match FOREIGN KEY (MatchID)
        REFERENCES Match(MatchID),
    CONSTRAINT FK_Perf_Student FOREIGN KEY (StudentID)
        REFERENCES Student(StudentID),
    CONSTRAINT FK_Perf_Team FOREIGN KEY (TeamID)
        REFERENCES Team(TeamID),
    CONSTRAINT UQ_Performance UNIQUE (MatchID, StudentID)
);

-- Table 16: EquipmentIssue
CREATE TABLE EquipmentIssue (
    IssueID     INT IDENTITY(1,1) PRIMARY KEY,
    IssueDate   DATE NOT NULL,
    ReturnDate  DATE,
    IsReturned  BIT DEFAULT 0,
    FineAmount  DECIMAL(8,2) DEFAULT 0,
    Remarks     NVARCHAR(255),
    EquipmentID INT NOT NULL,
    StudentID   INT NOT NULL,
    CONSTRAINT FK_Issue_Equipment FOREIGN KEY (EquipmentID)
        REFERENCES Equipment(EquipmentID),
    CONSTRAINT FK_Issue_Student FOREIGN KEY (StudentID)
        REFERENCES Student(StudentID),
    CONSTRAINT CHK_ReturnDate CHECK (ReturnDate IS NULL
        OR ReturnDate >= IssueDate)
);

-- Table 17: PointsTable
CREATE TABLE PointsTable (
    PointsTableID INT IDENTITY(1,1) PRIMARY KEY,
    TournamentID  INT NOT NULL,
    TeamID        INT NOT NULL,
    MatchesPlayed INT DEFAULT 0,
    Wins          INT DEFAULT 0,
    Losses        INT DEFAULT 0,
    Draws         INT DEFAULT 0,
    GoalsFor      INT DEFAULT 0,
    GoalsAgainst  INT DEFAULT 0,
    Points        INT DEFAULT 0,
    CONSTRAINT FK_Points_Tournament FOREIGN KEY (TournamentID)
        REFERENCES Tournament(TournamentID),
    CONSTRAINT FK_Points_Team FOREIGN KEY (TeamID)
        REFERENCES Team(TeamID),
    CONSTRAINT UQ_PointsTable UNIQUE (TournamentID, TeamID)
);
GO

-- Verify
SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES
WHERE TABLE_TYPE = 'BASE TABLE'
ORDER BY TABLE_NAME;
-- You should see 17 tables