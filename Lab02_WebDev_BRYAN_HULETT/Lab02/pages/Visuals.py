import streamlit as st
import matplotlib.pyplot as plt
import json
from pathlib import Path

st.set_page_config(
    page_title="Running Visualizations",
    page_icon="📊"
)

st.title("📊 My Weekly Running Miles")


data_path = Path(__file__).resolve().parent.parent / "data.json"


with open(data_path, "r", encoding="utf-8") as file:
    data = json.load(file)

running_miles = data["running_miles"]

days = list(running_miles.keys())
miles = list(running_miles.values())

st.metric("Total Miles This Week", sum(miles))



st.header("Miles Run Each Day")

st.write("This chart shows all seven days of the week.")

fig1, ax1 = plt.subplots()

ax1.bar(days, miles, color="cornflowerblue")

ax1.set_title("Daily Running Miles")
ax1.set_xlabel("Day of the Week")
ax1.set_ylabel("Miles Run")

plt.setp(ax1.get_xticklabels(), rotation=25, ha="right")
fig1.tight_layout()

st.pyplot(fig1)
plt.close(fig1)



st.header("Compare Selected Days")

st.write("Select days to see their share of the selected mileage.")


if "selected_days" not in st.session_state:
    st.session_state["selected_days"] = days.copy()

st.multiselect(
    "Choose days:",
    options=days,
    key="selected_days"
)

selected_days = st.session_state["selected_days"]

selected_miles = []

for day in selected_days:
    selected_miles.append(running_miles[day])

if len(selected_days) == 0:
    st.info("Select at least one day.")

elif sum(selected_miles) == 0:
    st.info("No miles were run on the selected days.")

else:
    fig2, ax2 = plt.subplots()

    ax2.pie(
        selected_miles,
        labels=selected_days,
        autopct="%1.1f%%",
        startangle=90
    )

    ax2.set_title("Running Mileage for Selected Days")
    ax2.axis("equal")

    st.pyplot(fig2)
    plt.close(fig2)

    st.write("Total miles for selected days:", sum(selected_miles))





# PART 2: CSV Visualizations
import pandas as pd

st.divider()
st.header("Part 2: Survey Running Data")
st.write("These charts use the running entries saved in data.csv.")

csv_path = Path(__file__).resolve().parent.parent / "data.csv"

week_days = [
    "Monday", "Tuesday", "Wednesday", "Thursday",
    "Friday", "Saturday", "Sunday"
]

if not csv_path.exists() or csv_path.stat().st_size == 0:
    st.info("Add running data on the Survey page first.")
    st.stop()

csv_data = pd.read_csv(csv_path)

if not {"Category", "Value"}.issubset(csv_data.columns):
    st.error("data.csv must contain Category and Value columns.")
    st.stop()

# Prepare the data without changing the CSV file.
csv_data["Category"] = (
    csv_data["Category"]
    .astype(str)
    .str.strip()
    .str.title()
)

csv_data["Value"] = pd.to_numeric(
    csv_data["Value"],
    errors="coerce"
)

valid_rows = (
    csv_data["Category"].isin(week_days)
    & csv_data["Value"].notna()
    & (csv_data["Value"] >= 0)
    & (csv_data["Value"] < float("inf"))
)

if not valid_rows.all():
    st.warning("Invalid days or mileage were excluded from the charts.")

csv_data = csv_data.loc[valid_rows]

if csv_data.empty:
    st.info("No valid running entries yet. Add data on the Survey page.")
    st.stop()

# Add together multiple entries for the same day.
daily_totals = (
    csv_data.groupby("Category")["Value"]
    .sum()
    .reindex(week_days, fill_value=0)
)

st.metric("Total Miles in CSV", f"{daily_totals.sum():g}")

st.caption(
    f"{len(csv_data)} valid entries. "
    "Days without entries are shown as zero miles."
)

# STATIC VISUALIZATION
# This chart only depends on the CSV data.
st.subheader("CSV Static Bar Chart")

fig3, ax3 = plt.subplots()

ax3.bar(
    week_days,
    daily_totals.values,
    color="seagreen"
)

ax3.set_title("Total Running Miles by Day (CSV)")
ax3.set_xlabel("Day of the Week")
ax3.set_ylabel("Total Miles Run")

plt.setp(
    ax3.get_xticklabels(),
    rotation=25,
    ha="right"
)

fig3.tight_layout()
st.pyplot(fig3)
plt.close(fig3)

# DYNAMIC VISUALIZATION
st.subheader("CSV Dynamic Line Chart")
st.write("Choose a range of days to change the chart.")

# The key stores the slider selection in st.session_state.
st.select_slider(
    "Days to display:",
    options=week_days,
    value=("Monday", "Sunday"),
    key="csv_day_range"
)

start_day, end_day = st.session_state["csv_day_range"]

start_index = week_days.index(start_day)
end_index = week_days.index(end_day)

visible_days = week_days[start_index:end_index + 1]
visible_miles = daily_totals.loc[visible_days]

fig4, ax4 = plt.subplots()

ax4.plot(
    visible_days,
    visible_miles.values,
    marker="o",
    color="darkorange"
)

ax4.set_title(
    f"Running Miles: {start_day} to {end_day} (CSV)"
)

ax4.set_xlabel("Day of the Week")
ax4.set_ylabel("Total Miles Run")
ax4.set_ylim(bottom=0)
ax4.grid(axis="y", alpha=0.3)

plt.setp(
    ax4.get_xticklabels(),
    rotation=25,
    ha="right"
)

fig4.tight_layout()
st.pyplot(fig4)
plt.close(fig4)

st.write(
    "Miles in selected range:",
    float(visible_miles.sum())
)
