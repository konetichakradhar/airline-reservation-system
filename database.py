import mysql.connector
from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Chakri@2004",
    database="airline_db"
)

cursor = db.cursor()

def get_flights():
    cursor.execute("SELECT * FROM flights")
    return cursor.fetchall()

def add_booking(passenger_name, flight_id, username):

    query = """
    INSERT INTO bookings
    (passenger_name, flight_id, username, status)
    VALUES(%s,%s,%s,%s)
    """

    cursor.execute(
        query,
        (passenger_name, flight_id, username, "Confirmed")
    )

    db.commit()

    return cursor.lastrowid


def get_bookings():

    cursor.execute("SELECT * FROM bookings")
    return cursor.fetchall()

def update_seats(flight_id):

    query = """
    UPDATE flights
    SET seats = seats - 1
    WHERE flight_id = %s
    """

    cursor.execute(query, (flight_id,))
    db.commit()

def get_flight(flight_id):

    query = """
    SELECT * FROM flights
    WHERE flight_id = %s
    """

    cursor.execute(query, (flight_id,))
    return cursor.fetchone()

def delete_booking(booking_id):

    query = """
    DELETE FROM bookings
    WHERE booking_id = %s
    """

    cursor.execute(query, (booking_id,))
    db.commit()
def increase_seat(flight_id):

    query = """
    UPDATE flights
    SET seats = seats + 1
    WHERE flight_id = %s
    """

    cursor.execute(query, (flight_id,))
    db.commit()

def cancel_booking(booking_id):

    query = """
    UPDATE bookings
    SET status='Cancelled'
    WHERE booking_id=%s
    """

    cursor.execute(query, (booking_id,))
    db.commit()


def get_booking(booking_id):

    query = """
    SELECT * FROM bookings
    WHERE booking_id = %s
    """

    cursor.execute(query, (booking_id,))
    return cursor.fetchone()

def register_user(username, password):

    hashed_password = generate_password_hash(password)

    query = """
    INSERT INTO users(username, password, role)
    VALUES(%s, %s, %s)
    """

    cursor.execute(query, (username, hashed_password, "user"))
    db.commit()

def login_user(username, password):

    query = """
    SELECT * FROM users
    WHERE username=%s
    """

    cursor.execute(query, (username,))
    user = cursor.fetchone()

    if user and check_password_hash(user[2], password):
        return user

    return None

def search_flights(source, destination, flight_date):

    query = """
    SELECT *
    FROM flights
    WHERE LOWER(source)=LOWER(%s)
      AND LOWER(destination)=LOWER(%s)
      AND flight_date=%s
    """

    cursor.execute(
        query,
        (source, destination, flight_date)
    )

    return cursor.fetchall()

def get_user_bookings(username):

    query = """
    SELECT
        b.booking_id,
        b.passenger_name,
        b.flight_id,
        f.source,
        f.destination,
        f.flight_date
    FROM bookings b
    JOIN flights f
        ON b.flight_id = f.flight_id
    WHERE b.username=%s
    """

    cursor.execute(query, (username,))
    return cursor.fetchall()

def get_all_flights():
    cursor.execute("SELECT * FROM flights")
    return cursor.fetchall()

def add_flight(flight_id, source, destination, seats, flight_date):

    query = """
    INSERT INTO flights(flight_id, source, destination, seats, flight_date)
    VALUES(%s, %s, %s, %s, %s)
    """

    cursor.execute(
        query,
        (flight_id, source, destination, seats, flight_date)
    )

    db.commit()

def update_flight(flight_id, source, destination, seats):

    query = """
    UPDATE flights
    SET source=%s, destination=%s, seats=%s
    WHERE flight_id=%s
    """

    cursor.execute(query, (source, destination, seats, flight_id))
    db.commit()


def get_flight_by_id(flight_id):

    query = """
    SELECT * FROM flights
    WHERE flight_id=%s
    """

    cursor.execute(query, (flight_id,))
    return cursor.fetchone()

def delete_flight(flight_id):

    query = """
    DELETE FROM flights
    WHERE flight_id=%s
    """
    
    cursor.execute(query, (flight_id,))
    db.commit()


def total_flights():
    cursor.execute("SELECT COUNT(*) FROM flights")
    return cursor.fetchone()[0]


def total_users():
    cursor.execute("SELECT COUNT(*) FROM users")
    return cursor.fetchone()[0]


def total_bookings():
    cursor.execute("SELECT COUNT(*) FROM bookings")
    return cursor.fetchone()[0]


def total_available_seats():
    cursor.execute("SELECT SUM(seats) FROM flights")
    result = cursor.fetchone()[0]
    return result if result else 0

def get_booking_details(booking_id):

    query = """
    SELECT
        bookings.booking_id,
        bookings.passenger_name,
        flights.flight_id,
        flights.source,
        flights.destination
    FROM bookings
    JOIN flights
        ON bookings.flight_id = flights.flight_id
    WHERE booking_id=%s
    """

    cursor.execute(query, (booking_id,))
    return cursor.fetchone()

def get_users():

    cursor.execute("""
    SELECT user_id, username, role
    FROM users
    """)

    return cursor.fetchall()


def get_user(username):

    query = """
    SELECT username, role
    FROM users
    WHERE username=%s
    """

    cursor.execute(query,(username,))

    return cursor.fetchone()

def bookings_chart():

    query = """

    SELECT destination,

    COUNT(*)

    FROM bookings b

    JOIN flights f

    ON b.flight_id=f.flight_id

    GROUP BY destination

    """

    cursor.execute(query)

    return cursor.fetchall()

def get_booking_history(username):

    query = """
    SELECT
        b.booking_id,
        b.passenger_name,
        b.flight_id,
        f.source,
        f.destination,
        f.flight_date,
        b.status
    FROM bookings b
    JOIN flights f
        ON b.flight_id = f.flight_id
    WHERE b.username=%s
    ORDER BY b.booking_id DESC
    """

    cursor.execute(query, (username,))
    return cursor.fetchall()

def cancel_booking_status(booking_id):

    query = """
    UPDATE bookings
    SET status='Cancelled'
    WHERE booking_id=%s
    """

    cursor.execute(query, (booking_id,))
    db.commit()

def profile_stats(username):

    query = """
    SELECT
        COUNT(*) AS total,
        SUM(CASE WHEN status='Confirmed' THEN 1 ELSE 0 END),
        SUM(CASE WHEN status='Cancelled' THEN 1 ELSE 0 END)
    FROM bookings
    WHERE username=%s
    """

    cursor.execute(query,(username,))
    return cursor.fetchone()