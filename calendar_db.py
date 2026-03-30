import sqlite3

# This creates a file called 'my_calendar.db' to hold our schedule
conn = sqlite3.connect('my_calendar.db')
cursor = conn.cursor()

# Create a table (like an Excel sheet) with time slots and tasks
cursor.execute('''
CREATE TABLE IF NOT EXISTS schedule (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    time_slot TEXT UNIQUE,
    task_name TEXT
)
''')

# Clear old data so we always start fresh when testing
cursor.execute('DELETE FROM schedule')

# Pre-book a slot so we can test the conflict feature!
cursor.execute('INSERT INTO schedule (time_slot, task_name) VALUES (?, ?)', ('10:00 AM', 'Daily Team Standup'))

conn.commit()
conn.close()

print("Calendar Database created! '10:00 AM' is currently booked.")