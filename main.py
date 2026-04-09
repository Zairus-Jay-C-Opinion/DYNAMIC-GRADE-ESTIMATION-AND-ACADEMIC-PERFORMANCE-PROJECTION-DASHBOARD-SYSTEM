from dashboard_screen  import GradeDashboard
from database import create_tables

def main():
    create_tables()

    root = GradeDashboard()
    root.mainloop()

if __name__ == "__main__":
    main()
