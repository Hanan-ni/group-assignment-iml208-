import tkinter as tk
from tkinter import messagebox
from tkinter import simpledialog

# List to store bookings
bookings = []

# Menu items and their prices
menu_items = {
    "breakfast meal sets": 50,
    "lunch meal sets": 150,
    "Dinner meal sets": 300,
    "Full meal sets": 850
}

# Dummy users for login/sign-up (In practice, this should be stored securely)
users = {}

# Main window object
root = tk.Tk()
root.geometry("400x300")
root.title("Login")

# Function to show the main booking system interface
def show_booking_system():
    # Clear the window
    for widget in root.winfo_children():
        widget.destroy()

    root.geometry("800x600")
    root.title("Restaurant Booking System")

    # Title Label for Restaurant Management System
    title_label = tk.Label(root, text="Restaurant Management System", font=('Arial', 24), bd=8)
    title_label.pack(pady=20)

    # Booking Form Section
    form_frame = tk.Frame(root)
    form_frame.pack(pady=20)

    # Customer Name
    tk.Label(form_frame, text="Customer Name", font=('Arial', 14)).grid(row=0, column=0, padx=10, pady=10)
    customer_name = tk.Entry(form_frame, font=('Arial', 12))
    customer_name.grid(row=0, column=1, padx=10, pady=10)

    # Phone Number
    tk.Label(form_frame, text="Phone Number", font=('Arial', 14)).grid(row=1, column=0, padx=10, pady=10)
    phone_number = tk.Entry(form_frame, font=('Arial', 12))
    phone_number.grid(row=1, column=1, padx=10, pady=10)

    # Number of People
    tk.Label(form_frame, text="Number of People", font=('Arial', 14)).grid(row=2, column=0, padx=10, pady=10)
    num_people_entry = tk.Entry(form_frame, font=('Arial', 12))
    num_people_entry.grid(row=2, column=1, padx=10, pady=10)

    # Date and Time
    tk.Label(form_frame, text="Date and Time (YYYY-MM-DD HH:MM)", font=('Arial', 14)).grid(row=3, column=0, padx=10, pady=10)
    booking_datetime_entry = tk.Entry(form_frame, font=('Arial', 12))
    booking_datetime_entry.grid(row=3, column=1, padx=10, pady=10)

    # Restaurant Selection
    restaurant_options = [ "The Garden of Eat's", "Rustica Steak House", "The Outer Clove Restaurant", "Coupa Couffee"]
    restaurant_var = tk.StringVar()
    restaurant_var.set(restaurant_options[0])

    tk.Label(form_frame, text="Select Restaurant", font=('Arial', 14)).grid(row=4, column=0, padx=10, pady=10)
    restaurant_menu = tk.OptionMenu(form_frame, restaurant_var, *restaurant_options)
    restaurant_menu.grid(row=4, column=1, padx=10, pady=10)

    # Menu Item Selection
    menu_options = ["Select Menu Item"] + list(menu_items.keys())
    menu_var = tk.StringVar()
    menu_var.set(menu_options[0])

    tk.Label(form_frame, text="Select Menu Item", font=('Arial', 14)).grid(row=5, column=0, padx=10, pady=10)
    menu_menu = tk.OptionMenu(form_frame, menu_var, *menu_options)
    menu_menu.grid(row=5, column=1, padx=10, pady=10)

    # Book Button
    book_button = tk.Button(form_frame, text="Book Table", font=('Arial', 14), command=lambda: book_table(customer_name, phone_number, num_people_entry, booking_datetime_entry, restaurant_var, menu_var))
    book_button.grid(row=6, column=0, columnspan=2, pady=20)

    # View and Cancel Bookings Section
    view_booking_button = tk.Button(root, text="View All Bookings", font=('Arial', 14), command=view_bookings)
    view_booking_button.pack(pady=10)

    cancel_booking_button = tk.Button(root, text="Cancel Booking", font=('Arial', 14), command=cancel_booking)
    cancel_booking_button.pack(pady=10)

    # Update Booking Button
    update_booking_button = tk.Button(root, text="Update Booking", font=('Arial', 14), command=update_booking)
    update_booking_button.pack(pady=10)

