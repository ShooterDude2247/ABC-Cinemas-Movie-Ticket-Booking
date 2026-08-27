# ABC CINEMAS - Booking Module
# =============================
# Handles ticket booking operations

from database import Database
from utils import Utils
from seats import Seats
from snacks import Snacks
from shows import Shows

class Booking:
    """
    Booking class for managing movie ticket bookings.
    """
    
    @staticmethod
    def create_booking(user_id, show_id, seat_ids, snack_items, payment_method):
        """
        Create a new booking with seats and snacks.
        
        Args:
            user_id (int): User ID
            show_id (int): Show ID
            seat_ids (list): List of seat IDs
            snack_items (list): List of (snack_id, quantity) tuples
            payment_method (str): Payment method
        
        Returns:
            tuple: (success: bool, booking_data: dict or error_message: str)
        """
        if not seat_ids:
            return False, "Please select at least one seat."
        
        # Get show details
        show = Shows.get_show_by_id(show_id)
        if not show:
            return False, "Show not found."
        
        # Verify seats are available
        if not Seats.check_seats_available(show_id, seat_ids):
            return False, "One or more selected seats have been booked. Please select different seats."
        
        try:
            # Calculate amounts
            ticket_price = float(show['ticket_price'])
            ticket_amount = ticket_price * len(seat_ids)
            snack_amount = Snacks.calculate_snack_total(snack_items)
            total_amount = ticket_amount + snack_amount
            
            # Generate booking code
            booking_code = Utils.generate_booking_code()
            
            # Start transaction
            # 1. Insert booking record
            booking_query = """
                INSERT INTO bookings (booking_code, user_id, show_id, 
                                    total_ticket_amount, total_snack_amount, 
                                    total_amount, payment_method, payment_status)
                VALUES (%s, %s, %s, %s, %s, %s, %s, 'paid')
            """
            booking_id = Database.insert_data(
                booking_query,
                (booking_code, user_id, show_id, ticket_amount, snack_amount, total_amount, payment_method)
            )
            
            if booking_id <= 0:
                return False, "Failed to create booking."
            
            # 2. Insert booking seats
            for seat_id in seat_ids:
                seat_booking_query = """
                    INSERT INTO booking_seats (booking_id, seat_id)
                    VALUES (%s, %s)
                """
                seat_result = Database.insert_data(seat_booking_query, (booking_id, seat_id))
                if seat_result <= 0:
                    # Rollback by deleting the booking
                    Database.delete_data("DELETE FROM bookings WHERE booking_id = %s", (booking_id,))
                    return False, "Failed to book seats."
            
            # 3. Book seats in seat_bookings table
            if not Seats.book_seats(show_id, booking_id, seat_ids):
                Database.delete_data("DELETE FROM bookings WHERE booking_id = %s", (booking_id,))
                return False, "Failed to reserve seats."
            
            # 4. Insert booking snacks
            for snack_id, quantity in snack_items:
                snack = Snacks.get_snack_by_id(snack_id)
                if snack:
                    snack_query = """
                        INSERT INTO booking_snacks (booking_id, snack_id, quantity, price_at_booking)
                        VALUES (%s, %s, %s, %s)
                    """
                    snack_result = Database.insert_data(
                        snack_query,
                        (booking_id, snack_id, quantity, snack['price'])
                    )
                    if snack_result <= 0:
                        Database.delete_data("DELETE FROM bookings WHERE booking_id = %s", (booking_id,))
                        return False, "Failed to add snacks to booking."
            
            # 5. Update available seats in shows table
            Shows.update_available_seats(show_id, len(seat_ids))
            
            return True, {
                'booking_id': booking_id,
                'booking_code': booking_code,
                'user_id': user_id,
                'show_id': show_id,
                'seats': seat_ids,
                'snacks': snack_items,
                'ticket_amount': ticket_amount,
                'snack_amount': snack_amount,
                'total_amount': total_amount,
                'payment_method': payment_method
            }
        
        except Exception as e:
            print(f"Booking Error: {e}")
            return False, f"Booking failed: {str(e)}"
    
    @staticmethod
    def get_booking_by_code(booking_code):
        """
        Get booking details by booking code.
        
        Args:
            booking_code (str): Booking code
        
        Returns:
            dict: Booking details or None
        """
        query = """
            SELECT b.booking_id, b.booking_code, b.user_id, b.show_id,
                   b.booking_date, b.total_ticket_amount, b.total_snack_amount,
                   b.total_amount, b.payment_method, b.payment_status
            FROM bookings b
            WHERE b.booking_code = %s
        """
        return Database.execute_query(query, (booking_code,), fetch_one=True, dictionary=True)
    
    @staticmethod
    def get_user_bookings(user_id):
        """
        Get all bookings for a user.
        
        Args:
            user_id (int): User ID
        
        Returns:
            list: List of booking dictionaries
        """
        query = """
            SELECT b.booking_id, b.booking_code, b.show_id, b.booking_date,
                   b.total_ticket_amount, b.total_snack_amount, b.total_amount,
                   b.payment_status, m.title as movie_title, s.show_date, s.show_time
            FROM bookings b
            JOIN shows s ON b.show_id = s.show_id
            JOIN movies m ON s.movie_id = m.movie_id
            WHERE b.user_id = %s
            ORDER BY b.booking_date DESC
        """
        return Database.execute_query(query, (user_id,), fetch_all=True, dictionary=True)
    
    @staticmethod
    def get_booking_details(booking_id):
        """
        Get complete booking details including seats and snacks.
        
        Args:
            booking_id (int): Booking ID
        
        Returns:
            dict: Complete booking information
        """
        # Get booking
        booking_query = """
            SELECT b.booking_id, b.booking_code, b.user_id, b.show_id,
                   b.booking_date, b.total_ticket_amount, b.total_snack_amount,
                   b.total_amount, b.payment_method, b.payment_status,
                   m.title as movie_title, m.poster_path, s.show_date, s.show_time,
                   s.ticket_price, u.full_name, u.email, u.phone
            FROM bookings b
            JOIN shows s ON b.show_id = s.show_id
            JOIN movies m ON s.movie_id = m.movie_id
            JOIN users u ON b.user_id = u.user_id
            WHERE b.booking_id = %s
        """
        booking = Database.execute_query(booking_query, (booking_id,), fetch_one=True, dictionary=True)
        
        if not booking:
            return None
        
        # Get seats
        seats = Seats.get_seats_by_booking(booking_id)
        booking['seats'] = seats
        
        # Get snacks
        snacks_query = """
            SELECT bs.booking_snack_id, s.snack_name, bs.quantity, bs.price_at_booking
            FROM booking_snacks bs
            JOIN snacks s ON bs.snack_id = s.snack_id
            WHERE bs.booking_id = %s
        """
        snacks = Database.execute_query(snacks_query, (booking_id,), fetch_all=True, dictionary=True)
        booking['snacks'] = snacks if snacks else []
        
        return booking
    
    @staticmethod
    def get_all_bookings():
        """
        Get all bookings (Admin function).
        
        Returns:
            list: List of all bookings
        """
        query = """
            SELECT b.booking_id, b.booking_code, b.user_id, b.show_id,
                   b.booking_date, b.total_ticket_amount, b.total_snack_amount,
                   b.total_amount, b.payment_status,
                   m.title as movie_title, s.show_date, s.show_time,
                   u.full_name, u.username
            FROM bookings b
            JOIN shows s ON b.show_id = s.show_id
            JOIN movies m ON s.movie_id = m.movie_id
            JOIN users u ON b.user_id = u.user_id
            ORDER BY b.booking_date DESC
        """
        return Database.execute_query(query, fetch_all=True, dictionary=True)
    
    @staticmethod
    def search_bookings(search_term):
        """
        Search bookings by booking code, customer name, or movie title (Admin).
        
        Args:
            search_term (str): Search query
        
        Returns:
            list: List of matching bookings
        """
        query = """
            SELECT b.booking_id, b.booking_code, b.user_id, b.show_id,
                   b.booking_date, b.total_ticket_amount, b.total_snack_amount,
                   b.total_amount, b.payment_status,
                   m.title as movie_title, s.show_date, s.show_time,
                   u.full_name, u.username
            FROM bookings b
            JOIN shows s ON b.show_id = s.show_id
            JOIN movies m ON s.movie_id = m.movie_id
            JOIN users u ON b.user_id = u.user_id
            WHERE b.booking_code LIKE %s OR u.full_name LIKE %s OR u.username LIKE %s OR m.title LIKE %s
            ORDER BY b.booking_date DESC
        """
        search_pattern = f"%{search_term}%"
        return Database.execute_query(
            query,
            (search_pattern, search_pattern, search_pattern, search_pattern),
            fetch_all=True,
            dictionary=True
        )
    
    @staticmethod
    def get_admin_statistics():
        """
        Get admin dashboard statistics.
        
        Returns:
            dict: Statistics dictionary
        """
        stats = {}
        
        # Total movies
        query = "SELECT COUNT(*) as count FROM movies WHERE status = 'active'"
        result = Database.execute_query(query, fetch_one=True, dictionary=True)
        stats['total_movies'] = result['count'] if result else 0
        
        # Total shows
        query = "SELECT COUNT(*) as count FROM shows WHERE status = 'active'"
        result = Database.execute_query(query, fetch_one=True, dictionary=True)
        stats['total_shows'] = result['count'] if result else 0
        
        # Total users
        query = "SELECT COUNT(*) as count FROM users"
        result = Database.execute_query(query, fetch_one=True, dictionary=True)
        stats['total_users'] = result['count'] if result else 0
        
        # Total bookings
        query = "SELECT COUNT(*) as count FROM bookings"
        result = Database.execute_query(query, fetch_one=True, dictionary=True)
        stats['total_bookings'] = result['count'] if result else 0
        
        # Total revenue
        query = "SELECT SUM(total_amount) as total FROM bookings"
        result = Database.execute_query(query, fetch_one=True, dictionary=True)
        stats['total_revenue'] = result['total'] if result and result['total'] else 0.00
        
        return stats
