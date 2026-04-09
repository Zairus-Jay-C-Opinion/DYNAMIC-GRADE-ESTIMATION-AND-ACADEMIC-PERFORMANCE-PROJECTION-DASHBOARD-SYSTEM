from database import connect_db

def create_subject(user_id, subject_name):
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO subjects (user_id, subject_name) VALUES (?, ?)",
        (user_id, subject_name)
    )

    conn.commit()
    conn.close()
    print("Subject created successfully.")

def get_user_subjects(user_id):
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT subject_id, subject_name FROM subjects WHERE user_id = ?",
        (user_id,)
    )

    subjects = cursor.fetchall()
    conn.close()

    return subjects

def get_components(subject_id):
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT component_id, component_name, weight, total_items FROM components WHERE subject_id = ?",
        (subject_id,)
    )

    components = cursor.fetchall()
    conn.close()

    return components