import tkinter as tk
from tkinter import messagebox
import json

# Global variables
users = {}  # Store user data
logged_in_user = None  # Currently logged-in user

# Destination and Accommodation Details
destination_details = {
    "Maldives": {"tax_rate": 0.67, "air_miles": 3191, "insurance": 500},
    "South Korea": {"tax_rate": 0.80, "air_miles": 4402, "insurance": 700},
    "Japan": {"tax_rate": 0.85, "air_miles": 5134, "insurance": 800},
    "Thailand": {"tax_rate": 0.50, "air_miles": 1688.4, "insurance": 300},
    "Vietnam": {"tax_rate": 0.50, "air_miles": 2412.8, "insurance": 400}
}

accommodation_details = {
    "7 days 6 nights": 3000,
    "10 days 9 nights": 7000,
    "15 days 14 nights": 9000
}

def load_data():
    global users
    try:
        with open('users_data.json', 'r') as file:
            users = json.load(file)
    except FileNotFoundError:
        users = {}

def save_data():
    with open('users_data.json', 'w') as file:
        json.dump(users, file, indent=4)

def clear_widgets(root):
    for widget in root.winfo_children():
        widget.destroy()

# Sign Up Functionality
def show_signup(root):
    clear_widgets(root)

    signup_label = tk.Label(root, text="Sign Up", font=("Arial", 14))
    signup_label.pack(pady=10)

    username_label = tk.Label(root, text="Username")
    username_label.pack()
    username_entry = tk.Entry(root)
    username_entry.pack()

    email_label = tk.Label(root, text="Email")
    email_label.pack()
    email_entry = tk.Entry(root)
    email_entry.pack()

    password_label = tk.Label(root, text="Password")
    password_label.pack()
    password_entry = tk.Entry(root, show="*")
    password_entry.pack()

    signup_button = tk.Button(root, text="Sign Up", command=lambda: signup_user(username_entry, email_entry, password_entry, root))
    signup_button.pack(pady=10)

    back_button = tk.Button(root, text="Back", command=lambda: back_to_menu(root))
    back_button.pack()

def signup_user(username_entry, email_entry, password_entry, root):
    username = username_entry.get()
    email = email_entry.get()
    password = password_entry.get()

    global users
    if email in users:
        messagebox.showerror("Error", "Email is already registered!")
    else:
        users[email] = {
            "username": username,
            "password": password,
            "personal_details": {},
            "travel_details": {},
            "receipt": {}
        }
        save_data()
        messagebox.showinfo("Success", "Registration successful! You can now log in.")

# Login Functionality
def show_login(root):
    clear_widgets(root)

    login_label = tk.Label(root, text="Login", font=("Arial", 14))
    login_label.pack(pady=10)

    email_label = tk.Label(root, text="Email")
    email_label.pack()
    email_entry = tk.Entry(root)
    email_entry.pack()

    password_label = tk.Label(root, text="Password")
    password_label.pack()
    password_entry = tk.Entry(root, show="*")
    password_entry.pack()

    login_button = tk.Button(root, text="Login", command=lambda: login_user(email_entry, password_entry, root))
    login_button.pack(pady=10)

    back_button = tk.Button(root, text="Back", command=lambda: back_to_menu(root))
    back_button.pack()

def login_user(email_entry, password_entry, root):
    global logged_in_user

    email = email_entry.get()
    password = password_entry.get()

    user = users.get(email)
    if user and user['password'] == password:
        logged_in_user = email
        messagebox.showinfo("Welcome", f"Welcome back, {user['username']}!")
        show_user_dashboard(root)
    else:
        messagebox.showerror("Error", "Invalid email or password!")

