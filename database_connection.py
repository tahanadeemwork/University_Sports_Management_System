import pyodbc
import pandas as pd
from contextlib import contextmanager


class DatabaseConnection:
    """
    Singleton Database Connection Class for SQL Server (SSMS)
    Handles all database connectivity for UniversitySportsDB
    """

    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(DatabaseConnection, cls).__new__(cls)
            cls._instance._initialized = False
            cls._instance._connection = None  # ← fixes the AttributeError
        return cls._instance

    def __init__(self):
        if self._initialized:
            return

        self.server = 'DESKTOP-7DVHREP'
        self.database = 'UniversitySportsDB'
        self.driver = '{ODBC Driver 17 for SQL Server}'
        self.trusted_connection = 'yes'
        self.username = ''
        self.password = ''

        self._connection = None
        self._initialized = True

    def get_connection_string(self):
        """Build and return the connection string"""
        if self.trusted_connection.lower() == 'yes':
            conn_str = (
                f"DRIVER={self.driver};"
                f"SERVER={self.server};"
                f"DATABASE={self.database};"
                f"Trusted_Connection={self.trusted_connection};"
            )
        else:
            conn_str = (
                f"DRIVER={self.driver};"
                f"SERVER={self.server};"
                f"DATABASE={self.database};"
                f"UID={self.username};"
                f"PWD={self.password};"
            )
        return conn_str

    def connect(self):
        """Establish database connection"""
        try:
            if self._connection is not None:
                try:
                    self._connection.close()
                except:
                    pass
                self._connection = None

            self._connection = pyodbc.connect(
                self.get_connection_string(),
                timeout=30
            )
            self._connection.autocommit = False
            return True, "Connection successful"
        except pyodbc.Error as e:
            self._connection = None
            error_msg = str(e)
            return False, f"Connection failed: {error_msg}"
        except Exception as e:
            self._connection = None
            return False, f"Unexpected error: {str(e)}"

    def disconnect(self):
        """Close database connection"""
        if self._connection:
            try:
                self._connection.close()
                self._connection = None
                return True, "Disconnected successfully"
            except Exception as e:
                self._connection = None
                return False, f"Error disconnecting: {str(e)}"
        return True, "No active connection"

    def is_connected(self):
        """Check if connection is active"""
        if self._connection is None:
            return False
        try:
            cursor = self._connection.cursor()
            cursor.execute("SELECT 1")
            cursor.close()
            return True
        except:
            self._connection = None
            return False

    def ensure_connected(self):
        """Ensure connection is active, reconnect if needed"""
        if not self.is_connected():
            success, msg = self.connect()
            return success, msg
        return True, "Already connected"

    @contextmanager
    def get_cursor(self):
        """Context manager for database cursor"""
        success, msg = self.ensure_connected()
        if not success:
            raise ConnectionError(f"Cannot connect to database: {msg}")

        cursor = self._connection.cursor()
        try:
            yield cursor
            self._connection.commit()
        except Exception as e:
            try:
                self._connection.rollback()
            except:
                pass
            raise e
        finally:
            try:
                cursor.close()
            except:
                pass

    def execute_query(self, query, params=None):
        """
        Execute a SELECT query and return results as DataFrame
        Returns: (DataFrame or None, error_message or None)
        """
        try:
            success, msg = self.ensure_connected()
            if not success:
                return None, msg

            cursor = self._connection.cursor()
            try:
                if params:
                    cursor.execute(query, params)
                else:
                    cursor.execute(query)

                columns = [column[0] for column in cursor.description]
                rows = cursor.fetchall()
                df = pd.DataFrame.from_records(rows, columns=columns)
                return df, None
            finally:
                cursor.close()

        except pyodbc.Error as e:
            return None, f"Database error: {str(e)}"
        except Exception as e:
            return None, f"Error: {str(e)}"

    def execute_non_query(self, query, params=None):
        """
        Execute INSERT, UPDATE, DELETE queries
        Returns: (rows_affected, error_message or None)
        """
        try:
            with self.get_cursor() as cursor:
                if params:
                    cursor.execute(query, params)
                else:
                    cursor.execute(query)
                return cursor.rowcount, None
        except ConnectionError as e:
            return 0, str(e)
        except pyodbc.Error as e:
            return 0, f"Database error: {str(e)}"
        except Exception as e:
            return 0, f"Error: {str(e)}"

    def execute_scalar(self, query, params=None):
        """
        Execute query and return single scalar value
        Returns: (value, error_message or None)
        """
        try:
            success, msg = self.ensure_connected()
            if not success:
                return None, msg

            cursor = self._connection.cursor()
            try:
                if params:
                    cursor.execute(query, params)
                else:
                    cursor.execute(query)
                row = cursor.fetchone()
                if row:
                    return row[0], None
                return None, None
            finally:
                cursor.close()

        except pyodbc.Error as e:
            return None, f"Database error: {str(e)}"
        except Exception as e:
            return None, f"Error: {str(e)}"

    def test_connection(self):
        """Test database connectivity"""
        success, msg = self.connect()
        if success:
            result, err = self.execute_scalar(
                "SELECT COUNT(*) FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_TYPE='BASE TABLE'"
            )
            if err:
                return True, f"Connected but query failed: {err}"
            if result is not None:
                return True, f"Connected! Found {result} tables in {self.database}."
            return True, f"Connected to {self.database} successfully!"
        return False, msg


# ============================================================
# Create the global singleton instance
# ============================================================
db = DatabaseConnection()