# Function to handle user sign-up
def sign_up():
    # Clear the window
    for widget in root.winfo_children():
        widget.destroy()

    root.geometry("400x300")
    root.title("Sign Up")

    # Title Label
    tk.Label(root, text="Sign Up", font=('Arial', 24), bd=8).pack(pady=20)

    # User Input Fields
    tk.Label(root, text="Username", font=('Arial', 14)).pack(pady=10)
    username_entry = tk.Entry(root, font=('Arial', 12))
    username_entry.pack(pady=10)

    tk.Label(root, text="Password", font=('Arial', 14)).pack(pady=10)
    password_entry = tk.Entry(root, font=('Arial', 12), show="*")
    password_entry.pack(pady=10)

    tk.Label(root, text="Confirm Password", font=('Arial', 14)).pack(pady=10)
    confirm_password_entry = tk.Entry(root, font=('Arial', 12), show="*")
    confirm_password_entry.pack(pady=10)

    # Register Button
    def register_user():
        username = username_entry.get().strip()
        password = password_entry.get().strip()
        confirm_password = confirm_password_entry.get().strip()

        if not username or not password or not confirm_password:
            messagebox.showerror("Error", "All fields must be filled out.")
            return
        
        if password != confirm_password:
            messagebox.showerror("Error", "Passwords do not match.")
            return
        
        if username in users:
            messagebox.showerror("Error", "Username already exists.")
            return

        users[username] = password
        messagebox.showinfo("Success", "Sign up successful!")
        show_login_window()

    sign_up_button = tk.Button(root, text="Register", font=('Arial', 14), command=register_user)
    sign_up_button.pack(pady=20)

# Function to handle user login
def log_in():
    # Clear the window
    for widget in root.winfo_children():
        widget.destroy()

    root.geometry("400x300")
    root.title("Log In")

    # Title Label
    tk.Label(root, text="Login", font=('Arial', 24), bd=8).pack(pady=20)

    # User Input Fields
    tk.Label(root, text="Username", font=('Arial', 14)).pack(pady=10)
    username_entry = tk.Entry(root, font=('Arial', 12))
    username_entry.pack(pady=10)

    tk.Label(root, text="Password", font=('Arial', 14)).pack(pady=10)
    password_entry = tk.Entry(root, font=('Arial', 12), show="*")
    password_entry.pack(pady=10)

    # Login Button
    def authenticate_user():
        username = username_entry.get().strip()
        password = password_entry.get().strip()

        if not username or not password:
            messagebox.showerror("Error", "Both fields are required.")
            return

        if username not in users or users[username] != password:
            messagebox.showerror("Error", "Invalid credentials.")
            return

        messagebox.showinfo("Success", "Login successful!")
        show_booking_system()

    login_button = tk.Button(root, text="Log In", font=('Arial', 14), command=authenticate_user)
    login_button.pack(pady=20)

# Function to handle booking table
def book_table(customer_name, phone_number, num_people_entry, booking_datetime_entry, restaurant_var, menu_var):
    name = customer_name.get().strip()
    phone = phone_number.get().strip()
    num_people = num_people_entry.get().strip()
    booking_datetime = booking_datetime_entry.get().strip()
    restaurant = restaurant_var.get()
    menu_item = menu_var.get()

    # Basic validation
    if not name or not phone or not num_people or not booking_datetime or restaurant == "Select Restaurant" or menu_item == "Select Menu Item":
        messagebox.showerror("Error", "Please fill in all fields")
        return

    if not num_people.isdigit():
        messagebox.showerror("Error", "Number of people must be a valid number")
        return

    # Check for existing bookings at the same time
    for booking in bookings:
        if booking['datetime'] == booking_datetime and booking['restaurant'] == restaurant:
            messagebox.showerror("Error", f"Sorry, there is already a booking at {restaurant} at this time.")
            return

    # Calculate total price (assuming the price is per person)
    menu_price = menu_items[menu_item]
    total_price = menu_price * int(num_people)

    # Add booking to the list
    new_booking = {
        "name": name,
        "phone": phone,
        "num_people": num_people,
        "datetime": booking_datetime,
        "restaurant": restaurant,
        "menu_item": menu_item,
        "price": total_price
    }

    bookings.append(new_booking)
    messagebox.showinfo("Success", "Table booked successfully!")

    # Generate and display receipt
    generate_receipt(new_booking)

    # Clear input fields
    customer_name.delete(0, tk.END)
    phone_number.delete(0, tk.END)
    num_people_entry.delete(0, tk.END)
    booking_datetime_entry.delete(0, tk.END)

