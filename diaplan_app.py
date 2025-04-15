import streamlit as st
import pandas as pd
import datetime

st.set_page_config(page_title="DiaPlan", layout="wide")
st.title("🥗 DiaPlan – Automatyzacja diety w cukrzycy")
st.caption("Zarządzaj dietą i produktami, by lepiej kontrolować poziom cukru")

# Inicjalizacja sesji
if "products" not in st.session_state:
    st.session_state.products = []

# Formularz dodawania produktu
with st.form("add_product"):
    st.subheader("Dodaj produkt do lodówki")
    name = st.text_input("Nazwa produktu")
    quantity = st.number_input("Ilość (np. sztuk, opakowań)", min_value=1, value=1)
    expiry = st.date_input("Data ważności", min_value=datetime.date.today())
    glycemic = st.selectbox("Indeks glikemiczny (IG)", ["Niski", "Średni", "Wysoki"])
    submitted = st.form_submit_button("Dodaj")
    if submitted and name:
        st.session_state.products.append({
            "Nazwa": name,
            "Ilość": quantity,
            "Data ważności": expiry,
            "IG": glycemic
        })
        st.success(f"Dodano produkt: {name}")

# Możliwość usuwania produktów
st.subheader("🗑️ Usuń produkt")
if st.session_state.products:
    names = [f"{i+1}. {p['Nazwa']} ({p['Data ważności']})" for i, p in enumerate(st.session_state.products)]
    to_delete = st.selectbox("Wybierz produkt do usunięcia", options=["---"] + names)
    if to_delete != "---":
        index = names.index(to_delete)
        if st.button("Usuń produkt"):
            removed = st.session_state.products.pop(index)
            st.success(f"Usunięto: {removed['Nazwa']}")

# Wyświetlanie produktów
st.subheader("📋 Produkty w lodówce")
if st.session_state.products:
    df = pd.DataFrame(st.session_state.products)
    today = datetime.date.today()
    df["Status"] = df["Data ważności"].apply(
        lambda x: "⚠️ Dziś" if x == today else ("🕓 Wkrótce" if x <= today + datetime.timedelta(days=2) else "✅ OK")
    )
    st.dataframe(df.sort_values(by="Data ważności"))
    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Pobierz listę jako CSV",
        data=csv,
        file_name='produkty_dla_cukrzyka.csv',
        mime='text/csv'
    )
else:
    st.info("Brak produktów w lodówce. Dodaj coś!")

# Przepisy przyjazne dla cukrzyków
st.subheader("🍽️ Przepisy odpowiednie dla cukrzyków")
diabetic_recipes = {
    "jajko": "Omlet z warzywami niskowęglowodanowy",
    "brokuł": "Brokuły na parze z tofu",
    "łosoś": "Łosoś pieczony z warzywami",
    "cukinia": "Placki z cukinii bez mąki",
    "migdały": "Smoothie z mlekiem migdałowym",
    "awokado": "Sałatka z awokado i jajkiem",
    "pierś z kurczaka": "Grillowana pierś z kurczaka z kaszą gryczaną"
}

available = [p["Nazwa"].lower() for p in st.session_state.products]
found = [r for i, r in diabetic_recipes.items() if i in available]

if found:
    for f in found:
        st.markdown(f"- {f}")
else:
    st.info("Brak przepisów – dodaj więcej odpowiednich produktów!")

# Porady dietetyczne
st.subheader("📚 Porady dla osób z cukrzycą")
tips = [
    "Spożywaj produkty o niskim indeksie glikemicznym (IG).",
    "Unikaj napojów słodzonych i przetworzonych przekąsek.",
    "Jedz regularnie – nie pomijaj posiłków.",
    "Planuj posiłki z wyprzedzeniem, by uniknąć skoków cukru.",
    "Monitoruj poziom glukozy i dopasuj dietę do wyników."
]
for tip in tips:
    st.markdown(f"✅ {tip}")

# Statystyki
st.subheader("📊 Statystyki")
total = len(st.session_state.products)
today = datetime.date.today()
expiring_today = sum(1 for p in st.session_state.products if p["Data ważności"] == today)
expiring_soon = sum(1 for p in st.session_state.products if p["Data ważności"] <= today + datetime.timedelta(days=2))

st.metric("Łączna liczba produktów", total)
st.metric("Produkty wygasające dziś", expiring_today)
st.metric("Produkty wygasające w ciągu 2 dni", expiring_soon)

# Stopka
st.caption("DiaPlan – aplikacja dietetyczna dla osób z cukrzycą – prototyp pracy dyplomowej")
