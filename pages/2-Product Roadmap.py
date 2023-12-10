#s1 import dependencies & loading bar
#s1- import dependencies
import streamlit as st
import pandas as pd
import plotly.express as px
import time
from session_state import SessionState

#s1 set up the page 
st.set_page_config(page_title="Product Roadmap", page_icon="🗺️", layout="wide")
st.markdown("##")


#s1a - progress bar
loading_page = "Please Wait 🤲🏽"
progress_text =loading_page
my_bar = st.progress(0, text=progress_text)

for percent_complete in range(100):
    time.sleep(0.01)
    my_bar.progress(percent_complete + 1, text=progress_text)
time.sleep(1)
my_bar.empty()

#s2 content
st.title('📍Product Roadmap')
st.subheader("👉 Click on each Phase to see whats next")
st.caption("👉 Click right-hand arrows to enlarge")

#s4b set the tabs up
tab1, tab2, tab3, tab4 = st.tabs(["🚩 Phase I", "🚩 Phase II", "🚩 Phase III", "🚩 Phase IV"])

with tab1:
   st.header("📅 Add More Securities & F-Scores")
   st.write("📌 Between Jan-Jun 2024 add more tickers")
   st.write("📝 Enable users to upload their own data and conduct analysis")
   st.image("https://tickertapecdn.tdameritrade.com/assets/images/pages/md/reit-subsectors.jpg", width=400)

with tab2:
   st.header("📅 Add More Insights")
   st.write("📌 Between Jun-Dec 2024 add more insights & charts")
   st.write("📝 e.g. conduct historical portfolio analysis")
   st.write("📝 e.g. conduct near real-time tradidng analysis")
   st.image("https://mma.prnewswire.com/media/2090559/Technavio_Global_Reit_Market_2023.jpg?p=publish", width=600)

with tab3:
   st.header("🤝 Community Feedback")
   st.write("📌 Between Jan-Apr 2024 release a repo that can run locally & in the cloud")
   st.write("📌 Deploy this as a teaching tool to blend Finance & Tech together")
   st.write("📌 Gather feedback from traders, financial advisors, and other ethusiasts in the space")
   st.image("https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQ4UulzMFW8KVY8yoQRUlCkzlWx-ObU7xEGnSqUH2_zyA&s", width=400)

with tab4:
   st.header("🤖 Advanced Features")
   st.write("📌 Incorporate NLP & LLM for REIT analysis & suggestions")
   st.write("📌 e.g. Create a chatbot that reads the financials of all RE focused securities ")
   st.image("https://etinsights.et-edge.com/wp-content/uploads/2023/05/llm.jpg", width=400)

#s4 reload button 
st.button("🔄 Reload")