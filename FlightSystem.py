import tkinter as tk
from tkinter import messagebox

# Sample flight data stored in lists
flights = [
    {"flight_number": "MY101", "departure": "Malaysia", "destination": "Maldives", "date": "2025-02-15", "available_seats": 50},
    {"flight_number": "MY102", "departure": "Malaysia", "destination": "South Korea", "date": "2025-02-16", "available_seats": 30},
    {"flight_number": "MY103", "departure": "Malaysia", "destination": "Japan", "date": "2025-02-17", "available_seats": 40},
    {"flight_number": "MY104", "departure": "Malaysia", "destination": "Thailand", "date": "2025-02-18", "available_seats": 25},
    {"flight_number": "MY105", "departure": "Malaysia", "destination": "Vietnam", "date": "2025-02-19", "available_seats": 35}
]

booked_flights = []

# Flight details 
seat_prices = {"Economy": 300, "Business": 700, "First Class": 1500}
destination_details = {
    "Maldives": {"tax_rate": 0.67, "air_miles": 3191, "insurance": 500},
    "South Korea": {"tax_rate": 0.80, "air_miles": 4402, "insurance": 700},
    "Japan": {"tax_rate": 0.85, "air_miles": 5134, "insurance": 800},
    "Thailand": {"tax_rate": 0.50, "air_miles": 1688.4, "insurance": 300},
    "Vietnam": {"tax_rate": 0.50, "air_miles": 2412.8, "insurance": 400}
}
accommodation_prices = {
    "7 days 6 nights": 3000, 
    "10 days 9 nights": 7000, 
    "15 days 14 nights": 9000
}

# User data for sign-up and login
users = {}

# Function to list all available flights
def list_flights():
    flight_list_text.delete(1.0, tk.END)  # Clear previous text
    if not flights:
        flight_list_text.insert(tk.END, "No flights available.\n")
    for flight in flights:
        flight_info = f"Flight {flight['flight_number']} | {flight['departure']} -> {flight['destination']} | Date: {flight['date']} | Available Seats: {flight['available_seats']}\n"
        flight_list_text.insert(tk.END, flight_info)

# Function to search for flights by departure and destination
def search_flight():
    departure = "Malaysia"
    destination = entry_destination.get()
    available_flights = [
        flight for flight in flights 
        if flight['departure'] == departure and flight['destination'] == destination
    ]

    flight_list_text.delete(1.0, tk.END)  # Clear previous text
    flight_selection_menu['menu'].delete(0, 'end')  # Clear previous flight options

    if not available_flights:
        flight_list_text.insert(tk.END, f"No available flights from {departure} to {destination}.\n")
    else:
        for flight in available_flights:
            flight_info = f"Flight {flight['flight_number']} | {flight['departure']} -> {flight['destination']} | Date: {flight['date']} | Available Seats: {flight['available_seats']}\n"
            flight_list_text.insert(tk.END, flight_info)
            flight_selection_menu['menu'].add_command(label=flight['flight_number'], command=tk._setit(selected_flight, flight['flight_number']))

# Function to calculate total cost based on selection
def calculate_cost(seat_class, destination, accommodation, extra_luggage):
    seat_price = seat_prices.get(seat_class, 0)
    destination_info = destination_details.get(destination, {"tax_rate": 0, "air_miles": 0, "insurance": 0})
    insurance = destination_info["insurance"]
    accommodation_price = accommodation_prices.get(accommodation, 0)
    
    total_cost = seat_price + accommodation_price + insurance
    if extra_luggage == "Yes":
        total_cost += 50  # Adding RM50 for extra luggage
    return total_cost

# Function to book a flight
def book_flight():
    flight_number = selected_flight.get()
    seat_class = entry_seat_class.get()  # Seat class input
    destination = entry_destination.get()
    accommodation = entry_accommodation.get()  # Accommodation input
    extra_luggage = entry_extra_luggage.get()  # Extra luggage input
    
    flight = next((flight for flight in flights if flight['flight_number'] == flight_number), None)
    
    if flight:
        if flight['available_seats'] > 0:
            flight['available_seats'] -= 1
            booked_flights.append(flight)
            
            # Calculate total cost
            total_cost = calculate_cost(seat_class, destination, accommodation, extra_luggage)
            messagebox.showinfo("Booking Successful", f"Successfully booked flight {flight_number}. Total cost: RM{total_cost}.")
        else:
            messagebox.showerror("Booking Failed", f"Sorry, no seats available for flight {flight_number}.")
    else:
        messagebox.showerror("Booking Failed", f"Flight number {flight_number} not found.")

