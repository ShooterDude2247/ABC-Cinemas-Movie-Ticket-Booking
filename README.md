# ABC CINEMAS - Movie Ticket Booking System

A comprehensive Python-based GUI application for booking movie tickets at ABC Cinemas, built using Tkinter and MySQL.

## Features

### User Features
- **User Registration & Authentication**: Secure login with email and password
- **Browse Movies**: View all currently showing movies with details
- **Seat Selection**: Interactive seat layout for selecting preferred seats
- **Snacks & Beverages**: Add food items to booking
- **Online Booking**: Complete ticket booking with invoice generation
- **Booking History**: View past bookings and booking details
- **Profile Management**: Update personal information

### Admin Features
- **Admin Dashboard**: View key statistics (total revenue, bookings, users, etc.)
- **Movie Management**: Add, update, and manage movies
- **Show Management**: Create and manage movie shows
- **Booking Search**: Search bookings by code, customer name, or movie
- **Revenue Analytics**: Track total revenue and booking statistics

### Technical Features
- **Secure Authentication**: Password hashing with SHA256
- **Database Management**: Complete MySQL database with proper relationships
- **Email Validation**: Validates email and phone formats
- **Invoice Generation**: Automatic invoice generation in text and HTML formats
- **Seat Management**: Real-time seat availability tracking
- **Transaction Handling**: Safe booking transactions with rollback on error

## Project Structure

```
ABC-Cinemas-Movie-Ticket-Booking/
├── main.py              # Main application entry point
├── config.py            # Configuration settings
├── database.py          # Database connection and operations
├── auth.py              # User authentication and registration
├── movies.py            # Movie management
├── shows.py             # Show management
├── seats.py             # Seat management
├── snacks.py            # Snacks/beverages management
├── booking.py           # Booking operations
├── invoice.py           # Invoice generation
├── utils.py             # Utility functions
├── database.sql         # Database schema and sample data
├── requirements.txt     # Python dependencies
└── README.md            # This file
```

## Requirements

- Python 3.7+
- MySQL 5.7+
- Tkinter (usually comes with Python)

## Installation

### 1. Clone the Repository
```bash
git clone https://github.com/ShooterDude2247/ABC-Cinemas-Movie-Ticket-Booking.git
cd ABC-Cinemas-Movie-Ticket-Booking
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Set Up MySQL Database

1. Open MySQL command line or MySQL Workbench
2. Run the database setup script:
```sql
source database.sql
```

Or manually execute the SQL statements from `database.sql` file.

### 4. Configure Database Connection

Edit `config.py` and update the database credentials:
```python
DB_CONFIG = {
    'host': 'localhost',           # Your MySQL host
    'user': 'root',                # Your MySQL username
    'password': 'your_password',   # Your MySQL password
    'database': 'abc_cinemas',     # Database name
    'port': 3306                   # MySQL port
}
```

### 5. Run the Application
```bash
python main.py
```

## Usage

### For Customers

1. **Register/Login**
   - Click "Register" to create a new account
   - Or login with existing credentials
   - Can browse as guest without login

2. **Browse Movies**
   - View all currently showing movies
   - See movie details (genre, language, duration, rating)

3. **Book Tickets**
   - Select a movie
   - Choose show date and time
   - Select desired seats (interactive seat layout)
   - Add snacks and beverages (optional)
   - Complete payment
   - View and save invoice

4. **Manage Account**
   - View booking history
   - Update profile information
   - Change password

### For Admins

1. **Login as Admin**
   - Select "Admin" option during login
   - Use admin credentials (default: username=admin, password=admin123)

2. **Dashboard**
   - View system statistics
   - Monitor revenue and bookings

3. **Manage Content**
   - Add/update/delete movies
   - Create and manage shows
   - Manage snacks inventory

4. **Manage Bookings**
   - Search bookings by various criteria
   - View booking details
   - Generate reports

## Sample Credentials

### Admin
```
Username: admin
Password: admin123
```

### Users
```
Username: johnsmith
Password: password

Username: priyasharma
Password: password

Username: amitpatel
Password: password
```

## Database Schema

The application uses the following tables:

- **users**: Customer accounts
- **admins**: Administrator accounts
- **movies**: Movie information
- **shows**: Movie show timings and pricing
- **seats**: Theatre seating layout
- **bookings**: Ticket booking records
- **booking_seats**: Seats for each booking
- **snacks**: Available snacks/beverages
- **booking_snacks**: Snacks added to each booking
- **seat_bookings**: Track booked seats per show

## Security Features

- **Password Hashing**: SHA256 hashing for password storage
- **SQL Injection Prevention**: Prepared statements with parameterized queries
- **Input Validation**: Email, phone, and password validation
- **Transaction Safety**: Database transactions with rollback on error
- **Duplicate Prevention**: Unique constraints on usernames and emails

## File Descriptions

### Core Application Files

**main.py**
- Main GUI application using Tkinter
- Implements all screens (login, registration, home, booking, etc.)
- Handles user interactions and navigation

**config.py**
- Application configuration settings
- Database connection parameters
- GUI theme colors and styling
- Paths and security settings

**database.py**
- Database connection management
- Query execution methods (SELECT, INSERT, UPDATE, DELETE)
- Connection pooling and error handling

### Business Logic Modules

**auth.py**
- User registration and login
- Password validation and hashing
- Admin authentication
- Profile updates and password changes

**movies.py**
- Movie browsing and search
- Movie filtering (by genre, language, rating)
- Admin movie management (add, update, delete)

**shows.py**
- Show retrieval and filtering
- Admin show management
- Seat availability tracking

**seats.py**
- Seat layout management
- Seat availability checking
- Seat booking and reservation

**snacks.py**
- Snacks/beverages inventory
- Price and availability management
- Admin snacks management

**booking.py**
- Booking creation and management
- Booking history and details
- Admin booking search and statistics
- Transaction handling

**invoice.py**
- Invoice generation (text and HTML formats)
- Invoice saving to files
- Invoice summary for display

**utils.py**
- Image loading and handling
- Currency formatting
- Date/time formatting
- File operations
- Window centering
- Booking code generation

## Future Enhancements

- [ ] Email notifications for bookings
- [ ] SMS alerts
- [ ] Payment gateway integration (Razorpay, Stripe)
- [ ] QR code generation for tickets
- [ ] Mobile app version
- [ ] Rating and review system
- [ ] Promotional codes and discounts
- [ ] Seat price variations (premium, standard)
- [ ] Cancellation and refund processing
- [ ] Advanced analytics and reporting

## Troubleshooting

### Database Connection Error
- Check MySQL is running
- Verify database credentials in `config.py`
- Ensure `abc_cinemas` database exists
- Check MySQL port (default 3306)

### Module Import Errors
- Ensure all Python files are in the same directory
- Verify Pillow and mysql-connector-python are installed:
  ```bash
  pip install Pillow mysql-connector-python
  ```

### GUI Issues
- Ensure Tkinter is installed (comes with Python)
- For Linux: `sudo apt-get install python3-tk`
- Check screen resolution (app requires 1200x750)

## Contributing

Contributions are welcome! Please feel free to submit pull requests or open issues for bugs and feature requests.

## License

This project is open source and available under the MIT License.

## Author

ShooterDude2247

## Support

For issues, questions, or suggestions, please create an issue on the GitHub repository.

---

**Last Updated**: August 2026
**Version**: 1.0.0
