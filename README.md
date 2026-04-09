# Dynamic Grade Monitoring System

A desktop application built with Python and Tkinter for tracking and projecting academic grades using a weighted grading system.

## Features

- **User Authentication** — Register and login with secure password hashing
- **Subject Management** — Create and manage multiple subjects per user
- **Component-Based Grading** — Define grading components (Quizzes, Exams, Activities) with weight percentages
- **Score Tracking** — Log scores per component with automatic weighted average calculation
- **Grade Calculation** — Computes weighted grade and converts to numeric grade (1.00–5.00 scale)
- **Grade Projection** — Projects required scores on future assessments to achieve a target grade, distributed equally across unscored components
- **Performance Classification** — Outstanding (1.00–1.50), Safe (1.75–2.50), At Risk (2.75–3.00), Critical (5.00)

## Grade Conversion Table

| Numeric | From % | To % |
|---------|--------|------|
| 1.00    | 98     | 100  |
| 1.25    | 94     | 97   |
| 1.50    | 90     | 93   |
| 1.75    | 88     | 89   |
| 2.00    | 85     | 87   |
| 2.25    | 83     | 84   |
| 2.50    | 80     | 82   |
| 2.75    | 78     | 79   |
| 3.00    | 75     | 77   |
| 5.00    | 0      | 74   |

## Project Structure

```
├── main.py          # Entry point
├── gui.py           # All GUI screens (Login, Dashboard, Projection)
├── database.py      # SQLite connection and table management
├── auth.py          # User registration and login
├── subject.py       # Subject CRUD operations
├── component.py     # Component CRUD operations
├── grade_logic.py   # Grade computation and projection logic
└── assets/          # Icons and images
    ├── icon_grade.png
    └── icon_grade.ico
```

## Requirements

```
Python 3.10+
Pillow (optional, for image icon support)
```

## Installation

1. Clone the repository:
```bash
git clone https://github.com/YOUR_USERNAME/Grade-Monitoring-System.git
cd Grade-Monitoring-System
```

2. Create and activate virtual environment:
```bash
python -m venv .venv
.venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install pillow
```

4. Run the application:
```bash
python main.py
```

## Disclaimer

This system is for grade and required score estimation only. It does not include mark transmutation or incentive-driven grades, focusing on raw grading for use with zero-based grading systems. Results do not reflect official final grades.

---
*Developed as part of CC 102 — Advanced Computer Programming*  
*Batangas State University*
