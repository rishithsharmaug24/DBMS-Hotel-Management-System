# ===============================================
#  Hotel Management System - Flask Application
# ===============================================

from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from database.queries import get_dashboard_stats, get_recent_bookings
import os

# -----------------------
# Flask App Configuration
# -----------------------
app = Flask(
    __name__,
    template_folder="frontend/templates",
    static_folder="frontend/static"
)
app.secret_key = os.getenv("SECRET_KEY", "super_secret_key")

# -----------------------
# Helper Functions
# -----------------------
def is_logged_in():
    """Check if user is logged in."""
    return 'username' in session


# -----------------------
# Routes
# -----------------------

@app.route('/')
def home_redirect():
    """Redirect root URL to login or dashboard."""
    if is_logged_in():
        return redirect(url_for('route_dashboard'))
    return redirect(url_for('route_login'))


# -----------------------
# Login Page
# -----------------------
@app.route('/login', methods=['GET', 'POST'])
def route_login():
    """Render login page and handle login form submission."""
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '').strip()

        # For now using static admin login (replace later with DB authentication)
        if username == 'admin' and password == 'admin123':
            session['username'] = username
            return redirect(url_for('route_dashboard'))
        else:
            return render_template('login.html', error="Invalid credentials. Try admin/admin123.")

    return render_template('login.html')


# -----------------------
# Logout
# -----------------------
@app.route('/logout')
def route_logout():
    """Logout the user."""
    session.clear()
    return redirect(url_for('route_login'))


# -----------------------
# Dashboard
# -----------------------
@app.route('/dashboard')
def route_dashboard():
    """Main dashboard view with live data."""
    if not is_logged_in():
        return redirect(url_for('route_login'))

    # Fetch stats and recent bookings from DB
    stats = get_dashboard_stats()
    stats["revenue_days_labels"] = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    stats["revenue_days_data"] = [2100, 2600, 1900, 2500, 3000, 2800, 2200]

    recent_bookings = get_recent_bookings()

    return render_template(
        'dashboard.html',
        stats=stats,
        recent_bookings=recent_bookings,
        user_name=session.get('username')
    )


# -----------------------
# Guests
# -----------------------
@app.route('/guests')
def route_guests():
    if not is_logged_in():
        return redirect(url_for('route_login'))
    return render_template('guests/guest_list.html', user_name=session.get('username'))


@app.route('/guests/register')
def route_register_guest():
    if not is_logged_in():
        return redirect(url_for('route_login'))
    return render_template('guests/register_guest.html', user_name=session.get('username'))


# -----------------------
# Rooms
# -----------------------
@app.route('/rooms')
def route_rooms():
    if not is_logged_in():
        return redirect(url_for('route_login'))
    return render_template('rooms/room_list.html', user_name=session.get('username'))


# -----------------------
# Bookings
# -----------------------
@app.route('/bookings')
def route_bookings():
    if not is_logged_in():
        return redirect(url_for('route_login'))
    return render_template('bookings/booking_list.html', user_name=session.get('username'))


# -----------------------
# Payments
# -----------------------
@app.route('/payments')
def route_payments():
    if not is_logged_in():
        return redirect(url_for('route_login'))
    return render_template('payments/payment_history.html', user_name=session.get('username'))


# -----------------------
# Bills
# -----------------------
@app.route('/bills')
def route_generate_bill():
    if not is_logged_in():
        return redirect(url_for('route_login'))
    return render_template('bills/generate_bill.html', user_name=session.get('username'))


# -----------------------
# Reports
# -----------------------
@app.route('/reports/revenue')
def route_reports_revenue():
    if not is_logged_in():
        return redirect(url_for('route_login'))
    return render_template('reports/revenue_report.html', user_name=session.get('username'))


# -----------------------
# Error Handlers
# -----------------------
@app.errorhandler(404)
def not_found(e):
    """Custom 404 page."""
    return render_template('404.html', error="Page Not Found"), 404


@app.errorhandler(500)
def server_error(e):
    """Custom 500 page."""
    return render_template('500.html', error="Internal Server Error"), 500


# -----------------------
# Main Entry Point
# -----------------------
if __name__ == '__main__':
    print("🚀 Starting Hotel Management System (Flask)")
    print("🔗 Running on: http://127.0.0.1:5000/")
    print("👤 Use credentials: admin / admin123\n")

    app.run(debug=True)
