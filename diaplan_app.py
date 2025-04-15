import streamlit as st
import datetime

st.set_page_config(page_title="DiaPlan", layout="wide")

# Stylizacja
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
            color: #386641;
            font-size: 1.2em;
            font-style: italic;
        }
        .desc-text {
            text-align: center;
            color: #6c757d;
            font-size: 0.9em;
        }
    </style>
""", unsafe_allow_html=True)

# Nagłówek
st.markdown("""
    <div class='main-header'>DiaPlan</div>
    <div class='sub-header'>Spersonalizowany plan diety dla cukrzyków</div>
    <div class='desc-text'>Śledź produkty, planuj posiłki i utrzymuj zdrową dietę</div>
    <br>
""", unsafe_allow_html=True)

# Inicjalizacja
if "products" not in st.session_state:
    st.session_state.products = []

# Sidebar
with st.sidebar:
    st.header("➕ Dodaj produkt")
    name = st.text_input("Nazwa produktu")
    quantity = st.number_input("Ilość", min_value=1, value=1)
    expiry = st.date_input("Data ważności", min_value=datetime.date.today())
    gly_index = st.selectbox("Indeks glikemiczny", ["Niski", "Średni", "Wysoki"])

    if st.button("Dodaj"):
        if name:
            st.session_state.products.append({
                "Nazwa": name,
                "Ilość": quantity,
                "Data ważności": expiry,
                "IG": gly_index
            })
            st.success(f"Dodano: {name}")

# Sekcja
page = st.selectbox("Wybierz sekcję", ["📋 Produkty", "🍱 Propozycje", "📚 Porady"])

if page == "📋 Produkty":
    st.subheader("📋 Produkty w diecie")
    if st.session_state.products:
        today = datetime.date.today()
        sorted_list = sorted(st.session_state.products, key=lambda x: x["Data ważności"])

        for i, p in enumerate(sorted_list, start=1):
            status = "✅ OK"
            if p["Data ważności"] == today:
                status = "⚠️ Dziś"
            elif p["Data ważności"] <= today + datetime.timedelta(days=2):
                status = "🕓 Wkrótce"

            st.markdown(f"{i}. **{p['Nazwa']}** – ilość: {p['Ilość']}, IG: {p['IG']}, ważność: {p['Data ważności']} – {status}")

        options = [f"{i+1}. {p['Nazwa']} ({p['Data ważności']})" for i, p in enumerate(st.session_state.products)]
        to_delete = st.selectbox("Usuń produkt", ["---"] + options)
        if to_delete != "---":
            index = int(to_delete.split('.')[0]) - 1
            if st.button("🗑️ Usuń"):
                removed = st.session_state.products.pop(index)
                st.success(f"Usunięto: {removed['Nazwa']}")
    else:
        st.info("Brak produktów. Dodaj coś w menu bocznym!")

elif page == "🍱 Propozycje":
    st.subheader("🍱 Pomysły na posiłki dla cukrzyków")
    ig_low = [p for p in st.session_state.products if p["IG"] == "Niski"]
    if ig_low:
        st.markdown("### Propozycje dań z produktów o niskim IG:")
        for p in ig_low:
            st.markdown(f"- Sałatka z {p['Nazwa']}, gotowane warzywa lub zupa krem")
    else:
        st.info("Dodaj produkty z niskim IG, aby zobaczyć propozycje")

elif page == "📚 Porady":
    st.subheader("📚 Porady dla diabetyków")
    tips = [
        "Jedz regularnie co 3–4 godziny",
        "Unikaj produktów o wysokim IG (np. biały chleb, słodycze)",
        "Spożywaj dużo błonnika (warzywa, pełnoziarniste produkty)",
        "Pij wodę zamiast słodzonych napojów",
        "Unikaj przetworzonych produktów",
        "Czytaj etykiety i sprawdzaj zawartość cukru"
    ]
    for tip in tips:
        st.markdown(f"✅ {tip}")

st.markdown("""
    <hr>
    <p style='text-align: center; font-size: 0.8em;'>DiaPlan – spersonalizowana aplikacja dietetyczna dla osób z cukrzycą</p>
""", unsafe_allow_html=True)
""", unsafe_allow_html=True)

# Inicjalizacja
if "products" not in st.session_state:
    st.session_state.products = []

# Sidebar
with st.sidebar:
    st.header("➕ Dodaj produkt")
    name = st.text_input("Nazwa produktu")
    quantity = st.number_input("Ilość", min_value=1, value=1)
    expiry = st.date_input("Data ważności", min_value=datetime.date.today())
    gly_index = st.selectbox("Indeks glikemiczny", ["Niski", "Średni", "Wysoki"])

    if st.button("Dodaj"):
        if name:
            st.session_state.products.append({
                "Nazwa": name,
                "Ilość": quantity,
                "Data ważności": expiry,
                "IG": gly_index
            })
            st.success(f"Dodano: {name}")

# Sekcja
page = st.selectbox("Wybierz sekcję", ["📋 Produkty", "🍱 Propozycje", "📚 Porady"])

if page == "📋 Produkty":
    st.subheader("📋 Produkty w diecie")
    if st.session_state.products:
        today = datetime.date.today()
        sorted_list = sorted(st.session_state.products, key=lambda x: x["Data ważności"])

        for i, p in enumerate(sorted_list, start=1):
            status = "✅ OK"
            if p["Data ważności"] == today:
                status = "⚠️ Dziś"
            elif p["Data ważności"] <= today + datetime.timedelta(days=2):
                status = "🕓 Wkrótce"

            st.markdown(f"{i}. **{p['Nazwa']}** – ilość: {p['Ilość']}, IG: {p['IG']}, ważność: {p['Data ważności']} – {status}")

        options = [f"{i+1}. {p['Nazwa']} ({p['Data ważności']})" for i, p in enumerate(st.session_state.products)]
        to_delete = st.selectbox("Usuń produkt", ["---"] + options)
        if to_delete != "---":
            index = int(to_delete.split('.')[0]) - 1
            if st.button("🗑️ Usuń"):
                removed = st.session_state.products.pop(index)
                st.success(f"Usunięto: {removed['Nazwa']}")
    else:
        st.info("Brak produktów. Dodaj coś w menu bocznym!")

elif page == "🍱 Propozycje":
    st.subheader("🍱 Pomysły na posiłki dla cukrzyków")
    ig_low = [p for p in st.session_state.products if p["IG"] == "Niski"]
    if ig_low:
        st.markdown("### Propozycje dań z produktów o niskim IG:")
        for p in ig_low:
            st.markdown(f"- Sałatka z {p['Nazwa']}, gotowane warzywa lub zupa krem")
    else:
        st.info("Dodaj produkty z niskim IG, aby zobaczyć propozycje")

elif page == "📚 Porady":
    st.subheader("📚 Porady dla diabetyków")
    tips = [
        "Jedz regularnie co 3–4 godziny",
        "Unikaj produktów o wysokim IG (np. biały chleb, słodycze)",
        "Spożywaj dużo błonnika (warzywa, pełnoziarniste produkty)",
        "Pij wodę zamiast słodzonych napojów",
        "Unikaj przetworzonych produktów",
        "Czytaj etykiety i sprawdzaj zawartość cukru"
    ]
    for tip in tips:
        st.markdown(f"✅ {tip}")

st.markdown("""
    <hr>
    <p style='text-align: center; font-size: 0.8em;'>DiaPlan – spersonalizowana aplikacja dietetyczna dla osób z cukrzycą</p>
""", unsafe_allow_html=True)