# Function to generate receipt
def generate_receipt(booking):
    receipt_text = (
        f"--- Restaurant Booking Receipt ---\n"
        f"Restaurant: {booking['restaurant']}\n"
        f"Customer Name: {booking['name']}\n"
        f"Phone Number: {booking['phone']}\n"
        f"Number of People: {booking['num_people']}\n"
        f"Menu Item: {booking['menu_item']}\n"
        f"Price per Person: RM{menu_items[booking['menu_item']]:.2f}\n"
        f"Total Price: RM{booking['price']:.2f}\n"
        f"Booking Date & Time: {booking['datetime']}\n"
        f"----------------------------------\n"
        f"Thank you for booking with us!"
    )
    
    # Display receipt in a new window
    receipt_window = tk.Toplevel(root)
    receipt_window.geometry("400x300")
    receipt_window.title("Booking Receipt")
    
    receipt_label = tk.Label(receipt_window, text=receipt_text, font=('Arial', 12), justify='left')
    receipt_label.pack(pady=20)

    # Save receipt to a file (optional)
    save_receipt = messagebox.askyesno("Save Receipt", "Do you want to save this receipt as a text file?")
    if save_receipt:
        save_receipt_to_file(booking)

# Function to save receipt to a file
def save_receipt_to_file(booking):
    receipt_text = (
        f"--- Restaurant Booking Receipt ---\n"
        f"Restaurant: {booking['restaurant']}\n"
        f"Customer Name: {booking['name']}\n"
        f"Phone Number: {booking['phone']}\n"
        f"Number of People: {booking['num_people']}\n"
        f"Menu Item: {booking['menu_item']}\n"
        f"Price per Person: RM{menu_items[booking['menu_item']]:.2f}\n"
        f"Total Price: RM{booking['price']:.2f}\n"
        f"Booking Date & Time: {booking['datetime']}\n"
        f"----------------------------------\n"
        f"Thank you for booking with us!"
    )

    # Ask user for file name and save the receipt
    filename = simpledialog.askstring("Save File", "Enter the filename to save the receipt (e.g., receipt.txt):")
    if filename:
        with open(filename, "w") as file:
            file.write(receipt_text)
        messagebox.showinfo("Success", f"Receipt saved as {filename}")

# Function to view all bookings
def view_bookings():
    if not bookings:
        messagebox.showinfo("No Bookings", "There are no bookings available.")
        return
    
    bookings_window = tk.Toplevel(root)
    bookings_window.geometry("600x400")
    bookings_window.title("All Bookings")

    bookings_listbox = tk.Listbox(bookings_window, width=80, height=20, font=('Arial', 12))
    bookings_listbox.pack(pady=20)

    for booking in bookings:
        booking_info = f"{booking['restaurant']} | {booking['name']} | {booking['phone']} | {booking['num_people']} People | {booking['menu_item']} | RM{booking['price']:.2f} | {booking['datetime']}"
        bookings_listbox.insert(tk.END, booking_info)

# Function to cancel a booking
def cancel_booking():
    cancel_window = tk.Toplevel(root)
    cancel_window.geometry("400x200")
    cancel_window.title("Cancel Booking")

    tk.Label(cancel_window, text="Enter the Date and Time to Cancel (YYYY-MM-DD HH:MM)", font=('Arial', 14)).pack(pady=10)
    cancel_entry = tk.Entry(cancel_window, font=('Arial', 12))
    cancel_entry.pack(pady=10)

    def confirm_cancel():
        cancel_datetime = cancel_entry.get().strip()

        if not cancel_datetime:
            messagebox.showerror("Error", "Please enter a date and time.")
            return

        # Find and remove the booking
        for booking in bookings:
            if booking['datetime'] == cancel_datetime:
                bookings.remove(booking)
                messagebox.showinfo("Success", "Booking cancelled successfully!")
                cancel_window.destroy()
                return
        
        messagebox.showerror("Error", "No booking found at that time.")

    cancel_button = tk.Button(cancel_window, text="Cancel Booking", font=('Arial', 14), command=confirm_cancel)
    cancel_button.pack(pady=10)

