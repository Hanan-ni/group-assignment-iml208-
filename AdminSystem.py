import tkinter as tk
from tkinter import ttk, messagebox
import json

# Global variables
users = {}  # Store user data
logged_in_admin = None  # Currently logged-in admin

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

def admin_login(root):
    clear_widgets(root)

    tk.Label(root, text="Admin Login", font=("Arial", 14)).pack(pady=10)

    tk.Label(root, text="Email").pack()
    email_entry = tk.Entry(root)
    email_entry.pack()

    tk.Label(root, text="Password").pack()
    password_entry = tk.Entry(root, show="*")
    password_entry.pack()

    tk.Button(root, text="Login", command=lambda: handle_admin_login(email_entry, password_entry, root)).pack(pady=10)

def handle_admin_login(email_entry, password_entry, root):
    global logged_in_admin
    email = email_entry.get()
    password = password_entry.get()

    # Admin credentials
    if email == "admin@example.com" and password == "admin123":
        logged_in_admin = email
        messagebox.showinfo("Welcome", f"Welcome back, Admin!")
        show_admin_dashboard(root)
    else:
        messagebox.showerror("Error", "Invalid credentials!")

def show_admin_dashboard(root):
    clear_widgets(root)

    tk.Label(root, text="Admin Dashboard", font=("Arial", 14)).pack(pady=10)

    tk.Button(root, text="View Users", width=30, command=lambda: view_users(root)).pack(pady=5)
    tk.Button(root, text="Logout", width=30, command=lambda: logout_admin(root)).pack(pady=5)

def view_users(root):
    clear_widgets(root)

    tk.Label(root, text="Registered Users", font=("Arial", 14)).pack(pady=10)

    tree = ttk.Treeview(root, columns=("Email", "Username", "Full Name", "Phone", "Destination", "Accommodation", "Extra Luggage"), show="headings")
    tree.heading("Email", text="Email")
    tree.heading("Username", text="Username")
    tree.heading("Full Name", text="Full Name")
    tree.heading("Phone", text="Phone")
    tree.heading("Destination", text="Destination")
    tree.heading("Accommodation", text="Accommodation")
    tree.heading("Extra Luggage", text="Extra Luggage")
    tree.pack(fill="both", expand=True, pady=10)

    load_data()  # Load data from the users_data.json file

    # Check if data is loaded correctly and populate the treeview
    for email, data in users.items():
        if 'personal_details' in data and 'travel_details' in data:
            full_name = data['personal_details'].get('name', 'N/A')
            phone = data['personal_details'].get('phone', 'N/A')
            destination = data['travel_details'].get('destination', 'N/A')
            accommodation = data['travel_details'].get('accommodation', 'N/A')
            extra_luggage = data['travel_details'].get('extra_luggage', 'N/A')

            tree.insert("", "end", values=(email, data['username'], full_name, phone, destination, accommodation, extra_luggage))

    # Bind the double-click event on the email column to view the user's receipt
    tree.bind("<Double-1>", lambda event: view_receipt(event, tree))

    # Buttons for update and delete actions
    tk.Button(root, text="Update User", command=lambda: update_user(tree)).pack(pady=5)
    tk.Button(root, text="Delete User", command=lambda: delete_user(tree)).pack(pady=5)

    tk.Button(root, text="Back", command=lambda: show_admin_dashboard(root)).pack(pady=10)

def view_receipt(event, tree):
    # Get the selected item's email address
    selected_item = tree.selection()
    if selected_item:
        email = tree.item(selected_item)["values"][0]  # Get email from the first column
        
        # Fetch the user's data from the users dictionary
        user = users.get(email)
        if user:
            receipt_details = f"Receipt for {email}:\n"
            receipt_details += f"Name: {user['personal_details'].get('name', 'N/A')}\n"
            receipt_details += f"Phone: {user['personal_details'].get('phone', 'N/A')}\n"
            receipt_details += f"Destination: {user['travel_details'].get('destination', 'N/A')}\n"
            receipt_details += f"Accommodation: {user['travel_details'].get('accommodation', 'N/A')}\n"
            receipt_details += f"Extra Luggage: {user['travel_details'].get('extra_luggage', 'N/A')}\n"
            
            # Display the receipt details
            messagebox.showinfo(f"Receipt for {email}", receipt_details)
        else:
            messagebox.showinfo("Error", "User data not found.")

