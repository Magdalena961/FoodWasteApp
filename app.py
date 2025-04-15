import streamlit as st
import pandas as pd
import datetime
from streamlit_extras.colored_header import colored_header

st.set_page_config(page_title="FoodWasteApp", layout="wide")

# Nagłówek z hierarchią
st.markdown("""
    <h2 style='text-align: center; color: #2e7d32;'>FoodWasteApp</h2>
    <h4 style='text-align: center; color: #555;'>Ogranicz marnowanie żywności</h4>
    <p style='text-align: center; color: #888;'>Kontroluj produkty, planuj zakupy i zużycie, ogranicz straty</p>
    <br>
""", unsafe_allow_html=True)

# Inicjalizacja sesji
if "products" not in st.session_state:
    st.session_state.products = []

# Sekcja dodawania produktów
with st.sidebar:
    st.header("➕ Dodaj produkt")
    name = st.text_input("Nazwa produktu")
    quantity = st.number_input("Ilość", min_value=1, value=1)
    expiry = st.date_input("Data ważności", min_value=datetime.date.today())
    if st.button("Dodaj"):
        if name:
            st.session_state.products.append({
                "Nazwa": name,
                "Ilość": quantity,
                "Data ważności": expiry
            })
            st.success(f"Dodano: {name}")

# Zakładki główne
page = st.selectbox("Wybierz sekcję", ["📋 Produkty", "📚 Porady", "📊 Statystyki"])

if page == "📋 Produkty":
    st.header("📋 Produkty w lodówce")
    if st.session_state.products:
        df = pd.DataFrame(st.session_state.products)
        today = datetime.date.today()
        df["Status"] = df["Data ważności"].apply(
            lambda x: "⚠️ Dziś" if x == today else ("🕓 Wkrótce" if x <= today + datetime.timedelta(days=2) else "✅ OK")
        )
        st.dataframe(df.sort_values(by="Data ważności"), use_container_width=True)

        st.markdown("---")
        names = [f"{i+1}. {p['Nazwa']} ({p['Data ważności']})" for i, p in enumerate(st.session_state.products)]
        to_delete = st.selectbox("Usuń produkt", options=["---"] + names)
        if to_delete != "---":
            index = names.index(to_delete)
            if st.button("🗑️ Usuń"):
                removed = st.session_state.products.pop(index)
                st.success(f"Usunięto: {removed['Nazwa']}")

        csv = df.to_csv(index=False).encode("utf-8")
        st.download_button("📥 Pobierz CSV", data=csv, file_name="produkty.csv", mime="text/csv")
    else:
        st.info("Brak produktów. Dodaj coś w menu bocznym!")

elif page == "📚 Porady":
    st.header("📚 Pomysły i wskazówki")

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
        "Nie kupuj na zapas bez potrzeby"
    ]
    for tip in tips:
        st.markdown(f"✅ {tip}")

elif page == "📊 Statystyki":
    st.header("📊 Statystyki")
    total = len(st.session_state.products)
    today = datetime.date.today()
    expiring_today = sum(1 for p in st.session_state.products if p["Data ważności"] == today)
    expiring_soon = sum(1 for p in st.session_state.products if today < p["Data ważności"] <= today + datetime.timedelta(days=2))

    st.metric("📦 Liczba produktów", total)
    st.metric("⏳ Wygasające dziś", expiring_today)
    st.metric("⚠️ Wkrótce wygasną", expiring_soon)

st.markdown("""
    <hr>
    <p style='text-align: center; font-size: 0.8em;'>FoodWasteApp – prototyp aplikacji dyplomowej do walki z marnowaniem żywności</p>
""", unsafe_allow_html=True)
