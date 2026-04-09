from database import connect_db

def add_component(subject_id, component_name, weight, total_items=None):
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO components (subject_id, component_name, weight, total_items) VALUES (?, ?, ?, ?)",
        (subject_id, component_name, weight, total_items)
    )
    conn.commit()
    conn.close()
    print("Component added successfully.")

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

def validate_weights(subject_id):
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT SUM(weight) FROM components WHERE subject_id = ?",
        (subject_id,)
    )

    total = cursor.fetchone()[0]
    conn.close()

    if total is None:
        return False

    return total == 100