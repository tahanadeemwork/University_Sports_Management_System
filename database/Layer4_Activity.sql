USE UniversitySportsDB;
GO

-- LAYER 4: Depends on Layer 3
-- Safe to run multiple times

DROP TABLE IF EXISTS PracticeAttendance;
DROP TABLE IF EXISTS TournamentTeam;
DROP TABLE IF EXISTS Match;
GO

-- Table 12: Match
CREATE TABLE Match (
    MatchID       INT IDENTITY(1,1) PRIMARY KEY,
    MatchDate     DATE NOT NULL,
    MatchTime     TIME,
    Round         NVARCHAR(50),
    Status        NVARCHAR(50) CHECK (Status IN
                  ('Scheduled', 'Ongoing', 'Completed', 'Postponed')),
    HomeTeamID    INT NOT NULL,
    AwayTeamID    INT NOT NULL,
    HomeTeamScore INT DEFAULT 0,
    AwayTeamScore INT DEFAULT 0,
    WinnerTeamID  INT,
    TournamentID  INT NOT NULL,
    VenueID       INT NOT NULL,
    CONSTRAINT FK_Match_HomeTeam FOREIGN KEY (HomeTeamID)
        REFERENCES Team(TeamID),
    CONSTRAINT FK_Match_AwayTeam FOREIGN KEY (AwayTeamID)
        REFERENCES Team(TeamID),
    CONSTRAINT FK_Match_Winner FOREIGN KEY (WinnerTeamID)
        REFERENCES Team(TeamID),
    CONSTRAINT FK_Match_Tournament FOREIGN KEY (TournamentID)
        REFERENCES Tournament(TournamentID),
    CONSTRAINT FK_Match_Venue FOREIGN KEY (VenueID)
        REFERENCES Venue(VenueID),
    CONSTRAINT CHK_Match_Teams CHECK (HomeTeamID <> AwayTeamID)
);

-- Table 13: TournamentTeam
CREATE TABLE TournamentTeam (
    TournamentTeamID INT IDENTITY(1,1) PRIMARY KEY,
    TournamentID     INT NOT NULL,
    TeamID           INT NOT NULL,
    RegistrationDate DATE,
    GroupName        NVARCHAR(20),
    CONSTRAINT FK_TournTeam_Tournament FOREIGN KEY (TournamentID)
        REFERENCES Tournament(TournamentID),
    CONSTRAINT FK_TournTeam_Team FOREIGN KEY (TeamID)
        REFERENCES Team(TeamID),
    CONSTRAINT UQ_TournamentTeam UNIQUE (TournamentID, TeamID)
);

-- Table 14: PracticeAttendance
CREATE TABLE PracticeAttendance (
    AttendanceID INT IDENTITY(1,1) PRIMARY KEY,
    SessionID    INT NOT NULL,
    StudentID    INT NOT NULL,
    Status       NVARCHAR(20) CHECK (Status IN ('Present', 'Absent', 'Late')),
    Remarks      NVARCHAR(255),
    CONSTRAINT FK_Attendance_Session FOREIGN KEY (SessionID)
        REFERENCES PracticeSession(SessionID),
    CONSTRAINT FK_Attendance_Student FOREIGN KEY (StudentID)
        REFERENCES Student(StudentID),
    CONSTRAINT UQ_Attendance UNIQUE (SessionID, StudentID)
);
GO

-- Verify
SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES
WHERE TABLE_TYPE = 'BASE TABLE'
ORDER BY TABLE_NAME;
-- You should see 14 tables