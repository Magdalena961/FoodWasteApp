import streamlit as st
from streamlit_extras.colored_header import colored_header
import pandas as pd
import datetime

st.set_page_config(page_title="DiaPlan", layout="wide")

# Nagłówek aplikacji
st.markdown("""
    <h2 style='text-align: center; color: #336699;'>DiaPlan</h2>
    <h4 style='text-align: center; color: #555;'>Automatyzacja diety dla osób z cukrzycą</h4>
    <p style='text-align: center; color: #888;'>Zaplanuj zdrowe posiłki i monitoruj składniki</p>
    <br>
""", unsafe_allow_html=True)

if "meals" not in st.session_state:
    st.session_state.meals = []

tabs = st.tabs(["🍽️ Zaplanuj posiłek", "📋 Moje posiłki", "💡 Zalecenia", "📊 Podsumowanie"])

# Dodawanie posiłku
with tabs[0]:
    with st.form("add_meal"):
        colored_header("Dodaj posiłek", "Wprowadź nazwę, typ posiłku i składniki", color_name="green-70")
        name = st.text_input("Nazwa posiłku")
        type_ = st.selectbox("Typ posiłku", ["Śniadanie", "Obiad", "Kolacja", "Przekąska"])
        ingredients = st.text_area("Składniki (oddzielone przecinkami)")
        date = st.date_input("Data", value=datetime.date.today())
        submit = st.form_submit_button("Dodaj posiłek")

        if submit and name and ingredients:
            st.session_state.meals.append({
                "Nazwa": name,
                "Typ": type_,
                "Składniki": ingredients,
                "Data": date
            })
            st.success(f"✅ Dodano: {name}")

# Moje posiłki
with tabs[1]:
    colored_header("Zapisane posiłki", "Sprawdź i zarządzaj swoimi planami żywieniowymi", color_name="blue-70")
    if st.session_state.meals:
        df = pd.DataFrame(st.session_state.meals)
        st.dataframe(df, use_container_width=True)
    else:
        st.info("Brak zapisanych posiłków. Dodaj coś!")

# Zalecenia
with tabs[2]:
    colored_header("Zalecenia żywieniowe", "Wskazówki dla diety cukrzycowej", color_name="orange-70")
    tips = [
        "🟢 Spożywaj produkty o niskim indeksie glikemicznym (IG)",
        "🥦 Jedz więcej warzyw i produktów pełnoziarnistych",
        "🚰 Pij dużo wody – unikaj słodzonych napojów",
        "🍽️ Jedz regularnie, 4–5 posiłków dziennie",
        "❌ Ogranicz cukry proste i tłuszcze trans"
    ]
    for tip in tips:
        st.markdown(tip)

# Podsumowanie
with tabs[3]:
    colored_header("Podsumowanie", "Twoje statystyki żywieniowe", color_name="violet-70")
    count = len(st.session_state.meals)
    today = datetime.date.today()
    todays_meals = sum(1 for m in st.session_state.meals if m["Data"] == today)

    st.metric("📋 Liczba zaplanowanych posiłków", count)
    st.metric("📆 Dzisiejsze posiłki", todays_meals)

# Stopka
st.markdown("""
    <hr>
    <p style='text-align: center; font-size: 0.8em;'>DiaPlan – automatyzacja diety dla osób z cukrzycą – prototyp pracy dyplomowej</p>
""", unsafe_allow_html=True)
