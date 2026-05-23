# backend.py
# Backend Business Logic Layer - OOP with Methods

import pandas as pd
from datetime import date, datetime


# ============================================================
# IMPORT DATABASE - Safe import with error handling
# ============================================================

def _get_db():
    """Safely get database connection"""
    try:
        from database_connection import db
        return db
    except Exception as e:
        raise ImportError(f"Cannot import database connection: {e}")


# ============================================================
# BASE REPOSITORY CLASS
# ============================================================

class BaseRepository:
    """Base class providing common CRUD operations"""

    def __init__(self):
        self._db = None

    @property
    def db(self):
        """Lazy database connection getter"""
        if self._db is None:
            self._db = _get_db()
        return self._db

    def _ensure_connected(self):
        """Ensure database connection is active"""
        success, msg = self.db.ensure_connected()
        if not success:
            raise ConnectionError(f"Database connection failed: {msg}")

    def get_all(self, table_name, order_by=None):
        """Get all records from a table"""
        query = f"SELECT * FROM {table_name}"
        if order_by:
            query += f" ORDER BY {order_by}"
        return self.db.execute_query(query)

    def get_by_id(self, table_name, id_column, id_value):
        """Get record by primary key"""
        query = f"SELECT * FROM {table_name} WHERE {id_column} = ?"
        return self.db.execute_query(query, (id_value,))

    def delete_by_id(self, table_name, id_column, id_value):
        """Delete record by primary key"""
        query = f"DELETE FROM {table_name} WHERE {id_column} = ?"
        rows, err = self.db.execute_non_query(query, (id_value,))
        if err:
            return False, f"Delete failed: {err}"
        if rows == 0:
            return False, "No record found with that ID"
        return True, "Record deleted successfully"

    def get_dropdown_options(self, table_name, id_col, name_col, order_by=None):
        """Get ID-Name pairs for dropdown menus"""
        order = order_by or name_col
        query = f"SELECT {id_col}, {name_col} FROM {table_name} ORDER BY {order}"
        df, err = self.db.execute_query(query)
        if err or df is None or df.empty:
            return {}
        return dict(zip(df[name_col].astype(str), df[id_col]))


# ============================================================
# DEPARTMENT REPOSITORY
# ============================================================

class DepartmentRepository(BaseRepository):

    def get_all_departments(self):
        query = """
            SELECT DepartmentID, DepartmentName, DeanName, 
                   ContactEmail, EstablishedYear 
            FROM Department 
            ORDER BY DepartmentName
        """
        return self.db.execute_query(query)

    def add_department(self, name, dean_name, email, established_year):
        query = """
            INSERT INTO Department (DepartmentName, DeanName, ContactEmail, EstablishedYear)
            VALUES (?, ?, ?, ?)
        """
        rows, err = self.db.execute_non_query(query, (name, dean_name, email, established_year))
        if err:
            return False, f"Error: {err}"
        return True, "Department added successfully!"

    def update_department(self, dept_id, name, dean_name, email, established_year):
        query = """
            UPDATE Department 
            SET DepartmentName=?, DeanName=?, ContactEmail=?, EstablishedYear=?
            WHERE DepartmentID=?
        """
        rows, err = self.db.execute_non_query(
            query, (name, dean_name, email, established_year, dept_id)
        )
        if err:
            return False, f"Error: {err}"
        return True, "Department updated successfully!"

    def delete_department(self, dept_id):
        return self.delete_by_id("Department", "DepartmentID", dept_id)

    def get_department_options(self):
        return self.get_dropdown_options("Department", "DepartmentID", "DepartmentName")


# ============================================================
# SPORT REPOSITORY
# ============================================================

class SportRepository(BaseRepository):

    def get_all_sports(self):
        query = "SELECT SportID, SportName, SportType, Description FROM Sport ORDER BY SportName"
        return self.db.execute_query(query)

    def add_sport(self, name, sport_type, description):
        query = "INSERT INTO Sport (SportName, SportType, Description) VALUES (?, ?, ?)"
        rows, err = self.db.execute_non_query(query, (name, sport_type, description))
        if err:
            return False, f"Error: {err}"
        return True, "Sport added successfully!"

    def update_sport(self, sport_id, name, sport_type, description):
        query = "UPDATE Sport SET SportName=?, SportType=?, Description=? WHERE SportID=?"
        rows, err = self.db.execute_non_query(query, (name, sport_type, description, sport_id))
        if err:
            return False, f"Error: {err}"
        return True, "Sport updated successfully!"

    def delete_sport(self, sport_id):
        return self.delete_by_id("Sport", "SportID", sport_id)

    def get_sport_options(self):
        return self.get_dropdown_options("Sport", "SportID", "SportName")


# ============================================================
# VENUE REPOSITORY
# ============================================================

class VenueRepository(BaseRepository):

    def get_all_venues(self):
        query = "SELECT VenueID, VenueName, Location, Capacity, VenueType FROM Venue ORDER BY VenueName"
        return self.db.execute_query(query)

    def add_venue(self, name, location, capacity, venue_type):
        query = "INSERT INTO Venue (VenueName, Location, Capacity, VenueType) VALUES (?, ?, ?, ?)"
        rows, err = self.db.execute_non_query(query, (name, location, capacity, venue_type))
        if err:
            return False, f"Error: {err}"
        return True, "Venue added successfully!"

    def update_venue(self, venue_id, name, location, capacity, venue_type):
        query = """
            UPDATE Venue 
            SET VenueName=?, Location=?, Capacity=?, VenueType=? 
            WHERE VenueID=?
        """
        rows, err = self.db.execute_non_query(
            query, (name, location, capacity, venue_type, venue_id)
        )
        if err:
            return False, f"Error: {err}"
        return True, "Venue updated successfully!"

    def delete_venue(self, venue_id):
        return self.delete_by_id("Venue", "VenueID", venue_id)

    def get_venue_options(self):
        return self.get_dropdown_options("Venue", "VenueID", "VenueName")


# ============================================================
# SEMESTER REPOSITORY
# ============================================================