# User Dashboard
def show_user_dashboard(root):
    clear_widgets(root)

    dashboard_label = tk.Label(root, text="User Dashboard", font=("Arial", 14))
    dashboard_label.pack(pady=10)

    btn_update_personal = tk.Button(root, text="Update Personal Details", width=30, command=lambda: update_personal_details(root))
    btn_update_personal.pack(pady=5)

    btn_enter_travel = tk.Button(root, text="Enter Travel Details", width=30, command=lambda: enter_travel_details(root))
    btn_enter_travel.pack(pady=5)

    btn_generate_receipt = tk.Button(root, text="Generate Receipt", width=30, command=lambda: generate_receipt(root))
    btn_generate_receipt.pack(pady=5)

    btn_payment = tk.Button(root, text="Click to Pay", width=30, command=lambda: initiate_payment(root))
    btn_payment.pack(pady=5)

    btn_logout = tk.Button(root, text="Logout", width=30, command=lambda: logout(root))
    btn_logout.pack(pady=5)

# Update Personal Details
def update_personal_details(root):
    clear_widgets(root)

    personal_label = tk.Label(root, text="Personal Details", font=("Arial", 14))
    personal_label.pack(pady=10)

    name_label = tk.Label(root, text="Full Name")
    name_label.pack()
    name_entry = tk.Entry(root)
    name_entry.pack()

    phone_label = tk.Label(root, text="Phone")
    phone_label.pack()
    phone_entry = tk.Entry(root)
    phone_entry.pack()

    email_label = tk.Label(root, text="Email")
    email_label.pack()
    email_entry = tk.Entry(root)
    email_entry.insert(0, logged_in_user)  # Pre-fill with logged-in user's email
    email_entry.config(state="disabled")  # Disable editing the email
    email_entry.pack()

    address_label = tk.Label(root, text="Address")
    address_label.pack()
    address_entry = tk.Entry(root)
    address_entry.pack()

    save_button = tk.Button(root, text="Save", command=lambda: save_personal_details(name_entry, phone_entry, address_entry, root))
    save_button.pack(pady=10)

    back_button = tk.Button(root, text="Back", command=lambda: show_user_dashboard(root))
    back_button.pack()

def save_personal_details(name_entry, phone_entry, address_entry, root):
    name = name_entry.get()
    phone = phone_entry.get()
    address = address_entry.get()

    user = users[logged_in_user]
    user['personal_details'] = {
        "name": name,
        "phone": phone,
        "address": address
    }
    save_data()
    messagebox.showinfo("Success", "Personal details updated successfully!")

# Enter Travel Details
def enter_travel_details(root):
    clear_widgets(root)

    travel_label = tk.Label(root, text="Travel Details", font=("Arial", 14))
    travel_label.pack(pady=10)

    # Destination Dropdown
    destination_label = tk.Label(root, text="Destination Country")
    destination_label.pack()
    destination_options = ["Maldives", "South Korea", "Japan", "Thailand", "Vietnam"]
    destination_var = tk.StringVar()
    destination_dropdown = tk.OptionMenu(root, destination_var, *destination_options)
    destination_var.set(destination_options[0])  # Default value
    destination_dropdown.pack()

    # Accommodation Dropdown
    accommodation_label = tk.Label(root, text="Accommodation")
    accommodation_label.pack()
    accommodation_options = ["7 days 6 nights", "10 days 9 nights", "15 days 14 nights"]
    accommodation_var = tk.StringVar()
    accommodation_dropdown = tk.OptionMenu(root, accommodation_var, *accommodation_options)
    accommodation_var.set(accommodation_options[0])  # Default value
    accommodation_dropdown.pack()

    # Extra Luggage Dropdown
    extra_luggage_label = tk.Label(root, text="Extra Luggage (Yes/No)")
    extra_luggage_label.pack()
    extra_luggage_var = tk.StringVar()
    extra_luggage_dropdown = tk.OptionMenu(root, extra_luggage_var, "Yes", "No")
    extra_luggage_var.set("No")  # Default value
    extra_luggage_dropdown.pack()

    # Save Button
    save_button = tk.Button(root, text="Save Travel Details", command=lambda: save_travel_details(destination_var, accommodation_var, extra_luggage_var, root))
    save_button.pack(pady=10)

    # Back Button
    back_button = tk.Button(root, text="Back", command=lambda: show_user_dashboard(root))
    back_button.pack()

