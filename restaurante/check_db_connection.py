
import MySQLdb
import sys

def check_connection():
    try:
        # Try connecting with default XAMPP/WAMP credentials
        print("Attempting to connect to MySQL (root/empty)...")
        db = MySQLdb.connect(
            host="127.0.0.1",
            user="root",
            passwd=""
        )
        print("SUCCESS: Connected to MySQL server.")
        
        cursor = db.cursor()
        cursor.execute("SELECT VERSION()")
        version = cursor.fetchone()[0]
        print(f"Server Version: {version}")
        
        # Check for MariaDB 10.4 incompatibility warning
        # Django 5 requires MariaDB 10.4 or higher.
        
        db_name = "restaurante_db"
        print(f"Creating database '{db_name}' if not exists...")
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {db_name} CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci")
        print(f"Database '{db_name}' ready.")
        
        db.close()
        return True
        
    except MySQLdb.Error as e:
        print(f"ERROR: Cannot connect to MySQL: {e}")
        return False

if __name__ == "__main__":
    if check_connection():
        sys.exit(0)
    else:
        sys.exit(1)
