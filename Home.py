# Dec2023-stuff that doesn't work once deployed
# 1-divider='rainbow' doesnt work on cloud 
# 2-trying to use multi line text as var to pass 

#s1- import dependencies
import streamlit as st
import pandas as pd
import plotly.express as px
import time
from session_state import SessionState

#s1a set up the page 
st.set_page_config(page_title="REIT ANALYSIS", page_icon="📈", layout="wide")
st.header("REIT ANALYSIS APP")
st.markdown("##")

#s1b progress bar
loading_page = "Please Wait 🤲🏽"
progress_text =loading_page
my_bar = st.progress(0, text=progress_text)
for percent_complete in range(100):
    time.sleep(0.01)
    my_bar.progress(percent_complete + 1, text=progress_text)
time.sleep(1)
my_bar.empty()


#s1c - info to user remember to leave double spaces after each line '''
st.title("👋 Welcome To Malcolm Decuire's REIT Analysis App")
st.title("💻 Blending Finance & CS ")
st.subheader("Purpose: Teach Finance & Programming")
st.subheader("❓Who is this for")
st.subheader("🏘️ Real Estate Enthusiats & 👨‍💻 Programmers")
st.divider()
st.link_button("▶️  Click here to reach-out via LinkedIn", "https://www.linkedin.com/in/malcolmdecuire/")
st.link_button("▶️  Click here to reach-out via Discord @mdecuire", "https://discord.com/" )
st.divider()

#s1d addtl user guide
st.title("SOURCES OF INSPIRATION")
col1, col2, col3 = st.columns(3, gap="small")

with col1:
   st.header("Finance Background")
   st.image('https://www.emorybusiness.com/wp-content/uploads/2020/10/i-3x8Jgqs-X3.jpg',caption='Working in Saas & Finance since 2013',width=400)

with col2:
   st.header("DEV Community")
   st.image('https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQZLTvKY-7gDQj2Ql1kNk0w2Jx8nfKMfdWP14wtmOmD7w&s',caption='Developing since 2018 w/ a focus on Finance & SaaS', width=250)

with col3:
   st.header("Personal Growth")
   st.image("https://assets-global.website-files.com/6384aadeeb9aef4298860dd3/6466fc4234a7324e51fd3491_annie-spratt-QckxruozjRg-unsplash.jpeg", caption='People Invest In People', width=400)

#s1e addtl user guide
st.header("Additional Resources")
col4, col5, col6 = st.columns(3, gap="medium")
with col4:
    st.link_button('▶️  1/ Ritviks Financial Programming Channel', 'https://www.linkedin.com/in/ritvikdashora/?originalSubdomain=in')

with col5:  
    st.link_button("▶️  2/ EDOHD Data & Applications","https://www.youtube.com/watch?v=yL7fcnn5P40&ab_channel=FinancialProgrammingwithRitvik%2CCFA")

with col6: 
    st.link_button('▶️  3/ Application of Piotroski', 'https://seekingalpha.com/article/4567246-top-piotroski-graham-long-term-value-portfolio-2022-returns-plus-new-january-2023-semi-annual-selections')
st.subheader("tl;dr Pay $50/mo to access financial & become a more intelligent investor")

st.divider()

#s2 setup
st.header("🤔 How do I use this app?")
st.subheader("👉 Select a REIT from dropdown to view Fundamentals")

#s2 Utilize the local excel file & link to the source of the data 
def main():
    uploaded_file = st.file_uploader("⚠️  WARNING-Only Upload EODHD Fundamentals Data", type=["xlsx"])

    if uploaded_file is not None:
        eodhd_df = pd.read_excel(uploaded_file, sheet_name=None)
    else:
        # for cloud & local deployment use a default file path (update as needed)
        file_path = "EODHD-Annual-RE Fundamentals-Final-v2-clean.xlsx"
        eodhd_df = pd.read_excel(file_path, sheet_name=None)

    if eodhd_df:
        sheet_names = list(eodhd_df.keys())
        selected_sheet = st.selectbox("Select a sheet", sheet_names)

        # for cloud & local deployment display the selected sheet's data
        st.dataframe(eodhd_df[selected_sheet])

if __name__ == "__main__":
    main()

#s3b create next section on pg
st.divider()

#s4
#placeholder for media 

#s5a progress bar reload 
st.button("🔄 Reload")