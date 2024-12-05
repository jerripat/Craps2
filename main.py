import random
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import sqlite3
import sys
import traceback

from Bank import CrapsBank


class CrapsGame:
    def __init__(self, root):
        self.balance_total = None
        self.root = root
        self.root.title("Craps Game")
        self.root.geometry("800x600")  # Adjust size for widgets
        self.comeout = 0
        self.point = None
        self.bank_id = 1
        self.bank = CrapsBank()  # Assuming CrapsBank is defined in Bank module
        self.create_widgets()

    def roll_dice(self):
        try:
            # Roll dice
            dice1 = random.randint(1, 6)
            dice2 = random.randint(1, 6)
            score = dice1 + dice2
            bank_id = 1
            point = 0
            # Update the dice roll result on the form
            self.label_result.config(
                text=f"Dice 1: {dice1}, Dice 2: {dice2}, Total: {score}"
            )

            # Handle come-out roll or point roll logic
            if self.comeout == 0:  # Come-out roll
                if score in (7, 11):
                    messagebox.showinfo("You Win!", "Natural! You Win!")
                elif score in (2, 3, 12):
                    messagebox.showinfo("You Lose", "Craps! You Lose.")
                else:
                    self.point = score
                    self.comeout = 1
                    self.point_label.config(text=f"Point: {self.point}")
                self.save_game_record(bank_id, point, dice1, dice2, score)
            else:  # Point roll
                if score == self.point:
                    messagebox.showinfo("You Win!", "You hit your point! You Win!")
                    self.comeout = 0
                    self.point_label.config(text="Point: None")
                elif score == 7:
                    messagebox.showinfo("You Lose", "Seven Out! You Lose.")
                    self.comeout = 0
                    self.point_label.config(text="Point: None")
                self.save_game_record(bank_id, point, dice1, dice2, score)
        except Exception as e:
            self.log_error(e)

    def save_game_record(self, bank_id, point, dice1, dice2, score):
        try:
            connection = sqlite3.connect("Craps_Bank.db")
            cursor = connection.cursor()
            # Ensure the Game_Records table exists
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS Game_Records (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    bank_id INTEGER NOT NULL,
                    point INTEGER,
                    die_one INTEGER,
                    die_two INTEGER,
                    score INTEGER
                );
            """)
            cursor.execute(
                "INSERT INTO GameRecords (bank_id, point, die_one, die_two, score) VALUES (?, ?, ?, ?, ?)",
                (bank_id, point, dice1, dice2, score),
            )
            connection.commit()
        except sqlite3.Error as e:
            self.log_error(e)
        finally:
            if connection:
                connection.close()

    def submit_deposit(self):
        try:
            deposit_amount = float(self.deposit_entry.get())
            if deposit_amount <= 0:
                raise ValueError("Deposit must be greater than zero.")
            self.bank.add_deposit(deposit_amount)
            self.update_balance()
            self.deposit_entry.delete(0, tk.END)
            self.label_result.config(text=f"Deposit of ${deposit_amount} added!")
        except ValueError as ve:
            self.log_error(ve)
        except Exception as e:
            self.log_error(e)

    def update_balance(self):
        try:
            balance = self.bank.get_balance()
            if balance is not None:
                self.balance_label.config(text=f"Current Balance: ${balance:.2f}")
        except Exception as e:
            self.log_error(e)

            
    def set_wager(self):
        try:
            wager_amount = float(self.wager_value.get())
            current_balance = self.bank.get_balance()
            if wager_amount <= 0 or wager_amount > current_balance:
                raise ValueError("Invalid wager amount.")
            self.bank.add_wager(wager_amount)
            self.wager = wager_amount
            self.update_balance()
            self.label_result.config(text=f"Wager of ${wager_amount} placed!")
        except ValueError as ve:
            self.log_error(ve)
        except Exception as e:
            self.log_error(e)





    def create_widgets(self):
        # Load and display the image
        try:
            image_path = "./images/Craps_Table.jpg"
            image = Image.open(image_path)
            image = image.resize((600, 400), Image.Resampling.LANCZOS)
            self.bg_image = ImageTk.PhotoImage(image)
            self.image_label = tk.Label(self.root, image=self.bg_image)
            self.image_label.pack()
        except Exception as e:
            self.log_error(e)

        # Deposit Section
        self.deposit_label = tk.Label(self.root, text="Enter Deposit:", font=("Helvetica", 10))
        self.deposit_label.place(x=50, y=450)
        self.deposit_entry = tk.Entry(self.root, font=("Helvetica", 14), width=10)
        self.deposit_entry.place(x=50, y=480)
        self.deposit_button = tk.Button(self.root, text="Deposit", command=self.submit_deposit)
        self.deposit_button.place(x=65, y=520)

        # Wager Section
        self.wager_label = tk.Label(self.root, text="Enter Wager:", font=("Helvetica", 10))
        self.wager_label.place(x=610, y=450)
        self.wager_value = tk.IntVar(value=5)  # Default wager is $5
        self.wager_5 = tk.Radiobutton(self.root, text="$5", variable=self.wager_value, value=5, font=("Helvetica", 14))
        self.wager_5.place(x=560, y=480)
        self.wager_10 = tk.Radiobutton(self.root, text="$10", variable=self.wager_value, value=10, font=("Helvetica", 14))
        self.wager_10.place(x=620, y=480)
        self.wager_25 = tk.Radiobutton(self.root, text="$25", variable=self.wager_value, value=25, font=("Helvetica", 14))
        self.wager_25.place(x=685, y=480)
        self.wager_button = tk.Button(self.root, text="Wager", command=self.set_wager)
        self.wager_button.place(x=620, y=520)

        # Balance Display Section
        self.balance_label = tk.Label(self.root, text="Current Balance:", font=("Helvetica", 10))
        self.balance_label.place(x=320, y=450)
        self.balance_label.config(text=f"Current Balance: ${self.bank.get_balance()}")

        # Roll Dice Section
        self.button_roll = tk.Button(self.root, text="Roll Dice", command=self.roll_dice)
        self.button_roll.place(x=350, y=520)
        self.label_result = tk.Label(self.root, text="", font=("Helvetica", 14))
        self.label_result.place(x=300, y=485)

        # Point Display Section
        self.point_label = tk.Label(self.root, text="Point: None", font=("Helvetica", 12))
        self.point_label.place(x=15, y=25)

    def log_error(self, exception):
        _, _, tb = sys.exc_info()
        line_number = traceback.extract_tb(tb)[-1].lineno
        messagebox.showerror("Error", f"An error occurred at line {line_number}: {exception}")



def initialize_database(db_name="Craps_Bank.db"):
    try:
        connection = sqlite3.connect(db_name)
        cursor = connection.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Bank (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                player_id INTEGER NOT NULL DEFAULT 1,
                deposit REAL DEFAULT 0 NOT NULL,
                debit REAL DEFAULT 0 NOT NULL,
                balance REAL DEFAULT 0 NOT NULL,
                point INTEGER DEFAULT NULL,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            );
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Game_Records (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                bank_id INTEGER NOT NULL,
                point INTEGER,
                die_one INTEGER,
                die_two INTEGER,
                score INTEGER
            );
        """)
        connection.commit()
    except sqlite3.Error as e:
        print(f"Database error: {e}")
    finally:
        if connection:
            connection.close()


if __name__ == "__main__":
    initialize_database()
    root = tk.Tk()
    game = CrapsGame(root)
    root.mainloop()
