# ABC CINEMAS - Database Configuration
# =====================================
# Modify the following settings to match your MySQL setup

# MySQL Connection Parameters
DB_CONFIG = {
    'host': 'localhost',           # MySQL server address
    'user': 'root',                 # MySQL username
    'password': 'password',         # CHANGE THIS to your MySQL password
    'database': 'abc_cinemas',      # Database name
    'port': 3306                    # MySQL port
}

# Application Settings
APP_TITLE = "ABC CINEMAS - Movie Ticket Booking System"
APP_WIDTH = 1200
APP_HEIGHT = 750

# Cinema Settings
CINEMA_NAME = "ABC CINEMAS"
CINEMA_ROWS = 6  # Rows A-F
CINEMA_SEATS_PER_ROW = 10  # 10 seats per row (1-10)

# GUI Theme Colors
BG_COLOR = "#1a1a1a"           # Dark background
FG_COLOR = "#ffffff"            # White text
ACCENT_COLOR = "#e74c3c"        # Red accent (cinema theme)
HOVER_COLOR = "#c0392b"         # Darker red for hover
SUCCESS_COLOR = "#27ae60"       # Green for success
WARNING_COLOR = "#f39c12"       # Orange for warning

# Paths
POSTERS_PATH = "posters"
INVOICES_PATH = "invoices"
PLACEHOLDER_POSTER = "posters/placeholder.png"

# Security
PASSWORD_HASH_ALGORITHM = "sha256"
MIN_PASSWORD_LENGTH = 6
