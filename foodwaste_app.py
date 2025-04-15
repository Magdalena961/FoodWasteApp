import streamlit as st
import datetime

st.set_page_config(page_title="FoodWasteApp", layout="wide")
st.title("🧊 FoodWasteApp")
st.caption("Ogranicz marnowanie jedzenia w swoim domu!")

# Inicjalizacja
if "products" not in st.session_state:
    st.session_state.products = []

# Dodawanie produktu
with st.form("add_item"):
    st.subheader("Dodaj produkt")
    name = st