# Function to cancel a flight
def cancel_flight():
    flight_number = selected_flight.get()
    flight = next((flight for flight in booked_flights if flight['flight_number'] == flight_number), None)
    if flight:
        flight['available_seats'] += 1
        booked_flights.remove(flight)
        messagebox.showinfo("Cancellation Successful", f"Successfully canceled flight {flight_number}.")
    else:
        messagebox.showerror("Cancellation Failed", f"You do not have a booking for flight {flight_number}.")

# Function to view booked flights
def view_booked_flights():
    booked_flights_text.delete(1.0, tk.END)  # Clear previous text
    if not booked_flights:
        booked_flights_text.insert(tk.END, "You have no booked flights.\n")
    else:
        for flight in booked_flights:
            flight_info = f"Flight {flight['flight_number']} | {flight['departure']} -> {flight['destination']} | Date: {flight['date']}\n"
            booked_flights_text.insert(tk.END, flight_info)

# Function to handle user sign-up
def sign_up():
    username = entry_signup_username.get()
    password = entry_signup_password.get()
    
    if username in users:
        messagebox.showerror("Sign Up Failed", "Username already exists.")
    else:
        users[username] = password
        messagebox.showinfo("Sign Up Successful", "You have successfully signed up.")

# Function to handle user login
def login():
    username = entry_login_username.get()
    password = entry_login_password.get()
    
    if username in users and users[username] == password:
        messagebox.showinfo("Login Successful", f"Welcome, {username}!")
        show_main_menu()
    else:
        messagebox.showerror("Login Failed", "Invalid username or password.")

# Function to show the main menu after login
def show_main_menu():
    # Hide login/signup frame and show the main system interface
    frame_login_signup.grid_forget()
    frame_main_menu.grid(row=0, column=0, padx=10, pady=10)

# Function to update an existing booking
def update_booking():
    flight_number = selected_flight.get()
    seat_class = entry_seat_class.get()  # Seat class input
    destination = entry_destination.get()
    accommodation = entry_accommodation.get()  # Accommodation input
    extra_luggage = entry_extra_luggage.get()  # Extra luggage input
    
    # Find the booked flight
    flight = next((flight for flight in booked_flights if flight['flight_number'] == flight_number), None)
    
    if flight:
        # Calculate the updated total cost based on new selections
        total_cost = calculate_cost(seat_class, destination, accommodation, extra_luggage)
        
        # Display the updated total cost in the receipt (text box)
        receipt_text = (
            f"Booking Updated:\n"
            f"Flight Number: {flight_number}\n"
            f"Seat Class: {seat_class}\n"
            f"Destination: {destination}\n"
            f"Accommodation: {accommodation}\n"
            f"Extra Luggage: {extra_luggage}\n"
            f"Total Cost: RM{total_cost}\n"
        )
        
        # Update the receipt text box with the new details
        booked_flights_text.delete(1.0, tk.END)  # Clear previous text
        booked_flights_text.insert(tk.END, receipt_text)  # Insert the new receipt info
        
        messagebox.showinfo("Booking Updated", f"Successfully updated your flight {flight_number}. New total cost: RM{total_cost}.")
    else:
        messagebox.showerror("Update Failed", f"You do not have a booking for flight {flight_number}.")

# Set up the tkinter window
root = tk.Tk()
root.title("Flight Reservation System")

# Frame for Login and Sign-up
frame_login_signup = tk.Frame(root)
frame_login_signup.grid(row=0, column=0, padx=10, pady=10)

label_login_heading = tk.Label(frame_login_signup, text="Login / Sign Up", font=("Arial", 16))
label_login_heading.grid(row=0, column=0, columnspan=2, pady=10)

# Sign-up section
label_signup_username = tk.Label(frame_login_signup, text="Username:")
label_signup_username.grid(row=1, column=0, padx=10, pady=5)
entry_signup_username = tk.Entry(frame_login_signup)
entry_signup_username.grid(row=1, column=1, padx=10, pady=5)

label_signup_password = tk.Label(frame_login_signup, text="Password:")
label_signup_password.grid(row=2, column=0, padx=10, pady=5)
entry_signup_password = tk.Entry(frame_login_signup, show="*")
entry_signup_password.grid(row=2, column=1, padx=10, pady=5)

button_signup = tk.Button(frame_login_signup, text="Sign Up", command=sign_up)
button_signup.grid(row=3, column=0, columnspan=2, pady=10)

# Login section
label_login_username = tk.Label(frame_login_signup, text="Username:")
label_login_username.grid(row=4, column=0, padx=10, pady=5)
entry_login_username = tk.Entry(frame_login_signup)
entry_login_username.grid(row=4, column=1, padx=10, pady=5)

