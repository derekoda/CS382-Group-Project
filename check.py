import sqlite3

# Connect to the database
conn = sqlite3.connect('afpwnsqt.db')

# Create a cursor object to execute SQL queries
cursor = conn.cursor()

# Execute the SELECT statement to retrieve all rows from the my_areas table
cursor.execute('SELECT * FROM my_areas')

# Fetch all the rows returned by the query
rows = cursor.fetchall()

# Iterate over the rows and print the data
for row in rows:
    print(row)

# Close the cursor and the database connection
cursor.close()
conn.close()
