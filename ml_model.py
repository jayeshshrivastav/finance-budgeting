import joblib
import pandas as pd

# Load trained model
model = joblib.load("expense_predictor.pkl")

def predict_expense(day_of_month, day_of_week, month, prev_day, prev_week):
    df = pd.DataFrame([{
        "DayOfMonth": day_of_month,
        "DayOfWeek": day_of_week,
        "Month": month,
        "PrevDayExpense": prev_day,
        "PrevWeekExpense": prev_week
    }])
    prediction = model.predict(df)[0]
    return prediction

