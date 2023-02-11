import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
import pandas_profiling
import warnings
warnings.filterwarnings('ignore') # to ignore warnings

st.title("By: Usama Bajwa")



# Adding a file uploader widget to select the input csv file
file = st.file_uploader("Upload the 'world_population.csv' file", type=["csv"])


st.write("## EDA, Wrangling")
if file is not None:
    df = pd.read_csv(file)
    # check the data for understanding of data 
    st.write("## Raw Data")
    st.write(df.head())

    # Verified the data type and Null values
    st.write(df.info())
    st.write("## Statistics of Data")
    st.write(df.describe())
    # Printed columns name for X and y
    st.write("## Column Names")
    st.write(df.columns)

    st.set_option('deprecation.showPyplotGlobalUse', False)

    # Adding a selectbox to select the columns for X
    X_columns = st.multiselect("Select columns for X:", df.columns, default=["1970 Population","1980 Population",'2022 Population', '2020 Population', '2015 Population', '2010 Population', '2000 Population', '1990 Population'])
    X = df[X_columns]
    st.write("Selected X columns:", X_columns)

    # Adding a selectbox to select the column for y
    
    a = df['World Population Percentage']

        # Plotting a scatter plot
    st.write("## Scatter Plot")
    sns.scatterplot(data=df, x=X.columns[0], y=a)
    st.pyplot()

    # Plotting a bar plot
    st.write("## Bar Plot")
    sns.barplot(data=df, x=a, y=X.columns[0])
    st.pyplot()

    # Plotting a line chart
    st.write("## Line Chart")
    st.line_chart(X)

    # Plotting a heatmap
    st.write("## Heatmap")
    sns.heatmap(df.corr(), annot=True)
    st.pyplot()
    
    min_population = int(df["2022 Population"].min().astype(int))
    max_population = int(df["2022 Population"].max().astype(int))


    # We changed the values by encoding as the y is countinous
    from sklearn import preprocessing
    from sklearn import utils
    lab = preprocessing.LabelEncoder()
    y = lab.fit_transform(a)
    # Adding sliders to filter the data based on Rank and Population



#Splited the dataset in two parts for test and train, we used the random state to get \
# the same results each time, if we select none everytime results will be changed
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Imported required Libraries for Machine learning
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score
from sklearn.model_selection import train_test_split

from sklearn.model_selection import GridSearchCV



import streamlit as st

models = [LogisticRegression(), SVC(), DecisionTreeClassifier(), RandomForestClassifier(), KNeighborsClassifier()]
model_names = ['Logistic Regression', 'SVM', 'Decision Tree', 'Random Forest', 'KNN']

# Add a sidebar to select the scoring method
scoring_method = st.sidebar.selectbox("Select the scoring method",
                                      ['accuracy', 'precision', 'recall', 'f1'])

models_scores = []
for model, model_name in zip(models, model_names):
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    if scoring_method == 'accuracy':
        score = accuracy_score(y_test, y_pred)
    elif scoring_method == 'precision':
        score = precision_score(y_test, y_pred, average='micro')
    elif scoring_method == 'recall':
        score = recall_score(y_test, y_pred, average='micro')
    else:
        score = f1_score(y_test, y_pred, average='micro')
    models_scores.append([model_name, score])

sorted_models = sorted(models_scores, key=lambda x: x[1], reverse=True)

st.write("## Model Scoring Results")
for model in sorted_models:
    st.write("{}: {:.2f}".format(model[0], model[1]))