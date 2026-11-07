# This creates the main landing page for the Streamlit application.
# Contains an introduction to the project and guide users to other pages.

# Import Streamlit
import streamlit as st

st.set_page_config(
    page_title="Weekly Running Dashboard",
    page_icon="🏃"
)

st.title("🏃 My Weekly Running Dashboard")

st.write(
    "This app shows how many miles I ran "
    "each day during one week."
)

st.subheader("My Running Charts")

st.write("Select Visuals in the sidebar to see my running data.")

st.write("- A bar chart showing miles run each day.")
st.write("- An interactive pie chart comparing selected days.")


st.subheader("Running Survey and CSV Charts")

st.write(
    "Select Survey in the sidebar to enter a day and miles run."
)

st.write(
    "Visuals also includes a static CSV bar chart and "
    "a dynamic CSV line chart with a day-range slider."
)
