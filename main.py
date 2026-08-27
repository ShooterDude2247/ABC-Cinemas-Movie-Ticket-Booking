# ABC CINEMAS - Main Application
# ==============================
# Entry point for the Movie Ticket Booking System

import tkinter as tk
from tkinter import ttk, messagebox
import config
from utils import Utils
from auth import Auth
from movies import Movies
from shows import Shows
from seats import Seats
from snacks import Snacks
from booking import Booking
from invoice import Invoice

class ABCCinemasApp:
    """
    Main application class for ABC Cinemas Movie Ticket Booking System.
    """
    
    def __init__(self, root):
        """
        Initialize the application.
        
        Args:
            root: Tkinter root window
        """
        self.root = root
        self.root.title(config.APP_TITLE)
        self.root.geometry(f"{config.APP_WIDTH}x{config.APP_HEIGHT}")
        Utils.center_window(self.root, config.APP_WIDTH, config.APP_HEIGHT)
        
        # Configure style
        self.setup_styles()
        
        # Current user (None = guest/logged out)
        self.current_user = None
        self.current_admin = None
        
        # Show login screen
        self.show_login_screen()
    
    def setup_styles(self):
        """Configure Tkinter styles for the application."""
        style = ttk.Style()
        style.theme_use('clam')
        
        # Configure colors
        style.configure('TLabel', background=config.BG_COLOR, foreground=config.FG_COLOR)
        style.configure('TButton', background=config.ACCENT_COLOR, foreground=config.FG_COLOR)
        style.map('TButton', background=[('active', config.HOVER_COLOR)])
        style.configure('TFrame', background=config.BG_COLOR)
    
    def clear_window(self):
        """Clear all widgets from the window."""
        for widget in self.root.winfo_children():
            widget.destroy()
    
    def show_login_screen(self):
        """Display the login screen."""
        self.clear_window()
        
        # Main container
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Title
        title = ttk.Label(main_frame, text=config.APP_TITLE, font=('Arial', 24, 'bold'))
        title.pack(pady=20)
        
        # Login type selection
        login_type_frame = ttk.Frame(main_frame)
        login_type_frame.pack(pady=10)
        
        ttk.Label(login_type_frame, text="Login As:", font=('Arial', 12)).pack(side=tk.LEFT, padx=10)
        
        self.login_type = tk.StringVar(value="user")
        ttk.Radiobutton(login_type_frame, text="User", variable=self.login_type, value="user").pack(side=tk.LEFT, padx=10)
        ttk.Radiobutton(login_type_frame, text="Admin", variable=self.login_type, value="admin").pack(side=tk.LEFT, padx=10)
        
        # Username
        ttk.Label(main_frame, text="Username:").pack(pady=5)
        self.login_username = ttk.Entry(main_frame, width=40)
        self.login_username.pack(pady=5)
        
        # Password
        ttk.Label(main_frame, text="Password:").pack(pady=5)
        self.login_password = ttk.Entry(main_frame, width=40, show="*")
        self.login_password.pack(pady=5)
        
        # Buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(pady=20)
        
        ttk.Button(button_frame, text="Login", command=self.handle_login).pack(side=tk.LEFT, padx=10)
        ttk.Button(button_frame, text="Register", command=self.show_register_screen).pack(side=tk.LEFT, padx=10)
        ttk.Button(button_frame, text="Continue as Guest", command=self.show_home_screen).pack(side=tk.LEFT, padx=10)
    
    def handle_login(self):
        """Handle user/admin login."""
        username = self.login_username.get()
        password = self.login_password.get()
        login_type = self.login_type.get()
        
        if not username or not password:
            messagebox.showerror("Error", "Please enter username and password.")
            return
        
        if login_type == "admin":
            success, result = Auth.login_admin(username, password)
            if success:
                self.current_admin = result
                self.show_admin_dashboard()
            else:
                messagebox.showerror("Login Failed", result)
        else:
            success, result = Auth.login_user(username, password)
            if success:
                self.current_user = result
                self.show_home_screen()
            else:
                messagebox.showerror("Login Failed", result)
    
    def show_register_screen(self):
        """Display the registration screen."""
        self.clear_window()
        
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        ttk.Label(main_frame, text="Create New Account", font=('Arial', 18, 'bold')).pack(pady=10)
        
        # Full Name
        ttk.Label(main_frame, text="Full Name:").pack(pady=5)
        full_name = ttk.Entry(main_frame, width=40)
        full_name.pack(pady=5)
        
        # Username
        ttk.Label(main_frame, text="Username:").pack(pady=5)
        username = ttk.Entry(main_frame, width=40)
        username.pack(pady=5)
        
        # Email
        ttk.Label(main_frame, text="Email:").pack(pady=5)
        email = ttk.Entry(main_frame, width=40)
        email.pack(pady=5)
        
        # Phone
        ttk.Label(main_frame, text="Phone (10 digits):").pack(pady=5)
        phone = ttk.Entry(main_frame, width=40)
        phone.pack(pady=5)
        
        # Password
        ttk.Label(main_frame, text="Password:").pack(pady=5)
        password = ttk.Entry(main_frame, width=40, show="*")
        password.pack(pady=5)
        
        # Confirm Password
        ttk.Label(main_frame, text="Confirm Password:").pack(pady=5)
        confirm_password = ttk.Entry(main_frame, width=40, show="*")
        confirm_password.pack(pady=5)
        
        def handle_register():
            success, message = Auth.register_user(
                full_name.get(), username.get(), email.get(),
                phone.get(), password.get(), confirm_password.get()
            )
            if success:
                messagebox.showinfo("Success", message)
                self.show_login_screen()
            else:
                messagebox.showerror("Registration Failed", message)
        
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(pady=20)
        
        ttk.Button(button_frame, text="Register", command=handle_register).pack(side=tk.LEFT, padx=10)
        ttk.Button(button_frame, text="Back to Login", command=self.show_login_screen).pack(side=tk.LEFT, padx=10)
    
    def show_home_screen(self):
        """Display the main home screen for users."""
        self.clear_window()
        
        # Top bar
        top_frame = ttk.Frame(self.root)
        top_frame.pack(fill=tk.X, padx=10, pady=10)
        
        if self.current_user:
            ttk.Label(top_frame, text=f"Welcome, {self.current_user['full_name']}!", font=('Arial', 12, 'bold')).pack(side=tk.LEFT)
        else:
            ttk.Label(top_frame, text="Guest Mode", font=('Arial', 12, 'bold')).pack(side=tk.LEFT)
        
        button_frame = ttk.Frame(top_frame)
        button_frame.pack(side=tk.RIGHT)
        
        if self.current_user:
            ttk.Button(button_frame, text="My Bookings", command=self.show_my_bookings).pack(side=tk.LEFT, padx=5)
            ttk.Button(button_frame, text="My Profile", command=self.show_profile).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(button_frame, text="Logout", command=self.show_login_screen).pack(side=tk.LEFT, padx=5)
        
        # Main content
        content_frame = ttk.Frame(self.root)
        content_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        ttk.Label(content_frame, text="Now Showing", font=('Arial', 16, 'bold')).pack(pady=10)
        
        # Get all movies
        movies_list = Movies.get_all_movies()
        
        if not movies_list:
            ttk.Label(content_frame, text="No movies available.").pack(pady=20)
            return
        
        # Create scrollable frame for movies
        canvas = tk.Canvas(content_frame, bg=config.BG_COLOR, highlightthickness=0)
        scrollbar = ttk.Scrollbar(content_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Display movies
        for movie in movies_list:
            movie_frame = ttk.Frame(scrollable_frame)
            movie_frame.pack(fill=tk.X, pady=10, padx=5)
            
            ttk.Label(movie_frame, text=f"{movie['title']} ({movie['language']})", font=('Arial', 12, 'bold')).pack(anchor=tk.W)
            ttk.Label(movie_frame, text=f"Genre: {movie['genre']} | Rating: {movie['rating']} | Duration: {movie['duration']} mins").pack(anchor=tk.W)
            ttk.Label(movie_frame, text=movie['description'][:100] + "...", wraplength=400).pack(anchor=tk.W)
            
            ttk.Button(movie_frame, text="Book Tickets", command=lambda m=movie['movie_id']: self.show_booking_screen(m)).pack(anchor=tk.W, pady=5)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
    
    def show_booking_screen(self, movie_id):
        """Display booking screen for a movie."""
        self.clear_window()
        
        # Back button
        ttk.Button(self.root, text="Back", command=self.show_home_screen).pack(anchor=tk.NW, padx=10, pady=10)
        
        # Get movie details
        movie = Movies.get_movie_by_id(movie_id)
        if not movie:
            messagebox.showerror("Error", "Movie not found.")
            self.show_home_screen()
            return
        
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        ttk.Label(main_frame, text=f"Book Tickets - {movie['title']}", font=('Arial', 16, 'bold')).pack(pady=10)
        
        # Get available shows
        shows_list = Shows.get_shows_by_movie(movie_id)
        if not shows_list:
            ttk.Label(main_frame, text="No shows available for this movie.").pack(pady=20)
            return
        
        # Display shows
        for show in shows_list:
            show_frame = ttk.Frame(main_frame)
            show_frame.pack(fill=tk.X, pady=10, padx=5)
            
            date_str = Utils.format_date(show['show_date'])
            time_str = Utils.format_time(show['show_time'])
            price_str = Utils.format_currency(show['ticket_price'])
            
            ttk.Label(show_frame, text=f"{date_str} at {time_str} - {price_str} per ticket | {show['available_seats']} seats available").pack(anchor=tk.W)
            ttk.Button(show_frame, text="Select Seats", command=lambda s=show['show_id']: self.show_seat_selection(s, movie['title'])).pack(anchor=tk.W, pady=5)
    
    def show_seat_selection(self, show_id, movie_title):
        """Display seat selection screen."""
        self.clear_window()
        
        ttk.Button(self.root, text="Back", command=lambda: self.show_booking_screen(1)).pack(anchor=tk.NW, padx=10, pady=10)
        
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        ttk.Label(main_frame, text=f"Select Seats - {movie_title}", font=('Arial', 16, 'bold')).pack(pady=10)
        
        # Get seat layout
        seat_layout = Seats.get_seat_layout()
        booked_seats = Seats.get_booked_seats_for_show(show_id)
        booked_seat_ids = [s['seat_id'] for s in booked_seats]
        
        self.selected_seats = []
        
        # Display seats
        for row_name in sorted(seat_layout.keys()):
            row_frame = ttk.Frame(main_frame)
            row_frame.pack(pady=5)
            
            ttk.Label(row_frame, text=f"Row {row_name}:", font=('Arial', 10, 'bold')).pack(side=tk.LEFT, padx=5)
            
            for seat in seat_layout[row_name]:
                is_booked = seat['seat_id'] in booked_seat_ids
                btn_text = f"{seat['row_name']}{seat['seat_number']}"
                btn_state = tk.DISABLED if is_booked else tk.NORMAL
                
                def toggle_seat(s=seat, booked=is_booked):
                    if not booked and s not in self.selected_seats:
                        self.selected_seats.append(s['seat_id'])
                    elif not booked and s['seat_id'] in self.selected_seats:
                        self.selected_seats.remove(s['seat_id'])
                
                ttk.Button(row_frame, text=btn_text, state=btn_state, command=toggle_seat, width=3).pack(side=tk.LEFT, padx=2)
        
        # Continue button
        def proceed_to_snacks():
            if self.current_user:
                self.show_snacks_selection(show_id, self.selected_seats)
            else:
                messagebox.showinfo("Info", "Please login to complete booking.")
                self.show_login_screen()
        
        ttk.Button(main_frame, text="Continue to Snacks", command=proceed_to_snacks).pack(pady=20)
    
    def show_snacks_selection(self, show_id, seat_ids):
        """Display snacks selection screen."""
        self.clear_window()
        
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        ttk.Label(main_frame, text="Add Snacks & Beverages", font=('Arial', 16, 'bold')).pack(pady=10)
        
        # Get snacks
        snacks_list = Snacks.get_all_snacks()
        
        self.snack_quantities = {}
        
        if snacks_list:
            for snack in snacks_list:
                snack_frame = ttk.Frame(main_frame)
                snack_frame.pack(fill=tk.X, pady=5, padx=5)
                
                ttk.Label(snack_frame, text=f"{snack['snack_name']} - {Utils.format_currency(snack['price'])}").pack(anchor=tk.W, side=tk.LEFT)
                
                qty_var = tk.IntVar(value=0)
                self.snack_quantities[snack['snack_id']] = qty_var
                
                ttk.Label(snack_frame, text="Qty:").pack(side=tk.LEFT, padx=(20, 0))
                ttk.Spinbox(snack_frame, from_=0, to=snack['available_quantity'], textvariable=qty_var, width=5).pack(side=tk.LEFT, padx=5)
        
        # Complete booking button
        def complete_booking():
            snack_items = [(snack_id, qty_var.get()) for snack_id, qty_var in self.snack_quantities.items() if qty_var.get() > 0]
            
            success, result = Booking.create_booking(
                self.current_user['user_id'],
                show_id,
                seat_ids,
                snack_items,
                'cash'
            )
            
            if success:
                booking_details = Booking.get_booking_details(result['booking_id'])
                self.show_confirmation_screen(booking_details)
            else:
                messagebox.showerror("Booking Failed", result)
        
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(pady=20)
        
        ttk.Button(button_frame, text="Complete Booking", command=complete_booking).pack(side=tk.LEFT, padx=10)
        ttk.Button(button_frame, text="Back", command=self.show_home_screen).pack(side=tk.LEFT, padx=10)
    
    def show_confirmation_screen(self, booking_details):
        """Display booking confirmation screen."""
        self.clear_window()
        
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        ttk.Label(main_frame, text="Booking Confirmed!", font=('Arial', 18, 'bold')).pack(pady=10)
        
        summary = Invoice.get_invoice_summary(booking_details)
        
        for key, value in summary.items():
            ttk.Label(main_frame, text=f"{key.replace('_', ' ').title()}: {value}").pack(anchor=tk.W, pady=3)
        
        def save_and_return():
            Invoice.save_invoice(booking_details, 'text')
            Invoice.save_invoice(booking_details, 'html')
            messagebox.showinfo("Success", f"Invoice saved to invoices/ folder")
            self.show_home_screen()
        
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(pady=20)
        
        ttk.Button(button_frame, text="Save Invoice & Continue", command=save_and_return).pack(side=tk.LEFT, padx=10)
        ttk.Button(button_frame, text="Home", command=self.show_home_screen).pack(side=tk.LEFT, padx=10)
    
    def show_my_bookings(self):
        """Display user's bookings."""
        self.clear_window()
        
        ttk.Button(self.root, text="Back", command=self.show_home_screen).pack(anchor=tk.NW, padx=10, pady=10)
        
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        ttk.Label(main_frame, text="My Bookings", font=('Arial', 16, 'bold')).pack(pady=10)
        
        if not self.current_user:
            ttk.Label(main_frame, text="Please login to view bookings.").pack(pady=20)
            return
        
        bookings_list = Booking.get_user_bookings(self.current_user['user_id'])
        
        if not bookings_list:
            ttk.Label(main_frame, text="You have no bookings yet.").pack(pady=20)
            return
        
        for booking in bookings_list:
            booking_frame = ttk.Frame(main_frame)
            booking_frame.pack(fill=tk.X, pady=10, padx=5)
            
            ttk.Label(booking_frame, text=f"Booking: {booking['booking_code']}", font=('Arial', 11, 'bold')).pack(anchor=tk.W)
            ttk.Label(booking_frame, text=f"Movie: {booking['movie_title']}").pack(anchor=tk.W)
            ttk.Label(booking_frame, text=f"Date: {booking['show_date']} at {booking['show_time']}").pack(anchor=tk.W)
            ttk.Label(booking_frame, text=f"Amount: {Utils.format_currency(booking['total_amount'])}").pack(anchor=tk.W)
    
    def show_profile(self):
        """Display user profile."""
        self.clear_window()
        
        ttk.Button(self.root, text="Back", command=self.show_home_screen).pack(anchor=tk.NW, padx=10, pady=10)
        
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        ttk.Label(main_frame, text="My Profile", font=('Arial', 16, 'bold')).pack(pady=10)
        
        if not self.current_user:
            ttk.Label(main_frame, text="Please login to view profile.").pack(pady=20)
            return
        
        ttk.Label(main_frame, text=f"Name: {self.current_user['full_name']}").pack(anchor=tk.W, pady=5)
        ttk.Label(main_frame, text=f"Email: {self.current_user['email']}").pack(anchor=tk.W, pady=5)
        ttk.Label(main_frame, text=f"Phone: {self.current_user['phone']}").pack(anchor=tk.W, pady=5)
    
    def show_admin_dashboard(self):
        """Display admin dashboard (simplified)."""
        self.clear_window()
        
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        ttk.Label(main_frame, text=f"Admin Dashboard - {self.current_admin['full_name']}", font=('Arial', 18, 'bold')).pack(pady=10)
        
        stats = Booking.get_admin_statistics()
        
        ttk.Label(main_frame, text=f"Total Movies: {stats['total_movies']}", font=('Arial', 12)).pack(anchor=tk.W, pady=5)
        ttk.Label(main_frame, text=f"Total Shows: {stats['total_shows']}", font=('Arial', 12)).pack(anchor=tk.W, pady=5)
        ttk.Label(main_frame, text=f"Total Users: {stats['total_users']}", font=('Arial', 12)).pack(anchor=tk.W, pady=5)
        ttk.Label(main_frame, text=f"Total Bookings: {stats['total_bookings']}", font=('Arial', 12)).pack(anchor=tk.W, pady=5)
        ttk.Label(main_frame, text=f"Total Revenue: {Utils.format_currency(stats['total_revenue'])}", font=('Arial', 12, 'bold')).pack(anchor=tk.W, pady=5)
        
        ttk.Button(main_frame, text="Logout", command=self.show_login_screen).pack(pady=20)


def main():
    """Main entry point for the application."""
    root = tk.Tk()
    app = ABCCinemasApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
