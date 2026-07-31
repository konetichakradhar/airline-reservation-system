from Flight import Flight
from database import get_flights
from database import add_booking
from database import get_bookings

flights = [
    Flight("101", "Hyderabad", "Delhi", 50),
    Flight("102", "Chennai", "Mumbai", 40),
    Flight("103", "Bangalore", "Kolkata", 30)
]

bookings = []

def view_flights():

    flights = get_flights()

    print("\nAvailable Flights")

    for flight in flights:
        print(
            "Flight ID:", flight[0],
            "| Source:", flight[1],
            "| Destination:", flight[2],
            "| Seats:", flight[3]
        )

from Booking import Booking
from database import update_seats
from database import get_flight

def book_ticket():

    name = input("Enter Passenger Name: ")
    flight_id = input("Enter Flight ID: ")

    flight = get_flight(flight_id)

    if flight is None:
        print("Flight Not Found")
        return

    if flight[3] <= 0:
        print("No Seats Available")
        return

    add_booking(name, flight_id)
    update_seats(flight_id)

    print("Ticket Booked Successfully")


def view_bookings():


    bookings = get_bookings()

    if len(bookings) == 0:
        print("No Bookings Found")
        return

    for booking in bookings:

        print(
            "Booking ID:", booking[0],
            "| Passenger:", booking[1],
            "| Flight ID:", booking[2]
        )

from database import get_booking
from database import delete_booking
from database import increase_seat

def cancel_booking():

    booking_id = input("Enter Booking ID: ")

    booking = get_booking(booking_id)

    if booking is None:
        print("Booking Not Found")
        return

    flight_id = booking[2]

    delete_booking(booking_id)

    increase_seat(flight_id)

    print("Booking Cancelled Successfully")


from database import register_user
from database import login_user

def register():

    username = input("Enter Username: ")
    password = input("Enter Password: ")

    try:
        register_user(username, password)
        print("Registration Successful")

    except:
        print("Username Already Exists")

def login():

    username = input("Enter Username: ")
    password = input("Enter Password: ")

    user = login_user(username, password)

    if user:
        print("Login Successful")
        return True

    print("Invalid Username or Password")
    return False


while True:

    print("\n==============================")
    print(" AIRLINE RESERVATION SYSTEM ")
    print("==============================")
    print("1. Register")
    print("2. Login")
    print("3. View Flights")
    print("4. Book Ticket")
    print("5. View Bookings")
    print("6. Cancel Booking")
    print("7. Exit")

    choice = input("Enter Choice: ")

    if choice == "1":
        register()

    elif choice == "2":
        login()

    elif choice == "3":
        view_flights()

    elif choice == "4":
        book_ticket()

    elif choice == "5":
        view_bookings()

    elif choice == "6":
        cancel_booking()

    elif choice == "7":
        print("Thank You")
        break

    else:
        print("Invalid Choice")