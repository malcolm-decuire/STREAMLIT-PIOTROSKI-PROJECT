#s1- import dependencies
import streamlit as st
import pandas as pd
import plotly.express as px
import time

#s1 set up the page 
st.set_page_config(page_title="Dashboard",page_icon="🌍",layout="wide")
st.subheader("🔔  Analytics Dashboard")
st.markdown("##")

theme_plotly = None # None or streamlit

#s1a Style
with open('style.css')as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html = True)
 
# Load Excel file into a Pandas DataFrame
file_path = "EODHD-Annual-RE Fundamentals-Final-v2-clean.xlsx"  # Replace with the actual file name
df = pd.read_excel(file_path)

# Streamlit app
st.title("Load Excel File Already in Directory")

# Display the DataFrame
st.write("Loaded DataFrame:")
st.write(df)

# You can now use 'df' as a variable in the rest of your Streamlit app or Python script
st.write("You can now use 'df' as a variable in the rest of your app.")


#theme
hide_st_style=""" 

<style>
#MainMenu {visibility:hidden;}
footer {visibility:hidden;}
header {visibility:hidden;}
</style>
"""



