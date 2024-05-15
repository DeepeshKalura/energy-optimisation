import os
import folium
import streamlit as st
import pandas as pd
from dotenv import load_dotenv
import plotly.express as px
from streamlit_folium import folium_static
from openai import OpenAI

from app.utlity import location_with_ip_address


load_dotenv()

# Set Streamlit page configuration
st.set_page_config(page_title="Saving Engery")

# Load the data
@st.cache_data
def load_data():
    return pd.read_csv('tri_valley_energy_data.csv')

df = load_data()

# Sidebar for user input
st.sidebar.header("Filter Options")
selected_years = st.sidebar.slider(
    "Select Year Range",
    min_value=2018,
    max_value=2023,
    value=(2018, 2023)
)

# Filter data based on user input
filtered_df = df[df['year'].between(selected_years[0], selected_years[1])]

st.title("Saving Engery")


st.subheader("Locations")
location , latlog = location_with_ip_address() 
@st.cache_data
def draw_map(location, latlog=None):
    st.write(f"Location: {location}")
    
    map_center = latlog if latlog else None

    if map_center:
            mymap = folium.Map(location=map_center, zoom_start=10)      
            folium.Marker(map_center, popup=location).add_to(mymap)
            folium_static(mymap)


# Added a graph
draw_map(location=location, latlog=latlog)

@st.cache_data
def response_from_openai(location:str):
    client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
    completion = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": "You are best suistabnable energy guider. You tell user the the tips for the saving more electriclity which leads them sustinable future ."},
        {"role": "user", "content": f"I live {location} please guide me the tips for saving more energy."},
        ]
    )
    return (completion.choices[0].message.content)


response = response_from_openai(location=location)

st.subheader("Tips for the user to save more energy:")
st.write(response)



# Bar charts using Plotly
st.subheader("Cost Savings Due to Energy Efficiency")
fig = px.bar(filtered_df, x='month', y='cost_savings', color='year', title='Cost Savings Over Time')
st.plotly_chart(fig)

# Pie charts using Plotly
st.subheader("Total Energy Savings by Year")
total_savings_by_year = filtered_df.groupby('year')['energy_savings'].sum().reset_index()
fig = px.pie(total_savings_by_year, values='energy_savings', names='year', title='Total Energy Savings by Year')
st.plotly_chart(fig)

# Histogram using Plotly
st.subheader("Distribution of Sustainable Measures Implemented")
fig = px.histogram(filtered_df, x='sustainable_measures', nbins=10, title='Distribution of Sustainable Measures')
st.plotly_chart(fig)


