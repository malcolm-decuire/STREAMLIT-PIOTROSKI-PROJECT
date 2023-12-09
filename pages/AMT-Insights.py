############################
#s1 import dependencies 
###########################
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as pg
from session_state import SessionState
 

#s1 set up the page 
st.set_page_config(page_title="Dashboard", page_icon="🌍", layout="wide")
st.subheader("🔔  Analytics Dashboard")
st.markdown("##")

#s1a Style
with open('style.css') as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

#s1a some suggestions? 
def load_data(file_path, sheet_name):
    try:
        return pd.read_excel(file_path, sheet_name=sheet_name,  index_col=0, parse_dates=True)
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return None

############################
#s2 XLSX upload
###########################
#s2b AMT data 
amt_bs = pd.read_excel('EODHD-Annual-RE Fundamentals-Final-v2-clean.xlsx', sheet_name='AMT-BS')
amt_is = pd.read_excel('EODHD-Annual-RE Fundamentals-Final-v2-clean.xlsx', sheet_name='AMT-IS')
amt_cf = pd.read_excel('EODHD-Annual-RE Fundamentals-Final-v2-clean.xlsx', sheet_name='AMT-CF')

#s2c Merge DataFrames on the 'date' column
merged_amt_bs_is = pd.merge(amt_bs, amt_is, on='date', how='outer')
merged_amt_df = pd.merge(merged_amt_bs_is, amt_cf, on='date', how='outer')

#s2d Display the merged DataFrame spot check
#st.dataframe(merged_amt_df)

#s2 set up session state
session_state = SessionState(
    merged_amt_df_score=None
)
#s2e -calculation try to pass session state across pages
def calculate_piotroski_f_score(merged_amt_df, session_state):
        # Factor 1: Net Income
        merged_amt_df['Profitability'] = merged_amt_df['netIncome_x'] > 0

        # Factor 2: Operating Cash Flow
        merged_amt_df['Operating Cash Flow'] = merged_amt_df['totalCashFromOperatingActivities'] > 0

        # Factor 3: Return on Assets (ROA)
        merged_amt_df['ROA'] = merged_amt_df['netIncome_x'] / merged_amt_df['totalAssets']

        # Factor 4: Cash Flow from Operations ROA
        merged_amt_df['Cash ROA'] = merged_amt_df['totalCashFromOperatingActivities'] / merged_amt_df['totalAssets']

        # Factor 5: Change in ROA
        merged_amt_df['Delta ROA'] = merged_amt_df['ROA'].diff()

        # Factor 6: Accruals
        merged_amt_df['Accruals'] = merged_amt_df['netIncome_x'] - merged_amt_df['totalCashFromOperatingActivities']

        # Factor 7: Change in Leverage (Long-term Debt)
        merged_amt_df['Delta Leverage'] = -(merged_amt_df['longTermDebt'] - merged_amt_df['longTermDebt'].shift(1))

        # Factor 8: Change in Current Ratio
        merged_amt_df['Delta Current Ratio'] = merged_amt_df['otherCurrentAssets']/ merged_amt_df['totalCurrentLiabilities']
        # Factor 9: Change in Shares Outstanding
        merged_amt_df['Delta Shares Outstanding'] = -(merged_amt_df['commonStockSharesOutstanding'] - merged_amt_df['commonStockSharesOutstanding'].shift(1))

        # Calculate F-Score
        merged_amt_df['Piotroski F-Score'] = (
            merged_amt_df['Profitability'].astype(int) +
            merged_amt_df['Operating Cash Flow'].astype(int) +
            (merged_amt_df['ROA'] > 0).astype(int) +
            (merged_amt_df['Cash ROA'] > 0).astype(int) +
            (merged_amt_df['Delta ROA'] > 0).astype(int) +
            (merged_amt_df['Accruals'] > 0).astype(int) +
            (merged_amt_df['Delta Leverage'] > 0).astype(int) +
            (merged_amt_df['Delta Current Ratio'] > 0).astype(int) +
            (merged_amt_df['Delta Shares Outstanding'] > 0).astype(int)
        )
        
        session_state.merged_amt_df_score = merged_amt_df
        return merged_amt_df

#s1 for multipage apps, include on all pages 

#s2f Calculate Piotroski F-Score
calculate_piotroski_f_score(merged_amt_df, session_state)

############################
#s3 session-state pass down
###########################

#s3 data spot check 
st.write("Did we find the session state", session_state.merged_amt_df_score)

############################
#s4 session-state pass down
###########################

#s4b  Sort the DataFrame by 'date'
df2 = session_state.merged_amt_df_score.sort_values(by="date")

#s4c Group by 'date' and create a new column 'counter' using cumcount
df2['counter'] = df2.groupby('date').cumcount() + 1

# Convert 'counter' to numeric
df2['counter'] = pd.to_numeric(df2['counter'])


#s4d data spot check 
#st.write(df2)

#s4e session-state chart placeholder
x_data = df2
y_data = session_state.merged_amt_df_score["Piotroski F-Score"]

#s4f this works -> 20231208 going fwd data spot check
# st.write("Session-state can pass whole df", x_data)
# st.write("session-state can pass filter df", y_data)

#s4g create a simple bar chart
fig = px.bar(df2, x='date', y='Piotroski F-Score', orientation='v',title=" Default: AMT F-Score")

tab1, tab2 = st.tabs(["Streamlit theme (default)", "Plotly native theme"])
with tab1: 
     # Use the Streamlit theme.
    # This is the default. So you can also omit the theme argument.
    st.plotly_chart(fig, theme="streamlit", use_container_width=True)
with tab2:
    # Use the native Plotly theme.
    st.plotly_chart(fig, theme=None, use_container_width=True)


#s4h color gradient bar chart 
fig_gradient = px.bar(df2, x=df2['date'], y=df2['Piotroski F-Score'],
             hover_data=['ROA', 'Cash ROA'], color='ROA',
             labels={'Piotroski F-Score':'AMT SCORE'}, height=400)
st.plotly_chart(fig_gradient, theme=None, use_container_width=True)