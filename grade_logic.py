from database import connect_db
from subject import get_components

GRADE_TABLE = [
    (1.00, 98, 100),
    (1.25, 94,  97),
    (1.50, 90,  93),
    (1.75, 88,  89),
    (2.00, 85,  87),
    (2.25, 83,  84),
    (2.50, 80,  82),
    (2.75, 78,  79),
    (3.00, 75,  77),
    (5.00,  0,  74),  # INC / Failed
]

def convert_to_numeric_grade(percentage):
    for numeric, low, high in GRADE_TABLE:
        if low <= round(percentage) <= high:
            return numeric
    return 5.00

def classify_performance(numeric_grade):
    if 1.00 <= numeric_grade <= 1.50:
        return "Outstanding"
    elif 1.75 <= numeric_grade <= 2.50:
        return "Safe"
    elif 2.75 <= numeric_grade <= 3.00:
        return "At Risk"
    else:
        return "Critical"

def add_score(component_id, score):
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO scores (component_id, score_value) VALUES (?, ?)",
        (component_id, score)
    )

    conn.commit()
    conn.close()

def get_score_for_component(component_id):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT score_value FROM scores WHERE component_id = ?",
        (component_id,)
    )
    scores = cursor.fetchall()
    conn.close()
    return [s[0] for s in scores]

def calculate_component_percentage(component_id):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT total_items FROM components WHERE component_id = ?", (component_id,))
    row = cursor.fetchone()

    if not row or not row[0]:
        conn.close()
        return 0
    total_items = row[0]

    cursor.execute("SELECT AVG(score_value) FROM scores WHERE component_id = ?", (component_id,))
    avg = cursor.fetchone()[0]
    conn.close()

    if avg is not None and total_items:
        return (avg / total_items) * 100
    return 0

def compute_weighted_grade(subject_id):
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT component_id, weight FROM components WHERE subject_id = ?",
        (subject_id,)
    )

    components = cursor.fetchall()
    conn.close()

    final_grade = 0

    for comp_id, weight in components:
        avg_pct = calculate_component_percentage(comp_id)
        scores = get_score_for_component(comp_id)
        if scores:
            final_grade += avg_pct * (weight / 100)

    return round(final_grade, 2)

def project_required_scores(subject_id, target_percentage):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute(
        """SELECT component_id, component_name, weight, total_items FROM components WHERE subject_id = ?""",
        (subject_id,)
    )

    components = cursor.fetchall()
    conn.close()

    if not components:
        return[]

    results = []

    already_earned_weight = 0.0
    unscored_total_weight = 0.0

    for comp in components:
        comp_id  = comp[0]
        comp_name = comp[1]
        weight = comp[2]
        total_items = comp[3]

        scores = get_score_for_component(comp_id)

        if scores and total_items:
            avg_pct = calculate_component_percentage(comp_id)
            earned_weight = avg_pct * (weight / 100)
            already_earned_weight += earned_weight

            results.append({
                'comp_id': comp_id,
                'name': comp_name,
                'weight': weight,
                'has_score': True,
                'actual_pct': round(avg_pct, 2),
                'earned_weight': round(earned_weight, 2),
                'required_pct': None,
                'required_score': None,
                'total_items': total_items,
                'status': 'done',
            })
        else:
            unscored_total_weight += weight
            results.append({
                'comp_id': comp_id,
                'name': comp_name,
                'weight': weight,
                'has_score': False,
                'actual_pct': None,
                'earned_weight': None,
                'required_pct': None,
                'required_score': None,
                'total_items': total_items,
                'status': 'pending',
            })
    remaining_weight_needed = target_percentage - already_earned_weight

    unscored_comps = [r for r in results if not r['has_score']]
    n_unscored = len(unscored_comps)

    for r in results:
        if r['has_score']:
            continue

        weight = r['weight']

        if n_unscored == 0 or unscored_total_weight == 0:
            r['required_pct'] = 0
            r['required_score'] = 0
            r['status'] = 'projected'
            continue

        required_pct = (remaining_weight_needed / unscored_total_weight) * 100
        required_pct = max(0, required_pct)

        r['required_pct'] = round(required_pct, 2)

        if r['total_items']:
            required_raw = (required_pct/ 100) * r['total_items']
            r['required_score'] = round(required_raw, 1)
            r['status'] = 'projected'
        else:
            r['status'] = 'projected_pct_only'

    return results

def calculate_passing_score(component_id):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT total_items FROM components WHERE component_id = ?", (component_id,))

    row = cursor.fetchone()
    conn.close()

    if row:
        return row[0] * 0.75
    return 0

def validate_passing_scores(subject_id):
    components = get_components(subject_id)
    passing_issues = []

    for comp in components:
        comp_id = comp[0]
        comp_name = comp[1]
        total_items = comp[3]

        scores = get_score_for_component(comp_id)
        if not scores or not total_items:
            continue

        avg_pct = calculate_component_percentage(comp_id)
        if avg_pct < 75.0:
            passing_issues.append({
                'component': comp_name,
                'current': round(avg_pct, 2),
                'required': 75.0
            })

    return passing_issues

