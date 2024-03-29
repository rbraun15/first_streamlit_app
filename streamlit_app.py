import streamlit
import pandas
import requests
import snowflake.connector
from urllib.error import URLError


streamlit.title('My Parents New Healthy Diner')

streamlit.header('Breakfast Favorites')
streamlit.text ('🥣 Omega 3 & Bluberry Otameal')
streamlit.text ('🥗 Kale, Spinach & Rocket Smoothie')
streamlit.text ('🐔 Hard-Boild Free-Range Egg')
streamlit.text ('🥑🍞 Avocado Toast')

streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')


my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list = my_fruit_list.set_index('Fruit')


# Let's put a pick list here so they can pick the fruit they want to include 
fruits_selected = streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index), ['Avocado','Strawberries'])
fruits_to_show = my_fruit_list.loc[fruits_selected]


# Display the table on the page.
streamlit.dataframe(fruits_to_show)

#New Section to display fruityvice api resopnse
streamlit.header("Fruityvice Fruit Advice!")

try:
   fruit_choice = streamlit.text_input('What fruit would you like information about?')
   if not fruit_choice:
        streamlit.error("Please select a fruit to get information.")
   else:
#streamlit.write('The user entered ', fruit_choice)
# fruityvice_response = requests.get("https://fruityvice.com/api/fruit/watermelon")
# streamlit.text(fruityvice_response.json())  # just writes the data to the screen
# fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + "kiwi")
      fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + fruit_choice)
# use pandas to format the data
      fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
# put response in a table
      streamlit.dataframe(fruityvice_normalized)

except URLError as e:
    streamlit.error()


streamlit.stop()

my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
my_cur = my_cnx.cursor()
# my_cur.execute("SELECT CURRENT_USER(), CURRENT_ACCOUNT(), CURRENT_REGION()")
my_cur.execute("SELECT * from fruit_load_list")
#my_data_row = my_cur.fetchone()
my_data_rows = my_cur.fetchall()
# streamlit.text("Hello from Snowflake:")
streamlit.header("The fruit load list contains:")
#streamlit.dataframe(my_data_row)
streamlit.dataframe(my_data_rows)

streamlit.header('Fruity Fruit Advice!')
 

#  allow the end user to add a fruit to the list
 
# Let's put a pick list here so they can pick the fruit they want to include

add_my_fruit = streamlit.text_input('What fruit would you like to add?')
streamlit.write('The user entered ', add_my_fruit)


my_cur.execute("insert into fruit_load_list values ('from streamlit')")












