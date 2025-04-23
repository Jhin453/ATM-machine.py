import tkinter as tk
from tkinter import messagebox, ttk
import random
import ttkbootstrap as ttkb

class ATM:
    def __init__(self, pin):
        self.pin = pin
        self.balance = 0

    def validate_pin(self, entered_pin):
        if entered_pin == self.pin:
            self.balance = random.randint(10000, 99999)
            return True
        return False

class ATMApp:
    def __init__(self, root):
        self.root = root
        self.root.title("ATM Machine")
        self.root.geometry("400x400")  # Fiksiraj veličinu prozora
        self.root.resizable(False, False)  # Ne dozvoljava promjenu veličine prozora
        self.atm = ATM(pin=55555)
        self.language = "en"  # Fiksiraj jezik na engleski
        self.frame = ttkb.Frame(self.root, padding=20)  # Create the frame here to reuse
        self.frame.pack(fill="both", expand=True)  # Expand frame to take full space
        self.language_screen()

    def clear_frame(self):
        # Remove all widgets from the frame without destroying the frame itself
        for widget in self.frame.winfo_children():
            widget.destroy()

    def language_screen(self):
        self.clear_frame()

        # Prikaz jezika umjesto "1 odabran"
        language_text = {
            "en": "English / Engleski",
            "bs": "Bosnian / Bosanski"
        }

        ttkb.Label(self.frame, text="Select language / Odaberite jezik").pack(pady=10)

        ttkb.Button(self.frame, text=language_text["en"], style="primary.TButton", command=lambda: self.set_language("en")).pack(pady=5, padx=20, fill="x")
        ttkb.Button(self.frame, text=language_text["bs"], style="primary.TButton", command=lambda: self.set_language("bs")).pack(pady=5, padx=20, fill="x")

    def set_language(self, lang):
        self.language = lang
        self.pin_screen()

    def pin_screen(self):
        self.clear_frame()

        label_text = {
            "en": "Enter your PIN:",
            "bs": "Unesite svoj PIN:"
        }

        ttkb.Label(self.frame, text=label_text[self.language]).pack(pady=10)
        self.pin_entry = ttkb.Entry(self.frame, show="*")
        self.pin_entry.pack(pady=10)
        ttkb.Button(self.frame, text="OK", style="success.TButton", command=self.check_pin).pack(pady=10)

    def check_pin(self):
        try:
            entered_pin = int(self.pin_entry.get())
            if self.atm.validate_pin(entered_pin):
                self.transaction_menu()
            else:
                messagebox.showerror("Error", "Invalid PIN" if self.language == "en" else "Neispravan PIN")
        except ValueError:
            messagebox.showerror("Error", "Enter numbers only." if self.language == "en" else "Unesite samo brojeve.")

    def transaction_menu(self):
        self.clear_frame()

        label_text = {
            "en": "Select transaction:",
            "bs": "Odaberite transakciju:"
        }

        ttkb.Label(self.frame, text=label_text[self.language]).pack(pady=10)

        # Centrira dugmadi i povecava ih, te koristi jezik koji je odabran
        if self.language == "en":
            ttkb.Button(self.frame, text="Deposit", style="primary.TButton", command=lambda: self.amount_window(is_deposit=True), width=20).pack(pady=10, padx=20, fill="x")
            ttkb.Button(self.frame, text="Withdraw", style="primary.TButton", command=lambda: self.amount_window(is_deposit=False), width=20).pack(pady=10, padx=20, fill="x")
        elif self.language == "bs":
            ttkb.Button(self.frame, text="Uplata", style="primary.TButton", command=lambda: self.amount_window(is_deposit=True), width=20).pack(pady=10, padx=20, fill="x")
            ttkb.Button(self.frame, text="Isplata", style="primary.TButton", command=lambda: self.amount_window(is_deposit=False), width=20).pack(pady=10, padx=20, fill="x")

    def amount_window(self, is_deposit):
        self.clear_frame()  # Clear the frame to show amount entry

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

        entry = ttkb.Entry(self.frame)
        entry.pack(pady=10)

        def submit():
            try:
                amount = int(entry.get())

                if amount <= 0:
                    msg = {
                        "en": "Amount must be greater than zero.",
                        "bs": "Iznos mora biti veći od nule."
                    }
                    messagebox.showerror("Error", msg[self.language])
                    return

                if is_deposit:
                    self.atm.balance += amount
                    msg = {
                        "en": f"Deposited {amount} KM.\nNew balance: {self.atm.balance} KM.",
                        "bs": f"Uplaćeno {amount} KM.\nNovi balans: {self.atm.balance} KM."
                    }
                else:
                    if amount > self.atm.balance:
                        msg = {
                            "en": "Insufficient funds.",
                            "bs": "Nedovoljno sredstava."
                        }
                        messagebox.showerror("Error", msg[self.language])
                        return
                    else:
                        self.atm.balance -= amount
                        msg = {
                            "en": f"Withdrawn {amount} KM.\nNew balance: {self.atm.balance} KM.",
                            "bs": f"Podignuto {amount} KM.\nNovi balans: {self.atm.balance} KM."
                        }

                messagebox.showinfo("Transaction", msg[self.language])
                self.transaction_menu()
            except ValueError:
                error_msg = {
                    "en": "Please enter a valid number.",
                    "bs": "Unesite ispravan broj."
                }
                messagebox.showerror("Error", error_msg[self.language])

        ttkb.Button(self.frame, text="OK", style="success.TButton", command=submit, width=20).pack(pady=10)

        # Fixed amount buttons
        for fixed in [10, 20, 50, 100, 200]:
            ttkb.Button(self.frame, text=f"{fixed} KM", style="info.TButton", command=lambda f=fixed: [entry.delete(0, tk.END), entry.insert(0, str(f))], width=20).pack(pady=2)

if __name__ == "__main__":
    root = ttkb.Window(themename="cyborg")  # Use cyborg theme
    app = ATMApp(root)
    root.mainloop()