def update_user(tree):
    selected_item = tree.selection()
    if selected_item:
        email = tree.item(selected_item)["values"][0]  # Get email from the first column
        
        # Fetch the user's data
        user = users.get(email)
        if user:
            update_window(user, email, tree)
        else:
            messagebox.showinfo("Error", "User data not found.")
    else:
        messagebox.showinfo("Error", "Please select a user to update.")

def update_window(user, email, tree):
    def save_update():
        # Update user data from input fields
        new_name = name_entry.get()
        new_phone = phone_entry.get()
        new_destination = destination_entry.get()
        new_accommodation = accommodation_entry.get()
        new_extra_luggage = extra_luggage_entry.get()

        # Update the user dictionary
        users[email]['personal_details']['name'] = new_name
        users[email]['personal_details']['phone'] = new_phone
        users[email]['travel_details']['destination'] = new_destination
        users[email]['travel_details']['accommodation'] = new_accommodation
        users[email]['travel_details']['extra_luggage'] = new_extra_luggage

        save_data()
        messagebox.showinfo("Success", "User details updated successfully!")
        view_users(root)

    # Open a new window to edit user details
    update_window = tk.Toplevel(root)
    update_window.title("Update User")

    tk.Label(update_window, text="Name").pack()
    name_entry = tk.Entry(update_window)
    name_entry.insert(0, user['personal_details'].get('name', ''))
    name_entry.pack()

    tk.Label(update_window, text="Phone").pack()
    phone_entry = tk.Entry(update_window)
    phone_entry.insert(0, user['personal_details'].get('phone', ''))
    phone_entry.pack()

    tk.Label(update_window, text="Destination").pack()
    destination_entry = tk.Entry(update_window)
    destination_entry.insert(0, user['travel_details'].get('destination', ''))
    destination_entry.pack()

    tk.Label(update_window, text="Accommodation").pack()
    accommodation_entry = tk.Entry(update_window)
    accommodation_entry.insert(0, user['travel_details'].get('accommodation', ''))
    accommodation_entry.pack()

    tk.Label(update_window, text="Extra Luggage").pack()
    extra_luggage_entry = tk.Entry(update_window)
    extra_luggage_entry.insert(0, user['travel_details'].get('extra_luggage', ''))
    extra_luggage_entry.pack()

    tk.Button(update_window, text="Save", command=save_update).pack(pady=10)

def delete_user(tree):
    selected_item = tree.selection()
    if selected_item:
        email = tree.item(selected_item)["values"][0]  # Get email from the first column

        # Confirm deletion
        if messagebox.askyesno("Confirm Deletion", f"Are you sure you want to delete the user with email: {email}?"):
            if email in users:
                del users[email]
                save_data()
                messagebox.showinfo("Success", f"User with email {email} has been deleted.")
                view_users(root)
            else:
                messagebox.showinfo("Error", "User data not found.")
    else:
        messagebox.showinfo("Error", "Please select a user to delete.")

def logout_admin(root):
    global logged_in_admin
    logged_in_admin = None
    clear_widgets(root)
    tk.Label(root, text="Admin Management System", font=("Arial", 18)).pack(pady=20)
    tk.Button(root, text="Admin Login", width=20, command=lambda: admin_login(root)).pack(pady=10)
    tk.Button(root, text="Exit", width=20, command=root.quit).pack(pady=5)

if __name__ == "__main__":
    load_data()  # Load existing users data
    root = tk.Tk()
    root.title("Admin Management System")
    admin_login(root)
    root.mainloop()
