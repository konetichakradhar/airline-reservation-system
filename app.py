from flask import Flask, render_template, request, redirect, flash
from database import get_flights, add_booking, update_seats, get_flight
from database import get_bookings
from database import get_booking
from database import delete_booking
from database import increase_seat
from database import register_user
from flask import session
from database import login_user, profile_stats
from database import search_flights
from database import get_user_bookings
from database import get_all_flights
from database import add_flight
from database import update_flight, get_flight_by_id
from database import delete_flight,cancel_booking_status
from database import get_users,get_user, get_booking_history
from database import (
    total_flights,
    total_users,
    total_bookings,
    total_available_seats
)
from flask import send_file
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from database import get_booking_details

app = Flask(__name__)
import os
from dotenv import load_dotenv

load_dotenv()

app.secret_key = os.getenv("SECRET_KEY")

@app.route('/')
def home():

    return render_template(
        "home.html",
        flights=total_flights(),
        users=total_users(),
        bookings=total_bookings(),
        seats=total_available_seats()
    )

@app.route('/flights')
def flights():
    flight_list = get_flights()
    return render_template("flights.html", flights=flight_list)


@app.route('/book/<flight_id>', methods=['GET', 'POST'])
def book(flight_id):

    if 'user' not in session:
        flash("Please login first.", "warning")
        return redirect('/login')

    flight = get_flight(flight_id)

    if flight is None:
        flash("Flight not found.", "danger")
        return redirect('/flights')

    if flight[3] <= 0:
        flash("No seats available.", "danger")
        return redirect('/flights')

    if request.method == 'POST':

        passenger_name = request.form['name']

        if passenger_name.strip() == "":
            flash("Passenger name cannot be empty.", "danger")
            return redirect(request.url)

        booking_id = add_booking(
        passenger_name,
        flight_id,
        session['user']
        )

        update_seats(flight_id)

        return render_template(
        "confirmation.html",
        booking_id=booking_id,
        passenger=passenger_name,
        flight=flight
        )

    return render_template(
        "book.html",
        flight=flight
    )



@app.route('/bookings')
def bookings():

    if 'user' not in session:
        return redirect('/login')

    username = session['user']

    booking_list = get_user_bookings(username)

    return render_template(
        "bookings.html",
        bookings=booking_list
    )


@app.route('/cancel/<int:booking_id>')
def cancel_booking(booking_id):

    booking = get_booking(booking_id)

    if booking is None:
        flash("Booking not found.", "danger")
        return redirect('/bookings')

    if booking[3] != session['user']:
        flash("Unauthorized.", "danger")
        return redirect('/bookings')

    flight_id = booking[2]

    # Increase seat count
    increase_seat(flight_id)

    # Change booking status
    cancel_booking_status(booking_id)

    flash("Booking cancelled successfully.", "success")
    return redirect('/history')

@app.route('/register', methods=['GET', 'POST'])
def register():

    if request.method == 'POST':

        username = request.form['username']
        password = request.form['password']

        try:
            register_user(username, password)

            flash("Registration Successful!", "success")

            return redirect('/login')

        except Exception:
            flash("Username already exists!", "danger")
            return redirect('/register')

    return render_template("register.html")


@app.route('/login', methods=['GET', 'POST'])
def login():

    if request.method == 'POST':

        username = request.form['username']
        password = request.form['password']

        user = login_user(username, password)

        if user:

            session['user'] = username
            session['role'] = user[3]

            flash("Welcome " + username + "!", "success")

            return redirect('/')

        flash("Invalid Username or Password!", "danger")

        return redirect('/login')

    return render_template("login.html")

@app.route('/logout')
def logout():

    session.pop('user', None)
    session.pop('role', None)
    session.clear()
    flash("Logged out successfully.", "info")

    return redirect('/')

@app.route('/search', methods=['GET', 'POST'])
def search():

    flights = []
    searched = False
    source = ""
    destination = ""
    flight_date = ""

    if request.method == 'POST':

        searched = True

        source = request.form['source']
        destination = request.form['destination']
        flight_date = request.form['flight_date']

        flights = search_flights(
            source,
            destination,
            flight_date
        )

    return render_template(
        "search.html",
        flights=flights,
        searched=searched,
        source=source,
        destination=destination,
        flight_date=flight_date
    )


