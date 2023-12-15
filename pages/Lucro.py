import pandas as pd
import streamlit as st
import plotly.express as px
import numpy as np

# Load data from CSV
file_path = "produto.csv"  # Replace with the actual file path
try:
    df_product_prices = pd.read_csv(file_path)
except FileNotFoundError:
    st.error(f"File not found: {file_path}")
    st.stop()

# Adicionar coluna de pct_lucro para cada produto em cada cidade
for city in df_product_prices.columns[2:6]:
    df_product_prices[f'{city}_pct_lucro'] = ((df_product_prices[city] - df_product_prices['farmprice']) / df_product_prices['farmprice']).replace([np.inf, -np.inf], np.nan) * 100

# Display the data
st.title("Análise de Produtos e Preços")
st.subheader("Preview of the Data:")
st.write(df_product_prices.head())

# Interactive filter for selecting products
selected_product = st.selectbox("Select a Product:", df_product_prices['productname'].unique())

# Filter data for the selected product
filtered_data = df_product_prices[df_product_prices['productname'] == selected_product]

# Visualization options
visualization_option = st.radio("Select Visualization Type:", ["Line Chart", "Bar Chart", "Scatter Plot"])

# Interactive filter for selecting cities
selected_cities = st.multiselect("Select Cities:", df_product_prices.columns[2:6])

# Plot selected visualization
st.subheader(f"{visualization_option} for {selected_product} in Selected Cities:")
if visualization_option == "Line Chart":
    fig = px.line(filtered_data, x='date', y=selected_cities, title=f"{selected_product} Prices Over Time")
elif visualization_option == "Bar Chart":
    fig = px.bar(filtered_data, x='date', y=selected_cities, title=f"{selected_product} Prices Over Time")
elif visualization_option == "Scatter Plot":
    fig = px.scatter(filtered_data, x='date', y=selected_cities, title=f"{selected_product} Prices Over Time")

# Show the interactive chart
st.plotly_chart(fig)

# Summary statistics
st.subheader("Summary Statistics:")
if selected_cities:
    st.write(filtered_data[selected_cities].describe())
else:
    st.warning("Please select at least one city for summary statistics.")

# Comparar a média de lucros dos produtos em cada cidade
st.header("Comparação da Média de Lucros dos Produtos em Cada Cidade:")
if selected_cities:
    avg_profit_comparison = filtered_data.groupby(selected_cities).mean()[[f'{city}_pct_lucro' for city in selected_cities]].reset_index()
    fig_avg_profit_comparison = px.bar(avg_profit_comparison, x=selected_cities, y=[f'{city}_pct_lucro' for city in selected_cities], title="Comparação da Média de Lucros")
    st.plotly_chart(fig_avg_profit_comparison)
else:
    st.warning("Please select at least one city for profit comparison.")

# Média de preço dos produtos com maiores average spread
st.header("Média de Preço dos Produtos com Maiores Average Spread:")
top_products_by_avg_spread = df_product_prices.groupby('productname')['averagespread'].max().nlargest(5).index
avg_price_top_products = df_product_prices[df_product_prices['productname'].isin(top_products_by_avg_spread)].groupby('productname').mean().reset_index()
fig_avg_price_top_products = px.bar(avg_price_top_products, x='productname', y=selected_cities, title="Média de Preço dos Produtos com Maiores Average Spread")
st.plotly_chart(fig_avg_price_top_products)