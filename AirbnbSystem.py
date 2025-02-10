import tkinter as tk
from tkinter import messagebox

# Sample property data stored
properties = [
    {"property_id": "P001", "location": "Maldives", "type": "Resort", "price_per_night": 300, "available_dates": ["2025-02-01", "2025-02-02", "2025-02-03"], "available_rooms": 3},
    {"property_id": "P002", "location": "South Korea", "type": "Apartment", "price_per_night": 500, "available_dates": ["2025-03-05", "2025-03-06", "2025-03-07"], "available_rooms": 4},
    {"property_id": "P003", "location": "Japan", "type": "House", "price_per_night": 200, "available_dates": ["2025-04-10", "2025-04-11", "2025-04-12"], "available_rooms": 5},
    {"property_id": "P004", "location": "Thailand", "type": "Hotel", "price_per_night": 400, "available_dates": ["2025-05-01", "2025-05-02", "2025-05-03"], "available_rooms": 3},
    {"property_id": "P005", "location": "Vietnam", "type": "Homestay", "price_per_night": 300, "available_dates": ["2025-06-01", "2025-06-02", "2025-06-03"], "available_rooms": 3}
]

booked_properties = []

# Function to list all available properties
def list_properties():
    properties_text.delete(1.0, tk.END)  # Clear previous text
    if not properties:
        properties_text.insert(tk.END, "No properties available.\n")
    for property in properties:
        property_info = f"Property {property['property_id']} | Location: {property['location']} | Type: {property['type']} | Price: ${property['price_per_night']}/night | Rooms Available: {property['available_rooms']}\n"
        properties_text.insert(tk.END, property_info)

# Function to search for properties by location and type
def search_properties():
    location = entry_location.get()
    property_type = entry_property_type.get()
    
    available_properties = [property for property in properties if property['location'] == location and property['type'].lower() == property_type.lower()]
    
    properties_text.delete(1.0, tk.END)  # Clear previous text
    if not available_properties:
        properties_text.insert(tk.END, f"No available properties found in {location} of type {property_type}.\n")
    else:
        for property in available_properties:
            property_info = f"Property {property['property_id']} | Location: {property['location']} | Type: {property['type']} | Price: ${property['price_per_night']}/night | Rooms Available: {property['available_rooms']}\n"
            properties_text.insert(tk.END, property_info)

# Function to book a property
def book_property():
    property_id = entry_property_id.get()
    check_in_date = entry_check_in.get()
    check_out_date = entry_check_out.get()
    
    property = next((property for property in properties if property['property_id'] == property_id), None)
    if property:
        if property['available_rooms'] > 0 and check_in_date in property['available_dates'] and check_out_date in property['available_dates']:
            property['available_rooms'] -= 1
            booked_properties.append({"property_id": property_id, "check_in": check_in_date, "check_out": check_out_date})
            messagebox.showinfo("Booking Successful", f"Successfully booked property {property_id} from {check_in_date} to {check_out_date}.")
        else:
            messagebox.showerror("Booking Failed", f"Sorry, no available rooms for this property or invalid dates.")
    else:
        messagebox.showerror("Booking Failed", f"Property ID {property_id} not found.")

# Function to cancel a booking
def cancel_booking():
    property_id = entry_property_id.get()
    
    booking = next((booking for booking in booked_properties if booking['property_id'] == property_id), None)
    if booking:
        booked_properties.remove(booking)
        # Find the booked property and increase the room count
        property = next((property for property in properties if property['property_id'] == property_id), None)
        if property:
            property['available_rooms'] += 1
        messagebox.showinfo("Cancellation Successful", f"Successfully canceled booking for property {property_id}.")
    else:
        messagebox.showerror("Cancellation Failed", f"No booking found for property ID {property_id}.")

# Function to view all booked properties
def view_booked_properties():
    booked_properties_text.delete(1.0, tk.END)  # Clear previous text
    if not booked_properties:
        booked_properties_text.insert(tk.END, "You have no booked properties.\n")
    else:
        for booking in booked_properties:
            booked_property_info = f"Property ID: {booking['property_id']} | Check-in: {booking['check_in']} | Check-out: {booking['check_out']}\n"
            booked_properties_text.insert(tk.END, booked_property_info)

# Set up the tkinter window
root = tk.Tk()
root.title("Airbnb Booking System")

# Create and place the widgets in the window
label_heading = tk.Label(root, text="Airbnb Booking System", font=("Arial", 16))
label_heading.grid(row=0, column=0, columnspan=2, pady=10)

# Input fields for search and booking
label_location = tk.Label(root, text="Location:")
label_location.grid(row=1, column=0, padx=10, pady=5)
entry_location = tk.Entry(root)
entry_location.grid(row=1, column=1, padx=10, pady=5)

label_property_type = tk.Label(root, text="Property Type:")
label_property_type.grid(row=2, column=0, padx=10, pady=5)
entry_property_type = tk.Entry(root)
entry_property_type.grid(row=2, column=1, padx=10, pady=5)

label_property_id = tk.Label(root, text="Property ID:")
label_property_id.grid(row=3, column=0, padx=10, pady=5)
entry_property_id = tk.Entry(root)
entry_property_id.grid(row=3, column=1, padx=10, pady=5)

label_check_in = tk.Label(root, text="Check-in Date (YYYY-MM-DD):")
label_check_in.grid(row=4, column=0, padx=10, pady=5)
entry_check_in = tk.Entry(root)
entry_check_in.grid(row=4, column=1, padx=10, pady=5)

label_check_out = tk.Label(root, text="Check-out Date (YYYY-MM-DD):")
label_check_out.grid(row=5, column=0, padx=10, pady=5)
entry_check_out = tk.Entry(root)
entry_check_out.grid(row=5, column=1, padx=10, pady=5)

# Buttons
button_search = tk.Button(root, text="Search Properties", command=search_properties)
button_search.grid(row=6, column=0, padx=10, pady=5)

button_book = tk.Button(root, text="Book Property", command=book_property)
button_book.grid(row=6, column=1, padx=10, pady=5)

button_cancel = tk.Button(root, text="Cancel Booking", command=cancel_booking)
button_cancel.grid(row=7, column=0, padx=10, pady=5)

button_view_booked = tk.Button(root, text="View Booked Properties", command=view_booked_properties)
button_view_booked.grid(row=7, column=1, padx=10, pady=5)

button_list_properties = tk.Button(root, text="List All Properties", command=list_properties)
button_list_properties.grid(row=8, column=0, columnspan=2, pady=10)

# Text box for property details
properties_text = tk.Text(root, height=10, width=50)
properties_text.grid(row=9, column=0, columnspan=2, padx=10, pady=10)

booked_properties_text = tk.Text(root, height=10, width=50)
booked_properties_text.grid(row=10, column=0, columnspan=2, padx=10, pady=10)

# Start the tkinter main loop
root.mainloop()
