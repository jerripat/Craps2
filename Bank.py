import sqlite3


class CrapsBank:
    def __init__(self, db_name="Craps_Bank.db"):
        self.db_name = db_name
        self.connection = sqlite3.connect(self.db_name, check_same_thread=False)
        self.cursor = self.connection.cursor()
        self._initialize_db()

    def _initialize_db(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS Bank (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                player_id INTEGER NOT NULL DEFAULT 1,
                deposit REAL DEFAULT 0,
                debit REAL DEFAULT 0,
                balance REAL DEFAULT 0,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            );
        """)
        self.connection.commit()

    def add_deposit(self, amount):
        current_balance = self.get_balance()
        if current_balance == None:
            current_balance = 0
        new_balance = current_balance + amount
        self.cursor.execute(
            "INSERT INTO Bank (deposit, balance) VALUES (?, ?)",
            (amount, new_balance)
        )
        self.connection.commit()

    def add_wager(self, amount):
        current_balance = self.get_balance()
        if amount > current_balance:
            raise ValueError("Wager exceeds current balance.")
        new_balance = current_balance - amount
        self.cursor.execute(
            "INSERT INTO Bank (debit, balance) VALUES (?, ?)", (amount, new_balance)
        )
        self.connection.commit()

    def get_balance(self):
        result = self.cursor.execute("SELECT balance FROM Bank ORDER BY id DESC LIMIT 1").fetchone()
        return result[0] if result else 0.0



    def close_connection(self):
        self.connection.close()


if __name__ == "__main__":
    bank = CrapsBank()
    print("Current balance:", bank.get_balance())
