## Task 6: Web Scraping Capstone project
# Save cleaned and transformed data into a Sqlite database
import pandas as pd
import sqlite3
import os
db_path = "./climate.db"
# Check if DB already exists
if os.path.exists(db_path):
    answer = input("The database exists.  Do you want to recreate it (y/n)?")
    if answer.lower() != 'y':
        exit(0)
    os.remove(db_path)
# Set up connection
conn = sqlite3.connect(db_path, isolation_level='IMMEDIATE')
conn.execute("PRAGMA foreign_keys = 1")
cursor = conn.cursor()

# Create tables
try: 
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS capitals (
        capital_id INTEGER PRIMARY KEY,          
        capital_name TEXT NOT NULL UNIQUE
    )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS temperatures (
            capital_id INTEGER NOT NULL,          
            max_temp INTEGER NOT NULL,
            min_temp INTEGER NOT NULL,
            mean_temp INTEGER NOT NULL,
            FOREIGN KEY (capital_id) REFERENCES capitals (capital_id)
        )
        """)
    cursor.execute("""
            CREATE TABLE IF NOT EXISTS precipitation (
                capital_id INTEGER NOT NULL,          
                precipitation_value REAL NOT NULL,
                FOREIGN KEY (capital_id) REFERENCES capitals (capital_id)
            )
            """)
except sqlite3.Error as error:
    print(f"An error occurred: {error}")
# Read csv with cleaned and transformed data
climate_df = pd.read_csv("climate_data_clean.csv")

print(climate_df.info())
# Fill capital table
capitals = climate_df["City"]
try:
    for capital in capitals:
        cursor.execute(
            "INSERT INTO capitals (capital_name) VALUES (?)",
            (capital,)
        )

except sqlite3.IntegrityError:
    print(f"{capital,} is already in the database.")
except sqlite3.Error as error:
    print(f"An error occurred: {error}")

# Fill temperatures table
try: 
    for _, row in climate_df.iterrows(): 
        cursor.execute( "SELECT capital_id FROM capitals WHERE capital_name = ?", 
                       (row["City"],) ) 
        result = cursor.fetchone()
        capital_id = result[0] 
        cursor.execute( """ INSERT INTO temperatures 
                            (capital_id, max_temp, min_temp, mean_temp) 
                            VALUES (?, ?, ?, ?) """, 
                            ( capital_id, row["High Temp"], row["Low Temp"], 
                             row["Mean Temp"] ) ) 

except sqlite3.Error as error:
    print(f"An error occurred: {error}")


# Fill precipitation data

try: 
    for _, row in climate_df.iterrows(): 
        cursor.execute( "SELECT capital_id FROM capitals WHERE capital_name = ?", 
                       (row["City"],) ) 
        result = cursor.fetchone()
        capital_id = result[0] 
        cursor.execute( """ INSERT INTO precipitation 
                            (capital_id, precipitation_value) 
                            VALUES (?, ?) """, 
                            ( capital_id, row["Precipitation"] ) ) 

except sqlite3.Error as error:
    print(f"An error occurred: {error}")

conn.commit()
conn.close()

