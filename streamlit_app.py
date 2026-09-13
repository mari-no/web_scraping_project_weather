import sqlite3
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt 
import plotly.express as px  # For interactive charts
import plotly.data as pldata
#Settings 
st.set_page_config(
    page_title = "Global Weather Dashboard",
    page_icon="🌡️",
    layout = "wide"

)
st.title("Global Weather 🌡️ Dashboard")
st.write("Explore global weather for capital cities around the world")


conn = None
try:
    #Connect to DB
    conn = sqlite3.connect("climate.db")
    cursor = conn.cursor()
    query = """
    SELECT c.capital_name,
           t.max_temp,
           t.min_temp,
           t.mean_temp,
           p.precipitation_value
    FROM capitals AS c
    JOIN temperatures AS t
    ON c.capital_id = t.capital_id
    JOIN precipitation p
    ON c.capital_id = p.capital_id;
    """
    df = pd.read_sql(query, conn)
    


except sqlite3.Error as error:
    print(f"An error occurred: {error}")
    if conn is not None:
        conn.rollback()
except Exception as e:
    if conn is not None:
        conn.rollback()  # Rollback transaction if there's an error
    print("Error:", e)
finally:
    if conn is not None:
        conn.close()



# Sidebar

st.sidebar.title("Filter by city")
sidebar_options = st.sidebar.multiselect("Select Cities",
                 df["capital_name"].sort_values(),
                 default = ["Moscow", "Bern", "Berlin", "Washington DC", "Caracas"])

filtered_df = df[df["capital_name"].isin(sidebar_options)]

# Create two side-by-side columns
col1, col2 = st.columns(2)

if filtered_df.empty:
    st.warning("Please select at least one city.")

else:
    with col1:  # Everything under this goes into the left column
    #Visualization 1 of averafge temperature

        st.subheader("Average temperature by Capital")
        filtered_df.plot(
        x="capital_name",
        y="mean_temp",
        kind = "bar",
        color="skyblue",
        title="Average Temperature by Capital",
        xlabel="Capital",
        ylabel="Average Temperature, F")
        plt.xticks(rotation=45)
        plt.tight_layout()
        st.pyplot(plt.gcf())

    with col2:  # Everything under this goes into the right column
    #Visualization 2: max and min temp  
        st.subheader("Maximum and Minimum Temperature")
    # # Line Plot
        filtered_df.plot(x="capital_name", y=["max_temp", "min_temp"], 
                    kind="line", title="Max vs. Min Temperature",
                    xlabel="Capital", ylabel="Temperature, F")
        plt.xticks(rotation=45)
        plt.tight_layout()
        st.pyplot(plt.gcf())




    #Visualization 3: Interactive Visualizations with Plotly
    st.subheader("Average Temperature vs Precipitation")
    fig = px.scatter(df, x='mean_temp',
                    y='precipitation_value',
                    color="capital_name",
                    title="Average Temperature vs Precipitation", hover_data=["capital_name"], 
                    color_discrete_sequence=px.colors.qualitative.Alphabet)

    fig.update_layout(legend_title_text = "City")
    st.plotly_chart(fig)