# ABC CINEMAS - Snacks Module
# ============================
# Handles snack/food management

from database import Database

class Snacks:
    """
    Snacks class for managing food and beverage items.
    """
    
    @staticmethod
    def get_all_snacks():
        """
        Get all active snacks.
        
        Returns:
            list: List of snack dictionaries
        """
        query = """
            SELECT snack_id, snack_name, price, available_quantity, status
            FROM snacks
            WHERE status = 'active'
            ORDER BY snack_name
        """
        return Database.execute_query(query, fetch_all=True, dictionary=True)
    
    @staticmethod
    def get_snack_by_id(snack_id):
        """
        Get a specific snack by ID.
        
        Args:
            snack_id (int): Snack ID
        
        Returns:
            dict: Snack details or None
        """
        query = """
            SELECT snack_id, snack_name, price, available_quantity, status
            FROM snacks
            WHERE snack_id = %s AND status = 'active'
        """
        return Database.execute_query(query, (snack_id,), fetch_one=True, dictionary=True)
    
    @staticmethod
    def add_snack(snack_name, price, available_quantity):
        """
        Add a new snack (Admin function).
        
        Args:
            snack_name (str): Snack name
            price (float): Price
            available_quantity (int): Available stock
        
        Returns:
            tuple: (success: bool, snack_id: int or message: str)
        """
        if not snack_name or not price or available_quantity is None:
            return False, "All fields are required."
        
        try:
            price = float(price)
            available_quantity = int(available_quantity)
            
            if price <= 0:
                return False, "Price must be greater than 0."
            if available_quantity < 0:
                return False, "Quantity cannot be negative."
        except ValueError:
            return False, "Invalid price or quantity."
        
        query = """
            INSERT INTO snacks (snack_name, price, available_quantity, status)
            VALUES (%s, %s, %s, 'active')
        """
        snack_id = Database.insert_data(query, (snack_name, price, available_quantity))
        
        if snack_id > 0:
            return True, snack_id
        else:
            return False, "Failed to add snack."
    
    @staticmethod
    def update_snack(snack_id, snack_name, price, available_quantity):
        """
        Update snack details (Admin function).
        
        Args:
            snack_id (int): Snack ID
            snack_name (str): Snack name
            price (float): Price
            available_quantity (int): Available stock
        
        Returns:
            tuple: (success: bool, message: str)
        """
        if not snack_name or not price or available_quantity is None:
            return False, "All fields are required."
        
        try:
            price = float(price)
            available_quantity = int(available_quantity)
            
            if price <= 0:
                return False, "Price must be greater than 0."
            if available_quantity < 0:
                return False, "Quantity cannot be negative."
        except ValueError:
            return False, "Invalid price or quantity."
        
        query = """
            UPDATE snacks
            SET snack_name = %s, price = %s, available_quantity = %s
            WHERE snack_id = %s
        """
        rows = Database.update_data(query, (snack_name, price, available_quantity, snack_id))
        
        if rows > 0:
            return True, "Snack updated successfully."
        else:
            return False, "Failed to update snack."
    
    @staticmethod
    def delete_snack(snack_id):
        """
        Delete a snack (Admin function).
        
        Args:
            snack_id (int): Snack ID
        
        Returns:
            tuple: (success: bool, message: str)
        """
        # Soft delete by marking as inactive
        query = "UPDATE snacks SET status = 'inactive' WHERE snack_id = %s"
        rows = Database.update_data(query, (snack_id,))
        
        if rows > 0:
            return True, "Snack deleted successfully."
        else:
            return False, "Failed to delete snack."
    
    @staticmethod
    def check_availability(snack_id, quantity):
        """
        Check if snack is available in requested quantity.
        
        Args:
            snack_id (int): Snack ID
            quantity (int): Requested quantity
        
        Returns:
            bool: True if available, False otherwise
        """
        query = "SELECT available_quantity FROM snacks WHERE snack_id = %s AND status = 'active'"
        result = Database.execute_query(query, (snack_id,), fetch_one=True, dictionary=True)
        
        if result and result['available_quantity'] >= quantity:
            return True
        return False
    
    @staticmethod
    def calculate_snack_total(snack_items):
        """
        Calculate total snack amount for a booking.
        
        Args:
            snack_items (list): List of (snack_id, quantity) tuples
        
        Returns:
            float: Total snack amount
        """
        total = 0.0
        for snack_id, quantity in snack_items:
            query = "SELECT price FROM snacks WHERE snack_id = %s"
            result = Database.execute_query(query, (snack_id,), fetch_one=True, dictionary=True)
            if result:
                total += result['price'] * quantity
        
        return total
