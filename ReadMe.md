Expense Tracker

A Flask-based Expense Tracker web application with authentication, CRUD functionality, and visual expense analytics using Chart.js.

This project allows users to:

Sign up, log in, and manage their account.

Add, view, and delete expenses.

Categorize expenses and view a pie chart breakdown.

Features

Authentication: Login, Sign up, Forgot Password, Reset Password

Expense Management: Add, delete, and view expenses

Category Analytics: Pie chart displaying expenses by category

Responsive UI: Dashboard styled for an intuitive experience

Tech Stack

Backend: Python, Flask, SQLAlchemy

Database: SQLite

Frontend: HTML, CSS, Jinja2 templates, Chart.js

Authentication: Flask-Login

Installation

Clone the repository:

git clone https://github.com/<your-username>/expense-tracker.git
cd expense-tracker


Create and activate a virtual environment:

python -m venv venv
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate


Install dependencies:

pip install -r requirements.txt

Setup

Ensure the instance/ folder exists (SQLite database will be created here).

Run the application:

python ET_App.py


Access the app at:

http://127.0.0.1:5000

Project Structure
Expense_Tracker/
├─ ET_App.py             # Main Flask app
├─ models.py             # Database models (User, Expense)
├─ routes/
│  └─ auth.py            # Authentication routes
├─ templates/
│  ├─ index.html         # Dashboard & expenses page
│  ├─ login.html
│  ├─ signup.html
│  ├─ forgot_password.html
│  └─ reset_password.html
├─ static/
│  └─ style.css          # All CSS styles
├─ instance/
│  └─ expenses.db        # SQLite database (not pushed)
├─ requirements.txt
└─ README.md

Notes

The database file (expenses.db) is automatically created inside the instance/ folder.

Make sure to never push your virtual environment or database to GitHub. .gitignore is configured to exclude them.

All flash messages, form validations, and charts rely on existing CSS and JS files.

License

This project is released under the MIT License.