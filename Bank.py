import sqlite3


class CrapsBank:
    def __init__(self, db_name="Craps_Bank.db"):
        self.db_name = db_name
        self.connection = sqlite3.connect(self.db_name, check_same_thread=False)
        self.cursor = self.connection.cursor()
        self._initialize_db()

    def _initialize_db(self):
        """Initialize the Bank table if it does not exist."""
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
        """Add a deposit to the player's account."""
        if amount <= 0:
            raise ValueError("Deposit amount must be greater than zero.")
        current_balance = self.get_balance()
        new_balance = current_balance + amount
        self.cursor.execute(
            "INSERT INTO Bank (deposit, balance) VALUES (?, ?)",
            (amount, new_balance)
        )
        self.connection.commit()

    def add_wager(self, amount):
        """Deduct a wager amount from the player's balance."""
        if amount <= 0:
            raise ValueError("Wager amount must be greater than zero.")
        current_balance = self.get_balance()
        if amount > current_balance:
            raise ValueError("Wager exceeds current balance.")
        new_balance = current_balance - amount
        self.cursor.execute(
            "INSERT INTO Bank (debit, balance) VALUES (?, ?)",
            (amount, new_balance)
        )
        self.connection.commit()

    def get_balance(self):
        """Retrieve the current balance of the player."""
        result = self.cursor.execute("SELECT balance FROM Bank ORDER BY id DESC LIMIT 1").fetchone()
        return result[0] if result else 0.0

    def get_transaction_history(self, limit=10):
        """Retrieve the last `limit` transactions."""
        self.cursor.execute("""
            SELECT id, deposit, debit, balance, timestamp
            FROM Bank
            ORDER BY id DESC
            LIMIT ?
        """, (limit,))
        return self.cursor.fetchall()

    def reset_balance(self):
        """Reset the player's balance to zero."""
        self.cursor.execute("INSERT INTO Bank (balance) VALUES (0)")
        self.connection.commit()

    def close_connection(self):
        """Close the database connection."""
        self.connection.close()
