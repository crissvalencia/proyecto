
import MySQLdb
import os
import sys

def reset_and_migrate():
    print("Resetting database...")
    try:
        db = MySQLdb.connect(host="127.0.0.1", user="root", passwd="")
        cursor = db.cursor()
        cursor.execute("DROP DATABASE IF EXISTS restaurante_db")
        cursor.execute("CREATE DATABASE restaurante_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci")
        db.close()
        print("Database reset successfully.")
    except Exception as e:
        print(f"Error resetting database: {e}")
        sys.exit(1)

    print("Running migrations...")
    exit_code = os.system("python manage.py migrate")
    if exit_code != 0:
        print("Migration failed.")
        sys.exit(1)
        
    print("Loading data...")
    # Using utf8 dump
    exit_code = os.system("python manage.py loaddata db_dump_utf8.json")
    if exit_code != 0:
        print("Data load failed.")
        sys.exit(1)
        
    print("Migration sequence completed successfully.")

if __name__ == "__main__":
    reset_and_migrate()
