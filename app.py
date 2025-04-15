import streamlit as st
import pandas as pd
import datetime
from streamlit.components.v1 import html

st.set_page_config(page_title="FoodWasteApp", layout="wide")

# Stylizacja CSS – styl boho i elegancki
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
        .desc-text {
            text-align: center;
            color: #a1887f;
            font-size: 0.9em;
        }
    </style>
""", unsafe_allow_html=True)

# Nagłówek
st.markdown("""
    <div class='main-header'>FoodWasteApp</div>
    <div class='sub-header'>Ogranicz marnowanie żywności</div>
    <div class='desc-text'>Zarządzaj produktami spożywczymi, planuj zakupy i zmniejsz straty</div>
    <br>
""", unsafe_allow_html=True)

# Inicjalizacja sesji
if "products" not in st.session_state:
    st.session_state.products = []

# Sidebar: dodawanie produktów
with st.sidebar:
    st.header("➕ Dodaj produkt")
    name = st.text_input("Nazwa produktu")
    quantity = st.number_input("Ilość", min_value=0.0, value=1.0, step=0.1)
    unit = st.selectbox("Jednostka", ["szt.", "g", "kg", "ml", "l"])
    expiry = st.date_input("Data ważności", min_value=datetime.date.today())
    if st.button("Dodaj"):
        if name:
            st.session_state.products.append({
                "Nazwa": name,
                "Ilość": quantity,
                "Jednostka": unit,
                "Data ważności": expiry
            })
            st.success(f"Dodano: {name}")

# Zakładki
page = st.selectbox("Wybierz sekcję", ["📋 Produkty", "📚 Porady", "📊 Statystyki", "🍽️ Przepisy"])

# Sekcja produktów
if page == "📋 Produkty":
    st.subheader("📋 Twoje produkty")
    if st.session_state.products:
        df = pd.DataFrame(st.session_state.products)
        today = datetime.date.today()
        df["Status"] = df["Data ważności"].apply(
            lambda x: "⚠️ Dziś" if x == today else ("🕓 Wkrótce" if x <= today + datetime.timedelta(days=2) else "✅ OK")
        )
        st.dataframe(df.sort_values(by="Data ważności"), use_container_width=True)

        st.markdown("---")
        names = [f"{idx + 1}. {p['Nazwa']} ({p['Data ważności']})" for idx, p in enumerate(st.session_state.products)]
        to_delete = st.selectbox("Usuń produkt", options=["---"] + names)
        if to_delete != "---":
            index = int(to_delete.split(".")[0]) - 1
            if st.button("🗑️ Usuń"):
                removed = st.session_state.products.pop(index)
                st.success(f"Usunięto: {removed['Nazwa']}")

        csv = df.to_csv(index=False).encode("utf-8")
        st.download_button("📥 Pobierz CSV", data=csv, file_name="produkty.csv", mime="text/csv")
    else:
        st.info("Brak produktów. Dodaj coś w menu bocznym!")

# Sekcja porad
elif page == "📚 Porady":
    st.subheader("📚 Pomysły i wskazówki")

    ideas = {
        "mleko": "Zrób koktajl lub naleśniki",
        "jajka": "Ugotuj jajka lub zrób jajecznicę",
        "chleb": "Zrób tosty, grzanki lub zapiekanki",
        "warzywa": "Ugotuj zupę lub danie jednogarnkowe",
        "ser": "Użyj do zapiekanek lub pizzy",
        "banany": "Zrób smoothie lub ciasto bananowe"
    }
    available = [p["Nazwa"].lower() for p in st.session_state.products]
    found = [idea for k, idea in ideas.items() if k in available]

    if found:
        st.markdown("### Co możesz zrobić z posiadanymi produktami:")
        for f in found:
            st.markdown(f"- {f}")
    else:
        st.info("Dodaj produkty, aby zobaczyć pomysły")

    st.markdown("### Ogólne porady")
    tips = [
        "Kupuj z listą zakupów",
        "Sprawdzaj daty ważności",
        "Zamrażaj jedzenie",
        "Wykorzystuj resztki",
        "Nie kupuj na zapas bez potrzeby",
        "Planuj posiłki z wyprzedzeniem",
        "Przechowuj żywność w odpowiednich warunkach",
        "Oznacz produkty etykietami z datą zakupu",
        "Przygotowuj dania z resztek jedzenia",
        "Przekazuj nadmiar jedzenia potrzebującym",
        "Regularnie przeglądaj zawartość lodówki",
        "Dziel się jedzeniem z sąsiadami lub znajomymi"
    ]
    for tip in tips:
        st.markdown(f"✅ {tip}")

# Sekcja statystyk
elif page == "📊 Statystyki":
    st.subheader("📊 Statystyki")
    total = len(st.session_state.products)
    today = datetime.date.today()
    expiring_today = sum(1 for p in st.session_state.products if p["Data ważności"] == today)
    expiring_soon = sum(1 for p in st.session_state.products if today < p["Data ważności"] <= today + datetime.timedelta(days=2))

    col1, col2, col3 = st.columns(3)
    col1.metric("📦 Liczba produktów", total)
    col2.metric("⏳ Wygasające dziś", expiring_today)
    col3.metric("⚠️ Wkrótce wygasną", expiring_soon)

# Sekcja przepisów
elif page == "🍽️ Przepisy":
    st.subheader("🍽️ Propozycje przepisów na podstawie Twoich produktów")
    available = [p["Nazwa"].lower() for p in st.session_state.products]
    recipes = {
        "banany": ["Chlebek bananowy", "https://source.unsplash.com/600x400/?banana,bread"],
        "jajka": ["Omlet z warzywami", "https://source.unsplash.com/600x400/?omelette"],
        "ser": ["Zapiekanka z serem", "https://source.unsplash.com/600x400/?cheese,casserole"],
        "chleb": ["Grzanki czosnkowe", "https://source.unsplash.com/600x400/?garlic,bread"],
        "mleko": ["Naleśniki mleczne", "https://source.unsplash.com/600x400/?pancakes"],
        "ziemniaki": ["Frytki pieczone", "https://source.unsplash.com/600x400/?fries"],
        "pomidor": ["Zupa pomidorowa", "https://source.unsplash.com/600x400/?tomato,soup"],
        "papryka": ["Faszerowana papryka", "https://source.unsplash.com/600x400/?stuffed,pepper"],
        "ryż": ["Ryż z warzywami", "https://source.unsplash.com/600x400/?rice,vegetables"],
        "makaron": ["Makaron z sosem", "https://source.unsplash.com/600x400/?pasta"],
        "kurczak": ["Kurczak pieczony", "https://source.unsplash.com/600x400/?roast,chicken"]
    }
    matched = False
    for name, (desc, img_url) in recipes.items():
        if name in available:
            st.image(img_url, use_column_width=True)
            st.markdown(f"### 🍽️ {desc}")
            matched = True

    if not matched:
        st.info("Dodaj produkty, aby zobaczyć pasujące przepisy")

st.markdown("""
    <hr>
    <p style='text-align: center; font-size: 0.8em;'>FoodWasteApp – prototyp aplikacji dyplomowej do walki z marnowaniem żywności</p>
""", unsafe_allow_html=True)
