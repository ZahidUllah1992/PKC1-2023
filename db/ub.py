import plotly.express as px
import streamlit as st
import os
import pandas as pd


st.set_page_config(page_title="Charts", page_icon=":chart_with_upwards_trend:", layout="wide")

# load the file
file = st.file_uploader("Upload your data file", type=["csv", "xlsx"])

if file is not None:
    file_extension = os.path.splitext(file.name)[1]
    if file_extension == ".csv":
        df = pd.read_csv(file, skiprows=6, skipfooter=1, engine="python")
    elif file_extension == ".xlsx":
        df = pd.read_excel(file)
    else:
        st.error("File format not supported")

# Get the unique values of the 2nd column
GCell_Group_names = df["GCell Group"].unique().tolist()

# Create a line chart
#fig = px.line(df, x=df['Date'], y='Total SDCCH Traffic (Erl)_South', color='GCell_Group_names')

# Update the x-axis tick format
# fig.update_xaxes(tickformat="%b\n%Y")

# # Show the figure
# fig.show()
fig = px.line(df, x=df['Date'], y=df['Total SDCCH Traffic (Erl)_South'],
              hover_data={"Date": "|%B %d, %Y"},
              title='custom tick labels',  color='GCell Group')
fig.update_xaxes(
    dtick="M1",
    tickformat="%b\n%Y")
fig.show()