import pandas as pd
from sklearn.ensemble import RandomForestRegressor
import joblib

# Load dataset
df = pd.read_csv("expenses.csv")

# Convert Date to datetime
df["Date"] = pd.to_datetime(df["Date"])

# Aggregate daily expenses
daily_expense = df.groupby(df["Date"].dt.date).agg({"Amount": "sum"}).reset_index()
daily_expense.rename(columns={"Amount": "DailyExpense"}, inplace=True)
daily_expense["Date"] = pd.to_datetime(daily_expense["Date"])

# Feature engineering
daily_expense["DayOfMonth"] = daily_expense["Date"].dt.day
daily_expense["DayOfWeek"] = daily_expense["Date"].dt.weekday
daily_expense["Month"] = daily_expense["Date"].dt.month
daily_expense["PrevDayExpense"] = daily_expense["DailyExpense"].shift(1)
daily_expense["PrevWeekExpense"] = daily_expense["DailyExpense"].shift(7)

daily_expense = daily_expense.dropna()

X = daily_expense[["DayOfMonth", "DayOfWeek", "Month", "PrevDayExpense", "PrevWeekExpense"]]
y = daily_expense["DailyExpense"]

# Train Random Forest
model = RandomForestRegressor(n_estimators=200, max_depth=10, random_state=42)
model.fit(X, y)

# Save model
joblib.dump(model, "expense_predictor.pkl")
print("✅ Model saved as expense_predictor.pkl")
