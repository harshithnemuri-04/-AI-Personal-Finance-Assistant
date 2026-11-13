import streamlit as st
import pandas as pd
import plotly.express as px

from database import get_connection
# ==============================
# Professional Dashboard UI
# ==============================

st.set_page_config(
    page_title="AI Finance Assistant",
    page_icon="💰",
    layout="wide"
)

# Custom CSS
st.markdown("""
<style>

.main-title {
    font-size: 42px;
    font-weight: 700;
    margin-bottom: 5px;
}

.subtitle {
    font-size: 18px;
    color: #888888;
    margin-bottom: 30px;
}

.dashboard-card {
    padding: 20px;
    border-radius: 12px;
    background-color: #1f2129;
    border: 1px solid #333333;
    text-align: center;
}

.dashboard-card h3 {
    font-size: 16px;
    margin-bottom: 10px;
}

.dashboard-card p {
    font-size: 26px;
    font-weight: 700;
}

</style>
""", unsafe_allow_html=True)


# Dashboard Header

st.markdown(
    '<div class="main-title">💰 AI Personal Finance Assistant</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">'
    'Smart expense tracking, budgeting, savings and AI-powered insights'
    '</div>',
    unsafe_allow_html=True
)
# ==============================
# Sidebar
# ==============================

with st.sidebar:

    st.title("💰 Finance AI")

    st.write("Your Personal Finance Assistant")

    st.divider()

    st.subheader("📌 Features")

    st.write("💳 Transactions")
    st.write("📊 Expense Analysis")
    st.write("💰 Budget Management")
    st.write("🎯 Savings Goals")
    st.write("🚨 Anomaly Detection")
    st.write("📈 Expense Prediction")
    st.write("💬 AI Chatbot")

    st.divider()

    st.caption(
        "AI Personal Finance Assistant"
    )

    st.caption(
        "Built with Python, Streamlit, MySQL & Machine Learning"
    )

# AI Expense Categorization

def categorize_expense(description):

    description = description.lower()

    if "swiggy" in description or "zomato" in description:
        return "Food"

    elif "uber" in description or "ola" in description:
        return "Transport"

    elif "amazon" in description or "flipkart" in description:
        return "Shopping"

    elif "netflix" in description or "movie" in description:
        return "Entertainment"

    elif "electricity" in description or "water bill" in description:
        return "Bills"

    elif "salary" in description:
        return "Salary"

    else:
        return "Other"
st.header("AI Expense Categorization")

test_description = st.text_input(
    "Enter an expense description"
)

if test_description:

    category = categorize_expense(test_description)

    st.success(f"AI Suggested Category: {category}")

st.title("AI-Powered Personal Finance Assistant")

st.write("Welcome to your personal finance assistant!")

# Get transactions from MySQL
connection = get_connection()

query = """
SELECT
    transaction_id,
    transaction_date,
    description,
    amount,
    transaction_type,
    category
FROM transactions
ORDER BY transaction_date DESC
"""

df = pd.read_sql(query, connection)

connection.close()

income = df[df["transaction_type"] == "Income"]["amount"].sum()

expenses = df[df["transaction_type"] == "Expense"]["amount"].sum()

savings = income - expenses
# ==============================
# Dashboard KPI Cards
# ==============================

st.subheader("📊 Financial Overview")

col1, col2, col3 = st.columns(3)

with col1:

    st.markdown(
        f"""
        <div class="dashboard-card">
            <h3>💰 Total Income</h3>
            <p>₹{income:,.2f}</p>
        </div>
        """,
        unsafe_allow_html=True
    )

with col2:

    st.markdown(
        f"""
        <div class="dashboard-card">
            <h3>💸 Total Expenses</h3>
            <p>₹{expenses:,.2f}</p>
        </div>
        """,
        unsafe_allow_html=True
    )

with col3:

    st.markdown(
        f"""
        <div class="dashboard-card">
            <h3>💵 Total Savings</h3>
            <p>₹{savings:,.2f}</p>
        </div>
        """,
        unsafe_allow_html=True
    )

st.divider()

