# Expense Tracker

A simple web-based expense tracking application built with **Flask**, **SQLAlchemy**, and **Chart.js**. Track your expenses by category, view summaries, and visualize spending with interactive charts.

## Features

- **User Authentication**
  - Sign up, log in, and log out securely
  - Password reset via email
- **Expense Management**
  - Add, view, and delete expenses
  - Categorize expenses (e.g., Food, Transport, Utilities)
- **Dashboard**
  - Interactive pie chart showing expenses by category
  - Table of all expenses
  - Responsive design inspired by popular expense tracker apps
- **User-specific Data**
  - Each user sees only their own expenses
  - Secure login with Flask-Login

## Technologies Used

- **Backend:** Flask, SQLAlchemy, Flask-Login
- **Frontend:** HTML, CSS, Chart.js
- **Database:** SQLite
- **Development Tools:** Python 3, VS Code

## Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/samtimi12/Expense_Tracker.git
   cd Expense_Tracker

2. **Create and activate a virtual environment**
    python -m venv venv
    # Windows
    venv\Scripts\activate
    # macOS/Linux
    source venv/bin/activate

3. **Install dependencies**
    pip install -r requirements.txt

4. **Run the application**
    python ET_App.py

5. **Open in your browser**
    http://127.0.0.1:5000/

## Folder Structure

Expense_Tracker/
│
├─ ET_App.py             # Main Flask application
├─ models.py             # Database models for User and Expense
├─ routes/
│   └─ auth.py           # Authentication routes
├─ templates/            # HTML templates
│   ├─ index.html
│   ├─ login.html
│   ├─ signup.html
│   ├─ forgot_password.html
│   └─ reset_password.html
├─ static/
│   └─ style.css         # Stylesheet for all pages
└─ instance/
    └─ expenses.db       # SQLite database

## Usage

- Sign up for a new account or log in.
- Add expenses with a description, amount, and category.
- View your expenses in a table and track category-wise spending through the chart.
- Delete expenses when needed.

## License

This project is open source and available under the MIT License.