import streamlit as st
from snowflake.snowpark.context import get_active_session

st.title(f"Customize Your Smoothie! :cup_with_straw: {st.__version__}")
st.write("Create your custom smoothie!")

session = get_active_session()
my_dataframe = session.table("smoothies.public.fruit_options")
fruits = [row['FRUIT_NAME'] for row in my_dataframe.collect()]

# Formulario para la orden
with st.form("smoothie_form"):
    # 1️⃣ Primero el nombre del smoothie / cliente
    name_on_order = st.text_input("Enter your name for the smoothie:")

    # 2️⃣ Luego la selección de ingredientes
    ingredients_list = st.multiselect(
        'Choose up to 5 ingredients:',
        fruits,
        max_selections=5
    )

    # Botón de submit
    submitted = st.form_submit_button("Submit Order")

    if submitted:
        if not name_on_order:
            st.error("Please enter your name!")
        elif not ingredients_list:
            st.error("Please select at least one ingredient!")
        else:
            ingredients_string = ' '.join(ingredients_list)

            my_insert_stmt = f"""
            INSERT INTO smoothies.public.orders(ingredients, name_on_order)
            VALUES ('{ingredients_string}', '{name_on_order}')
            """

            # Ejecutar en Snowflake
            session.sql(my_insert_stmt).collect()

            st.success(f"Order submitted! {name_on_order}'s smoothie: {ingredients_string}")
