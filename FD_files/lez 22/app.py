import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime, timedelta
from meteostat import Point, Daily
import altair as alt
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut

# Page config
st.set_page_config(layout="wide", page_title="Weather Dashboard")

# Title
st.title("🌤️ Weather Analysis Dashboard")

# Initialize Nominatim geocoder
geolocator = Nominatim(user_agent="my_weather_app")

# Sidebar
st.sidebar.header("Settings")

# City search function
@st.cache_data
def get_city_coordinates(city_name):
    try:
        location = geolocator.geocode(city_name)
        if location:
            return {
                'lat': location.latitude,
                'lon': location.longitude,
                'address': location.address
            }
        return None
    except GeocoderTimedOut:
        return None

# City input
city_input = st.sidebar.text_input("Enter City Name", "Bologna")

# Search button
if st.sidebar.button("Search City"):
    location_data = get_city_coordinates(city_input)
    if location_data:
        st.session_state['location_data'] = location_data
        st.sidebar.success(f"Found: {location_data['address']}")
    else:
        st.sidebar.error("City not found. Please try another search.")

# Initialize location data in session state if not present
if 'location_data' not in st.session_state:
    # Default to Bologna
    st.session_state['location_data'] = {
        'lat': 44.498955,
        'lon': 11.327591,
        'address': 'Bologna, Emilia-Romagna, Italy'
    }

# Date range selection
col1, col2 = st.sidebar.columns(2)
with col1:
    start_date = st.date_input(
        "Start Date",
        datetime(2022, 1, 1).date()
    )
with col2:
    end_date = st.date_input(
        "End Date",
        datetime.now().date()
    )

# Convert date to datetime
start_datetime = datetime.combine(start_date, datetime.min.time())
end_datetime = datetime.combine(end_date, datetime.min.time())

# Fetch data function
@st.cache_data
def fetch_weather_data(lat, lon, start, end):
    city_point = Point(lat, lon, 20)
    data = Daily(city_point, start, end)
    df = data.fetch()
    return df

# Load data
try:
    df = fetch_weather_data(
        st.session_state['location_data']['lat'],
        st.session_state['location_data']['lon'],
        start_datetime,
        end_datetime
    )
    
    # Main content
    st.header(f"Weather Analysis for {st.session_state['location_data']['address']}")
    
    # Temperature trends
    st.subheader("Temperature Trends")
    fig = px.line(df, 
                  x=df.index,
                  y=['tavg', 'tmin', 'tmax'],
                  title="Temperature Overview",
                  labels={'value': 'Temperature (°C)',
                         'variable': 'Temperature Type',
                         'index': 'Date'},
                  width=1000,
                  height=500)
    
    # Update line names to be more readable
    new_names = {'tavg': 'Average Temperature',
                 'tmin': 'Minimum Temperature',
                 'tmax': 'Maximum Temperature'}
    
    fig.for_each_trace(lambda t: t.update(name = new_names[t.name]))
    
    fig.update_layout(
        legend=dict(
            yanchor="top",
            y=0.99,
            xanchor="left",
            x=0.01
        ),
        legend_title_text='',
        hovermode='x unified'
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Monthly analysis
    st.subheader("Monthly Analysis")
    
    # Add year and month columns
    df['year'] = pd.DatetimeIndex(df.index).year
    df['month'] = pd.DatetimeIndex(df.index).month
    
    # Create heatmap
    heatmap = alt.Chart(df).mark_rect().encode(
        x='year:O',
        y='month:O',
        color=alt.Color('tavg:Q', scale=alt.Scale(scheme='viridis'),
                       title='Average Temperature (°C)')
    ).properties(
        width=800,
        height=400,
        title='Temperature Heatmap by Month and Year'
    )
    
    st.altair_chart(heatmap, use_container_width=True)
    
    # Statistics
    st.subheader("Weather Statistics")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Average Temperature", f"{df['tavg'].mean():.1f} C")
    with col2:
        st.metric("Maximum Temperature", f"{df['tmax'].max():.1f} C")
    with col3:
        st.metric("Minimum Temperature", f"{df['tmin'].min():.1f} C")
    
    # Additional weather metrics
    if not df.empty:
        st.subheader("Additional Weather Metrics")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Average Precipitation", f"{df['prcp'].mean():.1f} mm")
        with col2:
            st.metric("Average Snow Depth", f"{df['snow'].mean():.1f} mm")
        with col3:
            st.metric("Average Wind Speed", f"{df['wdir'].mean():.1f} deg")
    
    # Show raw data
    if st.checkbox("Show Raw Data"):
        st.dataframe(df)

except Exception as e:
    st.error(f"Error fetching data: {str(e)}")

# Add information about data source
st.sidebar.markdown("---")
st.sidebar.info("Data provided by Meteostat")
