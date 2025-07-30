import streamlit as st
import pandas as pd
import plotly.express as px

# Load Data
@st.cache_data
def load_data():
    df = pd.read_csv("flights.csv", parse_dates=["departure_time", "arrival_time"])
    df.dropna(subset=['airline', 'departure_airport', 'arrival_airport'], inplace=True)
    return df

df = load_data()

# Sidebar Filters
st.sidebar.title("Filters")
airlines = st.sidebar.multiselect("Select Airline(s)", options=df['airline'].unique(), default=df['airline'].unique())
departure_iata = st.sidebar.multiselect("Select Departure Airport(s)", options=df['departure_iata'].unique(), default=df['departure_iata'].unique())
arrival_iata = st.sidebar.multiselect("Select Arrival Airport(s)", options=df['arrival_iata'].unique(), default=df['arrival_iata'].unique())

# Filter data
filtered_df = df[
    (df['airline'].isin(airlines)) &
    (df['departure_iata'].isin(departure_iata)) &
    (df['arrival_iata'].isin(arrival_iata))
]

st.title("✈️ Airline Market Demand Dashboard")

# Section 1: Top Routes
st.header("📌 Top 10 Most Frequent Routes")
filtered_df['route'] = filtered_df['departure_iata'] + " → " + filtered_df['arrival_iata']
top_routes = filtered_df['route'].value_counts().head(10).reset_index()
top_routes.columns = ['Route', 'Count']
fig1 = px.bar(top_routes, x='Route', y='Count', title="Most Popular Flight Routes", color='Route')
st.plotly_chart(fig1)

# Section 2: Airline Market Share
st.header("🛩️ Airline Market Share")
airline_share = filtered_df['airline'].value_counts().reset_index()
airline_share.columns = ['Airline', 'Flights']
fig2 = px.pie(airline_share, names='Airline', values='Flights', title="Airline Distribution")
st.plotly_chart(fig2)

# Section 3: Time Series
st.header("📈 Flights Over Time")
filtered_df['departure_date'] = pd.to_datetime(filtered_df['departure_time']).dt.date
flight_counts_by_day = filtered_df.groupby('departure_date').size().reset_index(name='Total Flights')
fig3 = px.line(flight_counts_by_day, x='departure_date', y='Total Flights', title="Flight Trends Over Time")
st.plotly_chart(fig3)

# Show Raw Data
with st.expander("🔍 Show Raw Data"):
    st.dataframe(filtered_df)
