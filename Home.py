#s1- import dependencies
import streamlit as st
import pandas as pd
import plotly.express as px
import time
from session_state import SessionState

#s1 set up the page 
st.set_page_config(page_title="PIOTROSKI REIT ANALYSIS", page_icon="📈", layout="wide")
st.subheader("📊 Piotroski Dashboard")
st.markdown("##")


#s1a - loading items 
loading_page = "Please Wait 🤲🏽"
bar = st.progress(70)
time.sleep(3)
bar.progress(100, text=loading_page)

#s1 - info to user
st.title("⏰ THANK YOU for your time!")
st.title("👋 DISCLAIMER: Opinions Expressed are my own")
st.subheader("Purpose:", divider='rainbow')
st.markdown("""
            Minimalist Project: 
            Applying Real Estate Finance Analysis & Python Development
            """)
st.title("SOURCES OF INSPIRATION")
st.image('https://www.emorybusiness.com/wp-content/uploads/2020/10/i-3x8Jgqs-X3.jpg',caption='BBA Finance Background & +5yrs Experience',width=400)
st.image('https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQZLTvKY-7gDQj2Ql1kNk0w2Jx8nfKMfdWP14wtmOmD7w&s',caption='EODHD API Python [Very easy to use Financial Data API] 🔴', width=200)
st.link_button('Checkout Ritviks Page', 'https://www.linkedin.com/in/ritvikdashora/?originalSubdomain=in')
st.link_button("Learn More about EDOHD","https://eodhd.com/financial-apis/stock-etfs-fundamental-data-feeds/")
st.link_button('Active investors using Piotroski', 'https://seekingalpha.com/article/4567246-top-piotroski-graham-long-term-value-portfolio-2022-returns-plus-new-january-2023-semi-annual-selections')
st.subheader("tl;dr Pay $50/mo to access financial & become a more intelligent investor")
st.subheader("❓ Why learn about Piotroski")
st.link_button("Quick LinkedIn Summary","https://www.linkedin.com/pulse/piotroski-f-score-its-importance-understanding-/")
st.subheader("❓ Whats in it for you")
st.link_button("Value Investors & Algo Traders use it for their benefit, why not you?","https://www.reddit.com/r/algotrading/comments/93pbwk/using_the_piotroski_f_score_as_a_factor/")

#s1a page setup-Style  Allow user to upload their own file
with open('style.css') as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

#s1b page setup-allow user to upload data with ease (assuming matching format from EODHD)
def load_data(file_path, sheet_name):
    try:
        return pd.read_excel(file_path, sheet_name=sheet_name)
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return None

#s1c page setup- guide 
st.subheader('Reasons for EODHD', divider='rainbow')
st.subheader('1. Trade-off between free datasets that interested me or paid ones that did')
st.subheader('2. Needed access to historical data without massive annual contracts (bloomberg is expensive)')
st.subheader('3. Its easier to work with data in environments Im already familiar with like Google Sheets, pandas, pyspark, etc')
st.subheader('4. :blue[Experiement with rapid-prototyping to simiulate commcercial deadlines]')

#s1d addtl page set up
st.title("Please upload EODHD XLSX File Export From Google Sheets only")
st.write("Check Roadmap for when other file types will be selected")
st.link_button("Resource", "https://eodhd.com/financial-apis/google-sheets-financial-add-in-for-eod-fundamentals-data/#Google_Sheets_Financial_Add-In")


#s2 Utilize the local excel file & link to the source of the data 
def main():
    uploaded_file = st.file_uploader("EODHD Fundamentals Formatted Data", type=["xlsx"])

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

#s4 implement a video about learning the Piotroski f-score 
st.header('Learn About Piotroski F-Score')
# YouTube video URL
youtube_url = "https://www.youtube.com/watch?v=HKI8pODEzVo&ab_channel=FinancialProgrammingwithRitvik%2CCFA"

#s4a Display the YouTube video in the Streamlit app 
# as of Dec2023 no current way to resize 
st.video(youtube_url)
st.divider()
st.title('📍 Product Roadmap')
st.subheader("Upcoming Phases")

#s4 set the tabs up
tab1, tab2, tab3 = st.tabs(["🚩 Phase I", "🚩 Phase II", "🚩 Phase III"])

with tab1:
   st.header("Add More Securities & F-Scores")
   st.write("Between Jan-Jun 2024 add more tickers")
   st.image("https://static.seekingalpha.com/uploads/2022/11/6/47791712-16677919823973587_origin.png", width=400)

with tab2:
   st.header("Add More Insights")
   st.write("Between Jun-Dec 2024 add graphs like Sankey to breakdown each statement")
   st.image("https://mma.prnewswire.com/media/2090559/Technavio_Global_Reit_Market_2023.jpg?p=publish", width=600)

with tab3:
   st.header("Community Feedback")
   st.write("Release a repo that can run locally & in the cloud")
   st.write("Gather feedback from traders, financial advisors, and other ethusiats in the space")
   st.image("https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQ4UulzMFW8KVY8yoQRUlCkzlWx-ObU7xEGnSqUH2_zyA&s", width=400)
