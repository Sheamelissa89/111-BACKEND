from flask import Flask, jsonify, request, render_template
import sqlite3

app = Flask(__name__)


# FRONTEND PAGE ROUTES

@app.route("/", methods=["GET"])
def home():
    connection = sqlite3.connect("budget_manager.db")
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()

    cursor.execute("""
        SELECT *
        FROM expenses
        ORDER BY expense_date DESC, expense_id DESC
    """)
    expenses = cursor.fetchall()

    connection.close()

    total_expenses = sum(expense["amount"] for expense in expenses)
    expense_count = len(expenses)
    recent_expenses = expenses[:5]

    return render_template(
        "home.html",
        total_expenses=total_expenses,
        expense_count=expense_count,
        recent_expenses=recent_expenses
    )


@app.route("/about", methods=["GET"])
def about():
    return render_template("about.html")


@app.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        message = request.form.get("message")

        print("Contact form submitted:")
        print(f"Name: {name}")
        print(f"Email: {email}")
        print(f"Message: {message}")

        return render_template(
            "contact.html",
            success_message=f"Thank you, {name}! Your message was submitted."
        )

    return render_template("contact.html")


# API HEALTH CHECK

@app.route("/api/health", methods=["GET"])
def health_check():
    return jsonify({"status": "OK"}), 200


# GET ALL EXPENSES

@app.route("/api/expenses", methods=["GET"])
def get_expenses():
    connection = sqlite3.connect("budget_manager.db")
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM expenses")
    expenses = cursor.fetchall()

    connection.close()

    expenses_list = [dict(expense) for expense in expenses]

    return jsonify(expenses_list), 200


# GET ONE EXPENSE

@app.route("/api/expenses/<int:expense_id>", methods=["GET"])
def get_expense(expense_id):
    connection = sqlite3.connect("budget_manager.db")
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()

    cursor.execute(
        "SELECT * FROM expenses WHERE expense_id = ?",
        (expense_id,)
    )
    expense = cursor.fetchone()

    connection.close()

    if expense is None:
        return jsonify({"error": "Expense not found"}), 404

    return jsonify(dict(expense)), 200


# UPDATE EXPENSE

@app.route("/api/expenses/<int:expense_id>", methods=["PUT"])
def update_expense(expense_id):
    data = request.get_json()

    allowed_categories = ["Food", "Education", "Entertainment"]

    if "category" in data and data["category"] not in allowed_categories:
        return jsonify({
            "error": "Category must be Food, Education, or Entertainment"
        }), 400

    connection = sqlite3.connect("budget_manager.db")
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()

    cursor.execute(
        "SELECT * FROM expenses WHERE expense_id = ?",
        (expense_id,)
    )
    expense = cursor.fetchone()

    if expense is None:
        connection.close()
        return jsonify({"error": "Expense not found"}), 404

    user_id = data.get("user_id", expense["user_id"])
    description = data.get("description", expense["description"])
    amount = data.get("amount", expense["amount"])
    category = data.get("category", expense["category"])
    expense_date = data.get("expense_date", expense["expense_date"])

    cursor.execute("""
        UPDATE expenses
        SET user_id = ?,
            description = ?,
            amount = ?,
            category = ?,
            expense_date = ?
        WHERE expense_id = ?
    """, (
        user_id,
        description,
        amount,
        category,
        expense_date,
        expense_id
    ))

    connection.commit()
    connection.close()

    return jsonify({"message": "Expense updated successfully"}), 200


# DELETE EXPENSE

@app.route("/api/expenses/<int:expense_id>", methods=["DELETE"])
def delete_expense(expense_id):
    connection = sqlite3.connect("budget_manager.db")
    cursor = connection.cursor()

    cursor.execute(
        "DELETE FROM expenses WHERE expense_id = ?",
        (expense_id,)
    )

    if cursor.rowcount == 0:
        connection.close()
        return jsonify({"error": "Expense not found"}), 404

    connection.commit()
    connection.close()

    return jsonify({"message": "Expense deleted successfully"}), 200


if __name__ == "__main__":
    app.run(debug=True)