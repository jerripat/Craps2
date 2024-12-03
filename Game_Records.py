import sqlite3


import sqlite3

class Game_Statistics:
    def __init__(self, bank_id, point, die_one, die_two, score, win, lose):
        self.bank_id = bank_id
        self.point = point
        self.die_one = die_one
        self.die_two = die_two
        self.score = score
        self.win = win
        self.lose = lose

    def save_to_db(self):
        """
        Saves the game statistics to the Game_Records table in the database.
        """
        try:
            # Connect to the SQLite database
            connection = sqlite3.connect('Craps_Bank.db')
            cursor = connection.cursor()

            # Ensure the Game_Records table exists
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS Game_Records (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    bank_id INTEGER NOT NULL,
                    point INTEGER,
                    die_one INTEGER,
                    die_two INTEGER,
                    score INTEGER,
                    win BOOLEAN,
                    lose BOOLEAN
                );
            """)

            # Insert the game record
            cursor.execute("""
                INSERT INTO Game_Records (bank_id, point, die_one, die_two, score)
                VALUES (?, ?, ?, ?, ?)
            """, (self.bank_id, self.point, self.die_one, self.die_two, self.score))

            # Commit the transaction
            connection.commit()
            print("Game record saved successfully.")
        except sqlite3.Error as e:
            print(f"Database error: {e}")
        finally:
            if connection:
                # Ensure the connection is closed
                connection.close()