class SemesterRepository(BaseRepository):

    def get_all_semesters(self):
        query = """
            SELECT SemesterID, SemesterName, StartDate, EndDate, AcademicYear 
            FROM Semester ORDER BY StartDate DESC
        """
        return self.db.execute_query(query)

    def add_semester(self, name, start_date, end_date, academic_year):
        query = """
            INSERT INTO Semester (SemesterName, StartDate, EndDate, AcademicYear)
            VALUES (?, ?, ?, ?)
        """
        rows, err = self.db.execute_non_query(query, (name, start_date, end_date, academic_year))
        if err:
            return False, f"Error: {err}"
        return True, "Semester added successfully!"

    def update_semester(self, sem_id, name, start_date, end_date, academic_year):
        query = """
            UPDATE Semester 
            SET SemesterName=?, StartDate=?, EndDate=?, AcademicYear=?
            WHERE SemesterID=?
        """
        rows, err = self.db.execute_non_query(
            query, (name, start_date, end_date, academic_year, sem_id)
        )
        if err:
            return False, f"Error: {err}"
        return True, "Semester updated successfully!"

    def delete_semester(self, sem_id):
        return self.delete_by_id("Semester", "SemesterID", sem_id)

    def get_semester_options(self):
        return self.get_dropdown_options("Semester", "SemesterID", "SemesterName")


# ============================================================
# STUDENT REPOSITORY
# ============================================================

