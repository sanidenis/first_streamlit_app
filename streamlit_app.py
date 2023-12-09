# Import python packages
import streamlit

# Write directly to the app
streamlit.title("My Parents' New Healthy Diner")
streamlit.header("Breakfast Menu")
streamlit.write("🥣 Omega 3 & Blueberry Oatmeal")
streamlit.write("🥗 Kale, Spinach & Rocket Smoothie")
streamlit.write("🐔 Hard-Boiled Free-Range Egg")
streamlit.write("🥑🍞 Avocado Toast")

streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')

import pandas
my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list = my_fruit_list.set_index('Fruit')
fruits_selected = streamlit.multiselect("Pick some fruits: ", list(my_fruit_list.index), ['Avocado','Strawberries'])
fruits_to_show = my_fruit_list.loc[fruits_selected]
streamlit.dataframe(fruits_to_show)

fruit_choice = streamlit.text_input('What fruit would you like information about?','apple')
streamlit.write('The user entered ', fruit_choice)

import requests
fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + fruit_choice)

#run panda's normalize function on the json response
fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
#make a new table withthe normalized response
streamlit.dataframe(fruityvice_normalized)

import snowflake as sf
from snowflake-connector-python import connector
