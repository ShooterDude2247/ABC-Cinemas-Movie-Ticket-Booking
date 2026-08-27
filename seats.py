# ABC CINEMAS - Seats Module
# ===========================
# Handles theatre seating and seat management

from database import Database

class Seats:
    """
    Seats class for managing theatre seating.
    """
    
    @staticmethod
    def get_all_seats():
        """
        Get all theatre seats.
        
        Returns:
            list: List of seat dictionaries
        """
        query = """
            SELECT seat_id, row_name, seat_number
            FROM seats
            ORDER BY row_name, seat_number
        """
        return Database.execute_query(query, fetch_all=True, dictionary=True)
    
    @staticmethod
    def get_seat_by_position(row_name, seat_number):
        """
        Get seat ID by row and seat number.
        
        Args:
            row_name (str): Row letter (A-F)
            seat_number (int): Seat number (1-10)
        
        Returns:
            dict: Seat details or None
        """
        query = """
            SELECT seat_id, row_name, seat_number
            FROM seats
            WHERE row_name = %s AND seat_number = %s
        """
        return Database.execute_query(query, (row_name, seat_number), fetch_one=True, dictionary=True)
    
    @staticmethod
    def get_booked_seats_for_show(show_id):
        """
        Get all booked seats for a specific show.
        
        Args:
            show_id (int): Show ID
        
        Returns:
            list: List of booked seat IDs
        """
        query = """
            SELECT DISTINCT s.seat_id, s.row_name, s.seat_number
            FROM seat_bookings sb
            JOIN seats s ON sb.seat_id = s.seat_id
            WHERE sb.show_id = %s
        """
        results = Database.execute_query(query, (show_id,), fetch_all=True, dictionary=True)
        return results if results else []
    
    @staticmethod
    def get_available_seats_for_show(show_id):
        """
        Get all available seats for a specific show.
        
        Args:
            show_id (int): Show ID
        
        Returns:
            list: List of available seat IDs
        """
        query = """
            SELECT s.seat_id, s.row_name, s.seat_number
            FROM seats s
            WHERE s.seat_id NOT IN (
                SELECT seat_id FROM seat_bookings WHERE show_id = %s
            )
            ORDER BY s.row_name, s.seat_number
        """
        return Database.execute_query(query, (show_id,), fetch_all=True, dictionary=True)
    
    @staticmethod
    def check_seats_available(show_id, seat_ids):
        """
        Check if selected seats are still available.
        
        Args:
            show_id (int): Show ID
            seat_ids (list): List of seat IDs to check
        
        Returns:
            bool: True if all seats available, False otherwise
        """
        if not seat_ids:
            return False
        
        placeholders = ','.join(['%s'] * len(seat_ids))
        query = f"""
            SELECT COUNT(*) as booked_count
            FROM seat_bookings
            WHERE show_id = %s AND seat_id IN ({placeholders})
        """
        params = [show_id] + seat_ids
        result = Database.execute_query(query, tuple(params), fetch_one=True, dictionary=True)
        
        # If no seats are booked, all are available
        return result['booked_count'] == 0 if result else False
    
    @staticmethod
    def book_seats(show_id, booking_id, seat_ids):
        """
        Book seats for a show.
        
        Args:
            show_id (int): Show ID
            booking_id (int): Booking ID
            seat_ids (list): List of seat IDs to book
        
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            # First verify all seats are available
            if not Seats.check_seats_available(show_id, seat_ids):
                return False
            
            # Insert seat bookings
            query = """
                INSERT INTO seat_bookings (show_id, seat_id, booking_id)
                VALUES (%s, %s, %s)
            """
            
            for seat_id in seat_ids:
                result = Database.insert_data(query, (show_id, seat_id, booking_id))
                if result <= 0:
                    return False
            
            return True
        except Exception as e:
            print(f"Error booking seats: {e}")
            return False
    
    @staticmethod
    def release_seats(booking_id):
        """
        Release seats from a booking (in case of cancellation).
        
        Args:
            booking_id (int): Booking ID
        
        Returns:
            bool: True if successful
        """
        query = "DELETE FROM seat_bookings WHERE booking_id = %s"
        rows = Database.delete_data(query, (booking_id,))
        return rows >= 0
    
    @staticmethod
    def get_seat_by_id(seat_id):
        """
        Get seat details by seat ID.
        
        Args:
            seat_id (int): Seat ID
        
        Returns:
            dict: Seat details or None
        """
        query = """
            SELECT seat_id, row_name, seat_number
            FROM seats
            WHERE seat_id = %s
        """
        return Database.execute_query(query, (seat_id,), fetch_one=True, dictionary=True)
    
    @staticmethod
    def get_seats_by_booking(booking_id):
        """
        Get all seats for a specific booking.
        
        Args:
            booking_id (int): Booking ID
        
        Returns:
            list: List of seat dictionaries
        """
        query = """
            SELECT s.seat_id, s.row_name, s.seat_number
            FROM booking_seats bs
            JOIN seats s ON bs.seat_id = s.seat_id
            WHERE bs.booking_id = %s
            ORDER BY s.row_name, s.seat_number
        """
        return Database.execute_query(query, (booking_id,), fetch_all=True, dictionary=True)
    
    @staticmethod
    def get_seat_layout():
        """
        Get theatre seat layout (all seats organized by row).
        
        Returns:
            dict: Seats organized by row
        """
        seats = Seats.get_all_seats()
        layout = {}
        
        for seat in seats:
            row = seat['row_name']
            if row not in layout:
                layout[row] = []
            layout[row].append(seat)
        
        # Sort seats in each row by number
        for row in layout:
            layout[row].sort(key=lambda x: x['seat_number'])
        
        return layout