label_login_password = tk.Label(frame_login_signup, text="Password:")
label_login_password.grid(row=5, column=0, padx=10, pady=5)
entry_login_password = tk.Entry(frame_login_signup, show="*")
entry_login_password.grid(row=5, column=1, padx=10, pady=5)

button_login = tk.Button(frame_login_signup, text="Login", command=login)
button_login.grid(row=6, column=0, columnspan=2, pady=10)

# Frame for Main Menu (after login)
frame_main_menu = tk.Frame(root)

label_heading = tk.Label(frame_main_menu, text="Flight Reservation System", font=("Arial", 16))
label_heading.grid(row=0, column=0, columnspan=2, pady=10)

# Input fields for search and booking
label_departure = tk.Label(frame_main_menu, text="Departure City:")
label_departure.grid(row=1, column=0, padx=10, pady=5)
entry_departure = tk.Entry(frame_main_menu)
entry_departure.insert(0, "Malaysia")
entry_departure.config(state="disabled")
entry_departure.grid(row=1, column=1, padx=10, pady=5)

label_destination = tk.Label(frame_main_menu, text="Destination City:")
label_destination.grid(row=2, column=0, padx=10, pady=5)
entry_destination = tk.StringVar()
destination_menu = tk.OptionMenu(frame_main_menu, entry_destination, "Maldives", "South Korea", "Japan", "Thailand", "Vietnam")
destination_menu.grid(row=2, column=1, padx=10, pady=5)

label_seat_class = tk.Label(frame_main_menu, text="Seat Class:")
label_seat_class.grid(row=3, column=0, padx=10, pady=5)
entry_seat_class = tk.StringVar()
seat_class_menu = tk.OptionMenu(frame_main_menu, entry_seat_class, "Economy", "Business", "First Class")
seat_class_menu.grid(row=3, column=1, padx=10, pady=5)

label_accommodation = tk.Label(frame_main_menu, text="Accommodation:")
label_accommodation.grid(row=4, column=0, padx=10, pady=5)
entry_accommodation = tk.StringVar()
accommodation_menu = tk.OptionMenu(frame_main_menu, entry_accommodation, "7 days 6 nights", "10 days 9 nights", "15 days 14 nights")
accommodation_menu.grid(row=4, column=1, padx=10, pady=5)

label_extra_luggage = tk.Label(frame_main_menu, text="Extra Luggage (Yes/No):")
label_extra_luggage.grid(row=5, column=0, padx=10, pady=5)
entry_extra_luggage = tk.StringVar()
extra_luggage_menu = tk.OptionMenu(frame_main_menu, entry_extra_luggage, "Yes", "No")
extra_luggage_menu.grid(row=5, column=1, padx=10, pady=5)

# Buttons for Main Menu
button_search = tk.Button(frame_main_menu, text="Search Flights", command=search_flight)
button_search.grid(row=6, column=0, columnspan=2, pady=5)

label_flight_number = tk.Label(frame_main_menu, text="Select Flight:")
label_flight_number.grid(row=7, column=0, padx=10, pady=5)
selected_flight = tk.StringVar()
flight_selection_menu = tk.OptionMenu(frame_main_menu, selected_flight, "")
flight_selection_menu.grid(row=7, column=1, padx=10, pady=5)

button_book = tk.Button(frame_main_menu, text="Book Flight", command=book_flight)
button_book.grid(row=8, column=0, padx=10, pady=5)

button_cancel = tk.Button(frame_main_menu, text="Cancel Flight", command=cancel_flight)
button_cancel.grid(row=8, column=1, padx=10, pady=5)

button_update = tk.Button(frame_main_menu, text="Update Booking", command=update_booking)
button_update.grid(row=9, column=0, padx=10, pady=5)

button_view_booked = tk.Button(frame_main_menu, text="View Booked Flights", command=view_booked_flights)
button_view_booked.grid(row=9, column=1, padx=10, pady=5)

button_list_flights = tk.Button(frame_main_menu, text="List All Flights", command=list_flights)
button_list_flights.grid(row=10, column=1, padx=10, pady=5)

# Text box for flight details
flight_list_text = tk.Text(frame_main_menu, height=10, width=50)
flight_list_text.grid(row=11, column=0, columnspan=2, padx=10, pady=10)
booked_flights_text = tk.Text(frame_main_menu, height=10, width=50)
booked_flights_text.grid(row=12, column=0, columnspan=2, padx=10, pady=10)

# Start the tkinter main loop
root.mainloop()
