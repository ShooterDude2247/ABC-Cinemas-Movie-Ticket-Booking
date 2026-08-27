# ABC CINEMAS - Utility Functions
# ===============================
# Helper functions for the application

import os
import hashlib
from datetime import datetime
from PIL import Image
import config

class Utils:
    """
    Utility class containing helper functions.
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
    def verify_password(password, hashed_password):
        """
        Verify a password against its hash.
        
        Args:
            password (str): Plain text password
            hashed_password (str): Hashed password from database
        
        Returns:
            bool: True if password matches, False otherwise
        """
        return Utils.hash_password(password) == hashed_password
    
    @staticmethod
    def validate_email(email):
        """
        Validate email format.
        
        Args:
            email (str): Email address
        
        Returns:
            bool: True if valid email format
        """
        import re
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None
    
    @staticmethod
    def validate_phone(phone):
        """
        Validate phone number (10 digits).
        
        Args:
            phone (str): Phone number
        
        Returns:
            bool: True if valid phone format
        """
        import re
        pattern = r'^[0-9]{10}$'
        return re.match(pattern, phone) is not None
    
    @staticmethod
    def validate_password(password):
        """
        Validate password strength.
        
        Args:
            password (str): Password to validate
        
        Returns:
            tuple: (is_valid: bool, message: str)
        """
        if len(password) < config.MIN_PASSWORD_LENGTH:
            return False, f"Password must be at least {config.MIN_PASSWORD_LENGTH} characters long."
        return True, "Password is valid."
    
    @staticmethod
    def format_currency(amount):
        """
        Format amount as Indian currency (₹).
        
        Args:
            amount (float): Amount to format
        
        Returns:
            str: Formatted currency string
        """
        return f"₹{float(amount):.2f}"
    
    @staticmethod
    def format_date(date_obj):
        """
        Format date for display.
        
        Args:
            date_obj (datetime or str): Date to format
        
        Returns:
            str: Formatted date
        """
        if isinstance(date_obj, str):
            try:
                date_obj = datetime.strptime(date_obj, '%Y-%m-%d')
            except:
                return str(date_obj)
        
        return date_obj.strftime('%d-%b-%Y')
    
    @staticmethod
    def format_time(time_obj):
        """
        Format time for display.
        
        Args:
            time_obj (str or time): Time to format
        
        Returns:
            str: Formatted time
        """
        if isinstance(time_obj, str):
            try:
                time_obj = datetime.strptime(time_obj, '%H:%M:%S').time()
            except:
                return str(time_obj)
        
        return time_obj.strftime('%I:%M %p')
    
    @staticmethod
    def generate_booking_code():
        """
        Generate a unique booking code.
        
        Returns:
            str: Booking code (format: ABCYYMMDDxxxxx)
        """
        import random
        timestamp = datetime.now().strftime('%y%m%d')
        random_part = ''.join([str(random.randint(0, 9)) for _ in range(5)])
        return f"ABC{timestamp}{random_part}"
    
    @staticmethod
    def load_image(image_path, width=None, height=None):
        """
        Load and optionally resize an image.
        
        Args:
            image_path (str): Path to image file
            width (int): Target width
            height (int): Target height
        
        Returns:
            PIL.Image or None
        """
        try:
            if not os.path.exists(image_path):
                # Return placeholder if file doesn't exist
                if os.path.exists(config.PLACEHOLDER_POSTER):
                    image_path = config.PLACEHOLDER_POSTER
                else:
                    return None
            
            image = Image.open(image_path)
            
            if width and height:
                image = image.resize((width, height), Image.Resampling.LANCZOS)
            
            return image
        except Exception as e:
            print(f"Error loading image {image_path}: {e}")
            return None
    
    @staticmethod
    def ensure_directory_exists(directory):
        """
        Create directory if it doesn't exist.
        
        Args:
            directory (str): Directory path
        
        Returns:
            bool: True if directory exists or was created
        """
        try:
            if not os.path.exists(directory):
                os.makedirs(directory)
            return True
        except Exception as e:
            print(f"Error creating directory {directory}: {e}")
            return False
    
    @staticmethod
    def save_text_file(file_path, content):
        """
        Save text content to file.
        
        Args:
            file_path (str): Path to save file
            content (str): Content to save
        
        Returns:
            bool: True if successful
        """
        try:
            # Ensure directory exists
            directory = os.path.dirname(file_path)
            if directory:
                Utils.ensure_directory_exists(directory)
            
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            return True
        except Exception as e:
            print(f"Error saving file {file_path}: {e}")
            return False
    
    @staticmethod
    def read_text_file(file_path):
        """
        Read content from text file.
        
        Args:
            file_path (str): Path to file
        
        Returns:
            str: File content or None
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return f.read()
        except Exception as e:
            print(f"Error reading file {file_path}: {e}")
            return None
    
    @staticmethod
    def center_window(window, width, height):
        """
        Center a Tkinter window on screen.
        
        Args:
            window: Tkinter window
            width (int): Window width
            height (int): Window height
        """
        screen_width = window.winfo_screenwidth()
        screen_height = window.winfo_screenheight()
        
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        
        window.geometry(f"{width}x{height}+{x}+{y}")
    
    @staticmethod
    def get_file_size(file_path):
        """
        Get file size in bytes.
        
        Args:
            file_path (str): Path to file
        
        Returns:
            int: File size in bytes, or -1 if error
        """
        try:
            return os.path.getsize(file_path)
        except Exception as e:
            print(f"Error getting file size: {e}")
            return -1
    
    @staticmethod
    def file_exists(file_path):
        """
        Check if file exists.
        
        Args:
            file_path (str): Path to file
        
        Returns:
            bool: True if file exists
        """
        return os.path.exists(file_path) and os.path.isfile(file_path)
    
    @staticmethod
    def get_current_timestamp():
        """
        Get current timestamp.
        
        Returns:
            str: Current timestamp (YYYY-MM-DD HH:MM:SS)
        """
        return datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    @staticmethod
    def get_current_date():
        """
        Get current date.
        
        Returns:
            str: Current date (YYYY-MM-DD)
        """
        return datetime.now().strftime('%Y-%m-%d')
    
    @staticmethod
    def truncate_string(text, length):
        """
        Truncate string to specified length.
        
        Args:
            text (str): Text to truncate
            length (int): Max length
        
        Returns:
            str: Truncated text with ellipsis if needed
        """
        if len(text) > length:
            return text[:length-3] + "..."
        return text
