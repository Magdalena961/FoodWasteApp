import streamlit as st
import pandas as pd
import datetime
import pytesseract
from PIL import Image
import plotly.express as px
import io

# Ustawienia aplikacji
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

# Sprawdzenie, czy produkty są zapisane w sesji
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
page = st.selectbox("Wybierz sekcję", ["📋 Produkty", "📚 Porady", "📊 Statystyki", "🍽️ Przepisy", "📈 Dane Eurostat", "📷 Skanowanie Paragonu"])

if page == "📋 Produkty":
    st.subheader("📋 Twoje produkty")
    if st.session_state.products:
        df = pd.DataFrame(st.session_state.products)
        df["Status"] = df["Data ważności"].apply(lambda x: "⚠️ Dziś" if x == today else ("🖓 Wkrótce" if x <= today + datetime.timedelta(days=2) else "✅ OK"))
        st.dataframe(df)

        st.markdown("---")
        names = [f"{p['Nazwa']} ({p['Data ważności']})" for p in st.session_state.products]
        to_delete = st.selectbox("Usuń produkt", options=["---"] + names)
        if to_delete != "---":
            index = next((i for i, p in enumerate(st.session_state.products) if f"{p['Nazwa']} ({p['Data ważności']})" == to_delete), None)
            if st.button("🗑️ Usuń") and index is not None:
                removed = st.session_state.products.pop(index)
                st.success(f"Usunięto: {removed['Nazwa']}")

        if st.button("♻️ Wyczyść listę"):
            st.session_state.products = []
            st.success("Wyczyszczono wszystkie produkty.")

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

    recipes = {
        "banany": ("Chlebek bananowy", "https://source.unsplash.com/600x400/?banana,bread"),
        "jajka": ("Omlet z warzywami", "https://source.unsplash.com/600x400/?omelette"),
        "ser": ("Zapiekanka z serem", "https://source.unsplash.com/600x400/?cheese,casserole"),
        "chleb": ("Grzanki czosnkowe", "https://source.unsplash.com/600x400/?garlic,bread"),
        "mleko": ("Naleśniki mleczne", "https://source.unsplash.com/600x400/?pancakes"),
        "ziemniaki": ("Frytki pieczone", "https://source.unsplash.com/600x400/?fries"),
        "pomidor": ("Zupa pomidorowa", "https://source.unsplash.com/600x400/?tomato,soup"),
        "papryka": ("Faszerowana papryka", "https://source.unsplash.com/600x400/?stuffed,pepper"),
        "ryż": ("Ryż z warzywami", "https://source.unsplash.com/600x400/?rice,vegetables"),
        "makaron": ("Makaron z sosem", "https://source.unsplash.com/600x400/?pasta"),
        "kurczak": ("Kurczak pieczony", "https://source.unsplash.com/600x400/?roast,chicken")
    }

    available = [p["Nazwa"].lower() for p in st.session_state.products]
    matched = False
    for key, (desc, img_url) in recipes.items():
        if key in available:
            st.image(img_url, use_container_width=True)
            st.markdown(f"### 🍽️ {desc}")
            matched = True
    if not matched:
        st.info("Dodaj produkty, aby zobaczyć pasujące przepisy")

elif page == "📈 Dane Eurostat":
    st.subheader("📈 Wskazówki na podstawie danych Eurostat")
    
    # Dodanie więcej szczegółowych danych
    st.markdown("""
    ## Wskaźniki marnotrawstwa żywności w Unii Europejskiej:
    
    - **88 milionów ton żywności** rocznie marnuje się w UE.
    - Średnia wielkość marnotrawstwa w każdym gospodarstwie domowym w UE to około **173 kg** na osobę rocznie.
    - **Owoce, warzywa, pieczywo** oraz **produkty mleczne** to najczęściej marnowane produkty.
    
    ## Dlaczego marnujemy żywność?
    - **Spożycie domowe**: Produkty często marnują się w wyniku przypadkowego nadmiaru zakupów, złego przechowywania, przekroczonej daty ważności i braku planowania posiłków.
    - **Sektor gastronomiczny**: W restauracjach żywność marnuje się na skutek nadmiaru przygotowanych posiłków oraz złych praktyk porcjowania.

    ## Wartość marnotrawstwa w gospodarstwach domowych:
    - W UE każde gospodarstwo domowe marnuje średnio **700 EUR rocznie** na jedzenie, które trafia do kosza.

    ## Sposoby ograniczenia marnotrawstwa:
    - **Planowanie posiłków**: Zrób listę zakupów i planuj posiłki na tydzień. W ten sposób unikniesz nadmiaru produktów.
    - **Przechowywanie żywności**: Właściwe przechowywanie produktów w odpowiednich warunkach pomoże w ich dłuższym przechowywaniu i zmniejszeniu marnotrawstwa.
    - **Wykorzystanie resztek**: Z resztek jedzenia możesz zrobić pyszne dania, np. zupy, zapiekanki, sałatki.

    ## Przykłady krajów aktywnie zmniejszających marnotrawstwo:
    - **Holandia, Szwecja i Niemcy**: Stosują programy edukacyjne oraz inicjatywy promujące mniejsze marnotrawstwo, w tym darowizny żywnościowe.
    
    ## Jakie są skutki marnotrawstwa?
    - **Ekologiczne**: Marnowanie żywności oznacza marnowanie zasobów, takich jak woda, energia i grunt. Marnowanie jedzenia generuje również ogromne emisje gazów cieplarnianych.
    - **Ekonomiczne**: Wyrzucanie jedzenia jest kosztowne – nie tylko dla konsumentów, ale także dla całej gospodarki.

    ### Zastosowanie rozwiązań:
    - Zmiana postaw konsumentów oraz działania na poziomie społecznym mogą przyczynić się do znacznego zmniejszenia marnotrawstwa żywności.
    """)
    
    st.markdown("---")
    st.markdown("**Dodatkowe źródła**:")
    st.markdown("[Eurostat - Marnowanie żywności w UE](https://ec.europa.eu/eurostat/statistics-explained/index.php?title=Food_waste_statistics)")

elif page == "📷 Skanowanie Paragonu":
    st.subheader("📷 Skanowanie paragonu lub listy zakupów")
    uploaded_file = st.file_uploader("Wybierz obrazek", type=["png", "jpg", "jpeg"])
    
    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        st.image(image, caption="Skanowany obrazek", use_column_width=True)

        # Przetwarzanie obrazu na tekst
        text = pytesseract.image_to_string(image)
        st.text_area("Odczytany tekst", text, height=200)

        # Przekształcanie odczytanych produktów na listę
        if st.button("Dodaj do listy produktów"):
            for line in text.splitlines():
                if line:  # Dodajemy produkty tylko jeśli linia nie jest pusta
                    st.session_state.products.append({
                        "Nazwa": line.strip(),
                        "Ilość": 1.0,  # Możesz to zmienić na automatyczne wykrywanie ilości
                        "Jednostka": "szt.",
                        "Data ważności": today  # Możesz zmienić, aby przypisać datę ważności ręcznie
                    })
            st.success("Produkty zostały dodane do listy!")
