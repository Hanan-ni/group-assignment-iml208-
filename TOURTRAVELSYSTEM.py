import tkinter as tk
from tkinter import messagebox
import time

class Travel:
    def __init__(self, root):
        self.root = root
        self.root.title("Travel Management System")
        self.root.geometry("800x600+100+50")
        self.root.configure(background='black')

        # Variables for Customer Details
        self.DateofOrder = tk.StringVar()
        self.DateofOrder.set(time.strftime("%d/%m/%Y"))
        self.Firstname = tk.StringVar()
        self.Surname = tk.StringVar()
        self.Address = tk.StringVar()
        self.PostCode = tk.StringVar()
        self.Mobile = tk.StringVar()
        self.Email = tk.StringVar()

        # Variables for Travel Details
        self.DepartureCountry = tk.StringVar(value="Malaysia")
        self.DestinationCountry = tk.StringVar()
        self.Accommodation = tk.StringVar()

        # Tax Payment Variables
        self.AirportTax = tk.DoubleVar(value=0)
        self.AirMiles = tk.DoubleVar(value=0)
        self.Insurance = tk.DoubleVar(value=0)
        self.ExtraLuggage = tk.DoubleVar(value=0)

        # Ticket Type and Class Selection
        self.TicketType = tk.StringVar(value="Single")
        self.var_standard = tk.IntVar()
        self.var_economy = tk.IntVar()
        self.var_first_class = tk.IntVar()

        # Special Needs Checkbox
        self.SpecialNeeds = tk.BooleanVar()

        # Data storage
        self.data_list = []

        # Destination Country Details (Tax, Air Miles, Insurance)
        self.destination_details = {
            "Maldives": {"tax_rate": 0.67, "air_miles": 3191, "insurance": 200},
            "South Korea": {"tax_rate": 0.80, "air_miles": 4402, "insurance": 440},
            "Japan": {"tax_rate": 0.85, "air_miles": 5134, "insurance": 570},
            "Thailand": {"tax_rate": 0.50, "air_miles": 1688.4, "insurance": 188},
            "Singapore": {"tax_rate": 0.50, "air_miles": 330, "insurance": 100},
        }

        # Accommodation Prices
        self.accommodation_prices = {
            "A": 3500,
            "B": 5500,
            "C": 7000,
        }

        # Layout
        self.create_widgets()

    def create_widgets(self):
        # Title Frame
        title_frame = tk.Frame(self.root, bg='black')
        title_frame.pack(side=tk.TOP, fill=tk.X, pady=10)
        title_label = tk.Label(
            title_frame,
            text="Travel Management System",
            font=('Arial', 18, 'bold'),
            fg='white',
            bg='black',
        )
        title_label.pack()

        # Customer Info Frame
        customer_frame = tk.Frame(self.root, bg='white', relief=tk.RIDGE, bd=8)
        customer_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=15, pady=8)

        labels = [
            ("First Name", self.Firstname),
            ("Surname", self.Surname),
            ("Address", self.Address),
            ("Post Code", self.PostCode),
            ("Mobile", self.Mobile),
            ("Email", self.Email),
        ]

        for i, (label_text, variable) in enumerate(labels):
            tk.Label(
                customer_frame, text=label_text, font=('Arial', 10), bg='white'
            ).grid(row=i, column=0, sticky="w", padx=5, pady=5)
            tk.Entry(
                customer_frame, textvariable=variable, font=('Arial', 10), width=25
            ).grid(row=i, column=1, padx=5, pady=5)

        # Travel Info Frame
        travel_frame = tk.Frame(self.root, bg='white', relief=tk.RIDGE, bd=8)
        travel_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=15, pady=8)

        # Destination Country
        tk.Label(travel_frame, text="Destination Country", font=('Arial', 10), bg='white').grid(
            row=0, column=0, sticky="w", padx=5, pady=10
        )
        destination_options = ["Maldives", "South Korea", "Japan", "Thailand", "Singapore"]
        self.destination_menu = tk.OptionMenu(travel_frame, self.DestinationCountry, *destination_options, command=self.update_travel_info)
        self.destination_menu.grid(row=0, column=1, padx=5, pady=10)

        # Accommodation Options
        tk.Label(travel_frame, text="Accommodation", font=('Arial', 10), bg='white').grid(
            row=1, column=0, sticky="w", padx=5, pady=10
        )
        accommodation_options = ["A (7 days 6 nights)", "B (10 days 9 nights)", "C (15 days 14 nights)"]
        self.accommodation_menu = tk.OptionMenu(travel_frame, self.Accommodation, *accommodation_options)
        self.accommodation_menu.grid(row=1, column=1, padx=5, pady=10)

        # Seat Class Selection
        tk.Label(travel_frame, text="Seat Class", font=('Arial', 10), bg='white').grid(row=2, column=0, sticky="w", padx=5, pady=10)

        self.check_standard = tk.Checkbutton(
            travel_frame,
            text="Standard (RM45)",
            variable=self.var_standard,
            font=('Arial', 10),
            bg='white',
        )
        self.check_standard.grid(row=2, column=1, sticky="w")

        self.check_economy = tk.Checkbutton(
            travel_frame,
            text="Economy (RM63)",
            variable=self.var_economy,
            font=('Arial', 10),
            bg='white',
        )
        self.check_economy.grid(row=3, column=1, sticky="w")

        self.check_first_class = tk.Checkbutton(
            travel_frame,
            text="First Class (RM334.59)",
            variable=self.var_first_class,
            font=('Arial', 10),
            bg='white',
        )
        self.check_first_class.grid(row=4, column=1, sticky="w")

        # Extra Luggage Selection
        tk.Label(travel_frame, text="Extra Luggage (More than 15KG)", font=('Arial', 10), bg='white').grid(
            row=5, column=0, sticky="w", padx=5, pady=10
        )
        self.extra_luggage_check = tk.Checkbutton(
            travel_frame,
            text="Yes (RM50)",
            variable=self.ExtraLuggage,
            font=('Arial', 10),
            bg='white',
        )
        self.extra_luggage_check.grid(row=5, column=1, sticky="w")

        # Button Frame
        button_frame = tk.Frame(travel_frame, bg='white')
        button_frame.grid(row=6, column=0, columnspan=2, pady=10)

        tk.Button(
            button_frame,
            text="Create",
            command=self.create_entry,
            font=('Arial', 10),
            width=8,
        ).grid(row=0, column=0, padx=10)

        tk.Button(
            button_frame,
            text="Reset",
            command=self.reset,
            font=('Arial', 10),
            width=8,
        ).grid(row=1, column=0, padx=10)

        tk.Button(
            button_frame,
            text="Update",
            command=self.update_entry,
            font=('Arial', 10),
            width=8,
        ).grid(row=2, column=0, padx=10)

        tk.Button(
            button_frame,
            text="Delete",
            command=self.delete_entry,
            font=('Arial', 10),
            width=8,
        ).grid(row=3, column=0, padx=10)

        # Receipt Frame
        self.txtReceipt = tk.Text(travel_frame, width=70, height=8, font=('Arial', 10))
        self.txtReceipt.grid(row=7, column=0, columnspan=2, pady=10)

    def update_travel_info(self, event=None):
        destination = self.DestinationCountry.get()
        details = self.destination_details.get(destination, {})
        if details:
            self.AirportTax.set(details["tax_rate"])
            self.AirMiles.set(details["air_miles"])
            self.Insurance.set(details["insurance"])

    def reset(self):
        self.Firstname.set("")
        self.Surname.set("")
        self.Address.set("")
        self.PostCode.set("")
        self.Mobile.set("")
        self.Email.set("")
        self.PaidTax.set("")
        self.SubTotal.set("")
        self.TotalCost.set("")
        self.txtReceipt.delete("1.0", tk.END)

        self.var_standard.set(0)
        self.var_economy.set(0)
        self.var_first_class.set(0)
        self.Accommodation.set("")
        self.DestinationCountry.set("")

    def create_entry(self):
        accommodation_price = self.accommodation_prices.get(self.Accommodation.get()[0], 0)
        selected_class_price = self.calculate_seat_class_price()
        airport_tax = self.AirportTax.get() * accommodation_price
        insurance = self.Insurance.get()
        extra_luggage_fee = 50 if self.ExtraLuggage.get() else 0

        subtotal = accommodation_price + selected_class_price + airport_tax + insurance + extra_luggage_fee
        paid_tax = 0.205 * subtotal
        total_cost = subtotal + paid_tax

        receipt = (
            f"First Name: {self.Firstname.get()}\n"
            f"Surname: {self.Surname.get()}\n"
            f"Address: {self.Address.get()}\n"
            f"Post Code: {self.PostCode.get()}\n"
            f"Mobile: {self.Mobile.get()}\n"
            f"Email: {self.Email.get()}\n\n"
            f"Destination Country: {self.DestinationCountry.get()}\n"
            f"Accommodation: {self.Accommodation.get()}\n"
            f"Ticket Class: {self.get_seat_class()}\n"
            f"Airport Tax: RM{airport_tax}\n"
            f"Insurance: RM{insurance}\n"
            f"Extra Luggage Fee: RM{extra_luggage_fee}\n"
            f"Subtotal: RM{subtotal}\n"
            f"Paid Tax (20.5%): RM{paid_tax}\n"
            f"Total Cost: RM{total_cost}\n"
        )

        self.txtReceipt.delete("1.0", tk.END)
        self.txtReceipt.insert(tk.END, receipt)

        # Add entry to data_list for future updates/deletes
        entry = {
            "FirstName": self.Firstname.get(),
            "Surname": self.Surname.get(),
            "Address": self.Address.get(),
            "PostCode": self.PostCode.get(),
            "Mobile": self.Mobile.get(),
            "Email": self.Email.get(),
            "Destination": self.DestinationCountry.get(),
            "Accommodation": self.Accommodation.get(),
            "SeatClass": self.get_seat_class(),
            "TotalCost": total_cost,
        }
        self.data_list.append(entry)

    def calculate_seat_class_price(self):
        price = 0
        if self.var_standard.get():
            price += 45
        if self.var_economy.get():
            price += 63
        if self.var_first_class.get():
            price += 334.59
        return price

    def get_seat_class(self):
        seat_classes = []
        if self.var_standard.get():
            seat_classes.append("Standard (RM45)")
        if self.var_economy.get():
            seat_classes.append("Economy (RM63)")
        if self.var_first_class.get():
            seat_classes.append("First Class (RM334.59)")
        return ", ".join(seat_classes)

    def update_entry(self):
        # Implement the update functionality here
        if len(self.data_list) == 0:
            messagebox.showerror("No Entry", "No entries to update.")
            return

        # Updating the last entry for the demonstration purpose
        entry = self.data_list[-1]  # Update the most recent entry

        # Update values based on current user input
        entry["FirstName"] = self.Firstname.get()
        entry["Surname"] = self.Surname.get()
        entry["Address"] = self.Address.get()
        entry["PostCode"] = self.PostCode.get()
        entry["Mobile"] = self.Mobile.get()
        entry["Email"] = self.Email.get()
        entry["Destination"] = self.DestinationCountry.get()
        entry["Accommodation"] = self.Accommodation.get()
        entry["SeatClass"] = self.get_seat_class()

        self.create_entry()  # To recalculate the cost and display the updated receipt

    def delete_entry(self):
        # Implement delete functionality
        if len(self.data_list) == 0:
            messagebox.showerror("No Entry", "No entries to delete.")
            return

        # Remove the most recent entry for the demonstration purpose
        self.data_list.pop()

        self.reset()  # Reset the fields after deletion
        self.txtReceipt.delete("1.0", tk.END)  # Clear the receipt area
        messagebox.showinfo("Delete", "Entry deleted successfully.")
        

if __name__ == "__main__":
    root = tk.Tk()
    app = Travel(root)
    root.mainloop()