# Display summary
st.header("Financial Summary")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Income", f"₹{income:,.2f}")

with col2:
    st.metric("Expenses", f"₹{expenses:,.2f}")

with col3:
    st.metric("Savings", f"₹{savings:,.2f}")

# Display transactions
st.header("Transactions")

st.dataframe(
    df,
    use_container_width=True
)

# Add Transaction
st.header("Add Transaction")

with st.form("transaction_form"):

    description = st.text_input("Description")

    amount = st.number_input(
        "Amount",
        min_value=0.0,
        step=100.0
    )

    transaction_type = st.selectbox(
        "Transaction Type",
        ["Income", "Expense"]
    )

 
    submitted = st.form_submit_button("Add Transaction")

    if submitted:

        if description == "":
            st.error("Please enter a description.")

        elif amount <= 0:
            st.error("Please enter a valid amount.")

        else:

            category = categorize_expense(description)

            connection = get_connection()

            cursor = connection.cursor()

            query = """
            INSERT INTO transactions
            (transaction_date, description, amount, transaction_type, category)
            VALUES (CURDATE(), %s, %s, %s, %s)
            """

            values = (
                description,
                amount,
                transaction_type,
                category
            )

            cursor.execute(query, values)

            connection.commit()

            cursor.close()
            connection.close()

            st.success("Transaction saved to MySQL!")

            st.write(
                "🤖 AI Suggested Category:",
                category
            )
            # Expense by Category Chart
st.header("Expenses by Category")

expense_df = df[df["transaction_type"] == "Expense"]

category_expenses = (
    expense_df.groupby("category")["amount"]
    .sum()
    .reset_index()
)

fig = px.pie(
    category_expenses,
    names="category",
    values="amount",
    title="Expenses by Category"
)

st.plotly_chart(fig, use_container_width=True)


# Income vs Expenses Chart
st.header("Income vs Expenses")

summary_data = pd.DataFrame({
    "Type": ["Income", "Expenses"],
    "Amount": [income, expenses]
})

fig2 = px.bar(
    summary_data,
    x="Type",
    y="Amount",
    title="Income vs Expenses",
    text="Amount"
)

st.plotly_chart(fig2, use_container_width=True)
# ==============================
# Budget Management
# ==============================

st.header("💰 Budget Management")

with st.form("budget_form"):

    budget_category = st.selectbox(
        "Budget Category",
        [
            "Food",
            "Transport",
            "Shopping",
            "Bills",
            "Entertainment",
            "Other"
        ]
    )

    budget_amount = st.number_input(
        "Monthly Budget",
        min_value=0.0,
        step=500.0
    )

    budget_submitted = st.form_submit_button(
        "Set Budget"
    )

    if budget_submitted:

        if budget_amount <= 0:

            st.error("Please enter a valid budget amount.")

        else:

            connection = get_connection()

            cursor = connection.cursor()

            query = """
            INSERT INTO budgets
            (category, budget_amount, month_year)
            VALUES (%s, %s, DATE_FORMAT(CURDATE(), '%Y-%m'))
            """

            values = (
                budget_category,
                budget_amount
            )

            cursor.execute(query, values)

            connection.commit()

            cursor.close()
            connection.close()

            st.success(
                f"₹{budget_amount:,.2f} budget set for {budget_category}!"
            )
            # ==============================
# Budget Usage & Alerts
# ==============================

st.header("📊 Budget Usage")

connection = get_connection()

budget_query = """
SELECT
    category,
    budget_amount
FROM budgets
WHERE month_year = DATE_FORMAT(CURDATE(), '%Y-%m')
"""

budget_df = pd.read_sql(
    budget_query,
    connection
)

connection.close()


