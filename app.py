import streamlit as st
import pandas as pd
from sqlalchemy import create_engine, exc, text
import altair as alt  
Database connection 
server_name = 'LAPTOP-UUOMM6JG\\SQLEXPRESS'
database_name = 'intern_p'
username = 'sa'
password = 'sql%40123'

# Create the connection string for SQL Server Authentication
connection_string = f'mssql+pyodbc://{username}:{password}@{server_name}/{database_name}?
driver=ODBC+Driver+17+for+SQL+Server'

# Creating engine
engine = create_engine(connection_string)

# Creating engine
16engine = create_engine(connection_string)

# Using CSS for table designing
css = """
<style>
table {
width: 100%;
border-collapse: collapse;
border-radius: 4px;
margin-bottom: 1em;
}
thead th {
background-color: #f2f2f2;
text-align: left;
padding: 12px;
}
tbody tr:nth-child(even) {
    background-color: #cdf5f7;
}
tbody tr:hover {
background-color: #fdf8d8;
}
td, th {
border: 1px dotted #dddddd;
text-align: left;
padding: 10px;
}
</style>
"""
st.write('TABLE-DETAILS')
st.write('INTERNSHIP-PROJECT')

# SQL query to fetch turbine data
query_turbines = """
SELECT [Date], [WTG], [Wind_speed], [Active_power]
FROM [intern_p].[dbo].[G4_Projectcsv]
"""

# Fetch data from SQL using SQLAlchemy engine 
try:
 with engine.connect() as connection:
 result = connection.execute(text(query_turbines))
 df_turbines = pd.DataFrame(result.fetchall(), columns=result.keys())
        
 # Convert 'Date' column to datetime and extract date
  df_turbines['Date'] = pd.to_datetime(df_turbines['Date']).dt.date
      
 # Group data by turbine and date
 grouped_df = df_turbines.groupby(['WTG', 'Date']).agg({
  'Wind_speed': 'mean',
  'Active_power': 'sum',
   }).reset_index()
     
 # Add new column for total revenue
  grouped_df['Total_Revenue'] = grouped_df['Active_power'] * 2.5
  grouped_df['power_KWH'] = grouped_df['Active_power'] / 6
      
# Add column for PLF calculation
grouped_df['PLF'] = grouped_df['power_KWH'] / 480
        
 grouped_df = grouped_df.sort_values(by=['WTG', 'Date'])

# Column ordering
grouped_df = grouped_df[['Date', 'WTG', 'Wind_speed', 'Active_power', 'power_KWH', 
'Total_Revenue', 'PLF']]
# Apply CSS
st.markdown(css, unsafe_allow_html=True)
st.table(grouped_df)
st.write(f"Grouped DataFrame Shape: {grouped_df.shape}") 

# Calculate SUM PLF for each WTG
sum_plf_rm01 = grouped_df[grouped_df['WTG'] == 'RM-01']['PLF'].sum() / 30
sum_plf_rm02 = grouped_df[grouped_df['WTG'] == 'RM-02']['PLF'].sum() / 30
sum_plf_rm04 = grouped_df[grouped_df['WTG'] == 'RM-04']['PLF'].sum() / 30
sum_plf_rm08 = grouped_df[grouped_df['WTG'] == 'RM-08']['PLF'].sum() / 30
sum_plf_rm09 = grouped_df[grouped_df['WTG'] == 'RM-09']['PLF'].sum() / 30
sum_plf_rm10 = grouped_df[grouped_df['WTG'] == 'RM-10']['PLF'].sum() / 30
sum_plf_rm11 = grouped_df[grouped_df['WTG'] == 'RM-11']['PLF'].sum() / 30
sum_plf_vr01 = grouped_df[grouped_df['WTG'] == 'VR-01']['PLF'].sum() / 30
sum_plf_vr02 = grouped_df[grouped_df['WTG'] == 'VR-02']['PLF'].sum() / 30  
sum_plf_vr04 = grouped_df[grouped_df['WTG'] == 'VR-04']['PLF'].sum() / 30       
 sum_plf_vr07 = grouped_df[grouped_df['WTG'] == 'VR-07']['PLF'].sum() / 30

