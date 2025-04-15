import streamlit as st
import pandas as pd
import datetime

st.set_page_config(page_title="DiaPlan - Dieta w cukrzycy", layout="wide")

# Stylizacja CSS
st.markdown("""
    <style>
        .main-header {
            text-align: center;
            color: #2e7d32;
            font-size: 3em;
            font-weight: bold;
            font-family: 'Georgia', serif;
            margin-top: 0.5em;
        }
        .sub-header {
            text-align: center;
            color: #8d6e63;
            font-size: 1.2em;
            font-style: italic;
        }
    </style>
""", unsafe_allow_html=True)

# Nagłówek
st.markdown("""
    <div class='main-header'>DiaPlan</div>
    <div class='sub-header'>Personalizowany planer diety dla osób z cukrzycą</div>
    <br>
""", unsafe_allow_html=True)

# Inicjalizacja sesji
if "meals" not in st.session_state:
    st.session_state.meals = []

# Sidebar: dodawanie posiłków
with st.sidebar:
    st.header("🍽️ Dodaj posiłek")
    meal_name = st.text_input("Nazwa posiłku")
    carbs = st.number_input("Węglowodany [g]", min_value=0)
    proteins = st.number_input("Białko [g]", min_value=0)
    fats = st.number_input("Tłuszcze [g]", min_value=0)
    date = st.date_input("Data", value=datetime.date.today())
    time = st.time_input("Godzina")
    if st.button("Dodaj posiłek"):
        if meal_name:
            st.session_state.meals.append({
                "Posiłek": meal_name,
                "Węglowodany": carbs,
                "Białko": proteins,
                "Tłuszcze": fats,
                "Data": date,
                "Godzina": time
            })
            st.success(f"Dodano: {meal_name}")

# Zakładki
page = st.selectbox("Wybierz sekcję", ["📅 Dziennik posiłków", "📈 Podsumowanie", "📚 Porady"])

if page == "📅 Dziennik posiłków":
    st.subheader("📅 Twoje posiłki")
    if st.session_state.meals:
        df = pd.DataFrame(st.session_state.meals)
        st.dataframe(df.sort_values(by=["Data", "Godzina"]), use_container_width=True)
        csv = df.to_csv(index=False).encode("utf-8")
        st.download_button("📥 Pobierz CSV", data=csv, file_name="posilki.csv", mime="text/csv")
    else:
        st.info("Brak posiłków. Dodaj coś w menu bocznym!")

elif page == "📈 Podsumowanie":
    st.subheader("📈 Podsumowanie dzienne")
    if st.session_state.meals:
        df = pd.DataFrame(st.session_state.meals)
        grouped = df.groupby("Data").sum(numeric_only=True)
        st.bar_chart(grouped[["Węglowodany", "Białko", "Tłuszcze"]])
    else:
        st.info("Brak danych do analizy.")

elif page == "📚 Porady":
    st.subheader("📚 Porady żywieniowe dla cukrzyków")
    tips = [
        "Jedz regularnie – 4-6 posiłków dziennie",
        "Kontroluj indeks glikemiczny spożywanych produktów",
        "Unikaj przetworzonych cukrów i słodyczy",
        "Zwiększ spożycie błonnika – warzywa, produkty pełnoziarniste",
        "Dbaj o nawodnienie – pij wodę zamiast słodzonych napojów",
        "Planuj posiłki z wyprzedzeniem",
        "Monitoruj poziom glukozy we krwi przed i po posiłkach",
        "Konsultuj dietę z dietetykiem lub lekarzem"
    ]
    for tip in tips:
        st.markdown(f"✅ {tip}")

st.markdown("""
    <hr>
    <p style='text-align: center; font-size: 0.8em;'>DiaPlan – wspomagaj swoje zdrowie poprzez świadome żywienie</p>
""", unsafe_allow_html=True)