if not budget_df.empty:

    for index, row in budget_df.iterrows():

        category = row["category"]
        budget = float(row["budget_amount"])

        # Get total spending for this category
        connection = get_connection()

        cursor = connection.cursor()

        expense_query = """
        SELECT COALESCE(SUM(amount), 0)
        FROM transactions
        WHERE category = %s
        AND transaction_type = 'Expense'
        AND DATE_FORMAT(transaction_date, '%Y-%m')
            = DATE_FORMAT(CURDATE(), '%Y-%m')
        """

        cursor.execute(
            expense_query,
            (category,)
        )

        result = cursor.fetchone()

        spent = float(result[0])

        cursor.close()
        connection.close()

        # Calculate remaining amount
        remaining = budget - spent

        # Calculate percentage used
        percentage_used = spent / budget

        st.subheader(category)

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric(
                "Budget",
                f"₹{budget:,.2f}"
            )

        with col2:
            st.metric(
                "Spent",
                f"₹{spent:,.2f}"
            )

        with col3:
            st.metric(
                "Remaining",
                f"₹{remaining:,.2f}"
            )

        # Progress bar
        progress = min(percentage_used, 1.0)

        st.progress(progress)

        st.write(
            f"Budget Used: {percentage_used * 100:.1f}%"
        )

        # Budget alerts

        if percentage_used >= 1:

            st.error(
                f"🚨 {category} budget exceeded!"
            )

        elif percentage_used >= 0.8:

            st.warning(
                f"⚠️ You have used {percentage_used * 100:.1f}% "
                f"of your {category} budget."
            )

        else:

            st.success(
                f"✅ {category} budget is under control."
            )
            # ==============================
# Savings Goals
# ==============================

st.header("🎯 Savings Goals")

with st.form("savings_goal_form"):

    goal_name = st.text_input(
        "Goal Name"
    )

    target_amount = st.number_input(
        "Target Amount",
        min_value=0.0,
        step=1000.0
    )

    saved_amount = st.number_input(
        "Amount Already Saved",
        min_value=0.0,
        step=500.0
    )

    goal_submitted = st.form_submit_button(
        "Create Savings Goal"
    )

    if goal_submitted:

        if goal_name == "":
            st.error("Please enter a goal name.")

        elif target_amount <= 0:
            st.error("Please enter a valid target amount.")

        elif saved_amount > target_amount:
            st.error(
                "Saved amount cannot be greater than target amount."
            )

        else:

            connection = get_connection()

            cursor = connection.cursor()

            query = """
            INSERT INTO savings_goals
            (goal_name, target_amount, saved_amount, created_date)
            VALUES (%s, %s, %s, CURDATE())
            """

            values = (
                goal_name,
                target_amount,
                saved_amount
            )

            cursor.execute(query, values)

            connection.commit()

            cursor.close()
            connection.close()

            st.success(
                f"Savings goal '{goal_name}' created successfully!"
            )


# Display Savings Goals

connection = get_connection()

goal_query = """
SELECT
    goal_id,
    goal_name,
    target_amount,
    saved_amount
FROM savings_goals
ORDER BY goal_id DESC
"""

goals_df = pd.read_sql(
    goal_query,
    connection
)

connection.close()


if not goals_df.empty:

    st.subheader("Your Savings Goals")

    for index, row in goals_df.iterrows():

        goal_name = row["goal_name"]
        target = float(row["target_amount"])
        saved = float(row["saved_amount"])

        remaining = target - saved

        progress = saved / target

        st.write(f"### 🎯 {goal_name}")

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric(
                "Target",
                f"₹{target:,.2f}"
            )

        with col2:
            st.metric(
                "Saved",
                f"₹{saved:,.2f}"
            )

        with col3:
            st.metric(
                "Remaining",
                f"₹{remaining:,.2f}"
            )

        st.progress(
            min(progress, 1.0)
        )

        st.write(
            f"Progress: {progress * 100:.1f}%"
        )

        if progress >= 1:

            st.success(
                f"🎉 Congratulations! "
                f"You reached your {goal_name} goal!"
            )

        else:

            st.info(
                f"₹{remaining:,.2f} remaining to reach your goal."
            )

    # ==============================
# Expense Anomaly Detection
# ==============================

st.header("🚨 Expense Anomaly Detection")

connection = get_connection()

anomaly_query = """
SELECT
    transaction_id,
    transaction_date,
    description,
    amount,
    category
FROM transactions
WHERE transaction_type = 'Expense'
ORDER BY transaction_date DESC
"""