@app.route('/admin')
def admin():

    if 'user' not in session:
        return redirect('/login')

    if session.get('role') != 'admin':
        return "Access Denied"

    return render_template(
        "admin.html",
        flights=total_flights(),
        users=total_users(),
        bookings=total_bookings(),
        seats=total_available_seats()
    )


@app.route('/admin/flights')
def admin_flights():

    if 'user' not in session:
        return redirect('/login')

    if session.get('role') != 'admin':
        return "Access Denied"

    flights = get_all_flights()

    return render_template(
        "admin_flights.html",
        flights=flights
    )

@app.route('/admin/add-flight', methods=['GET', 'POST'])
def add_new_flight():

    if 'user' not in session:
        return redirect('/login')

    if session.get('role') != 'admin':
        return "Access Denied"

    if request.method == 'POST':
        
        flight_id = request.form['flight_id']
        source = request.form['source']
        destination = request.form['destination']
        seats = request.form['seats']
        existing = get_flight(flight_id)
        date = request.form['Date']

        if existing:
            flash("Flight ID already exists.", "danger")
            return redirect('/admin/add-flight')
        if int(seats) <= 0:
            flash("Seats must be greater than zero.","danger")

        add_flight(flight_id, source, destination, seats, date)

        return redirect('/admin/flights')

    return render_template("add_flight.html")

@app.route('/admin/edit-flight/<flight_id>', methods=['GET', 'POST'])
def edit_flight(flight_id):

    if 'user' not in session:
        return redirect('/login')

    if session.get('role') != 'admin':
        return "Access Denied"

    flight = get_flight_by_id(flight_id)

    if request.method == 'POST':

        source = request.form['source']
        destination = request.form['destination']
        seats = request.form['seats']

        update_flight(
            flight_id,
            source,
            destination,
            seats
        )

        return redirect('/admin/flights')

    return render_template(
        "edit_flight.html",
        flight=flight
    )

@app.route('/admin/delete-flight/<flight_id>')
def admin_delete_flight(flight_id):

    if 'user' not in session:
        return redirect('/login')

    if session.get('role') != 'admin':
        return "Access Denied"

    delete_flight(flight_id)

    return redirect('/admin/flights')

@app.route('/ticket/<int:booking_id>')
def download_ticket(booking_id):

    booking = get_booking_details(booking_id)

    if booking is None:
        return "Booking Not Found"

    filename = f"ticket_{booking_id}.pdf"

    pdf = SimpleDocTemplate(filename)

    styles = getSampleStyleSheet()

    elements = []

    elements.append(Paragraph("<b>AIRLINE RESERVATION SYSTEM</b>", styles["Title"]))
    elements.append(Paragraph(f"Booking ID : {booking[0]}", styles["Normal"]))
    elements.append(Paragraph(f"Passenger : {booking[1]}", styles["Normal"]))
    elements.append(Paragraph(f"Flight ID : {booking[2]}", styles["Normal"]))
    elements.append(Paragraph(f"Source : {booking[3]}", styles["Normal"]))
    elements.append(Paragraph(f"Destination : {booking[4]}", styles["Normal"]))
    elements.append(Paragraph("Status : Confirmed", styles["Normal"]))

    pdf.build(elements)

    return send_file(
        filename,
        as_attachment=True
    )

@app.route("/profile")
def profile():

    if "user" not in session:
        return redirect("/login")

    user = get_user(session["user"])
    stats = profile_stats(session["user"])

    return render_template(
        "profile.html",
        user=user,
        stats=stats
    )

@app.route('/admin/bookings')
def admin_bookings():

    if session.get('role') != 'admin':
        return "Access Denied"

    bookings = get_bookings()

    return render_template(
        "admin_bookings.html",
        bookings=bookings
    )

@app.route('/admin/users')
def admin_users():

    if session.get('role') != 'admin':
        return "Access Denied"

    users = get_users()

    return render_template(
        "admin_users.html",
        users=users
    )

@app.route('/history')
def history():

    if 'user' not in session:
        flash("Please login first.", "warning")
        return redirect('/login')

    username = session['user']

    history = get_booking_history(username)
    print(history)

    return render_template(
        "history.html",
        history=history
    )


if __name__ == "__main__":
    app.run(debug=True)