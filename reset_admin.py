import sqlite3
import os
from werkzeug.security import generate_password_hash

# Correct path based on root execution
DB_PATH = os.path.join("database", "dermatology.db")

def reset_admin_password():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    
    new_pass = "admin123"
    hashed = generate_password_hash(new_pass)
    
    # Update 'admin' user
    try:
        cur.execute("UPDATE users SET password_hash = ? WHERE username = 'admin'", (hashed,))
        if cur.rowcount > 0:
            print(f"Password for 'admin' has been reset to '{new_pass}'")
        else:
            print("User 'admin' not found. Creating it...")
            cur.execute("INSERT INTO users (username, password_hash, role, is_verified) VALUES (?, ?, ?, ?)",
                        ('admin', hashed, 'admin', 1))
            print(f"User 'admin' created with password '{new_pass}'")
            
        conn.commit()
    except Exception as e:
        print(f"Error: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    reset_admin_password()