anomaly_df = pd.read_sql(
    anomaly_query,
    connection
)

connection.close()


if len(anomaly_df) >= 5:

    from sklearn.ensemble import IsolationForest

    model = IsolationForest(
        contamination=0.1,
        random_state=42
    )

    anomaly_df["anomaly"] = model.fit_predict(
        anomaly_df[["amount"]]
    )

    unusual_expenses = anomaly_df[
        anomaly_df["anomaly"] == -1
    ]

    if not unusual_expenses.empty:

        st.warning(
            "⚠️ Unusually high expenses detected!"
        )

        st.dataframe(
            unusual_expenses[
                [
                    "transaction_date",
                    "description",
                    "amount",
                    "category"
                ]
            ],
            use_container_width=True
        )

    else:

        st.success(
            "✅ No unusual expenses detected."
        )

else:

    st.info(
        "ℹ️ Add at least 5 expense transactions "
        "to perform anomaly detection."
    )
    # ==============================
# Expense Prediction
# ==============================

st.header("📈 Expense Prediction")

from sklearn.linear_model import LinearRegression

connection = get_connection()

prediction_query = """
SELECT
    transaction_date,
    SUM(amount) AS daily_expense
FROM transactions
WHERE transaction_type = 'Expense'
GROUP BY transaction_date
ORDER BY transaction_date
"""

prediction_df = pd.read_sql(
    prediction_query,
    connection
)

connection.close()


if len(prediction_df) >= 5:

    # Convert date column to datetime
    prediction_df["transaction_date"] = pd.to_datetime(
        prediction_df["transaction_date"]
    )

    # Create numerical day values
    prediction_df["day_number"] = range(
        len(prediction_df)
    )

    # Prepare data for machine learning
    X = prediction_df[["day_number"]]

    y = prediction_df["daily_expense"]

    # Create Linear Regression model
    model = LinearRegression()

    model.fit(X, y)

    # Predict next 7 days
    future_days = pd.DataFrame({
        "day_number": range(
            len(prediction_df),
            len(prediction_df) + 7
        )
    })

    predictions = model.predict(
        future_days
    )

    total_prediction = predictions.sum()

    st.success(
        f"📊 Predicted expenses for the next 7 days: "
        f"₹{total_prediction:,.2f}"
    )

    # Display prediction table

    prediction_result = pd.DataFrame({
        "Day": [
            "Day 1",
            "Day 2",
            "Day 3",
            "Day 4",
            "Day 5",
            "Day 6",
            "Day 7"
        ],
        "Predicted Expense": predictions
    })

    prediction_result["Predicted Expense"] = (
        prediction_result["Predicted Expense"]
        .clip(lower=0)
    )

    st.dataframe(
        prediction_result,
        use_container_width=True
    )

    # Prediction chart

    fig_prediction = px.line(
        prediction_result,
        x="Day",
        y="Predicted Expense",
        markers=True,
        title="Predicted Expenses for Next 7 Days"
    )

    st.plotly_chart(
        fig_prediction,
        use_container_width=True
    )

else:

    st.info(
        "ℹ️ Add expenses on at least 5 different dates "
        "to generate an expense prediction."
    )
    # ==============================

    # ==============================
# AI Finance Chatbot
# ==============================

st.header("🤖 AI Finance Chatbot")

st.write(
    "Ask questions about your income, expenses, savings, and spending."
)

# Chatbot input
user_question = st.text_input(
    "Ask your finance question:"
)

