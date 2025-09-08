import streamlit as st
import pandas as pd
import altair as alt

st.set_page_config(
    page_title="US Population Dashboard",
    layout="wide",
    initial_sidebar_state="expanded")

alt.themes.enable("dark")

df_food = pd.read_csv('data/foodpanda_analysis.csv')
    
def make_bar_chart(input_df, input_x, input_y, input_color):
    age_counts = input_df['age'].value_counts().reindex(['Adult', 'Teenager', 'Senior']).fillna(0)
    age_counts = age_counts.reset_index()
    age_counts.columns = ['Age Group', 'Count']
    bar_chart = alt.Chart(age_counts).mark_bar(color=input_color).encode(
        x=alt.X('Age Group', sort=['Adult', 'Teenager', 'Senior']),
        y='Count'
    ).properties(
        width=400,
        height=350
    )
    return bar_chart

# Function to create a line graph of number of orders over time
def make_orders_line_graph(input_df, date_column, line_color='#1f77b4'):
    df = input_df.copy()
    df[date_column] = pd.to_datetime(df[date_column], errors='coerce')
    orders_by_date = df.groupby(date_column).size().reset_index(name='Order Count')
    orders_by_date = orders_by_date.sort_values(date_column)
    line_chart = alt.Chart(orders_by_date).mark_line(color=line_color, point=True).encode(
        x=alt.X(date_column, title='Order Date'),
        y=alt.Y('Order Count', title='Number of Orders')
    ).properties(
        width=600,
        height=350
    )
    return line_chart

# Positioning
col = st.columns((1.5, 4.5, 2), gap='medium')
with col[1]:
    st.markdown('#### Age Group Distribution')
    bar_chart = make_bar_chart(df_food, 'age', 'count', "#6DC8E4")
    st.altair_chart(bar_chart, use_container_width=True)

    st.markdown('#### Frequency of Orders Over Time')
    line_graph = make_orders_line_graph(df_food, 'order_date', "#6DC8E4")
    st.altair_chart(line_graph, use_container_width=True)

with col[2]:
    st.markdown('#### Top Cities by Number of Orders')
    top_cities = df_food['city'].value_counts().reset_index()
    top_cities.columns = ['City', 'Order Count']
    st.dataframe(
        top_cities,
        column_order=("City", "Order Count"),
        hide_index=True,
        use_container_width=True,
        column_config={
            "City": st.column_config.TextColumn("City"),
            "Order Count": st.column_config.ProgressColumn(
                "Order Count",
                format="%d",
                min_value=0,
                max_value=int(top_cities["Order Count"].max()),
            ),
        },
    )
    with st.expander('About', expanded=True):
        st.write('''
            - Data: [FoodPanda Review Dataset](<https://www.kaggle.com/datasets/zubairamuti/foodpanda-review-dataset>).
            - :orange[**Age Group Distribution**]: distribution of customers across different age groups (teenagers, adults, seniors)
            - :orange[**Frequency of Orders Over Time**]: number of orders placed over time from 2024 to 2025
            ''')

