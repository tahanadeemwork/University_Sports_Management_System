USE UniversitySportsDB;
GO

-- LAYER 3: Depends on Layer 2
-- Safe to run multiple times

DROP TABLE IF EXISTS PracticeSession;
DROP TABLE IF EXISTS Tournament;
DROP TABLE IF EXISTS TeamPlayer;
GO

-- Table 9: TeamPlayer
CREATE TABLE TeamPlayer (
    TeamPlayerID INT IDENTITY(1,1) PRIMARY KEY,
    TeamID       INT NOT NULL,
    StudentID    INT NOT NULL,
    JoinDate     DATE,
    Position     NVARCHAR(50),
    IsActive     BIT DEFAULT 1,
    CONSTRAINT FK_TeamPlayer_Team FOREIGN KEY (TeamID)
        REFERENCES Team(TeamID),
    CONSTRAINT FK_TeamPlayer_Student FOREIGN KEY (StudentID)
        REFERENCES Student(StudentID),
    CONSTRAINT UQ_TeamPlayer UNIQUE (TeamID, StudentID)
);

-- Table 10: Tournament
CREATE TABLE Tournament (
    TournamentID   INT IDENTITY(1,1) PRIMARY KEY,
    TournamentName NVARCHAR(150) NOT NULL,
    StartDate      DATE NOT NULL,
    EndDate        DATE NOT NULL,
    Status         NVARCHAR(50) CHECK (Status IN
                   ('Upcoming', 'Ongoing', 'Completed', 'Cancelled')),
    OrganizerName  NVARCHAR(100),
    SportID        INT NOT NULL,
    SemesterID     INT NOT NULL,
    CONSTRAINT FK_Tournament_Sport FOREIGN KEY (SportID)
        REFERENCES Sport(SportID),
    CONSTRAINT FK_Tournament_Semester FOREIGN KEY (SemesterID)
        REFERENCES Semester(SemesterID),
    CONSTRAINT CHK_Tournament_Dates CHECK (EndDate >= StartDate)
);

-- Table 11: PracticeSession
CREATE TABLE PracticeSession (
    SessionID   INT IDENTITY(1,1) PRIMARY KEY,
    SessionDate DATE NOT NULL,
    StartTime   TIME NOT NULL,
    EndTime     TIME NOT NULL,
    Notes       NVARCHAR(255),
    TeamID      INT NOT NULL,
    CoachID     INT NOT NULL,
    VenueID     INT NOT NULL,
    CONSTRAINT FK_Session_Team FOREIGN KEY (TeamID)
        REFERENCES Team(TeamID),
    CONSTRAINT FK_Session_Coach FOREIGN KEY (CoachID)
        REFERENCES Coach(CoachID),
    CONSTRAINT FK_Session_Venue FOREIGN KEY (VenueID)
        REFERENCES Venue(VenueID),
    CONSTRAINT CHK_Session_Time CHECK (EndTime > StartTime)
);
GO

-- Verify
SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES
WHERE TABLE_TYPE = 'BASE TABLE'
ORDER BY TABLE_NAME;
-- You should see 11 tables