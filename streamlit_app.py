import streamlit as st
import pandas as pd
import plotly.express as px
from PIL import Image

# -------------------- PAGE CONFIG --------------------
st.set_page_config(page_title="Incredible India", layout="wide")

# -------------------- LOAD DATA --------------------
@st.cache_data
def load_data():
    travel_df = pd.read_csv("Expanded_Indian_Travel_Dataset.csv")
    tourism_stats_df = pd.read_csv("India-Tourism-Statistics-2021-Table-5.2.3.csv")
    tourism_stats_df.columns = tourism_stats_df.columns.str.strip()
    return travel_df, tourism_stats_df

travel_df, tourism_stats_df = load_data()

# -------------------- SIDEBAR NAVIGATION --------------------
st.sidebar.title("Explore India")
page = st.sidebar.radio("Go to", ["Home", "Explore Destinations", "Festivals of India", "Tourism Insights"])

# -------------------- PAGE: HOME --------------------
if page == "Home":
    st.title("🇮🇳 Incredible India: A Cultural Odyssey")

    # Large, centered image just like other pages
    st.image("assets/india_collage.png", use_container_width=True)

    st.markdown("""
    ## Welcome to a Data-Driven Journey 🌍
    Dive into the rich tapestry of India's cultural heritage with:
    - 🏞️ Cultural destinations across regions  
    - 🎉 Festival calendars  
    - 🏛️ Tourism insights and trends  

    Discover hidden gems and ancient traditions — one state at a time.
    """)
    st.success("Let your journey begin!")

# -------------------- PAGE: EXPLORE DESTINATIONS --------------------
elif page == "Explore Destinations":
    st.title("🧭 Explore Cultural Destinations")
    st.image("assets/khajuraho.jpg", use_container_width=True)

    region = st.selectbox("Select Region", sorted(travel_df['Region'].dropna().unique()))
    filtered = travel_df[travel_df['Region'] == region]

    if not filtered.empty:
        state = st.selectbox("Select State", sorted(filtered['State'].dropna().unique()))
        filtered_state = filtered[filtered['State'] == state]
        st.dataframe(filtered_state)

        st.download_button("Download CSV", filtered_state.to_csv(index=False), "destinations.csv", "text/csv")
    else:
        st.warning("No data available for the selected region.")

# -------------------- PAGE: FESTIVALS --------------------
elif page == "Festivals of India":
    st.title("🎊 Festivals of India 2025")
    st.image("assets/holi.png", use_container_width=True)

    festivals_2025 = {
        "January": [("Pongal", "January 14"), ("Makar Sankranti", "January 14"), ("Republic Day", "January 26")],
        "February": [("Maha Shivaratri", "February 26")],
        "March": [("Holi", "March 14")],
        "April": [("Baisakhi", "April 13"), ("Rama Navami", "April 6")],
        "May": [("Buddha Purnima", "May 12")],
        "June": [],
        "July": [("Rath Yatra", "July 7"), ("Guru Purnima", "July 20")],
        "August": [("Raksha Bandhan", "August 9"), ("Independence Day", "August 15"), ("Janmashtami", "August 16"), ("Onam", "August 28")],
        "September": [("Ganesh Chaturthi", "September 6")],
        "October": [("Navratri", "October 1"), ("Dussehra", "October 10")],
        "November": [("Diwali", "November 1"), ("Bhai Dooj", "November 3"), ("Guru Nanak Jayanti", "November 12")],
        "December": [("Christmas", "December 25")]
    }

    month = st.selectbox("Select Month", list(festivals_2025.keys()))
    st.subheader(f"Festivals in {month} 2025")

    if festivals_2025[month]:
        for fest, date in festivals_2025[month]:
            st.write(f"🎉 {fest} - {date}")
    else:
        st.info("No major festivals in this month.")

# -------------------- PAGE: TOURISM INSIGHTS --------------------
elif page == "Tourism Insights":
    st.title("📊 Tourism Trends Across Monuments")
    st.image("assets/tajmahal.jpg", use_container_width=True)

    top_monuments = tourism_stats_df.head(10)

    fig = px.bar(
        top_monuments,
        x='Name of the Monument',
        y=['Domestic-2019-20', 'Domestic-2020-21'],
        barmode='group',
        title="Top 10 Monuments - Domestic Visitors (2019-2021)",
        labels={"value": "Number of Visitors", "variable": "Year", "Name of the Monument": "Monument"}
    )
    st.plotly_chart(fig)

    fig_pie = px.pie(
        top_monuments,
        names='Name of the Monument',
        values='Domestic-2019-20',
        title='Visitor Distribution (2019-20)'
    )
    st.plotly_chart(fig_pie)

    st.markdown("_Note: COVID-19 had a significant impact on tourism in 2020-21._")
    st.download_button("Download Tourism Data", top_monuments.to_csv(index=False), "tourism_stats.csv", "text/csv")
