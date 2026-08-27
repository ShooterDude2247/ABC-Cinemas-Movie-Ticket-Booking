# ABC CINEMAS - Database Module
# =============================
# Handles all database connections and operations

import mysql.connector
from mysql.connector import Error
import config

class Database:
    """
    Database class for managing MySQL connections and operations.
    """
    
    @staticmethod
    def get_connection():
        """
        Create and return a MySQL database connection.
        
        Returns:
            mysql.connector.MySQLConnection or None
        """
        try:
            connection = mysql.connector.connect(**config.DB_CONFIG)
            if connection.is_connected():
                return connection
        except Error as e:
            print(f"Error connecting to MySQL: {e}")
            return None
    
    @staticmethod
    def execute_query(query, params=None, fetch_one=False, fetch_all=False, dictionary=False):
        """
        Execute a SELECT query and return results.
        
        Args:
            query (str): SQL query to execute
            params (tuple): Query parameters for prepared statement
            fetch_one (bool): Return only one row
            fetch_all (bool): Return all rows
            dictionary (bool): Return results as dictionaries
        
        Returns:
            dict, list, or None depending on parameters
        """
        connection = Database.get_connection()
        if not connection:
            return None
        
        try:
            cursor = connection.cursor(dictionary=dictionary)
            
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            
            if fetch_one:
                result = cursor.fetchone()
            elif fetch_all:
                result = cursor.fetchall()
            else:
                result = None
            
            cursor.close()
            connection.close()
            return result
        
        except Error as e:
            print(f"Query execution error: {e}")
            print(f"Query: {query}")
            return None
        finally:
            if connection.is_connected():
                connection.close()
    
    @staticmethod
    def insert_data(query, params=None):
        """
        Execute an INSERT query.
        
        Args:
            query (str): SQL INSERT query
            params (tuple): Query parameters
        
        Returns:
            int: ID of inserted row, or -1 on error
        """
        connection = Database.get_connection()
        if not connection:
            return -1
        
        try:
            cursor = connection.cursor()
            
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            
            connection.commit()
            inserted_id = cursor.lastrowid
            
            cursor.close()
            return inserted_id
        
        except Error as e:
            print(f"Insert error: {e}")
            print(f"Query: {query}")
            connection.rollback()
            return -1
        finally:
            if connection.is_connected():
                connection.close()
    
    @staticmethod
    def update_data(query, params=None):
        """
        Execute an UPDATE query.
        
        Args:
            query (str): SQL UPDATE query
            params (tuple): Query parameters
        
        Returns:
            int: Number of rows updated, or -1 on error
        """
        connection = Database.get_connection()
        if not connection:
            return -1
        
        try:
            cursor = connection.cursor()
            
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            
            connection.commit()
            rows_affected = cursor.rowcount
            
            cursor.close()
            return rows_affected
        
        except Error as e:
            print(f"Update error: {e}")
            print(f"Query: {query}")
            connection.rollback()
            return -1
        finally:
            if connection.is_connected():
                connection.close()
    
    @staticmethod
    def delete_data(query, params=None):
        """
        Execute a DELETE query.
        
        Args:
            query (str): SQL DELETE query
            params (tuple): Query parameters
        
        Returns:
            int: Number of rows deleted, or -1 on error
        """
        connection = Database.get_connection()
        if not connection:
            return -1
        
        try:
            cursor = connection.cursor()
            
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            
            connection.commit()
            rows_affected = cursor.rowcount
            
            cursor.close()
            return rows_affected
        
        except Error as e:
            print(f"Delete error: {e}")
            print(f"Query: {query}")
            connection.rollback()
            return -1
        finally:
            if connection.is_connected():
                connection.close()
    
    @staticmethod
    def test_connection():
        """
        Test database connection.
        
        Returns:
            bool: True if connection successful, False otherwise
        """
        connection = Database.get_connection()
        if connection and connection.is_connected():
            connection.close()
            print("Database connection successful!")
            return True
        else:
            print("Failed to connect to database.")
            return False
