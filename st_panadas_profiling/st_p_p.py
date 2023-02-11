import pandas as pd 
import numpy as np
from pandas_profiling import ProfileReport
import streamlit as st
from streamlit_pandas_profiling import st_profile_report
import seaborn as sns 


st.markdown('''
## EDA and Wrangling
 
    ''')

# upload file

with st.sidebar.header("Upload CSV file"):
    uploaded_file = st.sidebar.file_uploader("upload file", type=['csv'])
    df = sns.load_dataset('titanic')
    st.sidebar.markdown('[Example file](df)')



if uploaded_file is not None:
    @st.cache
    def load_csv():
        csv = pd.read_csv(uploaded_file,encoding='unicode_escape')
        return csv
    df = load_csv()
    pr = ProfileReport(df, explorative=True)
    st.header('Input DF')
    st.write(df)
    st.write('---')
    st.header('Profiling report')
    st_profile_report(pr)
else:
    st.info('Awaitng for CSV')
    if st.button('press to use example data'):
        def load_data():
            a = sns.load_dataset('titanic')
            return a
        df = load_data()
        pr = ProfileReport(df, explorative=True)
        st.header('Input DF')
        st.write(df)
        st.write('---')
        st.header('Profiling report')
        st_profile_report(pr)
