#s1 import dependencies
import streamlit as st
import pandas as pd
import plotly.express as px
import time
from session_state import SessionState

#s1 set up the page 
st.set_page_config(page_title="ABOUT", page_icon="❓", layout="wide")
st.header("REAL-ESTATE APP")
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

#s1 user info 
st.title("❓ Why should you care")
st.header("💰: Increase your investment acumen")
st.link_button("🔗 Value Investing","https://www.reddit.com/r/algotrading/comments/93pbwk/using_the_piotroski_f_score_as_a_factor/")

#s1b background about REIT
st.title("❓ What are REITs")
st.subheader("5-min. read on REITs")
st.link_button("🔗 LinkedIn Post", "https://www.linkedin.com/pulse/reits-everything-you-need-know-credence-family-office/")


#s1 addtil info- piot
st.title("❓ Why learn about Piotroski")
st.link_button("🔗 Quick LinkedIn Summary","https://www.linkedin.com/pulse/piotroski-f-score-its-importance-understanding-/")

#s1c addtl user guide- eod
st.title("❓ What is EODHD")
st.header("EODHD is a French based SaaS firm that offers Robust, powerful and easy to use APIs & Ready-to-go solutions")
st.link_button("🔗 Python docs", "https://eodhd.com/financial-apis/python-financial-libraries-and-code-samples/")


#s1a page setup-Style  Allow user to upload their own file
with open('style.css') as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

#s1c page setup- guide 
st.title('❓ Why choose EODHD data')
st.divider()
st.subheader('1. Trade-off between free datasets that bored me vs paid-ones that didnt 😅')
st.subheader('2. Needed access to historical data without massive annual contracts (bloomberg is expensive)')
st.subheader('3. Its easier to work with data in environments Im already familiar with like Google Sheets, pandas, pyspark, etc')
st.subheader('4. :blue[Experiement with rapid-prototyping to simiulate commcercial deadlines]')


#s1d addtl page set up 
st.divider()
st.header("🎮 Demo Disclaimer:")
st.subheader("2 tickers analyzed: AMT & PLD")
st.header("☑ NEXT STEPS Disclaimer")
st.subheader("visit roadmap")

st.divider()

#s1e addtl guide info 
col7, col8 = st.columns(2)
with col7:
    st.header("What is AMT")
    st.write("AMT is a leading independent owner, operator and developer of multitenant communications real estate with a portfolio")
    st.image("https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcR1pPomlHQGDNA4vWGuw-icR36y57RYJkyC7kEG5NBC5g&s", caption='AMT', width=250)
    st.link_button("AMTs SEC Filings", "https://www.americantower.com/investor-relations/sec-filings/")

#s1f guide info PLD
with col8:
    st.header("What is PLD")
    st.write("PLD acquires, develop, and maintain the largest collection of high-quality logistics real estate in the world.")
    st.image("https://www.midamericaroofing.com/assets/1/6/MainFCKEditorDimension/3e6e40c833c0c17196fdb7a863329325.jpeg", caption='AMT',width=250)
    st.link_button("PLDs SEC Filings", "https://ir.prologis.com/financials/sec-filings")


#s2a notes to user
st.subheader("EODHD workflow resource")
st.caption("Here's how to automate the EODHD process")
st.link_button("Resource", "https://eodhd.com/financial-apis/google-sheets-financial-add-in-for-eod-fundamentals-data/#Google_Sheets_Financial_Add-In")

#s2b reload 
st.button("🔄 Reload")