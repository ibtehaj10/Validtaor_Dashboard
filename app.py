import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

# Load the DataFrame from CSV
df = pd.read_csv('vtrust_log.csv', parse_dates=['datetime'])
# Ensure the 'datetime' column is in datetime format
df['datetime'] = pd.to_datetime(df['datetime'])

# Define time ranges
today = datetime.now()
last_week = today - timedelta(days=7)
print("last_week : "+str(last_week))
last_month = today - timedelta(days=30)
print("last_month : "+str(last_month))
last_six_months = today - timedelta(days=30*6)
print("last_six : "+str(last_six_months))

# Filter options
option = st.sidebar.selectbox(
    "Select Time Range:",
    ("Today", "Last Week", "Last Month", "Last 6 Months")
)
SN_options = st.sidebar.selectbox("Select SN:", options=df["SN"].unique())

SN = df[df['SN'] == SN_options]



st.write("Filtered Data:", SN)
if option == "Today":
    start_date = today
elif option == "Last Week":
    start_date = last_week
elif option == "Last Month":
    start_date = last_month
elif option == "Last 6 Months":
    start_date = last_six_months



# Plotting
if option== "Today":


    fig, ax = plt.subplots()
    ax.plot(SN['Date'], SN['Vtrust'], marker='o', linestyle='-', color='blue')
    ax.set_title(f'Vtrust Over Time - {option}')
    ax.set_xlabel('Date')
    ax.set_ylabel('Vtrust')
    ax.grid(True)
    plt.xticks(rotation=45)
    plt.tight_layout()
    st.pyplot(fig)


# Optionally display the filtered DataFrame

