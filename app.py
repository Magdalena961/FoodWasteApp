import streamlit as st
import pandas as pd
import datetime
from streamlit_extras.colored_header import colored_header

st.set_page_config(page_title="FoodWasteApp", layout="wide")

# Nagłówek z hierarchią
st.markdown("""
    <h2 style='text-align: center; color: #2e7d32;'>FoodWasteApp</h2>
    <h4 style='text-align: center; color: #555;'>Zarządzaj jedzeniem</h4>
    <p style='text-align: center; color: #888;'>Kontroluj produkty, ogranicz marnowanie i planuj sprytnie</p>
    <br>
""", unsafe_allow_html=True)

# Inicjalizacja sesji
if "products" not in st.session_state:
    st.session_state.products = []

# Sekcja dodawania produktów
tabs = st.tabs(["➕ Dodaj produkt", "📋 Produkty", "📚 Porady", "📊 Statystyki"])

with tabs[0]:
    with st.form("add_product"):
        colored_header(label="Dodaj produkt do lodówki", description="Wprowadź nazwę, ilość i datę ważności.", color_name="green-70")
        name = st.text_input("Nazwa produktu")
        quantity = st.number_input("Ilość (np. sztuk, opakowań)", min_value=1, value=1)
        expiry = st.date_input("Data ważności", min_value=datetime.date.today())
        submitted = st.form_submit_button("Dodaj")
        if submitted and name:
            st.session_state.products.append({
                "Nazwa": name,
                "Ilość": quantity,
                "Data ważności": expiry
            })
            st.success(f"✅ Dodano produkt: {name}")

# Zakładka - Produkty
with tabs[1]:
    colored_header(label="Twoje produkty", description="Zarządzaj zawartością lodówki i usuwaj to, czego nie potrzebujesz.", color_name="blue-70")

    if st.session_state.products:
        df = pd.DataFrame(st.session_state.products)
        today = datetime.date.today()
        df["Status"] = df["Data ważności"].apply(
            lambda x: "⚠️ Dziś" if x == today else ("🕓 Wkrótce" if x <= today + datetime.timedelta(days=2) else "✅ OK")
        )
        st.dataframe(df.sort_values(by="Data ważności"), use_container_width=True)

        # Usuwanie produktów
        st.divider()
        st.markdown("### Usuń produkt")
        names = [f"{i+1}. {p['Nazwa']} ({p['Data ważności']})" for i, p in enumerate(st.session_state.products)]
        to_delete = st.selectbox("Wybierz produkt do usunięcia", options=["---"] + names)
        if to_delete != "---":
            index = names.index(to_delete)
            if st.button("🗑️ Usuń produkt"):
                removed = st.session_state.products.pop(index)
                st.success(f"🗑️ Usunięto: {removed['Nazwa']}")

        # Pobieranie CSV
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Pobierz listę jako CSV",
            data=csv,
            file_name='produkty_w_lodowce.csv',
            mime='text/csv'
        )
    else:
        st.info("Brak produktów w lodówce. Dodaj coś!")

# Zakładka - Porady i pomysły
with tabs[2]:
    colored_header(label="Pomysły i porady", description="Wykorzystaj produkty zanim się zmarnują", color_name="orange-70")

    ideas = {
        "mleko": "Zrób naleśniki lub koktajl owocowy",
        "jajka": "Ugotuj jajka na twardo lub zrób omlet",
        "chleb": "Zrób grzanki lub zapiekanki",
        "warzywa": "Przygotuj zupę krem lub warzywne curry",
        "ser": "Wykorzystaj do zapiekanek lub kanapek",
        "banany": "Zrób smoothie lub chlebek bananowy"
    }

    available = [p["Nazwa"].lower() for p in st.session_state.products]
    found = [idea for k, idea in ideas.items() if k in available]

    if found:
        for f in found:
            st.markdown(f"- {f}")
    else:
        st.info("Brak sugestii – dodaj więcej produktów!")

    st.markdown("---")
    st.markdown("### Porady przeciw marnowaniu żywności")
    tips = [
        "Planuj zakupy z listą i nie kupuj na zapas",
        "Sprawdzaj daty ważności i zużywaj produkty na czas",
        "Przechowuj żywność w odpowiednich warunkach",
        "Wykorzystuj resztki do tworzenia nowych potraw",
        "Zamrażaj nadmiar jedzenia, zanim się zepsuje"
    ]
    for tip in tips:
        st.markdown(f"✅ {tip}")

# Zakładka - Statystyki
with tabs[3]:
    colored_header(label="Statystyki", description="Monitoruj ile produktów posiadasz i co się kończy", color_name="violet-70")
    total = len(st.session_state.products)
    today = datetime.date.today()
    expiring_today = sum(1 for p in st.session_state.products if p["Data ważności"] == today)
    expiring_soon = sum(1 for p in st.session_state.products if today < p["Data ważności"] <= today + datetime.timedelta(days=2))

    st.metric("📦 Łączna liczba produktów", total)
    st.metric("⏳ Wygasające dziś", expiring_today)
    st.metric("⚠️ Wygasające w 2 dni", expiring_soon)

# Stopka
st.markdown("""
    <hr>
    <p style='text-align: center; font-size: 0.8em;'>FoodWasteApp – aplikacja do zarządzania jedzeniem – prototyp pracy dyplomowej</p>
""", unsafe_allow_html=True)
