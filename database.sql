-- ABC CINEMAS - Movie Ticket Booking System Database
-- ==================================================
-- This script creates the complete database schema and sample data

-- Create Database
DROP DATABASE IF EXISTS abc_cinemas;
CREATE DATABASE abc_cinemas;
USE abc_cinemas;

-- =============================================
-- 1. USERS TABLE (Customer Accounts)
-- =============================================
CREATE TABLE users (
    user_id INT PRIMARY KEY AUTO_INCREMENT,
    full_name VARCHAR(100) NOT NULL,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    phone VARCHAR(15) NOT NULL,
    password_hash VARCHAR(256) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- =============================================
-- 2. ADMINS TABLE
-- =============================================
CREATE TABLE admins (
    admin_id INT PRIMARY KEY AUTO_INCREMENT,
    username VARCHAR(50) UNIQUE NOT NULL,
    password_hash VARCHAR(256) NOT NULL,
    full_name VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- =============================================
-- 3. MOVIES TABLE
-- =============================================
CREATE TABLE movies (
    movie_id INT PRIMARY KEY AUTO_INCREMENT,
    title VARCHAR(150) NOT NULL,
    genre VARCHAR(50) NOT NULL,
    language VARCHAR(30) NOT NULL,
    duration INT NOT NULL COMMENT 'Duration in minutes',
    rating VARCHAR(10) NOT NULL COMMENT 'U, UA, A, S',
    description TEXT,
    poster_path VARCHAR(255),
    status VARCHAR(20) DEFAULT 'active' COMMENT 'active or inactive',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FULLTEXT INDEX ft_title (title)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- =============================================
-- 4. SHOWS TABLE (Movie Shows)
-- =============================================
CREATE TABLE shows (
    show_id INT PRIMARY KEY AUTO_INCREMENT,
    movie_id INT NOT NULL,
    show_date DATE NOT NULL,
    show_time TIME NOT NULL,
    ticket_price DECIMAL(10, 2) NOT NULL,
    total_seats INT DEFAULT 60,
    available_seats INT DEFAULT 60,
    status VARCHAR(20) DEFAULT 'active',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (movie_id) REFERENCES movies(movie_id) ON DELETE CASCADE,
    INDEX idx_movie_date (movie_id, show_date),
    UNIQUE KEY unique_show (movie_id, show_date, show_time)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- =============================================
-- 5. SEATS TABLE (Theatre Seating Layout)
-- =============================================
CREATE TABLE seats (
    seat_id INT PRIMARY KEY AUTO_INCREMENT,
    row_name CHAR(1) NOT NULL COMMENT 'A-F',
    seat_number INT NOT NULL COMMENT '1-10',
    UNIQUE KEY unique_seat (row_name, seat_number)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- =============================================
-- 6. BOOKINGS TABLE (Customer Bookings)
-- =============================================
CREATE TABLE bookings (
    booking_id INT PRIMARY KEY AUTO_INCREMENT,
    booking_code VARCHAR(30) UNIQUE NOT NULL COMMENT 'e.g., ABC20260827001',
    user_id INT NOT NULL,
    show_id INT NOT NULL,
    booking_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    total_ticket_amount DECIMAL(10, 2) NOT NULL,
    total_snack_amount DECIMAL(10, 2) DEFAULT 0.00,
    total_amount DECIMAL(10, 2) NOT NULL,
    payment_method VARCHAR(30) DEFAULT 'cash',
    payment_status VARCHAR(20) DEFAULT 'paid',
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
    FOREIGN KEY (show_id) REFERENCES shows(show_id) ON DELETE CASCADE,
    INDEX idx_user_id (user_id),
    INDEX idx_show_id (show_id),
    INDEX idx_booking_code (booking_code)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- =============================================
-- 7. BOOKING_SEATS TABLE (Seats in each booking)
-- =============================================
CREATE TABLE booking_seats (
    booking_seat_id INT PRIMARY KEY AUTO_INCREMENT,
    booking_id INT NOT NULL,
    seat_id INT NOT NULL,
    FOREIGN KEY (booking_id) REFERENCES bookings(booking_id) ON DELETE CASCADE,
    FOREIGN KEY (seat_id) REFERENCES seats(seat_id) ON DELETE CASCADE,
    UNIQUE KEY unique_booking_seat (booking_id, seat_id),
    INDEX idx_booking_id (booking_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- =============================================
-- 8. SNACKS TABLE
-- =============================================
CREATE TABLE snacks (
    snack_id INT PRIMARY KEY AUTO_INCREMENT,
    snack_name VARCHAR(100) NOT NULL,
    price DECIMAL(10, 2) NOT NULL,
    available_quantity INT NOT NULL,
    status VARCHAR(20) DEFAULT 'active',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- =============================================
-- 9. BOOKING_SNACKS TABLE (Snacks in each booking)
-- =============================================
CREATE TABLE booking_snacks (
    booking_snack_id INT PRIMARY KEY AUTO_INCREMENT,
    booking_id INT NOT NULL,
    snack_id INT NOT NULL,
    quantity INT NOT NULL,
    price_at_booking DECIMAL(10, 2) NOT NULL COMMENT 'Price stored at time of booking',
    FOREIGN KEY (booking_id) REFERENCES bookings(booking_id) ON DELETE CASCADE,
    FOREIGN KEY (snack_id) REFERENCES snacks(snack_id) ON DELETE CASCADE,
    INDEX idx_booking_id (booking_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- =============================================
-- 10. SEAT_BOOKINGS TABLE (Track which seats are booked for which show)
-- =============================================
CREATE TABLE seat_bookings (
    seat_booking_id INT PRIMARY KEY AUTO_INCREMENT,
    show_id INT NOT NULL,
    seat_id INT NOT NULL,
    booking_id INT NOT NULL,
    booked_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (show_id) REFERENCES shows(show_id) ON DELETE CASCADE,
    FOREIGN KEY (seat_id) REFERENCES seats(seat_id) ON DELETE CASCADE,
    FOREIGN KEY (booking_id) REFERENCES bookings(booking_id) ON DELETE CASCADE,
    UNIQUE KEY unique_show_seat (show_id, seat_id),
    INDEX idx_show_id (show_id),
    INDEX idx_seat_id (seat_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- =============================================
-- INSERT SAMPLE DATA
-- =============================================

-- Insert Sample Admin
-- Username: admin, Password: admin123 (SHA256 hash)
INSERT INTO admins (username, password_hash, full_name) VALUES 
('admin', '0192023a7bbd73250516f069df18b500', 'Admin User');

-- Insert Sample Users
INSERT INTO users (full_name, username, email, phone, password_hash) VALUES 
('John Smith', 'johnsmith', 'john@example.com', '9876543210', '8d969eef6ecad3c29a3a873fba8973a7'),
('Priya Sharma', 'priyasharma', 'priya@example.com', '9123456789', '8d969eef6ecad3c29a3a873fba8973a7'),
('Amit Patel', 'amitpatel', 'amit@example.com', '8765432109', '8d969eef6ecad3c29a3a873fba8973a7');

-- Insert Sample Movies
INSERT INTO movies (title, genre, language, duration, rating, description, poster_path, status) VALUES 
('Avengers: Endgame', 'Action/Sci-Fi', 'English', 181, 'U/A', 'The Avengers assemble one last time to save the universe from Thanos.', 'posters/avengers.jpg', 'active'),
('Interstellar', 'Sci-Fi/Drama', 'English', 169, 'U/A', 'A team of astronauts travels through a wormhole in space in an attempt to ensure humanity\'s survival.', 'posters/interstellar.jpg', 'active'),
('Inception', 'Sci-Fi/Thriller', 'English', 148, 'U/A', 'A skilled thief who steals corporate secrets through dream-sharing technology.', 'posters/inception.jpg', 'active'),
('Spider-Man: No Way Home', 'Action/Adventure', 'English', 159, 'U/A', 'With Spider-Man\'s identity now revealed, Peter Parker must travel the Multiverse.', 'posters/spiderman.jpg', 'active'),
('The Dark Knight', 'Crime/Drama', 'English', 152, 'U/A', 'The Joker wreaks havoc on Gotham, forcing Batman to push beyond his limits.', 'posters/darkknight.jpg', 'active');

-- Insert Sample Shows (for the next 7 days)
-- Adjust dates as needed (this uses relative dates from today)
INSERT INTO shows (movie_id, show_date, show_time, ticket_price, total_seats, available_seats) VALUES 
(1, CURDATE() + INTERVAL 1 DAY, '10:00:00', 250.00, 60, 60),
(1, CURDATE() + INTERVAL 1 DAY, '13:30:00', 250.00, 60, 60),
(1, CURDATE() + INTERVAL 1 DAY, '17:00:00', 300.00, 60, 60),
(1, CURDATE() + INTERVAL 1 DAY, '20:30:00', 300.00, 60, 60),
(2, CURDATE() + INTERVAL 2 DAY, '10:00:00', 250.00, 60, 60),
(2, CURDATE() + INTERVAL 2 DAY, '13:30:00', 250.00, 60, 60),
(2, CURDATE() + INTERVAL 2 DAY, '17:00:00', 300.00, 60, 60),
(2, CURDATE() + INTERVAL 2 DAY, '20:30:00', 300.00, 60, 60),
(3, CURDATE() + INTERVAL 3 DAY, '10:00:00', 250.00, 60, 60),
(3, CURDATE() + INTERVAL 3 DAY, '13:30:00', 250.00, 60, 60),
(3, CURDATE() + INTERVAL 3 DAY, '17:00:00', 300.00, 60, 60),
(3, CURDATE() + INTERVAL 3 DAY, '20:30:00', 300.00, 60, 60),
(4, CURDATE() + INTERVAL 1 DAY, '10:00:00', 300.00, 60, 60),
(4, CURDATE() + INTERVAL 2 DAY, '13:30:00', 300.00, 60, 60),
(5, CURDATE() + INTERVAL 3 DAY, '17:00:00', 250.00, 60, 60);

-- Insert Theatre Seats (6 rows, 10 seats each = 60 total seats)
INSERT INTO seats (row_name, seat_number) VALUES 
('A', 1), ('A', 2), ('A', 3), ('A', 4), ('A', 5), ('A', 6), ('A', 7), ('A', 8), ('A', 9), ('A', 10),
('B', 1), ('B', 2), ('B', 3), ('B', 4), ('B', 5), ('B', 6), ('B', 7), ('B', 8), ('B', 9), ('B', 10),
('C', 1), ('C', 2), ('C', 3), ('C', 4), ('C', 5), ('C', 6), ('C', 7), ('C', 8), ('C', 9), ('C', 10),
('D', 1), ('D', 2), ('D', 3), ('D', 4), ('D', 5), ('D', 6), ('D', 7), ('D', 8), ('D', 9), ('D', 10),
('E', 1), ('E', 2), ('E', 3), ('E', 4), ('E', 5), ('E', 6), ('E', 7), ('E', 8), ('E', 9), ('E', 10),
('F', 1), ('F', 2), ('F', 3), ('F', 4), ('F', 5), ('F', 6), ('F', 7), ('F', 8), ('F', 9), ('F', 10);

-- Insert Sample Snacks
INSERT INTO snacks (snack_name, price, available_quantity, status) VALUES 
('Popcorn', 150.00, 100, 'active'),
('Cheese Popcorn', 180.00, 80, 'active'),
('Nachos', 120.00, 60, 'active'),
('Soft Drink (Large)', 80.00, 150, 'active'),
('Water Bottle', 40.00, 200, 'active'),
('Combo Meal (Popcorn + Drink)', 250.00, 50, 'active'),
('Candy Pack', 100.00, 120, 'active'),
('Samosa', 60.00, 90, 'active');

-- Insert Sample Booking (example only)
INSERT INTO bookings (booking_code, user_id, show_id, total_ticket_amount, total_snack_amount, total_amount, payment_method, payment_status) 
VALUES ('ABC20260827001', 1, 1, 500.00, 150.00, 650.00, 'cash', 'paid');

-- Insert sample booking seats
INSERT INTO booking_seats (booking_id, seat_id) 
VALUES (1, 1), (1, 2);

-- Insert sample booking snacks
INSERT INTO booking_snacks (booking_id, snack_id, quantity, price_at_booking) 
VALUES (1, 1, 1, 150.00);

-- Insert sample seat bookings
INSERT INTO seat_bookings (show_id, seat_id, booking_id) 
VALUES (1, 1, 1), (1, 2, 1);

-- =============================================
-- CREATE INDEXES
-- =============================================
CREATE INDEX idx_users_username ON users(username);
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_shows_movie ON shows(movie_id);
CREATE INDEX idx_bookings_user ON bookings(user_id);
CREATE INDEX idx_bookings_show ON bookings(show_id);
CREATE INDEX idx_booking_seats_booking ON booking_seats(booking_id);
CREATE INDEX idx_booking_snacks_booking ON booking_snacks(booking_id);
CREATE INDEX idx_seat_bookings_show ON seat_bookings(show_id);

-- =============================================
-- DATABASE SETUP COMPLETE
-- =============================================
-- Sample Credentials:
-- Admin: username="admin", password="admin123"
-- User 1: username="johnsmith", password="password"
-- User 2: username="priyasharma", password="password"
-- User 3: username="amitpatel", password="password"
