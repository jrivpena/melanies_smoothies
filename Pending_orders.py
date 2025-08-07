# Import python packages
import streamlit as st
from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col, when_matched 


# Write directly to the app
st.title(":cup_with_straw: Pending Smoothie Orders :cup_with_straw:")
st.write(
  """**Orders that need to be filled.** 
  """)
# name_on_order = st.text_input('Nome on Smoothie:')
# st.write('The name in your Smoothie will be:', name_on_order)

session = get_active_session()
my_dataframe = session.table("smoothies.public.orders").filter(col("ORDER_FILLED")==0).collect()


if my_dataframe:
    
    editable_df = st.data_editor(my_dataframe)
    
    submitted = st.button('Submit')
    
    if submitted:
                
        og_dataset = session.table("smoothies.public.orders")
        edited_dataset = session.create_dataframe(editable_df)

        try:
            og_dataset.merge(edited_dataset
                         , (og_dataset['ORDER_UID'] == edited_dataset['ORDER_UID'])
                         , [when_matched().update({'ORDER_FILLED': edited_dataset['ORDER_FILLED']})]
                        )
    
            st.success("Someone clicked the button.", icon="👍")
        except:
            st.write('Something went wrong')
else:
    st.success('There are no pending orders right now',icon="👍" )



##Para mostrar el contenido del dataframe
##st.dataframe(data=my_dataframe, use_container_width=True)




## Este codigo viene de la copia anterior

# ingredients_list = st.multiselect(
#     'Choose up to 5 ingredientes:'
#     , my_dataframe
#     )
# if ingredients_list:
    
#     ingredients_string = ''
    
#     for fruit_chosen in ingredients_list:
#         ingredients_string += fruit_chosen + ' '
#     st.write(ingredients_string)

#     my_insert_stmt = """ insert into smoothies.public.orders(ingredients,name_on_orders)
#             values ('""" + ingredients_string + """','""" + name_on_order + """')"""

#     ## Just for testing the SQL 
#     ##st.write(my_insert_stmt)
#     ##st.stop()
    

#     #st.write(my_insert_stmt)
#     time_to_insert = st.button('Submit Order')
    
#     if time_to_insert:
#         session.sql(my_insert_stmt).collect()

#         st.success(f'Your Smoothie is ordered, {name_on_order}', icon="✅")
