import sqlite3

conn = sqlite3.connect("database.db")
cursor = conn.cursor()

# Delete all data
cursor.execute("DELETE FROM users")

# Reset auto-increment
cursor.execute("DELETE FROM sqlite_sequence WHERE name='users'")

conn.commit()

# Verify
cursor.execute("SELECT * FROM sqlite_sequence")
print(cursor.fetchall())

conn.close()

print("Reset done")