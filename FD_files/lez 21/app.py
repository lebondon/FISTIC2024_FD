import streamlit as st
import polars as pl
import pandas as pd
from prophet import Prophet
import matplotlib.pyplot as plt

st.title('Time Series Forecasting with Prophet')

# File upload
uploaded_file = st.file_uploader("Choose your CSV file", type='csv')

if uploaded_file is not None:
    # Read the CSV file
    df = pl.read_csv(uploaded_file)
    
    # Show the raw data
    st.subheader('Raw data preview')
    st.write(df.head())
    
    # Column selection with default values
    columns = list(df.columns)
    default_datetime_idx = columns.index('Datetime (UTC)') if 'Datetime (UTC)' in columns else 0
    default_value_idx = columns.index('Renewable Percentage') if 'Renewable Percentage' in columns else 0
    
    datetime_col = st.selectbox(
        'Select the datetime column',
        columns,
        index=default_datetime_idx
    )
    
    value_col = st.selectbox(
        'Select the value column to forecast',
        columns,
        index=default_value_idx
    )
    
    # Model parameters
    st.sidebar.subheader('Model Parameters')
    yearly_seasonality = st.sidebar.checkbox('Yearly Seasonality', value=True)
    weekly_seasonality = st.sidebar.checkbox('Weekly Seasonality', value=False)
    daily_seasonality = st.sidebar.checkbox('Daily Seasonality', value=False)
    interval_width = st.sidebar.slider('Confidence Interval Width', 0.5, 0.99, 0.95)
    
    # Forecast parameters
    forecast_periods = st.slider('Number of periods to forecast', 1, 24, 24)
    
    if st.button('Generate Forecast'):
        try:
            # Prepare data for Prophet
            df = df.select([
                pl.col(datetime_col).alias("ds"),
                pl.col(value_col).alias("y")
            ])
            
            # Convert to pandas and format datetime
            df_pandas = df.to_pandas()
            df_pandas['ds'] = pd.to_datetime(df_pandas['ds']).dt.strftime('%Y-%m-%d %H:%M')
            
            # Create and fit the model
            model = Prophet(
                yearly_seasonality=yearly_seasonality,
                weekly_seasonality=weekly_seasonality,
                daily_seasonality=daily_seasonality,
                interval_width=interval_width
            )
            model.fit(df_pandas)
            
            # Create future dates
            future_dates = model.make_future_dataframe(
                periods=forecast_periods,
                freq='MS'
            )
            
            # Make predictions
            forecast = model.predict(future_dates)
            
            # Plot the forecast
            st.subheader('Forecast Plot')
            fig = model.plot(forecast)
            plt.title('Time Series Forecast')
            plt.xlabel('Date')
            plt.ylabel('Value')
            st.pyplot(fig)
            
            # Show components plot
            st.subheader('Forecast Components')
            fig2 = model.plot_components(forecast)
            st.pyplot(fig2)
            
            # Show forecast data
            st.subheader('Forecast Data')
            forecast_subset = forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].tail(forecast_periods)
            st.write(forecast_subset)
            
            # Download forecast data
            st.download_button(
                label="Download forecast data as CSV",
                data=forecast_subset.to_csv(index=False),
                file_name="forecast.csv",
                mime="text/csv"
            )
            
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")
            st.write("Please check your data format.")

else:
    st.write('Please upload a CSV file to begin.')