def save_travel_details(destination_var, accommodation_var, extra_luggage_var, root):
    destination = destination_var.get()
    accommodation = accommodation_var.get()
    extra_luggage = extra_luggage_var.get()

    accommodation_price = accommodation_details[accommodation]

    # Save travel details
    user = users[logged_in_user]
    user['travel_details'] = {
        "destination": destination,
        "accommodation": accommodation,
        "extra_luggage": extra_luggage,
        "accommodation_price": accommodation_price,
        "tax_rate": destination_details[destination]["tax_rate"],
        "air_miles": destination_details[destination]["air_miles"],
        "insurance": destination_details[destination]["insurance"]
    }
    save_data()
    messagebox.showinfo("Success", "Travel details saved successfully!")

# Generate Receipt
def generate_receipt(root):
    global logged_in_user
    if not logged_in_user:
        messagebox.showerror("Error", "Please log in first.")
        return

    user = users[logged_in_user]
    personal = user['personal_details']
    travel = user['travel_details']

    # Receipt content
    receipt = f"Name: {personal['name']}\n"
    receipt += f"Email: {logged_in_user}\n"
    receipt += f"Phone: {personal['phone']}\n"
    receipt += f"Address: {personal['address']}\n"
    receipt += f"\nDestination: {travel['destination']}\n"
    receipt += f"Accommodation: {travel['accommodation']}\n"
    receipt += f"Extra Luggage: {travel['extra_luggage']}\n"
    receipt += f"\nTax Rate: {travel['tax_rate'] * 100}%\n"
    receipt += f"Air Miles: {travel['air_miles']} KM\n"
    receipt += f"Insurance: RM{travel['insurance']}\n"
    
    # Calculate total cost
    total_cost = travel['accommodation_price'] + travel['insurance']
    if travel['extra_luggage'] == "Yes":
        total_cost += 50  # Assuming an additional RM50 for extra luggage

    receipt += f"\nTotal Cost: RM {total_cost}\n"

    # Add payment status
    if user['receipt'].get("payment_status"):
        receipt += f"\nPayment Status: {user['receipt']['payment_status']}"

    messagebox.showinfo("Receipt", receipt)

# Payment Method - Online Banking
def initiate_payment(root):
    clear_widgets(root)

    payment_label = tk.Label(root, text="Online Banking Payment", font=("Arial", 14))
    payment_label.pack(pady=10)

    # Prompt for banking details
    username_label = tk.Label(root, text="Banking Username")
    username_label.pack()
    username_entry = tk.Entry(root)
    username_entry.pack()

    password_label = tk.Label(root, text="Banking Password")
    password_label.pack()
    password_entry = tk.Entry(root, show="*")
    password_entry.pack()

    # Pay Button
    pay_button = tk.Button(root, text="Pay", command=lambda: process_payment(username_entry, password_entry, root))
    pay_button.pack(pady=10)

    back_button = tk.Button(root, text="Back", command=lambda: show_user_dashboard(root))
    back_button.pack()

def process_payment(username_entry, password_entry, root):
    username = username_entry.get()
    password = password_entry.get()

    # Simulate online banking validation (in reality, you'd integrate with a payment gateway)
    if username and password:
        # Update payment status in user's data
        user = users[logged_in_user]
        user['receipt']["payment_status"] = "Payment Successful"
        save_data()
        messagebox.showinfo("Payment", "Payment Successful!")
        show_user_dashboard(root)
    else:
        messagebox.showerror("Error", "Invalid banking details!")

# Logout
def logout(root):
    global logged_in_user
    logged_in_user = None
    show_login(root)

def back_to_menu(root):
    clear_widgets(root)
    create_widgets(root)

def create_widgets(root):
    title_label = tk.Label(root, text="Travel Management System", font=("Arial", 18))
    title_label.pack(pady=20)

    # Add buttons for navigation
    btn_signup = tk.Button(root, text="Sign Up", width=20, command=lambda: show_signup(root))
    btn_signup.pack(pady=5)

    btn_login = tk.Button(root, text="Login", width=20, command=lambda: show_login(root))
    btn_login.pack(pady=5)

    btn_exit = tk.Button(root, text="Exit", width=20, command=root.quit)
    btn_exit.pack(pady=5)


if __name__ == "__main__":
    root = tk.Tk()
    load_data()  # Load users data when the program starts
    create_widgets(root)
    root.mainloop()
