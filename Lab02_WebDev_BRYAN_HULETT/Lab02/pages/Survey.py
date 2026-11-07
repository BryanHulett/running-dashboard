# This creates the page for users to input data.
# The collected data should be appended to the 'data.csv' file.

import streamlit as st
import pandas as pd
import os # The 'os' module is used for file system operations (e.g. checking if a file exists).
import csv
import math
# PAGE CONFIGURATION
st.set_page_config(
    page_title="Survey",
    page_icon="📝",
)

# PAGE TITLE AND USER DIRECTIONS
st.title("Data Collection Survey 📝")
st.write("Please fill out the form below to add your data to the dataset.")

# DATA INPUT FORM
# 'st.form' creates a container that groups input widgets.
# The form is submitted only when the user clicks the 'st.form_submit_button'.
# This is useful for preventing the app from re-running every time a widget is changed.
with st.form("survey_form"):
    # Create text input widgets for the user to enter data.
    # The first argument is the label that appears above the input box.
    category_input = st.text_input("Enter a day:")
    value_input = st.text_input("Enter the miles:")

    # The submit button for the form.
    submitted = st.form_submit_button("Submit Data")

    # This block of code runs ONLY when the submit button is clicked.
if submitted:
    day = category_input.strip().title()

    days = [
        "Monday", "Tuesday", "Wednesday", "Thursday",
        "Friday", "Saturday", "Sunday"
    ]

    try:
        miles = float(value_input.strip())
    except ValueError:
        miles = None

    if day not in days:
        st.error("Enter a full day name, such as Monday.")

    elif miles is None or not math.isfinite(miles) or miles < 0:
        st.error("Enter a valid number of miles, such as 0, 3, or 3.5.")

    else:
        needs_header = (
            not os.path.exists("data.csv")
            or os.path.getsize("data.csv") == 0
        )

        with open("data.csv", "a", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)

            if needs_header:
                writer.writerow(["Day", "Miles"])

            writer.writerow([day, miles])

        st.success("Your data has been submitted!")
        st.write(f"Day: {day} | Miles: {miles:g}")
# DATA DISPLAY
# This section shows the current contents of the CSV file, which helps in debugging.
st.divider() # Adds a horizontal line for visual separation.
st.header("Current Data in CSV")

# Check if the CSV file exists and is not empty before trying to read it.
if os.path.exists('data.csv') and os.path.getsize('data.csv') > 0:
    # Read the CSV file into a pandas DataFrame.
    current_data_df = pd.read_csv('data.csv')
    # Display the DataFrame as a table.
    st.dataframe(current_data_df)
else:
    st.warning("The 'data.csv' file is empty or does not exist yet.")
