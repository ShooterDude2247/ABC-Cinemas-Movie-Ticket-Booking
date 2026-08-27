# ABC CINEMAS - Database Module
# ==============================
# Handles all database connectivity and operations

import mysql.connector
from mysql.connector import Error
import config
from contextlib import contextmanager

class Database:
    """
    Database class for handling MySQL connections and queries.
    Provides a centralized connection management system.
    """
    
    @staticmethod
    def get_connection():
        """
        Create and return a MySQL database connection.
        
        Returns:
            mysql.connector.connection.MySQLConnection or None
        
        Raises:
            Error: If connection fails
        """
        try:
            connection = mysql.connector.connect(**config.DB_CONFIG)
            return connection
        except Error as e:
            print(f"Database Connection Error: {e}")
            return None
    
    @staticmethod
    @contextmanager
    def get_db_cursor(dictionary=False):
        """
        Context manager for database cursor.
        Automatically handles connection and cursor cleanup.
        
        Args:
            dictionary (bool): If True, return results as dictionaries
        
        Yields:
            tuple: (cursor, connection) for use in with statement
        """
        connection = Database.get_connection()
        if not connection:
            raise Exception("Could not connect to database")
        
        cursor = connection.cursor(dictionary=dictionary)
        try:
            yield cursor, connection
        finally:
            cursor.close()
            connection.close()
    
    @staticmethod
    def execute_query(query, params=None, fetch_all=False, fetch_one=False, dictionary=False, commit=False):
        """
        Execute a database query with proper error handling.
        
        Args:
            query (str): SQL query to execute
            params (tuple): Query parameters for parameterized queries
            fetch_all (bool): Fetch all results
            fetch_one (bool): Fetch single result
            dictionary (bool): Return results as dictionaries
            commit (bool): Commit transaction
        
        Returns:
            Results from query or None on error
        """
        try:
            with Database.get_db_cursor(dictionary=dictionary) as (cursor, connection):
                if params:
                    cursor.execute(query, params)
                else:
                    cursor.execute(query)
                
                if fetch_all:
                    return cursor.fetchall()
                elif fetch_one:
                    return cursor.fetchone()
                elif commit:
                    connection.commit()
                    return cursor.rowcount
                else:
                    return cursor.fetchall()
        
        except Error as e:
            print(f"Database Query Error: {e}")
            return None
    
    @staticmethod
    def insert_data(query, params):
        """
        Insert data into database.
        
        Args:
            query (str): INSERT query
            params (tuple): Data to insert
        
        Returns:
            int: Last inserted ID or -1 on error
        """
        try:
            with Database.get_db_cursor() as (cursor, connection):
                cursor.execute(query, params)
                connection.commit()
                return cursor.lastrowid
        except Error as e:
            print(f"Insert Error: {e}")
            return -1
    
    @staticmethod
    def update_data(query, params):
        """
        Update data in database.
        
        Args:
            query (str): UPDATE query
            params (tuple): Data to update
        
        Returns:
            int: Number of rows affected or -1 on error
        """
        try:
            with Database.get_db_cursor() as (cursor, connection):
                cursor.execute(query, params)
                connection.commit()
                return cursor.rowcount
        except Error as e:
            print(f"Update Error: {e}")
            return -1
    
    @staticmethod
    def delete_data(query, params):
        """
        Delete data from database.
        
        Args:
            query (str): DELETE query
            params (tuple): Condition parameters
        
        Returns:
            int: Number of rows affected or -1 on error
        """
        try:
            with Database.get_db_cursor() as (cursor, connection):
                cursor.execute(query, params)
                connection.commit()
                return cursor.rowcount
        except Error as e:
            print(f"Delete Error: {e}")
            return -1
    
    @staticmethod
    def transaction(queries_and_params):
        """
        Execute multiple queries in a single transaction.
        Rolls back if any query fails.
        
        Args:
            queries_and_params (list): List of (query, params) tuples
        
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            with Database.get_db_cursor() as (cursor, connection):
                for query, params in queries_and_params:
                    if params:
                        cursor.execute(query, params)
                    else:
                        cursor.execute(query)
                
                connection.commit()
                return True
        except Error as e:
            print(f"Transaction Error: {e}")
            return False

# Test database connection on module import
def test_connection():
    """Test if database connection works"""
    conn = Database.get_connection()
    if conn:
        conn.close()
        return True
    return False
