from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, login_required, current_user
import os
from models import db, Expense, User
from collections import defaultdict

# --- Flask App Setup ---
app = Flask(__name__)
app.secret_key = "supersecretkey"

# --- Database Setup ---
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
db_path = os.path.join(BASE_DIR, "instance", "expenses.db")
os.makedirs(os.path.join(BASE_DIR, "instance"), exist_ok=True)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + db_path
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

# --- Flask-Login Setup ---
login_manager = LoginManager()
login_manager.login_view = "auth.login"
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# --- Routes ---
@app.route("/")
@login_required
def index():
    expenses = Expense.query.filter_by(user_id=current_user.id).all()

    # Build categories dictionary
    categories = {}
    for exp in expenses:
        if exp.category in categories:
            categories[exp.category] += exp.amount
        else:
            categories[exp.category] = exp.amount

    return render_template("index.html", expenses=expenses, categories=categories)


@app.route("/add", methods=["POST"])
@login_required
def add():
    description = request.form.get("description")
    amount = float(request.form.get("amount"))
    category = request.form.get("category")

    new_expense = Expense(
        description=description,
        amount=float(amount),
        category=category,
        user_id=current_user.id  # <-- associate expense with logged-in user
    )
    db.session.add(new_expense)
    db.session.commit()
    flash("Expense added successfully.", "success")
    return redirect(url_for("index"))

@app.route("/delete/<int:id>", methods=["POST"])
@login_required
def delete_expense(id):
    expense = Expense.query.get_or_404(id)
    if expense.user_id != current_user.id:
        flash("You cannot delete this expense.", "danger")
        return redirect(url_for("index"))

    db.session.delete(expense)
    db.session.commit()
    flash("Expense deleted successfully.", "success")
    return redirect(url_for("index"))

@app.route("/edit/<int:id>", methods=["GET", "POST"])
@login_required
def edit_expense(id):
    expense = Expense.query.get_or_404(id)

    if request.method == "POST":
        expense.description = request.form.get("description")
        expense.amount = float(request.form.get("amount"))
        expense.category = request.form.get("category")
        db.session.commit()
        flash("Expense updated successfully.", "success")
        return redirect(url_for("index"))

    return render_template("edit_expense.html", expense=expense)

# --- Blueprints ---
from routes.auth import auth
app.register_blueprint(auth, url_prefix="/")

# --- Run App ---
if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
