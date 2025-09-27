import streamlit as st
from ml_model import predict_expense
import pandas as pd

# In-memory transactions
transactions = []

st.title("💰 Expense Tracker & Expense Predictor")

# ----------------- Add Transaction -----------------
st.header("Add Transaction")
with st.form("transaction_form"):
    date = st.date_input("Date")
    description = st.text_input("Description")
    amount = st.number_input("Amount", min_value=0.0, step=1.0)
    category = st.selectbox("Category", ["Income", "Expense"])
    submitted = st.form_submit_button("Add Transaction")
    
    if submitted:
        transactions.append({
            "date": str(date),
            "description": description,
            "amount": float(amount),
            "category": category
        })
        st.success("✅ Transaction added successfully!")

# ----------------- View Transactions -----------------
st.header("View Transactions")
if transactions:
    df = pd.DataFrame(transactions)
    st.dataframe(df)
else:
    st.info("No transactions yet.")

# ----------------- View Summary -----------------
st.header("Summary")
if transactions:
    total_income = sum(t['amount'] for t in transactions if t['category'].lower() == "income")
    total_expense = sum(t['amount'] for t in transactions if t['category'].lower() == "expense")
    balance = total_income - total_expense
    st.write(f"**Total Income:** ${total_income}")
    st.write(f"**Total Expense:** ${total_expense}")
    st.write(f"**Balance:** ${balance}")
else:
    st.info("No transactions yet to calculate summary.")

# ----------------- Predict Expense -----------------
st.header("Predict Expense for a Day")
with st.form("predict_form"):
    day_of_month = st.number_input("Day of Month", min_value=1, max_value=31, value=1)
    day_of_week = st.number_input("Day of Week (0=Mon, 6=Sun)", min_value=0, max_value=6, value=0)
    month = st.number_input("Month", min_value=1, max_value=12, value=1)
    prev_day_expense = st.number_input("Previous Day Expense", min_value=0.0, value=0.0)
    prev_week_expense = st.number_input("Previous Week Expense", min_value=0.0, value=0.0)
    
    pred_submitted = st.form_submit_button("Predict Expense")
    
    if pred_submitted:
        predicted = predict_expense(day_of_month, day_of_week, month, prev_day_expense, prev_week_expense)
        st.success(f"💸 Predicted Expense: ${predicted:.2f}")
