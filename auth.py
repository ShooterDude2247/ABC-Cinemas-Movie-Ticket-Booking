# ABC CINEMAS - Authentication Module
# ====================================
# Handles user login, registration, and password hashing

import hashlib
import re
from database import Database

class Auth:
    """
    Authentication system for users and admins.
    Handles login, registration, and password verification.
    """
    
    @staticmethod
    def hash_password(password):
        """
        Hash a password using SHA256.
        
        Args:
            password (str): Plain text password
        
        Returns:
            str: Hashed password
        """
        return hashlib.sha256(password.encode()).hexdigest()
    
    @staticmethod
    def validate_email(email):
        """
        Validate email format.
        
        Args:
            email (str): Email to validate
        
        Returns:
            bool: True if valid, False otherwise
        """
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None
    
    @staticmethod
    def validate_phone(phone):
        """
        Validate phone number (Indian format).
        
        Args:
            phone (str): Phone number to validate
        
        Returns:
            bool: True if valid, False otherwise
        """
        # Remove spaces and hyphens
        phone = phone.replace(" ", "").replace("-", "")
        # Check if it's 10 digits and starts with 6-9
        return len(phone) == 10 and phone[0] in '6789' and phone.isdigit()
    
    @staticmethod
    def register_user(full_name, username, email, phone, password, confirm_password):
        """
        Register a new user.
        
        Args:
            full_name (str): User's full name
            username (str): Desired username
            email (str): User's email
            phone (str): User's phone number
            password (str): Desired password
            confirm_password (str): Password confirmation
        
        Returns:
            tuple: (success: bool, message: str)
        """
        # Validation
        if not full_name or not username or not email or not phone or not password:
            return False, "All fields are required."
        
        if len(username) < 3:
            return False, "Username must be at least 3 characters."
        
        if not Auth.validate_email(email):
            return False, "Invalid email format."
        
        if not Auth.validate_phone(phone):
            return False, "Invalid phone number. Enter a 10-digit number."
        
        if len(password) < 6:
            return False, "Password must be at least 6 characters."
        
        if password != confirm_password:
            return False, "Passwords do not match."
        
        # Check for duplicate username
        query = "SELECT user_id FROM users WHERE username = %s"
        result = Database.execute_query(query, (username,), fetch_one=True)
        if result:
            return False, "Username already exists. Please choose another."
        
        # Check for duplicate email
        query = "SELECT user_id FROM users WHERE email = %s"
        result = Database.execute_query(query, (email,), fetch_one=True)
        if result:
            return False, "Email already registered. Please use another email."
        
        # Insert new user
        query = """
            INSERT INTO users (full_name, username, email, phone, password_hash)
            VALUES (%s, %s, %s, %s, %s)
        """
        password_hash = Auth.hash_password(password)
        user_id = Database.insert_data(query, (full_name, username, email, phone, password_hash))
        
        if user_id > 0:
            return True, "Account created successfully!"
        else:
            return False, "Registration failed. Please try again."
    
    @staticmethod
    def login_user(username, password):
        """
        Authenticate a user.
        
        Args:
            username (str): Username or email
            password (str): Password
        
        Returns:
            tuple: (success: bool, user_data: dict or error_message: str)
        """
        if not username or not password:
            return False, "Username and password are required."
        
        # Query user by username or email
        query = """
            SELECT user_id, full_name, username, email, phone, password_hash
            FROM users
            WHERE username = %s OR email = %s
        """
        result = Database.execute_query(query, (username, username), fetch_one=True, dictionary=True)
        
        if not result:
            return False, "Invalid username or password."
        
        # Verify password
        password_hash = Auth.hash_password(password)
        if result['password_hash'] != password_hash:
            return False, "Invalid username or password."
        
        return True, result
    
    @staticmethod
    def login_admin(username, password):
        """
        Authenticate an admin.
        
        Args:
            username (str): Admin username
            password (str): Admin password
        
        Returns:
            tuple: (success: bool, admin_data: dict or error_message: str)
        """
        if not username or not password:
            return False, "Username and password are required."
        
        query = """
            SELECT admin_id, username, full_name, password_hash
            FROM admins
            WHERE username = %s
        """
        result = Database.execute_query(query, (username,), fetch_one=True, dictionary=True)
        
        if not result:
            return False, "Invalid admin credentials."
        
        # Verify password
        password_hash = Auth.hash_password(password)
        if result['password_hash'] != password_hash:
            return False, "Invalid admin credentials."
        
        return True, result
    
    @staticmethod
    def update_user_profile(user_id, full_name, phone, email):
        """
        Update user profile information.
        
        Args:
            user_id (int): User ID
            full_name (str): Updated full name
            phone (str): Updated phone
            email (str): Updated email
        
        Returns:
            tuple: (success: bool, message: str)
        """
        if not Auth.validate_phone(phone):
            return False, "Invalid phone number."
        
        if not Auth.validate_email(email):
            return False, "Invalid email format."
        
        # Check if email is already used by another user
        query = "SELECT user_id FROM users WHERE email = %s AND user_id != %s"
        result = Database.execute_query(query, (email, user_id), fetch_one=True)
        if result:
            return False, "Email already in use."
        
        query = """
            UPDATE users
            SET full_name = %s, phone = %s, email = %s
            WHERE user_id = %s
        """
        rows = Database.update_data(query, (full_name, phone, email, user_id))
        
        if rows > 0:
            return True, "Profile updated successfully."
        else:
            return False, "Failed to update profile."
    
    @staticmethod
    def change_password(user_id, old_password, new_password, confirm_password):
        """
        Change user password.
        
        Args:
            user_id (int): User ID
            old_password (str): Current password
            new_password (str): New password
            confirm_password (str): Confirm new password
        
        Returns:
            tuple: (success: bool, message: str)
        """
        if len(new_password) < 6:
            return False, "New password must be at least 6 characters."
        
        if new_password != confirm_password:
            return False, "New passwords do not match."
        
        # Verify old password
        query = "SELECT password_hash FROM users WHERE user_id = %s"
        result = Database.execute_query(query, (user_id,), fetch_one=True, dictionary=True)
        
        if not result:
            return False, "User not found."
        
        old_hash = Auth.hash_password(old_password)
        if result['password_hash'] != old_hash:
            return False, "Current password is incorrect."
        
        # Update password
        new_hash = Auth.hash_password(new_password)
        query = "UPDATE users SET password_hash = %s WHERE user_id = %s"
        rows = Database.update_data(query, (new_hash, user_id))
        
        if rows > 0:
            return True, "Password changed successfully."
        else:
            return False, "Failed to change password."
