import streamlit
import pandas
import requests
import snowflake.connector
from urllib.error import URLError

streamlit.title('My Mums New Healthy Diner')

streamlit.header('Breakfast Favourites')

streamlit.text('🥣 Omega 3 & Blueberry Oatmeal')
streamlit.text('🥬 Kale, Spinach & Rocket Smoothie')
streamlit.text('🐔 Hard-Boiled Free Range Egg')
streamlit.text('🥑🍞 Avocado Toast')
streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')

#import pandas
my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list = my_fruit_list.set_index('Fruit')

# Let's put a pick list here so they can pick the fruit they want to include 
fruits_selected = streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index),['Avocado','Strawberries'])
fruits_to_show = my_fruit_list.loc[fruits_selected]

# Display the table on the page.
streamlit.dataframe(fruits_to_show)

# End of first section
# exit script here
#streamlit.stop()

#Create a repeatable block of code (called a function)
def get_fruityvicedata(this_fruit_choice):
  fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + this_fruit_choice)
  # take the json version of the response and normalise it
  fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
  return fruityvice_normalized

# New section to display fruityvice api response
streamlit.header("Fruityvice Fruit Advice!")
try:
  fruit_choice = streamlit.text_input('What fruit would you like information about?')
  if not fruit_choice:
      streamlit.error('Please select a fruit to get info.')
  else:
    back_from_function = get_fruityvicedata(fruit_choice)
    # output it to the screen as a table
    streamlit.dataframe(back_from_function)

except URLError as e:
      streamlit.error()  
    
# end of second section
# exit script here
streamlit.stop()
    
#      streamlit.write('The user entered ', fruit_choice)

# import requests
#fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + fruit_choice)
#streamlit.text(fruityvice_response.json())

# take the json version of the response and normalise it. 
#fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
# output it to the screen as a table
#streamlit.dataframe(fruityvice_normalized)

streamlit.header("The fruit load list contains:")

# snowflake-related function ...
def get_fruit_load_list():
  with my_cnx.cursor() as my_cur:
    my_cur.execute("SELECT * from fruit_load_list")
    return my_cur.fetchall()
# add a button to load the fruit ...
if streamlit.button('Get Fruit Load List'):
  # import snowflake connector
  my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
  my_data_rows = get_fruit_load_list()
  streamlit.dataframe(my_data_rows)

# Allow the end user to add a fruit to the list

# Define a function

def insert_row_snowflake(new_fruit):
  with my_cnx.cursor() as my_cur:
    my_cur.execute("INSERT into fruit_load_list values ('from Streamlit')")
    return 'Thanks for adding '+ new_fruit
#

add_my_fruit = streamlit.text_input('Any fruit you would like to add?')
if streamlit.button('Add a fruit to the list'):
  my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
  back_from_function = insert_row_snowflake(add_my_fruit)    
  streamlit.text(back_from_function)
  
# exit script here
streamlit.stop()

# my_cur = my_cnx.cursor()
# my_cur.execute("SELECT CURRENT_USER(), CURRENT_ACCOUNT(), CURRENT_REGION()")

my_cur.execute("SELECT * from fruit_load_list")

my_data_row = my_cur.fetchall()

# streamlit.text("Hello from Snowflake:")

streamlit.text("The fruit load list contains:")

streamlit.dataframe(my_data_row)



# Let's put another pick list here so they can pick the fruit they want to add to the list 
add_my_fruit = streamlit.multiselect("Any fruit you would like to add?:", list(my_fruit_list.index))

streamlit.write('Thanks for adding ', add_my_fruit)





