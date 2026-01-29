# Import python packages
import streamlit as st
from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col

# Write directly to the app
st.title(":cup_with_straw: customize your smoothie :cup_with_straw:")
st.write(
  " shoose the fruit you want in your custum  smoothie "
)


name_on_order = st.text_input('Name on Smoothie')
st.write('the name on your smotthie wuil be', name_on_order)

cnx=st.connection("snowflake")
session = cnx.session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))


ingredients_list = st.multiselect(
    'choose up to 5 ingredients',
    my_dataframe,
    max_selections=5
)


if ingredients_list :
  ingredient_string =''

  for fruit_chosen in ingredients_list:
    ingredients_list += fruit_chosen + ''

  
  my_insert_stmt = """ insert into smoothies.public.orders(ingredients,name_on_order)
            values ('""" + ingredient_string + """','"""+ name_on_order +"""')"""

  st.write(my_insert_stmt)
  if ingredient_string:
    session.sql(my_insert_stmt).collect()
    st.success('Your Smoothie is ordered!', icon="✅")

