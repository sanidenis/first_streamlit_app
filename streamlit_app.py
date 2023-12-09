# Import python packages
import streamlit
import pandas
import requests
import snowflake as sf
from snowflake import connector
from urllib.error import URLError

# Write directly to the app
streamlit.title("My Parents' New Healthy Diner")
streamlit.header("Breakfast Menu")
streamlit.write("🥣 Omega 3 & Blueberry Oatmeal")
streamlit.write("🥗 Kale, Spinach & Rocket Smoothie")
streamlit.write("🐔 Hard-Boiled Free-Range Egg")
streamlit.write("🥑🍞 Avocado Toast")

streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')

my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list = my_fruit_list.set_index('Fruit')
fruits_selected = streamlit.multiselect("Pick some fruits: ", list(my_fruit_list.index), ['Avocado','Strawberries'])
fruits_to_show = my_fruit_list.loc[fruits_selected]
streamlit.dataframe(fruits_to_show)

def get_fruityvice_data(this_fruit_choice):
  #run panda's normalize function on the json response
  fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + this_fruit_choice)
  #make a new table withthe normalized response
  fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
  return fruityvice_normalized

streamlit.header('Fruityvice Fruit Advice!')

try:
  fruit_choice = streamlit.text_input('What fruit would you like information about?','apple')
  if not fruit_choice:
    streamlit.error("Please select a fruit to get information.")
  else:
    back_from_function = get_fruityvice_data(fruit_choice)
    streamlit.dataframe(back_from_function)

except URLError as e:
  streamlit.error()

# don't run anything past here while we troubleshoot
# streamlit.stop()

streamlit.header("The fruit load list contains:")
def get_fruit_load_list():
  with my_cnx.cursor() as my_cur:
    my_cur.execute("select * from pc_rivery_db.public.fruit_load_list")
    return my_cur.fetchall()

#add a button to load the fruit
if streamlit.button('Get Fruit Load List'):
  my_cnx = sf.connector.connect(**streamlit.secrets["snowflake"])
  my_data_rows = get_fruit_load_list()
  streamlit.dataframe(my_data_rows)

fruit_add = streamlit.text_input('What fruit would you like to add?','jackfruit')
streamlit.write('Thanks for adding ', fruit_add)

my_cur.execute("INSERT INTO FRUIT_LOAD_LIST VALUES ('from streamlit')")
