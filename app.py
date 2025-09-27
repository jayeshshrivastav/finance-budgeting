from flask import Flask, request, jsonify, render_template
from ml_model import predict_expense

app = Flask(__name__)

# In-memory transactions
transactions = []

# Homepage
@app.route("/")
def home():
    return render_template("index.html")

# Add transaction
@app.route("/add_transaction", methods=["POST"])
def add_transaction():
    data = request.get_json()
    transactions.append({
        "date": data["date"],
        "description": data["description"],
        "amount": float(data["amount"]),
        "category": data["category"]
    })
    return jsonify({"message": "Transaction added successfully!"})

# View transactions
@app.route("/view_transactions", methods=["GET"])
def view_transactions():
    return jsonify(transactions)

# Summary
@app.route("/summary", methods=["GET"])
def summary():
    total_income = sum(t['amount'] for t in transactions if t['category'].lower() == "income")
    total_expense = sum(t['amount'] for t in transactions if t['category'].lower() == "expense")
    balance = total_income - total_expense
    return jsonify({
        "total_income": total_income,
        "total_expense": total_expense,
        "balance": balance
    })

# Predict expense
@app.route("/predict_expense", methods=["POST"])
def predict():
    data = request.get_json()
    day = data["DayOfMonth"]
    dow = data["DayOfWeek"]
    month = data["Month"]
    prev_day = data["PrevDayExpense"]
    prev_week = data["PrevWeekExpense"]

    result = predict_expense(day, dow, month, prev_day, prev_week)
    return jsonify({"PredictedExpense": result})

if __name__ == "__main__":
    app.run(debug=True)
