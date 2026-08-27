# ABC CINEMAS - Utility Functions
# ================================
# Common utility functions used throughout the application

import os
from PIL import Image, ImageTk
import config
from datetime import datetime

class Utils:
    """
    Utility functions for the application.
    """
    
    @staticmethod
    def load_image(image_path, width=200, height=300):
        """
        Load and resize an image from a file path.
        Returns a PhotoImage suitable for Tkinter.
        
        Args:
            image_path (str): Path to image file
            width (int): Target width in pixels
            height (int): Target height in pixels
        
        Returns:
            ImageTk.PhotoImage or None
        """
        try:
            if not os.path.exists(image_path):
                # Use placeholder if file doesn't exist
                image_path = config.PLACEHOLDER_POSTER
                if not os.path.exists(image_path):
                    return None
            
            image = Image.open(image_path)
            image = image.resize((width, height), Image.Resampling.LANCZOS)
            photo = ImageTk.PhotoImage(image)
            return photo
        except Exception as e:
            print(f"Error loading image {image_path}: {e}")
            return None
    
    @staticmethod
    def create_placeholder_image(width=200, height=300):
        """
        Create a placeholder image when poster cannot be loaded.
        
        Args:
            width (int): Image width
            height (int): Image height
        
        Returns:
            ImageTk.PhotoImage
        """
        try:
            image = Image.new('RGB', (width, height), color=config.ACCENT_COLOR)
            photo = ImageTk.PhotoImage(image)
            return photo
        except Exception as e:
            print(f"Error creating placeholder: {e}")
            return None
    
    @staticmethod
    def format_currency(amount):
        """
        Format amount as Indian Rupees.
        
        Args:
            amount (float): Amount to format
        
        Returns:
            str: Formatted currency string
        """
        return f"₹{amount:,.2f}"
    
    @staticmethod
    def format_date(date_obj):
        """
        Format date in readable format.
        
        Args:
            date_obj: Date object or string
        
        Returns:
            str: Formatted date
        """
        if isinstance(date_obj, str):
            return date_obj
        return date_obj.strftime("%d %B %Y")
    
    @staticmethod
    def format_time(time_obj):
        """
        Format time in 12-hour format.
        
        Args:
            time_obj: Time object or string
        
        Returns:
            str: Formatted time
        """
        if isinstance(time_obj, str):
            # Convert HH:MM:SS to HH:MM AM/PM
            time_parts = time_obj.split(':')
            hour = int(time_parts[0])
            minute = time_parts[1]
            
            period = 'AM' if hour < 12 else 'PM'
            if hour > 12:
                hour -= 12
            elif hour == 0:
                hour = 12
            
            return f"{hour:02d}:{minute} {period}"
        return str(time_obj)
    
    @staticmethod
    def generate_booking_code():
        """
        Generate a unique booking code.
        Format: ABC + Date (YYYYMMDD) + Sequential number
        
        Returns:
            str: Booking code
        """
        from database import Database
        
        date_str = datetime.now().strftime("%Y%m%d")
        
        # Query the last booking code for today
        query = """
            SELECT MAX(CAST(SUBSTRING(booking_code, 10) AS UNSIGNED)) as last_num
            FROM bookings
            WHERE booking_code LIKE %s
        """
        result = Database.execute_query(
            query,
            (f"ABC{date_str}%",),
            fetch_one=True,
            dictionary=True
        )
        
        next_num = 1
        if result and result['last_num']:
            next_num = result['last_num'] + 1
        
        booking_code = f"ABC{date_str}{next_num:04d}"
        return booking_code
    
    @staticmethod
    def ensure_directory_exists(directory):
        """
        Create directory if it doesn't exist.
        
        Args:
            directory (str): Directory path
        """
        if not os.path.exists(directory):
            os.makedirs(directory)
    
    @staticmethod
    def save_text_file(filename, content):
        """
        Save text content to a file.
        
        Args:
            filename (str): File path
            content (str): Content to save
        
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            Utils.ensure_directory_exists(os.path.dirname(filename) or '.')
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(content)
            return True
        except Exception as e:
            print(f"Error saving file: {e}")
            return False
    
    @staticmethod
    def center_window(root, width=1200, height=750):
        """
        Center a Tkinter window on the screen.
        
        Args:
            root: Tkinter root window
            width (int): Window width
            height (int): Window height
        """
        root.geometry(f"{width}x{height}")
        
        # Get screen dimensions
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        
        # Calculate position
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        
        root.geometry(f"{width}x{height}+{x}+{y}")
    
    @staticmethod
    def seats_to_string(seat_list):
        """
        Convert list of seats to readable string.
        
        Args:
            seat_list (list): List of (row, number) tuples
        
        Returns:
            str: Comma-separated seat string
        """
        return ", ".join([f"{row}{num}" for row, num in seat_list])
    
    @staticmethod
    def get_seat_display(seat_info):
        """
        Get seat display name from tuple.
        
        Args:
            seat_info (tuple): (row_name, seat_number)
        
        Returns:
            str: Display name like "A1"
        """
        return f"{seat_info[0]}{seat_info[1]}"
