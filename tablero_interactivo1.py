# Streamlit code for dashboard creation
streamlit_code = """
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the data
data_path = 'Steam_2024_with_predictions.csv'
data = pd.read_csv(data_path)

# Set the page layout
st.set_page_config(page_title="2024 Steam Statistics", layout="wide")

# Title
st.title("2024 Steam Statistics")

# Key Metrics
total_revenue = data['revenue'].sum()
total_games_sold = data['copiesSold'].sum()
total_games = data['name'].nunique()

col1, col2, col3 = st.columns(3)
col1.metric("Total Revenue", f"${total_revenue/1e9:.2f}B")
col2.metric("Games Sold", f"{total_games_sold/1e6:.1f}M")
col3.metric("Total Games", total_games)

# Games Sold vs Revenue
st.subheader("Games Sold vs Revenue")
top_games = data.nlargest(10, 'revenue')
fig1, ax1 = plt.subplots()
ax1.barh(top_games['name'], top_games['copiesSold'], label='Games Sold', color='skyblue')
ax1.set_xlabel("Games Sold")
ax1.set_ylabel("Game")
ax12 = ax1.twinx()
ax12.barh(top_games['name'], top_games['revenue'], label='Revenue', color='pink', alpha=0.7)
ax12.set_xlabel("Revenue")
fig1.legend(["Games Sold", "Revenue"], loc="lower right")
st.pyplot(fig1)

# Game Price vs Games Sold
st.subheader("Game Price vs Games Sold")
fig2, ax2 = plt.subplots()
sns.scatterplot(data=data, x='copiesSold', y='price', size='revenue', hue='reviewScore', alpha=0.7, ax=ax2)
ax2.set_xlabel("Games Sold")
ax2.set_ylabel("Price")
st.pyplot(fig2)

# Publisher Class Distribution
st.subheader("Publisher Class Distribution")
publisher_class_counts = data['publisherClass'].value_counts()
fig3, ax3 = plt.subplots()
ax3.pie(publisher_class_counts, labels=publisher_class_counts.index, autopct='%1.1f%%', startangle=90)
ax3.set_title("Publisher Class Distribution")
st.pyplot(fig3)

# Total Revenue by Publisher
st.subheader("Total Revenue by Publisher")
revenue_by_publisher = data.groupby('publishers')['revenue'].sum().nlargest(10)
fig4, ax4 = plt.subplots()
revenue_by_publisher.plot(kind='bar', ax=ax4)
ax4.set_ylabel("Revenue")
ax4.set_title("Total Revenue by Publisher")
st.pyplot(fig4)

# Review Score vs Playtime
st.subheader("Review Score vs Playtime")
fig5, ax5 = plt.subplots()
sns.scatterplot(data=data, x='reviewScore', y='avgPlaytime', size='copiesSold', hue='publisherClass', alpha=0.7, ax=ax5)
ax5.set_xlabel("Review Score")
ax5.set_ylabel("Average Playtime")
st.pyplot(fig5)
"""

# Save the Streamlit code to a file for user to download
streamlit_file_path = '/mnt/data/streamlit_dashboard.py'
with open(streamlit_file_path, 'w') as f:
    f.write(streamlit_code)

streamlit_file_path