class StudentRepository(BaseRepository):

    def get_all_students(self):
        query = """
            SELECT s.StudentID, s.RegistrationNo, s.FullName, s.Gender,
                   s.DateOfBirth, s.ContactNo, s.Email, s.Address,
                   s.EnrollmentYear, d.DepartmentName, sem.SemesterName
            FROM Student s
            JOIN Department d ON s.DepartmentID = d.DepartmentID
            JOIN Semester sem ON s.SemesterID = sem.SemesterID
            ORDER BY s.FullName
        """
        return self.db.execute_query(query)

    def add_student(self, reg_no, full_name, gender, dob, contact, email,
                    address, enrollment_year, dept_id, sem_id):
        query = """
            INSERT INTO Student (RegistrationNo, FullName, Gender, DateOfBirth,
                                ContactNo, Email, Address, EnrollmentYear, 
                                DepartmentID, SemesterID)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
        rows, err = self.db.execute_non_query(
            query, (reg_no, full_name, gender, dob, contact, email,
                    address, enrollment_year, dept_id, sem_id)
        )
        if err:
            return False, f"Error: {err}"
        return True, "Student added successfully!"

    def update_student(self, student_id, reg_no, full_name, gender, dob,
                       contact, email, address, enrollment_year, dept_id, sem_id):
        query = """
            UPDATE Student 
            SET RegistrationNo=?, FullName=?, Gender=?, DateOfBirth=?,
                ContactNo=?, Email=?, Address=?, EnrollmentYear=?,
                DepartmentID=?, SemesterID=?
            WHERE StudentID=?
        """
        rows, err = self.db.execute_non_query(
            query, (reg_no, full_name, gender, dob, contact, email,
                    address, enrollment_year, dept_id, sem_id, student_id)
        )
        if err:
            return False, f"Error: {err}"
        return True, "Student updated successfully!"

    def delete_student(self, student_id):
        return self.delete_by_id("Student", "StudentID", student_id)

    def get_student_options(self):
        query = """
            SELECT StudentID, 
                   FullName + ' (' + RegistrationNo + ')' AS DisplayName 
            FROM Student ORDER BY FullName
        """
        df, err = self.db.execute_query(query)
        if err or df is None or df.empty:
            return {}
        return dict(zip(df['DisplayName'].astype(str), df['StudentID']))

    def search_students(self, search_term):
        query = """
            SELECT s.StudentID, s.RegistrationNo, s.FullName, s.Gender,
                   s.ContactNo, s.Email, d.DepartmentName, sem.SemesterName
            FROM Student s
            JOIN Department d ON s.DepartmentID = d.DepartmentID
            JOIN Semester sem ON s.SemesterID = sem.SemesterID
            WHERE s.FullName LIKE ? OR s.RegistrationNo LIKE ?
            ORDER BY s.FullName
        """
        term = f"%{search_term}%"
        return self.db.execute_query(query, (term, term))


# ============================================================
# COACH REPOSITORY
# ============================================================

class CoachRepository(BaseRepository):

    def get_all_coaches(self):
        query = """
            SELECT c.CoachID, c.FullName, c.Gender, c.ContactNo, c.Email,
                   c.Qualification, c.ExperienceYears,
                   d.DepartmentName, s.SportName
            FROM Coach c
            JOIN Department d ON c.DepartmentID = d.DepartmentID
            JOIN Sport s ON c.SportID = s.SportID
            ORDER BY c.FullName
        """
        return self.db.execute_query(query)

    def add_coach(self, full_name, gender, contact, email, qualification,
                  experience_years, dept_id, sport_id):
        query = """
            INSERT INTO Coach (FullName, Gender, ContactNo, Email, Qualification,
                              ExperienceYears, DepartmentID, SportID)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """
        rows, err = self.db.execute_non_query(
            query, (full_name, gender, contact, email, qualification,
                    experience_years, dept_id, sport_id)
        )
        if err:
            return False, f"Error: {err}"
        return True, "Coach added successfully!"

    def update_coach(self, coach_id, full_name, gender, contact, email,
                     qualification, experience_years, dept_id, sport_id):
        query = """
            UPDATE Coach 
            SET FullName=?, Gender=?, ContactNo=?, Email=?, Qualification=?,
                ExperienceYears=?, DepartmentID=?, SportID=?
            WHERE CoachID=?
        """
        rows, err = self.db.execute_non_query(
            query, (full_name, gender, contact, email, qualification,
                    experience_years, dept_id, sport_id, coach_id)
        )
        if err:
            return False, f"Error: {err}"
        return True, "Coach updated successfully!"

    def delete_coach(self, coach_id):
        return self.delete_by_id("Coach", "CoachID", coach_id)

    def get_coach_options(self):
        return self.get_dropdown_options("Coach", "CoachID", "FullName")


# ============================================================
# TEAM REPOSITORY
# ============================================================

class TeamRepository(BaseRepository):

    def get_all_teams(self):
        query = """
            SELECT t.TeamID, t.TeamName, t.Gender, t.FormationYear,
                   d.DepartmentName, s.SportName, 
                   ISNULL(c.FullName, 'No Coach') AS CoachName
            FROM Team t
            JOIN Department d ON t.DepartmentID = d.DepartmentID
            JOIN Sport s ON t.SportID = s.SportID
            LEFT JOIN Coach c ON t.CoachID = c.CoachID
            ORDER BY t.TeamName
        """
        return self.db.execute_query(query)

    def add_team(self, team_name, gender, formation_year, dept_id, sport_id, coach_id):
        query = """
            INSERT INTO Team (TeamName, Gender, FormationYear, DepartmentID, SportID, CoachID)
            VALUES (?, ?, ?, ?, ?, ?)
        """
        coach_val = int(coach_id) if coach_id else None
        rows, err = self.db.execute_non_query(
            query, (team_name, gender, formation_year, dept_id, sport_id, coach_val)
        )
        if err:
            return False, f"Error: {err}"
        return True, "Team added successfully!"

    def update_team(self, team_id, team_name, gender, formation_year,
                    dept_id, sport_id, coach_id):
        query = """
            UPDATE Team 
            SET TeamName=?, Gender=?, FormationYear=?, 
                DepartmentID=?, SportID=?, CoachID=?
            WHERE TeamID=?
        """
        coach_val = int(coach_id) if coach_id else None
        rows, err = self.db.execute_non_query(
            query, (team_name, gender, formation_year, dept_id,
                    sport_id, coach_val, team_id)
        )
        if err:
            return False, f"Error: {err}"
        return True, "Team updated successfully!"

    def delete_team(self, team_id):
        return self.delete_by_id("Team", "TeamID", team_id)

    def get_team_options(self):
        return self.get_dropdown_options("Team", "TeamID", "TeamName")

    def get_team_players(self, team_id):
        query = """
            SELECT tp.TeamPlayerID, s.FullName, s.RegistrationNo,
                   tp.JoinDate, 
                   ISNULL(tp.Position, 'Player') AS Position, 
                   tp.IsActive
            FROM TeamPlayer tp
            JOIN Student s ON tp.StudentID = s.StudentID
            WHERE tp.TeamID = ?
            ORDER BY tp.IsActive DESC, tp.Position
        """
        return self.db.execute_query(query, (team_id,))

    def add_player_to_team(self, team_id, student_id, join_date, position):
        query = """
            INSERT INTO TeamPlayer (TeamID, StudentID, JoinDate, Position, IsActive)
            VALUES (?, ?, ?, ?, 1)
        """
        rows, err = self.db.execute_non_query(
            query, (team_id, student_id, join_date, position)
        )
        if err:
            return False, f"Error: {err}"
        return True, "Player added to team successfully!"

    def remove_player_from_team(self, team_player_id):
        query = "DELETE FROM TeamPlayer WHERE TeamPlayerID = ?"
        rows, err = self.db.execute_non_query(query, (team_player_id,))
        if err:
            return False, f"Error: {err}"
        return True, "Player removed successfully!"


# ============================================================
# EQUIPMENT REPOSITORY
# ============================================================

class EquipmentRepository(BaseRepository):

    def get_all_equipment(self):
        query = """
            SELECT e.EquipmentID, e.EquipmentName, e.Category,
                   e.TotalQuantity, e.AvailableQty, 
                   ISNULL(e.Condition, 'N/A') AS Condition,
                   e.PurchaseDate, s.SportName
            FROM Equipment e
            JOIN Sport s ON e.SportID = s.SportID
            ORDER BY e.EquipmentName
        """
        return self.db.execute_query(query)

    def add_equipment(self, name, category, total_qty, available_qty,
                      condition, purchase_date, sport_id):
        query = """
            INSERT INTO Equipment (EquipmentName, Category, TotalQuantity, 
                                  AvailableQty, Condition, PurchaseDate, SportID)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """
        rows, err = self.db.execute_non_query(
            query, (name, category, total_qty, available_qty,
                    condition, purchase_date, sport_id)
        )
        if err:
            return False, f"Error: {err}"
        return True, "Equipment added successfully!"

    def update_equipment(self, equip_id, name, category, total_qty, available_qty,
                         condition, purchase_date, sport_id):
        query = """
            UPDATE Equipment 
            SET EquipmentName=?, Category=?, TotalQuantity=?, AvailableQty=?,
                Condition=?, PurchaseDate=?, SportID=?
            WHERE EquipmentID=?
        """
        rows, err = self.db.execute_non_query(
            query, (name, category, total_qty, available_qty,
                    condition, purchase_date, sport_id, equip_id)
        )
        if err:
            return False, f"Error: {err}"
        return True, "Equipment updated successfully!"

    def delete_equipment(self, equip_id):
        return self.delete_by_id("Equipment", "EquipmentID", equip_id)

    def get_equipment_options(self):
        return self.get_dropdown_options("Equipment", "EquipmentID", "EquipmentName")

    def get_equipment_issues(self):
        query = """
            SELECT ei.IssueID, e.EquipmentName, s.FullName AS StudentName,
                   ei.IssueDate, ei.ReturnDate, 
                   ei.IsReturned, 
                   ISNULL(ei.FineAmount, 0) AS FineAmount, 
                   ISNULL(ei.Remarks, '') AS Remarks
            FROM EquipmentIssue ei
            JOIN Equipment e ON ei.EquipmentID = e.EquipmentID
            JOIN Student s ON ei.StudentID = s.StudentID
            ORDER BY ei.IssueDate DESC
        """
        return self.db.execute_query(query)

    def issue_equipment(self, equip_id, student_id, issue_date, remarks):
        query = """
            INSERT INTO EquipmentIssue 
                (IssueDate, IsReturned, FineAmount, Remarks, EquipmentID, StudentID)
            VALUES (?, 0, 0.00, ?, ?, ?)
        """
        rows, err = self.db.execute_non_query(
            query, (issue_date, remarks, equip_id, student_id)
        )
        if err:
            return False, f"Error: {err}"
        return True, "Equipment issued successfully!"

    def return_equipment(self, issue_id, return_date, fine_amount, remarks):
        query = """
            UPDATE EquipmentIssue 
            SET ReturnDate=?, IsReturned=1, FineAmount=?, Remarks=?
            WHERE IssueID=?
        """
        rows, err = self.db.execute_non_query(
            query, (return_date, fine_amount, remarks, issue_id)
        )
        if err:
            return False, f"Error: {err}"
        return True, "Equipment returned successfully!"


# ============================================================
# TOURNAMENT REPOSITORY
# ============================================================

class TournamentRepository(BaseRepository):

    def get_all_tournaments(self):
        query = """
            SELECT t.TournamentID, t.TournamentName, t.StartDate, t.EndDate,
                   ISNULL(t.Status, 'Upcoming') AS Status, 
                   ISNULL(t.OrganizerName, 'N/A') AS OrganizerName, 
                   s.SportName, sem.SemesterName
            FROM Tournament t
            JOIN Sport s ON t.SportID = s.SportID
            JOIN Semester sem ON t.SemesterID = sem.SemesterID
            ORDER BY t.StartDate DESC
        """
        return self.db.execute_query(query)

    def add_tournament(self, name, start_date, end_date, status,
                       organizer, sport_id, semester_id):
        query = """
            INSERT INTO Tournament 
                (TournamentName, StartDate, EndDate, Status, 
                 OrganizerName, SportID, SemesterID)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """
        rows, err = self.db.execute_non_query(
            query, (name, start_date, end_date, status,
                    organizer, sport_id, semester_id)
        )
        if err:
            return False, f"Error: {err}"
        return True, "Tournament added successfully!"

    def update_tournament(self, tourn_id, name, start_date, end_date,
                          status, organizer, sport_id, semester_id):
        query = """
            UPDATE Tournament 
            SET TournamentName=?, StartDate=?, EndDate=?, Status=?,
                OrganizerName=?, SportID=?, SemesterID=?
            WHERE TournamentID=?
        """
        rows, err = self.db.execute_non_query(
            query, (name, start_date, end_date, status, organizer,
                    sport_id, semester_id, tourn_id)
        )
        if err:
            return False, f"Error: {err}"
        return True, "Tournament updated successfully!"

    def delete_tournament(self, tourn_id):
        return self.delete_by_id("Tournament", "TournamentID", tourn_id)

    def get_tournament_options(self):
        return self.get_dropdown_options("Tournament", "TournamentID", "TournamentName")

    def register_team_in_tournament(self, tournament_id, team_id, reg_date, group_name):
        query = """
            INSERT INTO TournamentTeam 
                (TournamentID, TeamID, RegistrationDate, GroupName)
            VALUES (?, ?, ?, ?)
        """
        rows, err = self.db.execute_non_query(
            query, (tournament_id, team_id, reg_date, group_name)
        )
        if err:
            return False, f"Error: {err}"
        return True, "Team registered successfully!"

    def get_tournament_teams(self, tournament_id):
        query = """
            SELECT tt.TournamentTeamID, t.TeamName, tt.RegistrationDate, 
                   ISNULL(tt.GroupName, 'N/A') AS GroupName,
                   d.DepartmentName, s.SportName
            FROM TournamentTeam tt
            JOIN Team t ON tt.TeamID = t.TeamID
            JOIN Department d ON t.DepartmentID = d.DepartmentID
            JOIN Sport s ON t.SportID = s.SportID
            WHERE tt.TournamentID = ?
            ORDER BY tt.GroupName, t.TeamName
        """
        return self.db.execute_query(query, (tournament_id,))

    def get_tournament_expenses(self, tournament_id):
        query = """
            SELECT ExpenseID, ExpenseTitle, 
                   ISNULL(Category, 'Other') AS Category, 
                   Amount, ExpenseDate, 
                   ISNULL(PaidBy, 'N/A') AS PaidBy
            FROM Expense 
            WHERE TournamentID = ?
            ORDER BY ExpenseDate
        """
        return self.db.execute_query(query, (tournament_id,))

    def add_expense(self, title, category, amount, expense_date, paid_by, tournament_id):
        query = """
            INSERT INTO Expense 
                (ExpenseTitle, Category, Amount, ExpenseDate, PaidBy, TournamentID)
            VALUES (?, ?, ?, ?, ?, ?)
        """
        rows, err = self.db.execute_non_query(
            query, (title, category, amount, expense_date, paid_by, tournament_id)
        )
        if err:
            return False, f"Error: {err}"
        return True, "Expense added successfully!"


# ============================================================
# MATCH REPOSITORY
# ============================================================

class MatchRepository(BaseRepository):

    def get_all_matches(self):
        query = """
            SELECT m.MatchID, m.MatchDate, m.MatchTime, 
                   ISNULL(m.Round, 'N/A') AS Round, 
                   ISNULL(m.Status, 'Scheduled') AS Status,
                   ht.TeamName AS HomeTeam, at2.TeamName AS AwayTeam,
                   ISNULL(m.HomeTeamScore, 0) AS HomeTeamScore, 
                   ISNULL(m.AwayTeamScore, 0) AS AwayTeamScore,
                   ISNULL(wt.TeamName, 'TBD') AS Winner,
                   t.TournamentName, v.VenueName
            FROM Match m
            JOIN Team ht ON m.HomeTeamID = ht.TeamID
            JOIN Team at2 ON m.AwayTeamID = at2.TeamID
            LEFT JOIN Team wt ON m.WinnerTeamID = wt.TeamID
            JOIN Tournament t ON m.TournamentID = t.TournamentID
            JOIN Venue v ON m.VenueID = v.VenueID
            ORDER BY m.MatchDate DESC
        """
        return self.db.execute_query(query)

    def add_match(self, match_date, match_time, round_name, status,
                  home_team_id, away_team_id, home_score, away_score,
                  winner_team_id, tournament_id, venue_id):
        query = """
            INSERT INTO Match 
                (MatchDate, MatchTime, Round, Status,
                 HomeTeamID, AwayTeamID, HomeTeamScore, AwayTeamScore,
                 WinnerTeamID, TournamentID, VenueID)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
        winner_val = int(winner_team_id) if winner_team_id else None
        time_val = str(match_time) if match_time else None

        rows, err = self.db.execute_non_query(
            query, (match_date, time_val, round_name, status,
                    home_team_id, away_team_id, home_score, away_score,
                    winner_val, tournament_id, venue_id)
        )
        if err:
            return False, f"Error: {err}"
        return True, "Match added successfully!"

    def update_match(self, match_id, match_date, match_time, round_name, status,
                     home_team_id, away_team_id, home_score, away_score,
                     winner_team_id, tournament_id, venue_id):
        query = """
            UPDATE Match 
            SET MatchDate=?, MatchTime=?, Round=?, Status=?,
                HomeTeamID=?, AwayTeamID=?, HomeTeamScore=?, AwayTeamScore=?,
                WinnerTeamID=?, TournamentID=?, VenueID=?
            WHERE MatchID=?
        """
        winner_val = int(winner_team_id) if winner_team_id else None
        time_val = str(match_time) if match_time else None

        rows, err = self.db.execute_non_query(
            query, (match_date, time_val, round_name, status,
                    home_team_id, away_team_id, home_score, away_score,
                    winner_val, tournament_id, venue_id, match_id)
        )
        if err:
            return False, f"Error: {err}"
        return True, "Match updated successfully!"

    def delete_match(self, match_id):
        return self.delete_by_id("Match", "MatchID", match_id)

    def get_match_options(self):
        query = """
            SELECT m.MatchID, 
                   ht.TeamName + ' vs ' + at2.TeamName + 
                   ' (' + CONVERT(varchar, m.MatchDate, 23) + ')' AS DisplayName
            FROM Match m
            JOIN Team ht ON m.HomeTeamID = ht.TeamID
            JOIN Team at2 ON m.AwayTeamID = at2.TeamID
            ORDER BY m.MatchDate DESC
        """
        df, err = self.db.execute_query(query)
        if err or df is None or df.empty:
            return {}
        return dict(zip(df['DisplayName'].astype(str), df['MatchID']))

    def get_match_performances(self, match_id):
        query = """
            SELECT mp.PerformanceID, s.FullName AS Player, t.TeamName,
                   ISNULL(mp.GoalsScored, 0) AS GoalsScored, 
                   ISNULL(mp.Assists, 0) AS Assists, 
                   ISNULL(mp.YellowCards, 0) AS YellowCards, 
                   ISNULL(mp.RedCards, 0) AS RedCards,
                   ISNULL(mp.MinutesPlayed, 0) AS MinutesPlayed, 
                   ISNULL(mp.PerformanceNote, '') AS PerformanceNote
            FROM MatchPerformance mp
            JOIN Student s ON mp.StudentID = s.StudentID
            JOIN Team t ON mp.TeamID = t.TeamID
            WHERE mp.MatchID = ?
            ORDER BY mp.GoalsScored DESC
        """
        return self.db.execute_query(query, (match_id,))

    def add_match_performance(self, match_id, student_id, team_id, goals,
                              assists, yellow_cards, red_cards, minutes, note):
        query = """
            INSERT INTO MatchPerformance 
                (MatchID, StudentID, TeamID, GoalsScored,
                 Assists, YellowCards, RedCards, MinutesPlayed, PerformanceNote)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
        rows, err = self.db.execute_non_query(
            query, (match_id, student_id, team_id, goals,
                    assists, yellow_cards, red_cards, minutes, note)
        )
        if err:
            return False, f"Error: {err}"
        return True, "Performance added successfully!"


# ============================================================
# PRACTICE SESSION REPOSITORY
# ============================================================

class PracticeSessionRepository(BaseRepository):

    def get_all_sessions(self):
        query = """
            SELECT ps.SessionID, ps.SessionDate, ps.StartTime, ps.EndTime,
                   ISNULL(ps.Notes, '') AS Notes, 
                   t.TeamName, c.FullName AS CoachName, v.VenueName
            FROM PracticeSession ps
            JOIN Team t ON ps.TeamID = t.TeamID
            JOIN Coach c ON ps.CoachID = c.CoachID
            JOIN Venue v ON ps.VenueID = v.VenueID
            ORDER BY ps.SessionDate DESC
        """
        return self.db.execute_query(query)

    def add_session(self, session_date, start_time, end_time, notes,
                    team_id, coach_id, venue_id):
        query = """
            INSERT INTO PracticeSession 
                (SessionDate, StartTime, EndTime, Notes, TeamID, CoachID, VenueID)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """
        rows, err = self.db.execute_non_query(
            query, (session_date, str(start_time), str(end_time),
                    notes, team_id, coach_id, venue_id)
        )
        if err:
            return False, f"Error: {err}"
        return True, "Practice session added successfully!"

    def update_session(self, session_id, session_date, start_time, end_time,
                       notes, team_id, coach_id, venue_id):
        query = """
            UPDATE PracticeSession 
            SET SessionDate=?, StartTime=?, EndTime=?, Notes=?,
                TeamID=?, CoachID=?, VenueID=?
            WHERE SessionID=?
        """
        rows, err = self.db.execute_non_query(
            query, (session_date, str(start_time), str(end_time), notes,
                    team_id, coach_id, venue_id, session_id)
        )
        if err:
            return False, f"Error: {err}"
        return True, "Session updated successfully!"

    def delete_session(self, session_id):
        return self.delete_by_id("PracticeSession", "SessionID", session_id)

    def get_session_options(self):
        query = """
            SELECT ps.SessionID, 
                   t.TeamName + ' - ' + 
                   CONVERT(varchar, ps.SessionDate, 23) AS DisplayName
            FROM PracticeSession ps
            JOIN Team t ON ps.TeamID = t.TeamID
            ORDER BY ps.SessionDate DESC
        """
        df, err = self.db.execute_query(query)
        if err or df is None or df.empty:
            return {}
        return dict(zip(df['DisplayName'].astype(str), df['SessionID']))

    def get_session_attendance(self, session_id):
        query = """
            SELECT pa.AttendanceID, s.FullName AS StudentName,
                   pa.Status, ISNULL(pa.Remarks, '') AS Remarks
            FROM PracticeAttendance pa
            JOIN Student s ON pa.StudentID = s.StudentID
            WHERE pa.SessionID = ?
            ORDER BY pa.Status, s.FullName
        """
        return self.db.execute_query(query, (session_id,))

    def mark_attendance(self, session_id, student_id, status, remarks):
        query = """
            INSERT INTO PracticeAttendance (SessionID, StudentID, Status, Remarks)
            VALUES (?, ?, ?, ?)
        """
        rows, err = self.db.execute_non_query(
            query, (session_id, student_id, status, remarks)
        )
        if err:
            return False, f"Error: {err}"
        return True, "Attendance marked successfully!"


# ============================================================
# INJURY REPOSITORY
# ============================================================

class InjuryRepository(BaseRepository):

    def get_all_injuries(self):
        query = """
            SELECT ir.InjuryID, ir.InjuryDate, 
                   ISNULL(ir.InjuryType, 'Unknown') AS InjuryType, 
                   ISNULL(ir.Severity, 'Minor') AS Severity,
                   ISNULL(ir.Description, '') AS Description, 
                   ISNULL(ir.RecoveryDays, 0) AS RecoveryDays, 
                   ir.IsRecovered,
                   s.FullName AS StudentName,
                   CASE WHEN ir.MatchID IS NOT NULL 
                        THEN ht.TeamName + ' vs ' + at2.TeamName 
                        ELSE 'N/A' END AS MatchInfo
            FROM InjuryRecord ir
            JOIN Student s ON ir.StudentID = s.StudentID
            LEFT JOIN Match m ON ir.MatchID = m.MatchID
            LEFT JOIN Team ht ON m.HomeTeamID = ht.TeamID
            LEFT JOIN Team at2 ON m.AwayTeamID = at2.TeamID
            ORDER BY ir.InjuryDate DESC
        """
        return self.db.execute_query(query)

    def add_injury(self, injury_date, injury_type, severity, description,
                   recovery_days, is_recovered, student_id, match_id=None):
        query = """
            INSERT INTO InjuryRecord 
                (InjuryDate, InjuryType, Severity, Description,
                 RecoveryDays, IsRecovered, StudentID, MatchID)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """
        match_val = int(match_id) if match_id else None
        rows, err = self.db.execute_non_query(
            query, (injury_date, injury_type, severity, description,
                    recovery_days, 1 if is_recovered else 0, student_id, match_val)
        )
        if err:
            return False, f"Error: {err}"
        return True, "Injury record added successfully!"

    def update_injury_recovery(self, injury_id, is_recovered, recovery_days):
        query = """
            UPDATE InjuryRecord 
            SET IsRecovered=?, RecoveryDays=?
            WHERE InjuryID=?
        """
        rows, err = self.db.execute_non_query(
            query, (1 if is_recovered else 0, recovery_days, injury_id)
        )
        if err:
            return False, f"Error: {err}"
        return True, "Updated successfully!"

    def delete_injury(self, injury_id):
        return self.delete_by_id("InjuryRecord", "InjuryID", injury_id)


# ============================================================
# PLAYER RATING REPOSITORY
# ============================================================

class PlayerRatingRepository(BaseRepository):

    def get_all_ratings(self):
        query = """
            SELECT pr.RatingID, s.FullName AS PlayerName, c.FullName AS CoachName,
                   sp.SportName, pr.Rating, 
                   ISNULL(pr.Review, '') AS Review, pr.RatingDate
            FROM PlayerRating pr
            JOIN Student s ON pr.StudentID = s.StudentID
            JOIN Coach c ON pr.CoachID = c.CoachID
            JOIN Sport sp ON pr.SportID = sp.SportID
            ORDER BY pr.RatingDate DESC
        """
        return self.db.execute_query(query)

    def add_rating(self, student_id, coach_id, sport_id, rating, review, rating_date):
        query = """
            INSERT INTO PlayerRating 
                (Rating, Review, RatingDate, StudentID, CoachID, SportID)
            VALUES (?, ?, ?, ?, ?, ?)
        """
        rows, err = self.db.execute_non_query(
            query, (rating, review, rating_date, student_id, coach_id, sport_id)
        )
        if err:
            return False, f"Error: {err}"
        return True, "Rating added successfully!"

    def delete_rating(self, rating_id):
        return self.delete_by_id("PlayerRating", "RatingID", rating_id)

    def get_top_rated_players(self, limit=10):
        query = f"""
            SELECT TOP {limit} s.FullName AS PlayerName, sp.SportName,
                   CAST(AVG(pr.Rating) AS DECIMAL(4,1)) AS AvgRating, 
                   COUNT(pr.RatingID) AS TotalRatings
            FROM PlayerRating pr
            JOIN Student s ON pr.StudentID = s.StudentID
            JOIN Sport sp ON pr.SportID = sp.SportID
            GROUP BY s.FullName, sp.SportName
            ORDER BY AvgRating DESC
        """
        return self.db.execute_query(query)


# ============================================================
# POINTS TABLE REPOSITORY
# ============================================================

class PointsTableRepository(BaseRepository):

    def get_points_table(self, tournament_id):
        query = """
            SELECT pt.PointsTableID, t.TeamName, d.DepartmentName,
                   ISNULL(pt.MatchesPlayed, 0) AS MatchesPlayed, 
                   ISNULL(pt.Wins, 0) AS Wins, 
                   ISNULL(pt.Losses, 0) AS Losses, 
                   ISNULL(pt.Draws, 0) AS Draws,
                   ISNULL(pt.GoalsFor, 0) AS GoalsFor, 
                   ISNULL(pt.GoalsAgainst, 0) AS GoalsAgainst, 
                   ISNULL(pt.GoalsFor, 0) - ISNULL(pt.GoalsAgainst, 0) AS GoalDiff,
                   ISNULL(pt.Points, 0) AS Points
            FROM PointsTable pt
            JOIN Team t ON pt.TeamID = t.TeamID
            JOIN Department d ON t.DepartmentID = d.DepartmentID
            WHERE pt.TournamentID = ?
            ORDER BY pt.Points DESC, pt.Wins DESC
        """
        return self.db.execute_query(query, (tournament_id,))

    def update_points(self, points_table_id, matches_played, wins, losses,
                      draws, goals_for, goals_against, points):
        query = """
            UPDATE PointsTable 
            SET MatchesPlayed=?, Wins=?, Losses=?, Draws=?,
                GoalsFor=?, GoalsAgainst=?, Points=?
            WHERE PointsTableID=?
        """
        rows, err = self.db.execute_non_query(
            query, (matches_played, wins, losses, draws,
                    goals_for, goals_against, points, points_table_id)
        )
        if err:
            return False, f"Error: {err}"
        return True, "Points updated successfully!"

    def add_points_entry(self, tournament_id, team_id):
        query = """
            INSERT INTO PointsTable 
                (TournamentID, TeamID, MatchesPlayed, Wins, 
                 Losses, Draws, GoalsFor, GoalsAgainst, Points)
            VALUES (?, ?, 0, 0, 0, 0, 0, 0, 0)
        """
        rows, err = self.db.execute_non_query(query, (tournament_id, team_id))
        if err:
            return False, f"Error: {err}"
        return True, "Points entry added successfully!"


# ============================================================
# REMINDER REPOSITORY
# ============================================================

class ReminderRepository(BaseRepository):

    def get_all_reminders(self):
        query = """
            SELECT r.ReminderID, r.Title, 
                   ISNULL(r.Message, '') AS Message, 
                   r.ReminderDate,
                   r.IsRead, 
                   ISNULL(r.ReminderType, 'General') AS ReminderType,
                   ISNULL(s.FullName, 'All Students') AS StudentName
            FROM Reminder r
            LEFT JOIN Student s ON r.StudentID = s.StudentID
            ORDER BY r.ReminderDate DESC
        """
        return self.db.execute_query(query)

    def add_reminder(self, title, message, reminder_date, reminder_type, student_id=None):
        query = """
            INSERT INTO Reminder 
                (Title, Message, ReminderDate, IsRead, ReminderType, StudentID)
            VALUES (?, ?, ?, 0, ?, ?)
        """
        student_val = int(student_id) if student_id else None
        rows, err = self.db.execute_non_query(
            query, (title, message, reminder_date, reminder_type, student_val)
        )
        if err:
            return False, f"Error: {err}"
        return True, "Reminder added successfully!"

    def mark_as_read(self, reminder_id):
        query = "UPDATE Reminder SET IsRead=1 WHERE ReminderID=?"
        rows, err = self.db.execute_non_query(query, (reminder_id,))
        if err:
            return False, f"Error: {err}"
        return True, "Marked as read!"

    def delete_reminder(self, reminder_id):
        return self.delete_by_id("Reminder", "ReminderID", reminder_id)

    def get_unread_count(self):
        result, err = self.db.execute_scalar(
            "SELECT COUNT(*) FROM Reminder WHERE IsRead=0"
        )
        return result or 0


# ============================================================
# DEPARTMENT RANKING REPOSITORY
# ============================================================

class DepartmentRankingRepository(BaseRepository):

    def get_all_rankings(self):
        query = """
            SELECT dr.RankingID, dr.RankPosition, 
                   ISNULL(dr.TotalPoints, 0) AS TotalPoints, 
                   ISNULL(dr.TotalWins, 0) AS TotalWins,
                   ISNULL(dr.TotalLosses, 0) AS TotalLosses, 
                   ISNULL(dr.Season, 'N/A') AS Season,
                   d.DepartmentName, s.SportName, sem.SemesterName
            FROM DepartmentRanking dr
            JOIN Department d ON dr.DepartmentID = d.DepartmentID
            JOIN Sport s ON dr.SportID = s.SportID
            JOIN Semester sem ON dr.SemesterID = sem.SemesterID
            ORDER BY dr.RankPosition
        """
        return self.db.execute_query(query)

    def add_ranking(self, rank_position, total_points, total_wins, total_losses,
                    season, dept_id, sport_id, semester_id):
        query = """
            INSERT INTO DepartmentRanking 
                (RankPosition, TotalPoints, TotalWins, TotalLosses,
                 Season, DepartmentID, SportID, SemesterID)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """
        rows, err = self.db.execute_non_query(
            query, (rank_position, total_points, total_wins, total_losses,
                    season, dept_id, sport_id, semester_id)
        )
        if err:
            return False, f"Error: {err}"
        return True, "Ranking added successfully!"

    def delete_ranking(self, ranking_id):
        return self.delete_by_id("DepartmentRanking", "RankingID", ranking_id)


# ============================================================
# DASHBOARD SERVICE
# ============================================================

class DashboardService(BaseRepository):

    def get_summary_stats(self):
        stats = {}
        queries = {
            'total_students': "SELECT COUNT(*) FROM Student",
            'total_coaches': "SELECT COUNT(*) FROM Coach",
            'total_teams': "SELECT COUNT(*) FROM Team",
            'total_tournaments': "SELECT COUNT(*) FROM Tournament",
            'total_matches': "SELECT COUNT(*) FROM Match",
            'total_sports': "SELECT COUNT(*) FROM Sport",
            'total_equipment': "SELECT COUNT(*) FROM Equipment",
            'unread_reminders': "SELECT COUNT(*) FROM Reminder WHERE IsRead=0",
            'active_injuries': "SELECT COUNT(*) FROM InjuryRecord WHERE IsRecovered=0",
            'pending_returns': "SELECT COUNT(*) FROM EquipmentIssue WHERE IsReturned=0",
        }
        for key, query in queries.items():
            try:
                result, err = self.db.execute_scalar(query)
                stats[key] = int(result) if result is not None else 0
            except:
                stats[key] = 0
        return stats

    def get_sports_distribution(self):
        query = """
            SELECT s.SportName, COUNT(DISTINCT tp.StudentID) AS PlayerCount
            FROM Sport s
            LEFT JOIN Team t ON s.SportID = t.SportID
            LEFT JOIN TeamPlayer tp ON t.TeamID = tp.TeamID
            GROUP BY s.SportName
            ORDER BY PlayerCount DESC
        """
        return self.db.execute_query(query)

    def get_recent_matches(self, limit=5):
        query = f"""
            SELECT TOP {limit} 
                   CONVERT(varchar, m.MatchDate, 23) AS MatchDate,
                   ht.TeamName AS HomeTeam, 
                   at2.TeamName AS AwayTeam,
                   ISNULL(m.HomeTeamScore, 0) AS HomeScore, 
                   ISNULL(m.AwayTeamScore, 0) AS AwayScore, 
                   ISNULL(m.Status, 'N/A') AS Status,
                   t.TournamentName
            FROM Match m
            JOIN Team ht ON m.HomeTeamID = ht.TeamID
            JOIN Team at2 ON m.AwayTeamID = at2.TeamID
            JOIN Tournament t ON m.TournamentID = t.TournamentID
            ORDER BY m.MatchDate DESC
        """
        return self.db.execute_query(query)

    def get_tournament_status_summary(self):
        query = """
            SELECT ISNULL(Status, 'Unknown') AS Status, COUNT(*) AS Count
            FROM Tournament
            GROUP BY Status
            ORDER BY Count DESC
        """
        return self.db.execute_query(query)

    def get_department_performance(self):
        query = """
            SELECT d.DepartmentName,
                   SUM(ISNULL(dr.TotalWins, 0)) AS TotalWins,
                   SUM(ISNULL(dr.TotalLosses, 0)) AS TotalLosses,
                   SUM(ISNULL(dr.TotalPoints, 0)) AS TotalPoints
            FROM DepartmentRanking dr
            JOIN Department d ON dr.DepartmentID = d.DepartmentID
            GROUP BY d.DepartmentName
            ORDER BY TotalPoints DESC
        """
        return self.db.execute_query(query)

    def get_top_scorers(self, limit=5):
        query = f"""
            SELECT TOP {limit} s.FullName AS PlayerName,
                   SUM(ISNULL(mp.GoalsScored, 0)) AS TotalGoals,
                   SUM(ISNULL(mp.Assists, 0)) AS TotalAssists
            FROM MatchPerformance mp
            JOIN Student s ON mp.StudentID = s.StudentID
            GROUP BY s.FullName
            ORDER BY TotalGoals DESC
        """
        return self.db.execute_query(query)

    def get_attendance_summary(self):
        query = """
            SELECT ISNULL(Status, 'Unknown') AS Status, COUNT(*) AS Count
            FROM PracticeAttendance
            GROUP BY Status
        """
        return self.db.execute_query(query)

    def get_equipment_status(self):
        query = """
            SELECT ISNULL(e.Condition, 'Unknown') AS Condition, 
                   COUNT(*) AS Count, 
                   SUM(ISNULL(e.AvailableQty, 0)) AS TotalAvailable
            FROM Equipment e
            GROUP BY e.Condition
            ORDER BY Count DESC
        """
        return self.db.execute_query(query)

    def get_expense_by_category(self):
        query = """
            SELECT ISNULL(Category, 'Other') AS Category, 
                   SUM(Amount) AS TotalAmount
            FROM Expense
            GROUP BY Category
            ORDER BY TotalAmount DESC
        """
        return self.db.execute_query(query)


# ============================================================
# SERVICE LOCATOR
# ============================================================

class ServiceLocator:
    """Central access point for all backend services"""

    def __init__(self):
        self._services = {}

    def _get_service(self, key, cls):
        if key not in self._services:
            self._services[key] = cls()
        return self._services[key]

    @property
    def departments(self):
        return self._get_service('departments', DepartmentRepository)

    @property
    def sports(self):
        return self._get_service('sports', SportRepository)

    @property
    def venues(self):
        return self._get_service('venues', VenueRepository)

    @property
    def semesters(self):
        return self._get_service('semesters', SemesterRepository)

    @property
    def students(self):
        return self._get_service('students', StudentRepository)

    @property
    def coaches(self):
        return self._get_service('coaches', CoachRepository)

    @property
    def teams(self):
        return self._get_service('teams', TeamRepository)

    @property
    def equipment(self):
        return self._get_service('equipment', EquipmentRepository)

    @property
    def tournaments(self):
        return self._get_service('tournaments', TournamentRepository)

    @property
    def matches(self):
        return self._get_service('matches', MatchRepository)

    @property
    def practice_sessions(self):
        return self._get_service('practice_sessions', PracticeSessionRepository)

    @property
    def injuries(self):
        return self._get_service('injuries', InjuryRepository)

    @property
    def ratings(self):
        return self._get_service('ratings', PlayerRatingRepository)

    @property
    def points_table(self):
        return self._get_service('points_table', PointsTableRepository)

    @property
    def reminders(self):
        return self._get_service('reminders', ReminderRepository)

    @property
    def rankings(self):
        return self._get_service('rankings', DepartmentRankingRepository)

    @property
    def dashboard(self):
        return self._get_service('dashboard', DashboardService)


# ============================================================
# Global service locator - NO database import at module level
# ============================================================
services = ServiceLocator()