import streamlit as st
import pandas as pd
import datetime
import requests

st.set_page_config(page_title="FoodWasteApp", layout="wide")

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
    <div class='desc-text'>Zarządzaj produktami, planuj zakupy i redukuj straty</div>
    <br>
""", unsafe_allow_html=True)

if "products" not in st.session_state:
    st.session_state.products = []

# Usuwanie przeterminowanych produktów
today = datetime.date.today()
st.session_state.products = [
    p for p in st.session_state.products if p["Data ważności"] >= today
]

# Sidebar: dodawanie produktów
with st.sidebar:
    st.header("➕ Dodaj produkt")
    name = st.text_input("Nazwa produktu")
    quantity = st.number_input("Ilość", min_value=0.0, value=1.0, step=0.1)
    unit = st.selectbox("Jednostka", ["szt.", "g", "kg", "ml", "l"])
    expiry = st.date_input("Data ważności", min_value=datetime.date.today())
    if st.button("Dodaj") and name:
        st.session_state.products.append({
            "Nazwa": name,
            "Ilość": quantity,
            "Jednostka": unit,
            "Data ważności": expiry
        })
        st.success(f"Dodano: {name}")

# Zakładki
page = st.selectbox("Wybierz sekcję", ["📋 Produkty", "📚 Porady", "📊 Statystyki", "🍽️ Przepisy", "📈 Dane Eurostat"])

if page == "📋 Produkty":
    st.subheader("📋 Twoje produkty")
    
    if st.session_state.products:
        df = pd.DataFrame(st.session_state.products)
        
        # Określanie statusu produktów na podstawie daty ważności
        df["Status"] = df["Data ważności"].apply(
            lambda x: "⚠️ Dziś" if x == today else 
                      ("🖓 Wkrótce" if x <= today + datetime.timedelta(days=2) else "✅ OK")
        )
        st.dataframe(df)

        # Alert dla produktów, które mają wygasnąć wkrótce
        expiring_soon = [p for p in st.session_state.products if p["Data ważności"] <= today + datetime.timedelta(days=2) and p["Data ważności"] > today]
        if expiring_soon:
            st.warning("Uwaga! Następujące produkty wygasną wkrótce:")
            for product in expiring_soon:
                st.markdown(f"⚠️ {product['Nazwa']} - ważność: {product['Data ważności']}")

        # Alert dla produktów, które wygasły
        expired = [p for p in st.session_state.products if p["Data ważności"] < today]
        if expired:
            st.error("UWAGA! Poniższe produkty są przeterminowane:")
            for product in expired:
                st.markdown(f"❌ {product['Nazwa']} - ważność: {product['Data ważności']}")

        # Usuwanie produktów
        st.markdown("---")
        names = [f"{p['Nazwa']} ({p['Data ważności']})" for p in st.session_state.products]
        to_delete = st.selectbox("Usuń produkt", options=["---"] + names)
        if to_delete != "---":
            index = next((i for i, p in enumerate(st.session_state.products) if f"{p['Nazwa']} ({p['Data ważności']})" == to_delete), None)
            if st.button("🗑️ Usuń") and index is not None:
                removed = st.session_state.products.pop(index)
                st.success(f"Usunięto: {removed['Nazwa']}")

        # Możliwość czyszczenia listy
        if st.button("♻️ Wyczyść listę"):
            st.session_state.products = []
            st.success("Wyczyszczono wszystkie produkty.")

        # Pobranie pliku CSV
        csv = pd.DataFrame(st.session_state.products).to_csv(index=False).encode("utf-8")
        st.download_button("📅 Pobierz CSV", data=csv, file_name="produkty.csv", mime="text/csv")
    else:
        st.info("Brak produktów. Dodaj coś w menu bocznym!")

elif page == "📚 Porady":
    st.subheader("📚 Wskazówki i inspiracje")

    tips = [
        "Kupuj z listą zakupów",
        "Sprawdzaj daty ważności",
        "Zamrażaj jedzenie",
        "Wykorzystuj resztki – np. do zup, zapiekanek, sałatek",
        "Nie kupuj na zapas – kupuj tylko to, czego naprawdę potrzebujesz",
        "Planuj tygodniowe menu",
        "Oznacz produkty datą zakupu lub otwarcia",
        "Przechowuj żywność poprawnie (np. w odpowiednich strefach lodówki)",
        "Przechowuj warzywa i owoce osobno",
        "Używaj przezroczystych pojemników – widzisz co masz",
        "Zrób dzień resztek raz w tygodniu",
        "Udostępniaj nadmiar przez aplikacje typu TooGoodToGo",
        "Regularnie przeglądaj zawartość lodówki",
        "Stosuj zasadę FIFO (pierwsze weszło, pierwsze wychodzi)"
    ]
    for tip in tips:
        st.markdown(f"✅ {tip}")

elif page == "📊 Statystyki":
    st.subheader("📊 Statystyki")
    total = len(st.session_state.products)
    expiring_today = sum(1 for p in st.session_state.products if p["Data ważności"] == today)
    expiring_soon = sum(1 for p in st.session_state.products if today < p["Data ważności"] <= today + datetime.timedelta(days=2))

    col1, col2, col3 = st.columns(3)
    col1.metric("📦 Produkty", total)
    col2.metric("⏳ Dziś wygasa", expiring_today)
    col3.metric("⚠️ Wkrótce wygasa", expiring_soon)

elif page == "🍽️ Przepisy":
    st.subheader("🍽️ Propozycje przepisów")

    # Przepisy
    recipes = {
        "banany": ("Chlebek bananowy", "https://source.unsplash.com/600x400/?banana,bread", "Banany, mąka, jajka", "100g bananów, 150g mąki, 2 jajka"),
        "jajka": ("Omlet z warzywami", "https://source.unsplash.com/600x400/?omelette", "Jajka, pomidory, cebula, papryka", "3 jajka, 1 pomidor, 1 cebula, 1 papryka"),
        "ser": ("Zapiekanka z serem", "https://source.unsplash.com/600x400/?cheese,casserole", "Ser, ziemniaki, cebula", "200g sera, 500g ziemniaków, 1 cebula"),
        "chleb": ("Grzanki czosnkowe", "https://source.unsplash.com/600x400/?garlic,bread", "Chleb, czosnek, masło", "4 kromki chleba, 2 ząbki czosnku, 50g masła"),
        "mleko": ("Naleśniki mleczne", "https://source.unsplash.com/600x400/?pancakes", "Mleko, mąka, jajka", "200ml mleka, 150g mąki, 1 jajko"),
        "ziemniaki": ("Frytki pieczone", "https://source.unsplash.com/600x400/?fries", "Ziemniaki, oliwa, przyprawy", "4 ziemniaki, 2 łyżki oliwy, sól, pieprz"),
        "pomidor": ("Zupa pomidorowa", "https://source.unsplash.com/600x400/?tomato,soup", "Pomidory, cebula, czosnek", "1 kg pomidorów, 1 cebula, 2 ząbki czosnku"),
        "papryka": ("Faszerowana papryka", "https://source.unsplash.com/600x400/?stuffed,pepper", "Papryka, mięso mielone, ryż", "4 papryki, 300g mięsa mielonego, 100g ryżu"),
        "ryż": ("Ryż z warzywami", "https://source.unsplash.com/600x400/?rice,vegetables", "Ryż, brokuł, marchewka", "200g ryżu, 1 brokuł, 2 marchewki")
    }

    # Wybór składników
    selected_ingredients = st.multiselect("Wybierz składniki", options=[product["Nazwa"] for product in st.session_state.products])

    # Szukanie przepisu
    matching_recipes = {k: v for k, v in recipes.items() if any(ingredient in selected_ingredients for ingredient in v[2].split(", "))}

    if matching_recipes:
        for name, recipe in matching_recipes.items():
            st.subheader(f"🍽️ {recipe[0]}")
            st.image(recipe[1], caption=recipe[0])
            st.write(f"Składniki: {recipe[2]}")
            st.write(f"Gramatura: {recipe[3]}")
            st.write("Wykonanie: Wymieszaj składniki, upiecz/grilluj na złoto, podawaj.")
    else:
        st.info("Nie znaleziono przepisu na podstawie wybranych składników.")