import random
import tkinter as tk
from Bank import CrapsBank
from PIL import Image, ImageTk
from tkinter import messagebox
import sys
import traceback
import sqlite3


class CrapsGame:
    def __init__(self):
        self.bank_id = 1
        self.dice1 = None
        self.dice2 = None
        self.wager = 0
        self.current_roll = None
        self.comeout = 0
        self.point = 0
        self.bank = CrapsBank()

        # Initialize the GUI
        self.root = tk.Tk()
        self.root.title("Craps Game")
        self.root.geometry("800x600")
        self.root.configure(background="white")
        self.create_widgets()


    def roll_dice(self):
        try:
            self.dice1 = random.randint(1, 6)
            self.dice2 = random.randint(1, 6)
            self.current_roll = self.dice1 + self.dice2

            # Update the balance display
            self.balance_total.config(text=f"Balance: ${self.bank.get_balance():.2f}")

            # Update the dice roll result on the form
            self.label_result.config(
                text=f"Dice 1: {self.dice1}, Dice 2: {self.dice2}, Total: {self.current_roll}"
            )

            # Handle game logic
            if self.comeout == 0:  # Come-out roll
                if self.current_roll in (7, 11):
                    messagebox.showinfo("You Win!", "Natural! You Win!")
                    self.save_to_db(self.bank_id, self.dice1, self.dice2, self.current_roll)
                elif self.current_roll in (2, 3, 12):
                    messagebox.showinfo("You Lose", "Craps! You Lose.")
                    self.save_to_db(self.bank_id, self.dice1, self.dice2, self.current_roll)
                else:  # Establish the point
                    self.point = self.current_roll
                    self.comeout = 1
                    self.point_label.config(text=f"Point: {self.point}")
                    self.insert_point(self.point)
                    self.save_to_db(self.bank_id, self.dice1, self.dice2, self.current_roll)
            else:  # Point roll
                if self.current_roll == self.point:
                    messagebox.showinfo("You Win!", "You hit your point! You Win!")
                    self.comeout = 0
                    self.point_label.config(text="Point: None")
                    self.save_to_db(self.bank_id, self.dice1, self.dice2, self.current_roll)
                elif self.current_roll == 7:
                    messagebox.showinfo("You Lose", "Seven Out! You Lose.")
                    self.comeout = 0
                    self.point_label.config(text="Point: None")
                    self.save_to_db(self.bank_id, self.dice1, self.dice2,self.current_roll)
        except Exception as e:
            self.log_error(e)

    def create_widgets(self):
        # Load and display the image
        image_path = "./images/Craps_Table.jpg"
        try:
            image = Image.open(image_path)
            image = image.resize((600, 400), Image.Resampling.LANCZOS)
            self.bg_image = ImageTk.PhotoImage(image)
            self.image_label = tk.Label(self.root, image=self.bg_image)
            self.image_label.pack()
        except Exception as e:
            self.log_error(e)

        # Deposit Section
        self.deposit_label = tk.Label(self.root, text="Enter Deposit:", font=("Helvetica", 10), bg="white", fg="green")
        self.deposit_label.place(x=25, y=450)
        self.deposit_entry = tk.Entry(self.root, font=("Helvetica", 14), width=10, bd=2, relief="sunken")
        self.deposit_entry.place(x=25, y=480)
        self.deposit_button = tk.Button(self.root, text="Deposit", command=self.submit_deposit)
        self.deposit_button.place(x=25, y=520)

        # Wager Section
        self.wager_label = tk.Label(self.root, text="Enter Wager:", font=("Helvetica", 10), bg="white", fg="green")
        self.wager_label.place(x=650, y=450)
        self.wager_entry = tk.Entry(self.root, font=("Helvetica", 14), width=10, bd=2, relief="sunken")
        self.wager_entry.place(x=650, y=480)
        self.wager_button = tk.Button(self.root, text="Wager", command=self.set_wager)
        self.wager_button.place(x=650, y=520)

        # Roll Dice Section
        self.button_roll = tk.Button(self.root, text="Roll Dice", command=self.roll_dice)
        self.button_roll.place(x=350, y=500)
        self.label_result = tk.Label(self.root, text="", font=("Helvetica", 14), bg="white", fg="green")
        self.label_result.place(x=300, y=550)

        # Show Balance
        self.balance_label = tk.Label(self.root, text="Current Balance:", font=("Helvetica", 10), bg="white", fg="green")
        self.balance_label.place(x=325, y=450)
        self.balance_total = tk.Label(self.root, text="Balance:", font=("Helvetica", 10), bg="white", fg="green")
        self.balance_total.place(x=325, y=470)

        # Point Display Section
        self.point_label = tk.Label(self.root, text="Point: None", font=("Helvetica", 12), bg="white", fg="blue")
        self.point_label.place(x=15, y=25)

    def log_error(self, exception):
        _, _, tb = sys.exc_info()
        line_number = traceback.extract_tb(tb)[-1].lineno
        messagebox.showerror("Error", f"An error occurred at line {line_number}: {exception}")

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

    def set_wager(self):
        try:
            wager_amount = float(self.wager_entry.get())
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

    def update_balance(self):
        try:
            balance = self.bank.get_balance()
            self.balance_total.config(text=f"Balance: ${balance:.2f}")
        except Exception as e:
            self.log_error(e)

    # def insert_point(self, point):
    #     """
    #     Updates the current point in the Bank table for the player.
    #     :param point: The point to record.
    #     """
    #     try:
    #         # Use the existing CrapsBank connection
    #         self.bank.cursor.execute(
    #             "UPDATE Bank SET point = ? WHERE player_id = ?", (point, 1)
    #         )
    #         self.bank.connection.commit()
    #         print(f"Point {point} recorded successfully.")
    #     except sqlite3.Error as e:
    #         self.log_error(e)

    def main_loop(self):
        self.root.mainloop()



def initialize_database(db_name="Craps_Bank.db"):
    """
    Initializes the database and ensures that the required tables are created.
    Also adds missing columns if necessary.
    """
    try:
        # Connect to the SQLite database
        connection = sqlite3.connect(db_name)
        cursor = connection.cursor()

        # Create the Bank table if it does not exist
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Bank (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                player_id INTEGER NOT NULL DEFAULT 1,
                deposit REAL DEFAULT 0 NOT NULL,
                debit REAL DEFAULT 0 NOT NULL,
                balance REAL DEFAULT 0 NOT NULL,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            );
        """)

        # Check if 'point' column exists and add it if missing
        cursor.execute("PRAGMA table_info(Bank);")
        columns = [column[1] for column in cursor.fetchall()]
        if "point" not in columns:
            cursor.execute("ALTER TABLE Bank ADD COLUMN point INTEGER DEFAULT NULL;")
            print("Added 'point' column to Bank table.")

        # Commit changes
        connection.commit()
        print(f"Database '{db_name}' initialized successfully.")
    except sqlite3.Error as e:
        print(f"Database initialization error: {e}")
    finally:
        if connection:
            connection.close()


if __name__ == "__main__":
       # Initialize the database
        initialize_database()

        # Start the game
        game = CrapsGame()
        game.main_loop()
