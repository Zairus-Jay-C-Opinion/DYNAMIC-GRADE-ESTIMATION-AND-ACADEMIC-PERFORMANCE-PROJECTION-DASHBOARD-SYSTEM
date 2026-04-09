import hashlib
import sqlite3

from database import connect_db

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def register_user(username, password):
    conn = connect_db()
    if not conn:
        return False
    cursor = conn.cursor()

    hashed_pw = hash_password(password)

    try:
        cursor.execute(
            "INSERT INTO users (username, password_hash) VALUES (?, ?)",
            (username, hashed_pw)
        )
        conn.commit()
        conn.close()
        print("User registered successfully.")
        return True
    except sqlite3.IntegrityError:
        conn.close()
        return False
    except Exception as e:
        print("Error:", e)
        conn.close()
        return False

def login_user(username, password):
    conn = connect_db()
    if not conn:
        return None
    cursor = conn.cursor()

    hashed_pw = hash_password(password)

    cursor.execute(
        "SELECT user_id FROM users WHERE username = ? AND password_hash = ?",
        (username, hashed_pw)
    )

    result = cursor.fetchone()
    conn.close()

    if result:
        print("Login successful.")
        return result[0]
    else:
        print("Invalid username or password.")
        return None

