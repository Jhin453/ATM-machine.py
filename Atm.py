import tkinter as tk
from tkinter import messagebox, ttk
import random
import ttkbootstrap as ttkb

# ATM class represents the ATM machine with a pin and balance
class ATM:
    def __init__(self, pin):
        self.pin = pin  # Set the PIN for the ATM
        self.balance = 0  # Initial balance is set to 0

    def validate_pin(self, entered_pin):
        # Check if the entered PIN is correct
        if entered_pin == self.pin:
            self.balance = random.randint(10000, 99999)  # Assign a random balance if PIN is correct
            return True
        return False  # Return False if PIN is incorrect

# ATMApp class handles the GUI for the ATM machine
class ATMApp:
    def __init__(self, root):
        self.root = root  # Main window for the application
        self.root.title("ATM Machine")  # Set window title
        self.root.geometry("400x400")  # Fixed size for the window
        self.root.resizable(False, False)  # Disable resizing of the window
        self.atm = ATM(pin=55555)  # Initialize ATM object with PIN 55555
        self.language = "en"  # Default language is English
        self.frame = ttkb.Frame(self.root, padding=20)  # Create the frame for the window content
        self.frame.pack(fill="both", expand=True)  # Expand frame to fill the window space
        self.language_screen()  # Show language selection screen initially

    # Clear the frame by removing all widgets
    def clear_frame(self):
        for widget in self.frame.winfo_children():
            widget.destroy()

    # Language selection screen
    def language_screen(self):
        self.clear_frame()  # Clear any previous content

        # Language options displayed based on the selected language
        language_text = {
            "en": "English / Engleski",
            "bs": "Bosnian / Bosanski"
        }

        ttkb.Label(self.frame, text="Select language / Odaberite jezik").pack(pady=10)

        # Buttons for language selection with a function to set the language
        ttkb.Button(self.frame, text=language_text["en"], style="primary.TButton", command=lambda: self.set_language("en")).pack(pady=5, padx=20, fill="x")
        ttkb.Button(self.frame, text=language_text["bs"], style="primary.TButton", command=lambda: self.set_language("bs")).pack(pady=5, padx=20, fill="x")

    # Set the selected language
    def set_language(self, lang):
        self.language = lang
        self.pin_screen()  # Show PIN entry screen after setting the language

    # PIN entry screen
    def pin_screen(self):
        self.clear_frame()  # Clear the frame to display the PIN screen

        # Label text based on the selected language
        label_text = {
            "en": "Enter your PIN:",
            "bs": "Unesite svoj PIN:"
        }

        ttkb.Label(self.frame, text=label_text[self.language]).pack(pady=10)
        self.pin_entry = ttkb.Entry(self.frame, show="*")  # Entry widget for the PIN (hidden input)
        self.pin_entry.pack(pady=10)
        ttkb.Button(self.frame, text="OK", style="success.TButton", command=self.check_pin).pack(pady=10)

    # Check the entered PIN against the stored PIN
    def check_pin(self):
        try:
            entered_pin = int(self.pin_entry.get())  # Get the entered PIN as integer
            if self.atm.validate_pin(entered_pin):  # Validate the entered PIN
                self.transaction_menu()  # If valid, go to transaction menu
            else:
                messagebox.showerror("Error", "Invalid PIN" if self.language == "en" else "Neispravan PIN")  # Show error if PIN is invalid
        except ValueError:
            messagebox.showerror("Error", "Enter numbers only." if self.language == "en" else "Unesite samo brojeve.")  # Show error if input is not a number

    # Show the transaction menu (Deposit / Withdraw options)
    def transaction_menu(self):
        self.clear_frame()  # Clear the frame to display the transaction options

        # Label text based on the selected language
        label_text = {
            "en": "Select transaction:",
            "bs": "Odaberite transakciju:"
        }

        ttkb.Label(self.frame, text=label_text[self.language]).pack(pady=10)

        # Create buttons for Deposit and Withdraw, based on the selected language
        if self.language == "en":
            ttkb.Button(self.frame, text="Deposit", style="primary.TButton", command=lambda: self.amount_window(is_deposit=True), width=20).pack(pady=10, padx=20, fill="x")
            ttkb.Button(self.frame, text="Withdraw", style="primary.TButton", command=lambda: self.amount_window(is_deposit=False), width=20).pack(pady=10, padx=20, fill="x")
        elif self.language == "bs":
            ttkb.Button(self.frame, text="Uplata", style="primary.TButton", command=lambda: self.amount_window(is_deposit=True), width=20).pack(pady=10, padx=20, fill="x")
            ttkb.Button(self.frame, text="Isplata", style="primary.TButton", command=lambda: self.amount_window(is_deposit=False), width=20).pack(pady=10, padx=20, fill="x")

    # Show amount entry screen for either Deposit or Withdraw
    def amount_window(self, is_deposit):
        self.clear_frame()  # Clear the frame to show amount entry screen

        # Label text based on the selected language
        label_text = {
            "en": "Enter amount:",
            "bs": "Unesite iznos:"
        }

        ttkb.Label(self.frame, text=label_text[self.language]).pack(pady=10)

        # Display the current balance
        balance_text = {
            "en": f"Current balance: {self.atm.balance} KM",
            "bs": f"Trenutni balans: {self.atm.balance} KM"
        }

        ttkb.Label(self.frame, text=balance_text[self.language]).pack(pady=5)

        entry = ttkb.Entry(self.frame)  # Entry widget for amount input
        entry.pack(pady=10)

        # Function to handle submitting the amount for deposit/withdraw
        def submit():
            try:
                amount = int(entry.get())  # Get the entered amount as integer

                if amount <= 0:  # Check if the amount is greater than zero
                    msg = {
                        "en": "Amount must be greater than zero.",
                        "bs": "Iznos mora biti veći od nule."
                    }
                    messagebox.showerror("Error", msg[self.language])  # Show error if the amount is invalid
                    return

                if is_deposit:
                    self.atm.balance += amount  # Add the amount to balance for deposit
                    msg = {
                        "en": f"Deposited {amount} KM.\nNew balance: {self.atm.balance} KM.",
                        "bs": f"Uplaćeno {amount} KM.\nNovi balans: {self.atm.balance} KM."
                    }
                else:
                    if amount > self.atm.balance:  # Check if there are sufficient funds for withdrawal
                        msg = {
                            "en": "Insufficient funds.",
                            "bs": "Nedovoljno sredstava."
                        }
                        messagebox.showerror("Error", msg[self.language])  # Show error if insufficient funds
                        return
                    else:
                        self.atm.balance -= amount  # Subtract the amount from balance for withdrawal
                        msg = {
                            "en": f"Withdrawn {amount} KM.\nNew balance: {self.atm.balance} KM.",
                            "bs": f"Podignuto {amount} KM.\nNovi balans: {self.atm.balance} KM."
                        }

                messagebox.showinfo("Transaction", msg[self.language])  # Show success message
                self.transaction_menu()  # Return to the transaction menu
            except ValueError:
                error_msg = {
                    "en": "Please enter a valid number.",
                    "bs": "Unesite ispravan broj."
                }
                messagebox.showerror("Error", error_msg[self.language])  # Show error if the amount is not a valid number

        # Submit button for the amount entry
        ttkb.Button(self.frame, text="OK", style="success.TButton", command=submit, width=20).pack(pady=10)

        # Fixed amount buttons for common values
        for fixed in [10, 20, 50, 100, 200]:
            ttkb.Button(self.frame, text=f"{fixed} KM", style="info.TButton", command=lambda f=fixed: [entry.delete(0, tk.END), entry.insert(0, str(f))], width=20).pack(pady=2)

# Main execution
if __name__ == "__main__":
    root = ttkb.Window(themename="cyborg")  # Create window with 'cyborg' theme
    app = ATMApp(root)  # Initialize the ATM application
    root.mainloop()  # Run the application
