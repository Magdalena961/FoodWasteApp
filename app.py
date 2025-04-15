import streamlit as st
import pandas as pd
import datetime

st.set_page_config(page_title="FoodWasteApp", layout="wide")
st.title("🍽️ FoodWasteApp – Zarządzaj jedzeniem i ogranicz marnowanie żywności")
st.caption("Kontroluj produkty w lodówce, redukuj straty i planuj posiłki z głową")

# Inicjalizacja sesji
if "products" not in st.session_state:
    st.session_state.products = []

# Formularz dodawania produktu
with st.form("add_product"):
    st.subheader("Dodaj produkt do lodówki")
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
        file_name='produkty_w_lodowce.csv',
        mime='text/csv'
    )
else:
    st.info("Brak produktów w lodówce. Dodaj coś!")

# Pomysły na wykorzystanie produktów
st.subheader("🍽️ Propozycje wykorzystania produktów")
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

# Porady dotyczące niemarnowania żywności
st.subheader("📚 Porady przeciw marnowaniu żywności")
tips = [
    "Planuj zakupy z listą i nie kupuj na zapas",
    "Sprawdzaj daty ważności i zużywaj produkty na czas",
    "Przechowuj żywność w odpowiednich warunkach",
    "Wykorzystuj resztki do tworzenia nowych potraw",
    "Zamrażaj nadmiar jedzenia, zanim się zepsuje"
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
st.caption("FoodWasteApp – aplikacja do zarządzania jedzeniem – prototyp pracy dyplomowej")