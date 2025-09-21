import streamlit as st
from snowflake.snowpark import Session

# 🚀 Conexión manual con Snowflake usando secrets.toml
connection_parameters = {
    "account": st.secrets["snowflake"]["account"],
    "user": st.secrets["snowflake"]["user"],
    "password": st.secrets["snowflake"]["password"],
    "role": st.secrets["snowflake"]["role"],
    "warehouse": st.secrets["snowflake"]["warehouse"],
    "database": st.secrets["snowflake"]["database"],
    "schema": st.secrets["snowflake"]["schema"]
}

session = Session.builder.configs(connection_parameters).create()

# 🚀 UI principal
st.title(f"Customize Your Smoothie! :cup_with_straw: (Streamlit {st.__version__})")
st.write("Create your custom smoothie!")

# 🚀 Leer frutas desde Snowflake
fruit_df = session.table("smoothies.public.fruit_options")
fruits = [row["FRUIT_NAME"] for row in fruit_df.collect()]

# 🚀 Formulario
with st.form("smoothie_form"):
    name_on_order = st.text_input("Enter your name for the smoothie:")
    ingredients_list = st.multiselect(
        "Choose up to 5 ingredients:",
        fruits,
        max_selections=5
    )
    submitted = st.form_submit_button("Submit Order")

    if submitted:
        if not name_on_order.strip():
            st.error("⚠️ Please enter your name!")
        elif not ingredients_list:
            st.error("⚠️ Please select at least one ingredient!")
        else:
            ingredients_string = " ".join(ingredients_list)

            # 🚀 Insert seguro en Snowflake
            session.table("smoothies.public.orders").insert({
                "INGREDIENTS": ingredients_string,
                "NAME_ON_ORDER": name_on_order
            })

            st.success(f"✅ Order submitted! {name_on_order}'s smoothie: {ingredients_string}")