# Function to update a booking
def update_booking():
    # Allow user to select the booking to update
    cancel_window = tk.Toplevel(root)
    cancel_window.geometry("400x300")
    cancel_window.title("Update Booking")

    tk.Label(cancel_window, text="Enter the Date and Time to Update (YYYY-MM-DD HH:MM)", font=('Arial', 14)).pack(pady=10)
    cancel_entry = tk.Entry(cancel_window, font=('Arial', 12))
    cancel_entry.pack(pady=10)

    def confirm_update():
        cancel_datetime = cancel_entry.get().strip()

        if not cancel_datetime:
            messagebox.showerror("Error", "Please enter a date and time.")
            return

        # Find and update the booking
        for booking in bookings:
            if booking['datetime'] == cancel_datetime:
                # Proceed to updating booking details
                update_window = tk.Toplevel(root)
                update_window.geometry("400x400")
                update_window.title("Update Booking")

                # Customer Name
                tk.Label(update_window, text="Customer Name", font=('Arial', 14)).grid(row=0, column=0, padx=10, pady=10)
                customer_name = tk.Entry(update_window, font=('Arial', 12))
                customer_name.insert(0, booking['name'])
                customer_name.grid(row=0, column=1, padx=10, pady=10)

                # Phone Number
                tk.Label(update_window, text="Phone Number", font=('Arial', 14)).grid(row=1, column=0, padx=10, pady=10)
                phone_number = tk.Entry(update_window, font=('Arial', 12))
                phone_number.insert(0, booking['phone'])
                phone_number.grid(row=1, column=1, padx=10, pady=10)

                # Number of People
                tk.Label(update_window, text="Number of People", font=('Arial', 14)).grid(row=2, column=0, padx=10, pady=10)
                num_people_entry = tk.Entry(update_window, font=('Arial', 12))
                num_people_entry.insert(0, booking['num_people'])
                num_people_entry.grid(row=2, column=1, padx=10, pady=10)

                # Date and Time
                tk.Label(update_window, text="Date and Time (YYYY-MM-DD HH:MM)", font=('Arial', 14)).grid(row=3, column=0, padx=10, pady=10)
                booking_datetime_entry = tk.Entry(update_window, font=('Arial', 12))
                booking_datetime_entry.insert(0, booking['datetime'])
                booking_datetime_entry.grid(row=3, column=1, padx=10, pady=10)

                # Restaurant Selection
                restaurant_options = [ "The Garden of Eat's", "Rustica Steak House", "The Outer Clove Restaurant", "Coupa Couffee"]
                restaurant_var = tk.StringVar()
                restaurant_var.set(booking['restaurant'])
                tk.Label(update_window, text="Select Restaurant", font=('Arial', 14)).grid(row=4, column=0, padx=10, pady=10)
                restaurant_menu = tk.OptionMenu(update_window, restaurant_var, *restaurant_options)
                restaurant_menu.grid(row=4, column=1, padx=10, pady=10)

                # Menu Item Selection
                menu_options = ["Select Menu Item"] + list(menu_items.keys())
                menu_var = tk.StringVar()
                menu_var.set(booking['menu_item'])
                tk.Label(update_window, text="Select Menu Item", font=('Arial', 14)).grid(row=5, column=0, padx=10, pady=10)
                menu_menu = tk.OptionMenu(update_window, menu_var, *menu_options)
                menu_menu.grid(row=5, column=1, padx=10, pady=10)

                def update_booking_info():
                    booking['name'] = customer_name.get()
                    booking['phone'] = phone_number.get()
                    booking['num_people'] = num_people_entry.get()
                    booking['datetime'] = booking_datetime_entry.get()
                    booking['restaurant'] = restaurant_var.get()
                    booking['menu_item'] = menu_var.get()

                    # Calculate total price
                    booking['price'] = menu_items[booking['menu_item']] * int(booking['num_people'])

                    messagebox.showinfo("Success", "Booking updated successfully!")
                    update_window.destroy()

                update_button = tk.Button(update_window, text="Update Booking", font=('Arial', 14), command=update_booking_info)
                update_button.grid(row=6, column=0, columnspan=2, pady=20)

                return
        messagebox.showerror("Error", "No booking found at that time.")

    cancel_button = tk.Button(cancel_window, text="Update Booking", font=('Arial', 14), command=confirm_update)
    cancel_button.pack(pady=10)

# Show login window initially
def show_login_window():
    for widget in root.winfo_children():
        widget.destroy()

    root.geometry("400x300")
    root.title("Login")

    # Title Label for Restaurant Management System
    title_label = tk.Label(root, text="Restaurant Management System", font=('Arial', 24, 'bold'), bd=8)
    title_label.pack(pady=20)

    # Login and Sign-Up buttons
    tk.Button(root, text="Log In", font=('Arial', 14), command=log_in).pack(pady=10)
    tk.Button(root, text="Sign Up", font=('Arial', 14), command=sign_up).pack(pady=10)

show_login_window()

root.mainloop()