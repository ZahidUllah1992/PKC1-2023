import plotly.express as px
import pandas as pd
import streamlit as st
import os

st.set_page_config(page_title="Charts", page_icon=":chart_with_upwards_trend:", layout="wide")

st.title("Dashboard")

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



# Get the list of KPI columns
kpi_cols = df.columns[df.columns.get_loc("Integrity")+1:]

# Create a sidebar for legend selection
show_legend = st.sidebar.checkbox("Show Legend", value=True)

# Plot multiple line charts for each KPI column
for col in kpi_cols:
    fig = px.line(df, x='Date', y=col, color=df.columns[1],
                  hover_data={"Date": "|%B %d, %Y"},
                  title=col)
    fig.update_layout(showlegend=show_legend)
    fig.update_xaxes(
        dtick="M1",
        tickformat="%b\n%Y")
    st.plotly_chart(fig)
