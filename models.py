from flask_login import UserMixin
from app.utils.db import get_connection
from app import login_manager

class User(UserMixin):
    def __init__(self, id, username, role, email, is_verified=0):
        self.id = id
        self.username = username
        self.role = role
        self.email = email
        self.is_verified = is_verified

    @staticmethod
    def get(user_id):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM users WHERE id = ?", (user_id,))
        user = cur.fetchone()
        conn.close()
        
        if not user:
            return None

        # Schema observed: 
        # 0:id, 1:username, 2:mobile, 3:role, 4:password_hash, 5:is_verified, 6:email
        
        # We need to handle cases where email might be None (old users) or exist.
        # mobile is at 2.
        
        mobile = user[2]
        role = user[3]
        # is_verified at 5
        is_verified = user[5] if len(user) > 5 else 1
        
        # email at 6
        email = user[6] if len(user) > 6 else None
        
        # If email is missing, maybe fallback to mobile or empty?
        # But our app now expects email.
        final_email = email if email else mobile # Fallback for display if needed
        
        return User(id=user[0], username=user[1], role=role, email=final_email, is_verified=is_verified)

    @staticmethod
    def get_by_username(username):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM users WHERE username = ?", (username,))
        user = cur.fetchone()
        conn.close()

        if not user:
            return None
            
        role = user[3]
        is_verified = user[5] if len(user) > 5 else 1
        email = user[6] if len(user) > 6 else None
        
        return User(id=user[0], username=user[1], role=role, email=email, is_verified=is_verified)

    @staticmethod
    def get_user_with_password(username):
        """Helper to get user with password hash for auth verification"""
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM users WHERE username = ?", (username,))
        user = cur.fetchone()
        conn.close()
        return user

@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)
