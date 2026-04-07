import sqlite3

def init_database():
    conn = sqlite3.connect('my_calendar.db') 
    cursor = conn.cursor()

    # 1. Ensure the Calendar table exists
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS calendar (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            time_slot TEXT NOT NULL,
            task_name TEXT NOT NULL
        )
    ''')

    # 2. Ensure the Tasks table exists
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            task_name TEXT NOT NULL,
            priority TEXT DEFAULT 'Medium',
            status TEXT DEFAULT 'Pending'
        )
    ''')

    conn.commit()
    conn.close()
    print("✅ Success: Database is fully prepped with both 'calendar' and 'tasks' tables!")

if __name__ == "__main__":
    init_database()