summary_df = pd.DataFrame({
'WTG': ['RM-01', 'RM-02', 'RM-04', 'RM-08', 'RM-09', 'RM-10', 'RM-11', 'VR-01', 'VR-02', 'VR-04', 'VR-07'],
'final-PLF': [sum_plf_rm01, sum_plf_rm02, sum_plf_rm04, sum_plf_rm08, sum_plf_rm09, 
sum_plf_rm10, sum_plf_rm11, sum_plf_vr01, sum_plf_vr02, sum_plf_vr04, sum_plf_vr07]
})

# Calculate total revenue per WTG for the summary table
total_revenue = grouped_df.groupby('WTG')['Total_Revenue'].sum().reset_index()
summary_df = pd.merge(summary_df, total_revenue, how='left', on='WTG')
summary_df.rename(columns={'Total_Revenue': 'Final_revenue'}, inplace=True) 114
# TOTAL WIND SPEED SUM
total_wind_speed = grouped_df.groupby('WTG')['Wind_speed'].mean().reset_index()
summary_df = pd.merge(summary_df, total_wind_speed, how='left', on='WTG')
summary_df.rename(columns={'Wind_speed': 'AVRAGE_WIND_SPEED'}, inplace=True) 119

# sum of  ACTIVE POWER
avg_active_power = grouped_df.groupby('WTG')['Active_power'].sum().reset_index()
summary_df = pd.merge(summary_df, avg_active_power, how='left', on='WTG')
summary_df.rename(columns={'Active_power': 'total_Active_Power'}, inplace=True) 124
st.write('TURBINE WISE DATA FOR MONTH')
st.table(summary_df)

# Create a new DataFrame for total revenue grouped by date
date_grouped_df = grouped_df.groupby('Date').agg({
'Total_Revenue': 'sum',
'Wind_speed': 'mean',
'Active_power':'sum'
}).reset_index()
date_grouped_df.rename(columns={'Total_Revenue': 'Sum_Total_Revenue', 'Wind_speed': 
'Avg_Wind_Speed','Active_power':'sum_active_power'}, inplace=True)
st.write('DATE WISE DATA :')
st.write('DATE WISE FOR ALL 11 TURBINE :')
st.table(date_grouped_df)

# Create bar chart using Altair for WTG and TOTAL-PLF
bar_chart = alt.Chart(summary_df).mark_bar().encode(
x='WTG',
y='final-PLF',
tooltip=['WTG', 'final-PLF']
).properties(
width=alt.Step(80),  # Adjust the width of bars
height=400
)
st.write('Bar Chart: WTG v/s final-PLF')
st.altair_chart(bar_chart, use_container_width=True) 152
bar_chart = alt.Chart(summary_df).mark_bar().encode(
x='WTG',
y='Final_revenue',
tooltip=['WTG', 'Final_revenue']
).properties(
width=alt.Step(80),  # Adjust the width of bars
height=400
)
st.write('Bar Chart: WTG v/s final revenue')
st.altair_chart(bar_chart, use_container_width=True) 164
bar_chart = alt.Chart(summary_df).mark_bar().encode(
x='WTG',
y='total_Active_Power',
tooltip=['WTG', 'total_Active_Power']
).properties(
width=alt.Step(80),  # Adjust the width of bars
height=400
)

st.write('Bar Chart: WTG v/s total_Active_Power')
st.altair_chart(bar_chart, use_container_width=True)

# Adjust date format to show only the day of the month
bar_chart = alt.Chart(date_grouped_df).mark_bar().encode(
x=alt.X('Date:T', axis=alt.Axis(format='%d')),
y='Sum_Total_Revenue',
tooltip=['Date', 'Sum_Total_Revenue']
).properties(
width=alt.Step(80),  # Adjusting the wridth of bar in charts  
height=400
)

st.write('Bar Chart: Date v/s Sum_Total_Revenue')
st.altair_chart(bar_chart, use_container_width=True)

bar_chart = alt.Chart(date_grouped_df).mark_bar().encode(
x=alt.X('Date:T', axis=alt.Axis(format='%d')),
y='Avg_Wind_Speed',
tooltip=['Date', 'Avg_Wind_Speed']
).properties(
width=alt.Step(80),  # Adjust the width of bars
height=400
)

st.write('Bar Chart: Date v/s Avg_Wind_Speed')
st.altair_chart(bar_chart, use_container_width=True)

except exc.SQLAlchemyError as e:
st.error(f"Error fetching data: {e}")

st.write('THIS IS THE FINAL TABLE')