if user_question:

    question = user_question.lower().strip()

    # Remove bullet points and extra characters
    question = question.replace("•", "")
    question = question.replace("?", "")
    question = question.strip()

    # Get latest financial data
    connection = get_connection()

    chatbot_query = """
    SELECT
        COALESCE(SUM(
            CASE
                WHEN transaction_type = 'Income'
                THEN amount
                ELSE 0
            END
        ), 0) AS total_income,

        COALESCE(SUM(
            CASE
                WHEN transaction_type = 'Expense'
                THEN amount
                ELSE 0
            END
        ), 0) AS total_expenses

    FROM transactions
    """

    chatbot_df = pd.read_sql(
        chatbot_query,
        connection
    )

    connection.close()

    total_income = float(
        chatbot_df.iloc[0]["total_income"]
    )

    total_expenses = float(
        chatbot_df.iloc[0]["total_expenses"]
    )

    total_savings = total_income - total_expenses

    # --------------------------------
    # Total expenses
    # --------------------------------

    if "expense" in question or "spent" in question:

        st.info(
            f"💸 Your total expenses are "
            f"₹{total_expenses:,.2f}."
        )

    # --------------------------------
    # Total income
    # --------------------------------

    elif "income" in question or "salary" in question:

        st.info(
            f"💰 Your total income is "
            f"₹{total_income:,.2f}."
        )

    # --------------------------------
    # Savings
    # --------------------------------

    elif "saving" in question:

        st.success(
            f"💰 Your total savings are "
            f"₹{total_savings:,.2f}."
        )

    # --------------------------------
    # Highest spending category
    # --------------------------------

    elif (
        "highest" in question
        or "most" in question
        or "top category" in question
    ):

        connection = get_connection()

        category_query = """
        SELECT
            category,
            SUM(amount) AS total
        FROM transactions
        WHERE transaction_type = 'Expense'
        GROUP BY category
        ORDER BY total DESC
        LIMIT 1
        """

        category_df = pd.read_sql(
            category_query,
            connection
        )

        connection.close()

        if not category_df.empty:

            category = category_df.iloc[0]["category"]
            amount = float(category_df.iloc[0]["total"])

            st.info(
                f"📊 Your highest spending category is "
                f"**{category}**, with ₹{amount:,.2f} spent."
            )

        else:

            st.info(
                "No expense data is available yet."
            )

    # --------------------------------
    # Food expenses
    # --------------------------------

    elif "food" in question:

        connection = get_connection()

        food_query = """
        SELECT
            COALESCE(SUM(amount), 0)
        FROM transactions
        WHERE transaction_type = 'Expense'
        AND category = 'Food'
        """

        cursor = connection.cursor()

        cursor.execute(food_query)

        food_expense = float(
            cursor.fetchone()[0]
        )

        cursor.close()
        connection.close()

        st.info(
            f"🍔 You have spent "
            f"₹{food_expense:,.2f} on food."
        )

    # --------------------------------
    # Transport expenses
    # --------------------------------

    elif "transport" in question:

        connection = get_connection()

        transport_query = """
        SELECT
            COALESCE(SUM(amount), 0)
        FROM transactions
        WHERE transaction_type = 'Expense'
        AND category = 'Transport'
        """

        cursor = connection.cursor()

        cursor.execute(transport_query)

        transport_expense = float(
            cursor.fetchone()[0]
        )

        cursor.close()
        connection.close()

        st.info(
            f"🚗 You have spent "
            f"₹{transport_expense:,.2f} on transport."
        )

    # --------------------------------
    # Budget questions
    # --------------------------------

    elif "budget" in question:

        connection = get_connection()

        budget_query = """
        SELECT
            COALESCE(SUM(budget_amount), 0)
        FROM budgets
        WHERE month_year =
        DATE_FORMAT(CURDATE(), '%Y-%m')
        """

        cursor = connection.cursor()

        cursor.execute(budget_query)

        total_budget = float(
            cursor.fetchone()[0]
        )

        cursor.close()
        connection.close()

        st.info(
            f"📋 Your total monthly budget is "
            f"₹{total_budget:,.2f}."
        )

    # --------------------------------
    # Unknown question
    # --------------------------------

    else:

        st.warning(
            "🤔 I don't understand that question yet."
        )

        st.write(
            "Try asking:"
        )

        st.write(
            "• How much did I spend?"
        )

        st.write(
            "• What is my income?"
        )

        st.write(
            "• How much did I save?"
        )

        st.write(
            "• What is my highest spending category?"
        )

        st.write(
            "• How much did I spend on food?"
        )

        st.write(
            "• How much did I spend on transport?"
        )

        st.write(
            "• What is my budget?"
        ) 
