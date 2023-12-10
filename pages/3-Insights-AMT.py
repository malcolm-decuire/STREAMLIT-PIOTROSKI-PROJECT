# If u r new to coding -> I hope these notes help
# If u r interested in the project please provide positive feedback 
# there's enough negativity in the world 

############################
#s1 import dependencies 
###########################
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as pg
from session_state import SessionState
from pandas.api.types import (
    is_categorical_dtype,
    is_datetime64_any_dtype,
    is_numeric_dtype,
    is_object_dtype,
)
 
#s1a page setup  
st.set_page_config(page_title="AMT-Dashboard", page_icon="🔎", layout="wide")
st.subheader("🔎 PIOTROSKI INSIGHTS: AMT")
st.markdown("##")

#s1b Style
with open('style.css') as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

#s1c local data load for beginners & users with minimal time
def load_data(file_path, sheet_name):
    try:
        return pd.read_excel(file_path, sheet_name=sheet_name,  index_col=0, parse_dates=True)
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return None

#1c project info guide  
st.title("❓ How do ya use it")
guide_1 ='''👉 select columns of interest  
-use the slider to filter down rows      
-notice the correlation between cols    
-i.e. high ROA + high FCF filters out a lot of rows     

''' 
st.markdown(guide_1) 

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

#s2d Display the merged DataFrame spot check & set up session state
#st.dataframe(merged_amt_df)
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


#s2f Calculate Piotroski F-Score
calculate_piotroski_f_score(merged_amt_df, session_state)

############################
#s3 session-state pass down & viz prep
###########################

#s3a data spot check -> 20231208 spot check
#st.write("EODHD + Piotroski", session_state.merged_amt_df_score)

#s3b row-selection from user attempt make sure add double space in order to create new line
st.title("AMT Piotroski Data Filter")
warning_note ='''⚠️ AS OF DEC 2023  
-SOME FILTER COMBINATIONS WILL THROW AN ERROR   
-INCLUDING: earningAssets/totalPermn.../noncontrolling...   
-EXPECTED FIX DATE: Q32024    
''' 
st.markdown(warning_note)     

#3c interactive data filter
def filter_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """
    From Streamlit Docs:
    Adds a UI on top of a dataframe to let viewers filter columns

    Args:
        df (pd.DataFrame): Original dataframe

    Returns:
        pd.DataFrame: Filtered dataframe
    """
    modify = st.checkbox("Select Fundamentals")

    if not modify:
        return df

    df = df.copy()

    # Try to convert datetimes into a standard format (datetime, no timezone)
    for col in df.columns:
        if is_object_dtype(df[col]):
            try:
                df[col] = pd.to_datetime(df[col])
            except Exception:
                pass

        if is_datetime64_any_dtype(df[col]):
            df[col] = df[col].dt.tz_localize(None)

    modification_container = st.container()

    with modification_container:
        to_filter_columns = st.multiselect("Filter dataframe on", df.columns)
        for column in to_filter_columns:
            left, right = st.columns((1, 20))
            left.write("↳")
            # Treat columns with < 10 unique values as categorical
            if is_categorical_dtype(df[column]) or df[column].nunique() < 10:
                user_cat_input = right.multiselect(
                    f"Values for {column}",
                    df[column].unique(),
                    default=list(df[column].unique()),
                )
                df = df[df[column].isin(user_cat_input)]
            elif is_numeric_dtype(df[column]):
                _min = float(df[column].min())
                _max = float(df[column].max())
                step = (_max - _min) / 100
                user_num_input = right.slider(
                    f"Values for {column}",
                    _min,
                    _max,
                    (_min, _max),
                    step=step,
                )
                df = df[df[column].between(*user_num_input)]
            elif is_datetime64_any_dtype(df[column]):
                user_date_input = right.date_input(
                    f"Values for {column}",
                    value=(
                        df[column].min(),
                        df[column].max(),
                    ),
                )
                if len(user_date_input) == 2:
                    user_date_input = tuple(map(pd.to_datetime, user_date_input))
                    start_date, end_date = user_date_input
                    df = df.loc[df[column].between(start_date, end_date)]
            else:
                user_text_input = right.text_input(
                    f"Substring or regex in {column}",
                )
                if user_text_input:
                    df = df[df[column].str.contains(user_text_input)]

    return df
df = session_state.merged_amt_df_score
st.dataframe(filter_dataframe(df))


###########################################
#s4 session-state pass down & visualization
###########################################
st.divider()


#s4a  Sort the DataFrame by 'date'
df2 = session_state.merged_amt_df_score.sort_values(by="date")

#s4b Group by 'date' and create a new column 'counter' using cumcount
df2['counter'] = df2.groupby('date').cumcount() + 1

#s4cConvert 'counter' to numeric
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

#s4g1 chart insights
st.title("📖 How do you read these charts")
st.header("Chart-1: Date x Score")
st.subheader("e.g. For 2015 AMT got a score of 8 which indicates a strong buy")

tab1, tab2 = st.tabs(["Streamlit theme (default)", "Plotly native theme"])
with tab1: 
     # Use the Streamlit theme.
    # This is the default. So you can also omit the theme argument.
    st.plotly_chart(fig, theme="streamlit", use_container_width=True)
with tab2:
    # Use the native Plotly theme.
    st.plotly_chart(fig, theme=None, use_container_width=True)

#s4 divide up the second chart 
st.divider()
#s4g2 chart insights
st.header("Chart-2: Date x ROA")
st.subheader("e.g. For 2015 AMT got a score of 8 and a ROA of .038 which indicates a healthy company")

#s4h color gradient bar chart 
fig_gradient = px.bar(df2, x=df2['date'], y=df2['Piotroski F-Score'],
             hover_data=['ROA', 'Cash ROA'], color='ROA',
             labels={'Piotroski F-Score':'AMT SCORE'}, height=400)
st.plotly_chart(fig_gradient, theme=None, use_container_width=True)