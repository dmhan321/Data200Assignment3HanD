
import streamlit as st
from datetime import datetime
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# Streamlit App
st.title("Salse Analysis of Pizzas")

# read csv file
data = pd.read_csv(r"pizza_sales.csv")
df = pd.DataFrame(data)
df['date'] = pd.to_datetime(df['date']) 
df = df.sort_values('date')
df['sales'] = df['price'] * df['quantity']

## Topic 1: Analyzing the Sales Patterns Over Time for the Pizza Store
st.subheader("Topic 1: What is the Sales Patterns Over Time for the Pizza Store?")

# group the data by 'date'
df_date = df.groupby('date')['sales'].sum().reset_index()

# Set the allowed date range for selection
allowed_start_date = datetime(2015, 1, 1)
allowed_end_date = datetime(2015, 12, 31)

# Create date selectors for start and end dates
start_date = st.date_input("Select a start date", allowed_start_date, 
                           allowed_start_date, allowed_end_date)
end_date = st.date_input("Select an end date", allowed_end_date, 
                         allowed_start_date, allowed_end_date)

if start_date and end_date:
    start_date = pd.to_datetime(start_date) # converts the start_date and end_date inputs from the date picker to Pandas Timestamps 
    end_date = pd.to_datetime(end_date)
    filtered_data = df_date[(df_date['date'] >= start_date) 
                            & (df_date['date'] <= end_date)]
    

    # Plotting the line chart
    fig, ax = plt.subplots()
    plt.figure(figsize=(8, 6))
    ax.plot(filtered_data['date'], filtered_data['sales'], linestyle='-', color='skyblue')
    plt.xticks(rotation=45) 
    plt.gca().xaxis.set_major_locator(plt.matplotlib.dates.DayLocator(interval=30))
    ax.set_xlabel('Date')
    ax.set_ylabel('Sales Amount (USD)')
    ax.set_title('Sales Trends')
    st.pyplot(fig)

st.write("""The line chart above illustrates the sales trends of the pizza store throughout the 
         year 2015. From the graph, it's evident that the daily revenue experiences fluctuations 
         without a smooth trajectory. However, overall, the revenue remains relatively low in the 
         first half of the year, showing an upward trend in October, followed by a slight 
         decline, and then another increase in December. The month of December marks 
         the peak season for sales. The pizza store might consider launching promotional campaigns
          during the first half of the year to stimulate an increase in revenue.""")

## Topic 2: Identify the Most Popular Day of the Week for Sales

st.subheader("Topic 2: Which day of the week sees the highest sales?")
# Group sales by day of the week and sum the sales amount
df['day_of_week'] = df['date'].dt.day_name()  # Extract day of the week
daily_sales = df.groupby('day_of_week')['sales'].sum().reset_index()
days_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
daily_sales['day_of_week'] = pd.Categorical(daily_sales['day_of_week'],
                                            categories=days_order, ordered=True)
daily_sales = daily_sales.sort_values('day_of_week')

# Plotting the sales by day of the week
fig, ax = plt.subplots()
plt.bar(daily_sales['day_of_week'], daily_sales['sales'], color='skyblue')
plt.xlabel('Day of the Week')
plt.ylabel('Total Sales Amount')
plt.title('Total Sales by Day of the Week')
plt.xticks(rotation=45)
plt.tight_layout()
st.pyplot(fig)

st.write("""The bar chart above displays the pizza store's sales performance on a daily basis 
         throughout the week. Overall, pizza sales show a noticeable increase starting from Monday, 
         reaching a peak by Thursday, then gradually declining, and reaching a low point by Sunday.
          The sales peak is concentrated between Thursday and Saturday. The pizza store could
          encourage staff to schedule their days off on Sundays, Mondays or Tuesdays to minimize 
         the impact on the business during these slower days.""")


st.subheader("Topic 3: Are there identifiable time slots during a day's operation that depict varying levels of activity?")

df['time'] = pd.to_datetime(df['time'])

# Extract hour from the 'time' column as string and split into hours and minutes
df['hour'] = df['time'].dt.strftime('%H:%M').str.split(':').str[0]

# Convert extracted hour back to numeric format (integer)
df['hour'] = pd.to_numeric(df['hour'])
# Plotting the sales distribution by hour using a histogram
fig, ax = plt.subplots()
plt.hist(df['hour'], bins=24, color='skyblue', edgecolor='black')
plt.xlabel('Hour of the Day')
plt.ylabel('Number of Sales')
plt.title('Sales Distribution by Hour of the Day')
plt.xlim(10, 23)
plt.xticks(range(10,24)) 
plt.tight_layout()

# Display the plot in Streamlit
st.pyplot(fig)
st.write("""The chart illustrates two prominent peaks in sales during the operational hours,
          occurring approximately from 12 to 13 o'clock and 17 to 18 o'clock, aligning perfectly 
         with the lunch and dinner periods. There's also a noticeable surge in sales around 
         15 o'clock, indicating a potential scenario where customers purchase pizzas for an 
         afternoon snack.""")

## Topic 4: Identify the top 5 popular pizzas

# Group sales by pizza name and sum the sales amount
popular_pizza = df.groupby('name')[['quantity','sales']].sum().reset_index().sort_values(
    ['quantity','sales'], ascending=True)

# Select top 5 popular pizzas
top_5_pizzas_sorted = popular_pizza.head(5)

# Streamlit app
st.subheader("Topic 4: What type of pizza is most preferred by customers?")

# Visualize the most popular pizza
fig, ax = plt.subplots()
bar_width = 0.35
bars1 = np.arange(len(top_5_pizzas_sorted))
bars2 = [x + bar_width for x in bars1]

plt.barh(bars1, top_5_pizzas_sorted['quantity'], bar_width, color='skyblue', label='Quantity')
plt.barh(bars2, top_5_pizzas_sorted['sales'], bar_width, color='orange', label='Sales')

plt.xlabel('Quantity / Sales')
plt.ylabel('Pizza Name')
plt.title('Top 5 Popular Pizzas by Quantity and Sales')
plt.yticks(bars1 + bar_width / 2, top_5_pizzas_sorted['name'])
plt.legend()
plt.tight_layout()
st.pyplot(fig)

st.write(""""The chart showcases the top five pizzas ranked by sales volume and revenue. Topping 
         the list is the Chicken Pesto Pizza, followed by the Soppresssata Pizza, the Mediterranean
          Pizza, the Calabrese Pizza and the Brie Carre Pizza. The pizza store can label these pizzas
          as 'bestsellers' on the menu for easier customer selection. Additionally, considering a
          moderate increase in the supply of these pizzas would be beneficial.""")

st.subheader("Topic 5: Is there a noticeable preference among customers regarding the size of pizzas?")

# Group sales by pizza size and sum the sales amount
size_preference = df.groupby('size')['quantity'].sum().reset_index()

# Visualize the size preference using a bar chart
fig, ax = plt.subplots()
plt.pie(size_preference['quantity'], labels=size_preference['size'], autopct='%1.1f%%', startangle=140)
plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
plt.title('Size Preference for Pizzas')
# Display the plot in Streamlit
st.pyplot(fig)

st.write("""The pie chart above illustrates the distribution of pizza sales across various sizes. 
         It's evident that the Large (L) size pizza comprises the highest portion, accounting for 
         52.6% of sales, surpassing the majority. On the contrary, the Extra Large (XL) size constitutes 
         the smallest proportion, merely 0.8% of the total sales. Based on this information, the pizza
          store could consider increasing the stock of Large (L) size pizzas while reducing the inventory
          for Extra Large (XL) size pizzas.""")
