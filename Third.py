import csv
import os
from datetime import datetime
import streamlit as st

data_file = "expenses.csv"

# Ensure the file exists with headers
def initialize_file():
    if not os.path.exists(data_file):
        with open(data_file, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Date", "Category", "Amount", "Description"])

def add_expense(category, amount, description):
    date = datetime.now().strftime("%Y-%m-%d")
    with open(data_file, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([date, category, amount, description])
    st.success("Expense added successfully!")

def view_expenses():
    if not os.path.exists(data_file) or os.stat(data_file).st_size == 0:
        st.warning("No expenses recorded yet.")
        return []
    
    with open(data_file, mode='r') as file:
        reader = csv.reader(file)
        next(reader)  # Skip header
        return list(reader)

def analyze_expenses():
    if not os.path.exists(data_file) or os.stat(data_file).st_size == 0:
        st.warning("No expenses recorded yet.")
        return {}
    
    expenses = {}
    total_expense = 0
    
    with open(data_file, mode='r') as file:
        reader = csv.reader(file)
        next(reader)  # Skip header
        for row in reader:
            category = row[1]
            amount = float(row[2])
            total_expense += amount
            expenses[category] = expenses.get(category, 0) + amount
    
    return expenses, total_expense

# Streamlit UI
st.title("Expense Tracker")
initialize_file()

menu = ["Add Expense", "View Expenses", "Analyze Expenses"]
choice = st.sidebar.selectbox("Menu", menu)

if choice == "Add Expense":
    st.subheader("Add New Expense")
    category = st.selectbox("Select Category", ["Food", "Transport", "Entertainment", "Other"])
    amount = st.number_input("Enter Amount", min_value=0.0, format="%.2f")
    description = st.text_input("Enter Description")
    if st.button("Add Expense"):
        add_expense(category, amount, description)

elif choice == "View Expenses":
    st.subheader("Expense Records")
    expenses = view_expenses()
    if expenses:
        st.table(expenses)

elif choice == "Analyze Expenses":
    st.subheader("Expense Analysis")
    expenses, total = analyze_expenses()
    if expenses:
        st.write("Category-wise Expenses:")
        st.bar_chart(expenses)
        st.write(f"Total Expenses: ${total:.2f}")
