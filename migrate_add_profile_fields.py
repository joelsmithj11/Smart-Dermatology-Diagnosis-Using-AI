"""
Database Migration Script: Add User Profile Fields
Adds patient information fields to users table for profile completion feature
"""

import sqlite3
import os

# Database path
DB_PATH = os.path.join(os.path.dirname(__file__), 'database', 'dermatology.db')

def migrate():
    """Add new columns to users table"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    try:
        print("Starting database migration...")
        
        # Check if columns already exist
        cursor.execute("PRAGMA table_info(users)")
        columns = [col[1] for col in cursor.fetchall()]
        
        # Add new columns if they don't exist
        new_columns = [
            ('patient_name', 'TEXT'),
            ('gender', 'TEXT'),
            ('location', 'TEXT'),
            ('state', 'TEXT'),
            ('country', 'TEXT'),
            ('profile_completed', 'INTEGER DEFAULT 0')
        ]
        
        for col_name, col_type in new_columns:
            if col_name not in columns:
                print(f"Adding column: {col_name}")
                cursor.execute(f"ALTER TABLE users ADD COLUMN {col_name} {col_type}")
            else:
                print(f"Column {col_name} already exists, skipping...")
        
        # Update is_verified default for new users (existing users keep their value)
        print("Migration completed successfully!")
        
        conn.commit()
        
        # Verify migration
        cursor.execute("PRAGMA table_info(users)")
        print("\nUpdated users table structure:")
        for col in cursor.fetchall():
            print(f"  - {col[1]} ({col[2]})")
        
    except Exception as e:
        print(f"ERROR during migration: {e}")
        conn.rollback()
        raise
    finally:
        conn.close()

if __name__ == "__main__":
    migrate()
