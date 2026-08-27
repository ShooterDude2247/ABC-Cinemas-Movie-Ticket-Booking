# ABC CINEMAS - Shows Module
# ===========================
# Handles show management and retrieval

from database import Database
from datetime import datetime

class Shows:
    """
    Shows class for managing movie shows.
    """
    
    @staticmethod
    def get_shows_by_movie(movie_id):
        """
        Get all shows for a specific movie.
        
        Args:
            movie_id (int): Movie ID
        
        Returns:
            list: List of shows
        """
        query = """
            SELECT show_id, movie_id, show_date, show_time, ticket_price,
                   total_seats, available_seats, status
            FROM shows
            WHERE movie_id = %s AND status = 'active'
            ORDER BY show_date, show_time
        """
        return Database.execute_query(query, (movie_id,), fetch_all=True, dictionary=True)
    
    @staticmethod
    def get_shows_by_date(movie_id, show_date):
        """
        Get shows for a movie on a specific date.
        
        Args:
            movie_id (int): Movie ID
            show_date (str): Date in YYYY-MM-DD format
        
        Returns:
            list: List of shows on that date
        """
        query = """
            SELECT show_id, movie_id, show_date, show_time, ticket_price,
                   total_seats, available_seats, status
            FROM shows
            WHERE movie_id = %s AND show_date = %s AND status = 'active'
            ORDER BY show_time
        """
        return Database.execute_query(query, (movie_id, show_date), fetch_all=True, dictionary=True)
    
    @staticmethod
    def get_show_by_id(show_id):
        """
        Get show details by ID.
        
        Args:
            show_id (int): Show ID
        
        Returns:
            dict: Show details or None
        """
        query = """
            SELECT show_id, movie_id, show_date, show_time, ticket_price,
                   total_seats, available_seats, status
            FROM shows
            WHERE show_id = %s
        """
        return Database.execute_query(query, (show_id,), fetch_one=True, dictionary=True)
    
    @staticmethod
    def get_available_dates(movie_id):
        """
        Get all available dates for a movie.
        
        Args:
            movie_id (int): Movie ID
        
        Returns:
            list: List of dates
        """
        query = """
            SELECT DISTINCT show_date
            FROM shows
            WHERE movie_id = %s AND status = 'active'
            ORDER BY show_date
        """
        results = Database.execute_query(query, (movie_id,), fetch_all=True, dictionary=True)
        return [r['show_date'] for r in results] if results else []
    
    @staticmethod
    def add_show(movie_id, show_date, show_time, ticket_price):
        """
        Add a new show (Admin function).
        
        Args:
            movie_id (int): Movie ID
            show_date (str): Date in YYYY-MM-DD format
            show_time (str): Time in HH:MM:SS format
            ticket_price (float): Ticket price
        
        Returns:
            tuple: (success: bool, show_id: int or message: str)
        """
        if not movie_id or not show_date or not show_time or not ticket_price:
            return False, "All fields are required."
        
        try:
            ticket_price = float(ticket_price)
            if ticket_price <= 0:
                return False, "Ticket price must be greater than 0."
        except ValueError:
            return False, "Invalid ticket price."
        
        # Check if movie exists
        query = "SELECT movie_id FROM movies WHERE movie_id = %s"
        if not Database.execute_query(query, (movie_id,), fetch_one=True):
            return False, "Movie not found."
        
        # Check for duplicate show
        query = "SELECT show_id FROM shows WHERE movie_id = %s AND show_date = %s AND show_time = %s"
        if Database.execute_query(query, (movie_id, show_date, show_time), fetch_one=True):
            return False, "Show already exists for this date and time."
        
        query = """
            INSERT INTO shows (movie_id, show_date, show_time, ticket_price, 
                             total_seats, available_seats, status)
            VALUES (%s, %s, %s, %s, 60, 60, 'active')
        """
        show_id = Database.insert_data(query, (movie_id, show_date, show_time, ticket_price))
        
        if show_id > 0:
            return True, show_id
        else:
            return False, "Failed to add show."
    
    @staticmethod
    def update_show(show_id, show_date, show_time, ticket_price):
        """
        Update show details (Admin function).
        
        Args:
            show_id (int): Show ID
            show_date (str): Date
            show_time (str): Time
            ticket_price (float): Ticket price
        
        Returns:
            tuple: (success: bool, message: str)
        """
        if not show_date or not show_time or not ticket_price:
            return False, "All fields are required."
        
        try:
            ticket_price = float(ticket_price)
            if ticket_price <= 0:
                return False, "Ticket price must be greater than 0."
        except ValueError:
            return False, "Invalid ticket price."
        
        query = """
            UPDATE shows
            SET show_date = %s, show_time = %s, ticket_price = %s
            WHERE show_id = %s
        """
        rows = Database.update_data(query, (show_date, show_time, ticket_price, show_id))
        
        if rows > 0:
            return True, "Show updated successfully."
        else:
            return False, "Failed to update show."
    
    @staticmethod
    def delete_show(show_id):
        """
        Delete a show (Admin function).
        
        Args:
            show_id (int): Show ID
        
        Returns:
            tuple: (success: bool, message: str)
        """
        # Check if show has bookings
        query = "SELECT COUNT(*) as count FROM bookings WHERE show_id = %s"
        result = Database.execute_query(query, (show_id,), fetch_one=True, dictionary=True)
        
        if result and result['count'] > 0:
            return False, "Cannot delete show with existing bookings."
        
        # Soft delete
        query = "UPDATE shows SET status = 'inactive' WHERE show_id = %s"
        rows = Database.update_data(query, (show_id,))
        
        if rows > 0:
            return True, "Show deleted successfully."
        else:
            return False, "Failed to delete show."
    
    @staticmethod
    def update_available_seats(show_id, seats_to_subtract):
        """
        Update available seats after booking.
        
        Args:
            show_id (int): Show ID
            seats_to_subtract (int): Number of seats booked
        
        Returns:
            bool: Success status
        """
        query = """
            UPDATE shows
            SET available_seats = available_seats - %s
            WHERE show_id = %s AND available_seats >= %s
        """
        rows = Database.update_data(query, (seats_to_subtract, show_id, seats_to_subtract))
        return rows > 0
