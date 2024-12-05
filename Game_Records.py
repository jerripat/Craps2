import sqlite3

def save_to_db(bank_id, point, die_one, die_two, score):
    """
    Saves the game statistics to the Game_Records table in the database.
    """
    try:
        # Debug: Print the values being inserted
        print(f"DEBUG: Attempting to save to DB -> bank_id: {bank_id}, point: {point}, die_one: {die_one}, die_two: {die_two}, score: {score}")

        # Connect to the SQLite database
        connection = sqlite3.connect('Craps_Bank.db')
        print("DEBUG: Connected to database 'Craps_Bank.db'.")  # Debug connection

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
        print("DEBUG: Ensured Game_Records table exists.")  # Debug table creation

        # Insert the game record
        cursor.execute("""
            INSERT INTO Game_Records (bank_id, point, die_one, die_two, score)
            VALUES (?, ?, ?, ?, ?)
        """, (bank_id, point, die_one, die_two, score))
        print("DEBUG: Executed INSERT statement.")  # Debug insert statement

        # Commit the transaction
        connection.commit()
        print("DEBUG: Transaction committed. Record saved successfully.")  # Debug commit

    except sqlite3.Error as e:
        print(f"ERROR: Database error: {e}")  # Debug database error
    finally:
        # Close the connection
        if connection:
            connection.close()
            print("DEBUG: Database connection closed.")  # Debug connection close


class Game_Statistics:
    def __init__(self, bank_id, point, die_one, die_two, score):
        """
        Initializes a game statistics record.
        """
        self.bank_id = bank_id
        self.point = point
        self.die_one = die_one
        self.die_two = die_two
        self.score = score

    def save(self):
        """
        Save the current game statistics to the database.
        """
        print(f"DEBUG: Creating Game_Statistics object with -> bank_id: {self.bank_id}, point: {self.point}, die_one: {self.die_one}, die_two: {self.die_two}, score: {self.score}")
        save_to_db(self.bank_id, self.point, self.die_one, self.die_two, self.score)


if __name__ == "__main__":
    # Example game record
    game_stats = Game_Statistics(
        bank_id=1,
        point=8,
        die_one=4,
        die_two=4,
        score=8
    )

    # Save to the database
    game_stats.save()

    # Verify the data in the database
    try:
        connection = sqlite3.connect("Craps_Bank.db")
        print("DEBUG: Connected to database for verification.")  # Debug connection for verification
        cursor = connection.cursor()

        # Fetch records
        cursor.execute("SELECT * FROM Game_Records;")
        rows = cursor.fetchall()

        print("\nDEBUG: Game_Records Table Content:")
        for row in rows:
            print(row)

    except sqlite3.Error as e:
        print(f"ERROR: Database query error: {e}")  # Debug query error
    finally:
        if connection:
            connection.close()
            print("DEBUG: Database connection closed after verification.")  # Debug connection close
