import streamlit as st
import pandas as pd
import plotly.express as px
import time
from streamlit_option_menu import option_menu

# Load dataset
df = pd.read_excel("data/Cleaned_Bookings_Dataset.xlsx")
df['Booking Date'] = pd.to_datetime(df['Booking Date'])

# Set full-screen layout
st.set_page_config(layout="wide")

# Custom CSS for UI and Full-Screen Loading
st.markdown("""
    <style>
    body {
        background-color: #121826;
        color: white;
    }
    .block-container {
        padding: 2rem;
    }
    .bento-box {
        display: grid;
        grid-template-columns: repeat(2, 1fr);
        gap: 15px;
    }
    .loading-overlay {
        position: fixed;
        top: 0; left: 0; width: 100%; height: 100%;
        background: rgba(0, 0, 0, 0.8);
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        color: white;
        font-size: 24px;
        z-index: 999;
    }
    </style>
    """, unsafe_allow_html=True)

# Sidebar Navigation
with st.sidebar:
    st.title("Dashboard")
    selected = option_menu(
        menu_title=None,
        options=["Overview", "Bookings Analysis", "Revenue Insights"],
        icons=["bar-chart", "clipboard-data", "cash"],
        menu_icon="cast",
        default_index=0,
        orientation="vertical"
    )

# Initialize session state for loading
if "loading" not in st.session_state:
    st.session_state.loading = True  # Start in loading state

# Placeholder for loading screen
loading_placeholder = st.empty()

# Show Loading Overlay
if st.session_state.loading:
    with loading_placeholder.container():
        st.markdown(
            '<div class="loading-overlay">⏳ Loading Data...<br><progress></progress></div>',
            unsafe_allow_html=True
        )

# Simulate a dynamic loading process
time.sleep(1.5)  # Simulate processing time

# Clear the loading overlay before rendering content
st.session_state.loading = False
loading_placeholder.empty()  # This clears the loading screen

# 🎯 **OVERVIEW PAGE**
if selected == "Overview":
    st.title("📊 Business Overview")

    # Bento Grid Layout
    col1, col2 = st.columns(2)
    
    with col1:
        st.metric("Total Revenue", f"${df['Price'].sum():,.2f}")
        st.metric("Total Bookings", df.shape[0])

        # Mini Revenue Chart
        df_rev_time = df.groupby(df['Booking Date'].dt.to_period('M'))['Price'].sum().reset_index()
        df_rev_time['Booking Date'] = df_rev_time['Booking Date'].astype(str)
        fig_rev = px.line(df_rev_time, x='Booking Date', y='Price', markers=True, color_discrete_sequence=['#ff6361'])
        st.plotly_chart(fig_rev, use_container_width=True)

    with col2:
        st.metric("Avg Booking Price", f"${df['Price'].mean():,.2f}")
        st.metric("Unique Customers", df['Customer Name'].nunique())

        # Mini Booking Chart
        df_bookings = df.groupby(df['Booking Date'].dt.to_period('M')).size().reset_index(name='Bookings')
        df_bookings['Booking Date'] = df_bookings['Booking Date'].astype(str)
        fig_bookings = px.bar(df_bookings, x='Booking Date', y='Bookings', color_discrete_sequence=['#1f77b4'])
        st.plotly_chart(fig_bookings, use_container_width=True)

# 🎯 **BOOKINGS ANALYSIS**
elif selected == "Bookings Analysis":
    st.title("📋 Bookings Analysis")

    col1, col2 = st.columns(2)
    
    with col1:
        # Fix: Group by 'Booking Type' and count occurrences
        booking_counts = df['Booking Type'].value_counts().reset_index()
        booking_counts.columns = ['Booking Type', 'Count']

        # Now create the correct bar chart
        fig2 = px.bar(
            booking_counts, x='Booking Type', y='Count', title='📊 Bookings by Type',
            text_auto=True, color='Booking Type', color_discrete_sequence=px.colors.qualitative.Pastel
        )

        st.plotly_chart(fig2, use_container_width=True)

    with col2:
        fig3 = px.pie(df, values='Price', names='Booking Type', title='💰 Revenue Share by Booking Type',
                      color_discrete_sequence=px.colors.sequential.Viridis)
        st.plotly_chart(fig3, use_container_width=True)

# 🎯 **REVENUE INSIGHTS**
elif selected == "Revenue Insights":
    st.title("💵 Revenue Insights")

    col1, col2 = st.columns(2)

    with col1:
        revenue = df.groupby('Booking Type')['Price'].sum().reset_index()
        fig4 = px.bar(revenue, x='Booking Type', y='Price', title='Revenue by Booking Type', 
                      color='Booking Type', text_auto=True)
        st.plotly_chart(fig4, use_container_width=True)

    with col2:
        df_rev_time = df.groupby(df['Booking Date'].dt.to_period('M'))['Price'].sum().reset_index()
        df_rev_time['Booking Date'] = df_rev_time['Booking Date'].astype(str)
        fig5 = px.area(df_rev_time, x='Booking Date', y='Price', title='📈 Monthly Revenue Trend',
                       color_discrete_sequence=['#ff6361'])
        st.plotly_chart(fig5, use_container_width=True)
