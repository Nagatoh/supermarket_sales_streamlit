import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from dash_bootstrap_templates import load_figure_template
# I was too lazy to configure the charts individually, and this dash library served very well :)
load_figure_template('minty')
st.set_page_config(layout="wide")
# ========== Data Preparation ========== #
@st.cache(allow_output_mutation=True)
def get_data():
    df_data = pd.read_csv("./data/supermarket_sales.csv")
    df_data["Date"] = pd.to_datetime(df_data["Date"])
    return df_data

@st.experimental_memo
def get_dfs_filtered(df_data,city_list,main_variable):
    operation = np.sum if main_variable == "gross income" else np.mean

    df_filtered = df_data[df_data["City"].isin(city_list)]
    df_city = df_filtered.groupby("City")[main_variable].apply(
        operation).to_frame().reset_index()
    df_gender = df_filtered.groupby(["Gender", "City"])[main_variable].apply(
        operation).to_frame().reset_index()
    df_payment = df_filtered.groupby("Payment")[main_variable].apply(
        operation).to_frame().reset_index()

    df_income_time = df_filtered.groupby("Date")[main_variable].apply(
        operation).to_frame().reset_index()
    df_product_income = df_filtered.groupby(["Product line", "City"])[
        main_variable].apply(operation).to_frame().reset_index()

    return df_city, df_gender,df_payment,df_income_time,df_product_income

@st.experimental_memo
def get_graphs(df_data,city_list,main_variable):
    df_city, df_gender,df_payment,df_income_time,df_product_income = get_dfs_filtered(df_data,city_list,main_variable)

    fig_city = px.bar(df_city, x="City", y=main_variable)
    fig_payment = px.bar(df_payment, y="Payment",x=main_variable, orientation="h")
    fig_gender = px.bar(df_gender, y="Gender", x=main_variable, color="City", barmode="group")
    fig_product_income = px.bar(df_product_income, x=main_variable, y="Product line", color="City", orientation="h", barmode="group")
    fig_income_date = px.bar(df_income_time, x="Date",y=main_variable,)

    for fig in [fig_city, fig_payment, fig_gender, fig_income_date, fig_product_income]:
        fig.update_layout(margin=dict(l=0, r=0, t=0, b=0), height=200,width=450)

    fig_product_income.update_layout(margin=dict(l=0, r=0, t=0, b=0), height=500, width=1300)
    fig_income_date.update_layout(margin=dict(l=0, r=0, t=0, b=0), height=500, width=1300)

    return fig_city, fig_payment, fig_gender, fig_product_income, fig_income_date

df_data = get_data()

# ========== Layout ========== #
# ========== Sidebar ========== #
st.sidebar.image('./assets/logo.png',width=90)
# Filters
city_list = st.sidebar.multiselect("Select City",options=df_data["City"].value_counts().index.to_list(),default=df_data["City"].value_counts().index.to_list())
main_variable = st.sidebar.radio("Select Variable",["gross income","Rating"])
# ========= Principal Row 1 ========== #
fig_city, fig_payment, fig_gender, fig_product_income, fig_income_date = get_graphs(df_data,city_list,main_variable)
chart1,chart2,chart3 = st.columns(3)
chart1.plotly_chart(fig_city, use_container_width=False)
chart2.plotly_chart(fig_gender, use_container_width=False)
chart3.plotly_chart(fig_payment, use_container_width=False)
# ========= Principal Row 2 ========== #
st.plotly_chart(fig_product_income,use_container_width=False)
st.plotly_chart(fig_income_date,use_container_width=False)