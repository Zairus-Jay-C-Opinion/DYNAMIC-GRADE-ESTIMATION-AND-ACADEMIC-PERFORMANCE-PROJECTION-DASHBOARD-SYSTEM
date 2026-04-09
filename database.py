import sqlite3

def connect_db():
    try:
        conn = sqlite3.connect("grade_system.db")
        conn.row_factory = sqlite3.Row
        return conn
    except sqlite3.Error as e:
        print(f"Database connection error: {e}")
        return None


def create_tables():
    conn = connect_db()
    if not conn:
        return
    cursor = conn.cursor()

    try:
        cursor.execute("PRAGMA foreign_keys = ON")

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS users(
            user_id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL
        )
        """)

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS subjects(
            subject_id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            subject_name TEXT NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
        )
        """)

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS components(
            component_id INTEGER PRIMARY KEY AUTOINCREMENT,
            subject_id INTEGER NOT NULL,
            component_name TEXT NOT NULL,
            weight REAL NOT NULL,
            total_items INTEGER,
            FOREIGN KEY (subject_id) REFERENCES subjects(subject_id) ON DELETE CASCADE
        )
        """)

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS scores(
            score_id INTEGER PRIMARY KEY AUTOINCREMENT,
            component_id INTEGER NOT NULL,
            score_value REAL NOT NULL,
            FOREIGN KEY (component_id) REFERENCES components(component_id) ON DELETE CASCADE
        )
        """)

        conn.commit()

        cursor.execute("PRAGMA table_info(components)")
        cols = cursor.fetchall()
        for col in cols:
            # col[1]=name, col[3]=notnull
            if col[1] == "total_items" and col[3] == 1:
                print("Migrating components table — removing NOT NULL on total_items...")
                cursor.executescript("""
                            PRAGMA foreign_keys = OFF;

                            CREATE TABLE IF NOT EXISTS components_new(
                                component_id   INTEGER PRIMARY KEY AUTOINCREMENT,
                                subject_id     INTEGER NOT NULL,
                                component_name TEXT NOT NULL,
                                weight         REAL NOT NULL,
                                total_items    INTEGER,
                                FOREIGN KEY (subject_id)
                                    REFERENCES subjects(subject_id) ON DELETE CASCADE
                            );

                            INSERT INTO components_new
                                (component_id, subject_id, component_name, weight, total_items)
                            SELECT component_id, subject_id, component_name, weight, total_items
                            FROM components;

                            DROP TABLE components;

                            ALTER TABLE components_new RENAME TO components;

                            PRAGMA foreign_keys = ON;
                        """)
                conn.commit()
                print("Migration complete.")
                break

    except sqlite3.Error as e:
        print(f"Table creation error: {e}")
    finally:
        conn.close()

def delete_subject(user_id, subject_id):
    conn = connect_db()
    if not conn:
        return False
    cursor = conn.cursor()
    try:
        cursor.execute(
            "DELETE FROM subjects WHERE subject_id = ? AND user_id = ?",
            (subject_id, user_id)
        )
        conn.commit()
        conn.close()
        return True
    except sqlite3.Error as e:
        print(f"Delete subject error: {e}")
        conn.close()
        return False

def delete_component(subject_id, component_id):
    conn = connect_db()
    if not conn:
        return False
    cursor = conn.cursor()
    try:
        cursor.execute(
            "DELETE FROM components WHERE component_id = ? AND subject_id = ?",
            (component_id, subject_id)
        )
        conn.commit()
        conn.close()
        return True
    except sqlite3.Error as e:
        print(f"Delete component error: {e}")
        conn.close()
        return False

def delete_scores_by_component(component_id):
    conn = connect_db()
    if not conn:
        return False
    cursor = conn.cursor()
    try:
        cursor.execute(
            "DELETE FROM scores WHERE component_id = ?",
            (component_id,)
        )
        conn.commit()
        conn.close()
        return True
    except sqlite3.Error as e:
        print(f"Delete scores error: {e}")
        conn.close()
        return False