# ABC CINEMAS - Invoice Module
# ============================
# Generates and manages invoices for bookings

from utils import Utils
from datetime import datetime

class Invoice:
    """
    Invoice class for generating booking receipts.
    """
    
    @staticmethod
    def generate_invoice_text(booking_details):
        """
        Generate a text-based invoice for a booking.
        
        Args:
            booking_details (dict): Complete booking information
        
        Returns:
            str: Invoice text
        """
        if not booking_details:
            return ""
        
        invoice = ""
        invoice += "=" * 60 + "\n"
        invoice += "ABC CINEMAS - MOVIE TICKET BOOKING INVOICE\n"
        invoice += "=" * 60 + "\n\n"
        
        # Header
        invoice += f"Booking Code: {booking_details.get('booking_code', 'N/A')}\n"
        invoice += f"Booking Date: {booking_details.get('booking_date', 'N/A')}\n"
        invoice += f"Payment Status: {booking_details.get('payment_status', 'N/A').upper()}\n"
        invoice += "-" * 60 + "\n\n"
        
        # Customer Details
        invoice += "CUSTOMER DETAILS\n"
        invoice += f"Name: {booking_details.get('full_name', 'N/A')}\n"
        invoice += f"Email: {booking_details.get('email', 'N/A')}\n"
        invoice += f"Phone: {booking_details.get('phone', 'N/A')}\n"
        invoice += "-" * 60 + "\n\n"
        
        # Show Details
        invoice += "SHOW DETAILS\n"
        invoice += f"Movie: {booking_details.get('movie_title', 'N/A')}\n"
        invoice += f"Date: {Utils.format_date(booking_details.get('show_date', 'N/A'))}\n"
        invoice += f"Time: {Utils.format_time(booking_details.get('show_time', 'N/A'))}\n"
        invoice += "-" * 60 + "\n\n"
        
        # Seat Details
        invoice += "SEATS BOOKED\n"
        seats = booking_details.get('seats', [])
        if seats:
            seat_display = ", ".join([f"{s['row_name']}{s['seat_number']}" for s in seats])
            invoice += f"Seat(s): {seat_display}\n"
        else:
            invoice += "Seats: None\n"
        invoice += "-" * 60 + "\n\n"
        
        # Amount Breakdown
        invoice += "AMOUNT BREAKDOWN\n"
        
        # Ticket amount
        num_seats = len(seats) if seats else 0
        ticket_price = booking_details.get('ticket_price', 0)
        ticket_total = booking_details.get('total_ticket_amount', 0)
        
        invoice += f"Tickets ({num_seats} x {Utils.format_currency(ticket_price)}): "
        invoice += f"{Utils.format_currency(ticket_total)}\n"
        
        # Snacks
        snacks = booking_details.get('snacks', [])
        if snacks:
            invoice += "\nSnacks:\n"
            snack_total = 0
            for snack in snacks:
                snack_price = float(snack.get('price_at_booking', 0))
                snack_qty = snack.get('quantity', 0)
                snack_item_total = snack_price * snack_qty
                snack_total += snack_item_total
                invoice += f"  - {snack.get('snack_name', 'N/A')} x{snack_qty}: "
                invoice += f"{Utils.format_currency(snack_item_total)}\n"
        
        snack_amount = booking_details.get('total_snack_amount', 0)
        if snack_amount > 0:
            invoice += f"Total Snacks: {Utils.format_currency(snack_amount)}\n"
        
        invoice += "\n" + "-" * 60 + "\n"
        
        # Total
        total_amount = booking_details.get('total_amount', 0)
        invoice += f"TOTAL AMOUNT: {Utils.format_currency(total_amount)}\n"
        invoice += f"Payment Method: {booking_details.get('payment_method', 'N/A').upper()}\n"
        
        invoice += "\n" + "=" * 60 + "\n"
        invoice += "Thank you for choosing ABC CINEMAS!\n"
        invoice += "For cancellations, contact us within 24 hours of booking.\n"
        invoice += "=" * 60 + "\n"
        
        return invoice
    
    @staticmethod
    def generate_invoice_html(booking_details):
        """
        Generate an HTML-based invoice for a booking.
        
        Args:
            booking_details (dict): Complete booking information
        
        Returns:
            str: HTML invoice
        """
        if not booking_details:
            return ""
        
        seats = booking_details.get('seats', [])
        snacks = booking_details.get('snacks', [])
        
        # Build seats display
        seat_display = ", ".join([f"{s['row_name']}{s['seat_number']}" for s in seats]) if seats else "N/A"
        
        # Build snacks table
        snacks_html = ""
        if snacks:
            snacks_html = "<h3>Snacks</h3><table border='1' cellpadding='5'><tr><th>Item</th><th>Quantity</th><th>Price</th><th>Total</th></tr>"
            for snack in snacks:
                snack_price = float(snack.get('price_at_booking', 0))
                snack_qty = snack.get('quantity', 0)
                snack_item_total = snack_price * snack_qty
                snacks_html += f"<tr><td>{snack.get('snack_name', 'N/A')}</td><td>{snack_qty}</td><td>{Utils.format_currency(snack_price)}</td><td>{Utils.format_currency(snack_item_total)}</td></tr>"
            snacks_html += "</table>"
        
        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>ABC Cinemas Invoice</title>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 20px; }}
                .invoice {{ max-width: 800px; margin: auto; border: 1px solid #ddd; padding: 20px; }}
                h1 {{ text-align: center; color: #e74c3c; }}
                h2 {{ color: #333; border-bottom: 2px solid #e74c3c; padding-bottom: 10px; }}
                table {{ width: 100%; border-collapse: collapse; }}
                table, th, td {{ border: 1px solid #ddd; }}
                th {{ background-color: #e74c3c; color: white; }}
                td {{ padding: 8px; }}
                .total {{ font-size: 18px; font-weight: bold; background-color: #f0f0f0; }}
                .header-info {{ display: grid; grid-template-columns: 1fr 1fr; gap: 20px; }}
                .info-box {{ background-color: #f9f9f9; padding: 10px; border-left: 4px solid #e74c3c; }}
            </style>
        </head>
        <body>
            <div class="invoice">
                <h1>ABC CINEMAS</h1>
                <h2>Movie Ticket Booking Invoice</h2>
                
                <div class="header-info">
                    <div class="info-box">
                        <strong>Booking Code:</strong> {booking_details.get('booking_code', 'N/A')}<br>
                        <strong>Booking Date:</strong> {booking_details.get('booking_date', 'N/A')}<br>
                        <strong>Payment Status:</strong> {booking_details.get('payment_status', 'N/A').upper()}
                    </div>
                    <div class="info-box">
                        <strong>Name:</strong> {booking_details.get('full_name', 'N/A')}<br>
                        <strong>Email:</strong> {booking_details.get('email', 'N/A')}<br>
                        <strong>Phone:</strong> {booking_details.get('phone', 'N/A')}
                    </div>
                </div>
                
                <h2>Show Details</h2>
                <div class="info-box">
                    <strong>Movie:</strong> {booking_details.get('movie_title', 'N/A')}<br>
                    <strong>Date:</strong> {Utils.format_date(booking_details.get('show_date', 'N/A'))}<br>
                    <strong>Time:</strong> {Utils.format_time(booking_details.get('show_time', 'N/A'))}<br>
                    <strong>Seats:</strong> {seat_display}
                </div>
                
                <h2>Amount Breakdown</h2>
                <table>
                    <tr>
                        <th>Description</th>
                        <th>Amount</th>
                    </tr>
                    <tr>
                        <td>Tickets ({len(seats)} x {Utils.format_currency(booking_details.get('ticket_price', 0))})</td>
                        <td>{Utils.format_currency(booking_details.get('total_ticket_amount', 0))}</td>
                    </tr>
                    <tr>
                        <td>Snacks</td>
                        <td>{Utils.format_currency(booking_details.get('total_snack_amount', 0))}</td>
                    </tr>
                    <tr class="total">
                        <td>TOTAL AMOUNT</td>
                        <td>{Utils.format_currency(booking_details.get('total_amount', 0))}</td>
                    </tr>
                </table>
                
                {snacks_html}
                
                <h2>Payment Information</h2>
                <div class="info-box">
                    <strong>Payment Method:</strong> {booking_details.get('payment_method', 'N/A').upper()}<br>
                    <strong>Payment Status:</strong> {booking_details.get('payment_status', 'N/A').upper()}
                </div>
                
                <hr>
                <p style="text-align: center; color: #666;">
                    Thank you for choosing ABC CINEMAS!<br>
                    For cancellations, contact us within 24 hours of booking.<br>
                    Enjoy your movie!
                </p>
            </div>
        </body>
        </html>
        """
        
        return html
    
    @staticmethod
    def save_invoice(booking_details, format_type='text'):
        """
        Save invoice to a file.
        
        Args:
            booking_details (dict): Complete booking information
            format_type (str): 'text' or 'html'
        
        Returns:
            tuple: (success: bool, file_path: str or message: str)
        """
        try:
            Utils.ensure_directory_exists('invoices')
            
            booking_code = booking_details.get('booking_code', 'invoice')
            
            if format_type == 'html':
                invoice_content = Invoice.generate_invoice_html(booking_details)
                filename = f"invoices/{booking_code}.html"
            else:
                invoice_content = Invoice.generate_invoice_text(booking_details)
                filename = f"invoices/{booking_code}.txt"
            
            if Utils.save_text_file(filename, invoice_content):
                return True, filename
            else:
                return False, "Failed to save invoice."
        
        except Exception as e:
            print(f"Invoice Save Error: {e}")
            return False, f"Error: {str(e)}"
    
    @staticmethod
    def get_invoice_summary(booking_details):
        """
        Get a summary of invoice information for display.
        
        Args:
            booking_details (dict): Complete booking information
        
        Returns:
            dict: Summary dictionary
        """
        return {
            'booking_code': booking_details.get('booking_code', 'N/A'),
            'customer_name': booking_details.get('full_name', 'N/A'),
            'movie_title': booking_details.get('movie_title', 'N/A'),
            'show_date': Utils.format_date(booking_details.get('show_date', 'N/A')),
            'show_time': Utils.format_time(booking_details.get('show_time', 'N/A')),
            'num_seats': len(booking_details.get('seats', [])),
            'seats': ", ".join([f"{s['row_name']}{s['seat_number']}" for s in booking_details.get('seats', [])]),
            'num_snacks': len(booking_details.get('snacks', [])),
            'ticket_amount': Utils.format_currency(booking_details.get('total_ticket_amount', 0)),
            'snack_amount': Utils.format_currency(booking_details.get('total_snack_amount', 0)),
            'total_amount': Utils.format_currency(booking_details.get('total_amount', 0)),
            'payment_method': booking_details.get('payment_method', 'N/A').upper(),
            'payment_status': booking_details.get('payment_status', 'N/A').upper()
        }
