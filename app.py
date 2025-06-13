import streamlit as st
import pandas as pd
import datetime
import pytesseract
from PIL import Image
import plotly.express as px
import io
import random
import folium
from streamlit_folium import folium_static

# Ustawienia aplikacji
st.set_page_config(page_title="FoodWasteApp+", layout="wide")

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
    <div class='main-header'>FoodWasteApp+</div>
    <div class='sub-header'>Ogranicz marnowanie żywności</div>
    <div class='desc-text'>Zarządzaj produktami, planuj zakupy i redukuj straty z głową – i misją!</div>
    <br>
""", unsafe_allow_html=True)

# Inicjalizacja stanu
if "products" not in st.session_state:
    st.session_state.products = []
if "saved_money" not in st.session_state:
    st.session_state.saved_money = 0.0
if "saved_kg" not in st.session_state:
    st.session_state.saved_kg = 0.0
if "badges" not in st.session_state:
    st.session_state.badges = set()

# Data i czyszczenie
today = datetime.date.today()
st.session_state.products = [
    p for p in st.session_state.products if p["Data ważności"] >= today
]

# Sidebar
with st.sidebar:
    st.header("➕ Dodaj produkt")
    name = st.text_input("Nazwa produktu")
    quantity = st.number_input("Ilość", min_value=0.0, value=1.0, step=0.1)
    unit = st.selectbox("Jednostka", ["szt.", "g", "kg", "ml", "l"])
    expiry = st.date_input("Data ważności", min_value=datetime.date.today())
    diet = st.multiselect("Preferencje diety", ["wegetariańska", "wegańska", "bezglutenowa", "bezlaktozowa"])
    if st.button("Dodaj") and name:
        st.session_state.products.append({
            "Nazwa": name,
            "Ilość": quantity,
            "Jednostka": unit,
            "Data ważności": expiry,
            "Dieta": diet
        })
        st.success(f"Dodano: {name}")

# Zakładki
page = st.selectbox("Wybierz sekcję", [
    "📋 Produkty", "📚 Porady i Edukacja", "📊 Statystyki", "🍽️ Przepisy", "🎮 Grywalizacja", "📍 Mapa lodówek", "📷 Skanowanie Paragonu"
])

if page == "📋 Produkty":
    st.subheader("📋 Twoje produkty")
    if st.session_state.products:
        df = pd.DataFrame(st.session_state.products)
        df["Status"] = df["Data ważności"].apply(lambda x: "⚠️ Dziś" if x == today else ("🖓 Wkrótce" if x <= today + datetime.timedelta(days=2) else "✅ OK"))
        st.dataframe(df)
        
        if st.button("♻️ Wyczyść listę"):
            st.session_state.products = []
            st.success("Wyczyszczono wszystkie produkty.")

        csv = df.to_csv(index=False).encode("utf-8")
        st.download_button("📅 Pobierz CSV", data=csv, file_name="produkty.csv", mime="text/csv")
    else:
        st.info("Brak produktów. Dodaj coś w menu bocznym!")

if page == "📚 Porady i Edukacja":
    st.subheader("🧠 Edukacja i motywacja")
    st.markdown("## Dlaczego warto nie marnować żywności?")
    st.image("https://source.unsplash.com/800x300/?food,waste")
    st.markdown("""
    - 🌍 **Marnowanie żywności = marnowanie zasobów**: wody, energii, pracy.
    - 💸 **Każdy kilogram jedzenia to średnio 5-10 zł** – miej to na uwadze.
    - 📉 **Twoje wybory mają znaczenie** – mniej odpadów = mniejszy ślad węglowy.
    
    **Porady praktyczne:**
    - Planuj tygodniowe menu 📅
    - Używaj oznaczeń (data otwarcia!) 🏷️
    - Ogranicz impulsywne zakupy 🛒
    - Gotuj z resztek! 🍲
    
    **Motywacja:**
    > "Kupujesz, by wyrzucić? Nie inwestuj w śmietnik!"
    
    **Odznaki do zdobycia:**
    - 🥇 "7 dni bez marnowania"
    - 🥈 "Uratowane 5 kg jedzenia"
    - 🥉 "Zaoszczędzono 50 zł"
    """)

if page == "📊 Statystyki":
    st.subheader("📊 Twoje statystyki")
    total = len(st.session_state.products)
    expiring_today = sum(1 for p in st.session_state.products if p["Data ważności"] == today)
    saved_value = round(st.session_state.saved_money, 2)
    saved_kg = round(st.session_state.saved_kg, 2)

    col1, col2, col3 = st.columns(3)
    col1.metric("📦 Produkty", total)
    col2.metric("💰 Zaoszczędzono", f"{saved_value} zł")
    col3.metric("🌿 Uratowano jedzenia", f"{saved_kg} kg")

    data = pd.DataFrame({
        "Kategorie": ["Uratowane kg", "Zaoszczędzone zł"],
        "Wartości": [saved_kg, saved_value]
    })
    fig = px.bar(data, x="Kategorie", y="Wartości", color="Kategorie", title="Oszczędności i ratunek")
    st.plotly_chart(fig)

if page == "🍽️ Przepisy":
    st.subheader("🍽️ Dopasowane przepisy")
    from random import choice
    dieta_uzytkownika = []
    for p in st.session_state.products:
        dieta_uzytkownika += p.get("Dieta", [])

    produkty = [p["Nazwa"].lower() for p in st.session_state.products if p["Data ważności"] <= today + datetime.timedelta(days=3)]
    przepisy = {
        "banany": ("Chlebek bananowy", "https://source.unsplash.com/600x400/?banana,bread", ["wegetariańska"]),
        "jajka": ("Omlet warzywny", "https://source.unsplash.com/600x400/?omelette", ["bezglutenowa"]),
        "chleb": ("Grzanki czosnkowe", "https://source.unsplash.com/600x400/?garlic,bread", ["wegetariańska"])
    }
    matched = False
    for p in produkty:
        if p in przepisy:
            desc, img, tags = przepisy[p]
            if not dieta_uzytkownika or any(d in dieta_uzytkownika for d in tags):
                st.image(img, use_column_width=True)
                st.markdown(f"### 🍽️ {desc}")
                matched = True
    if not matched:
        st.warning("Brak pasujących przepisów. Dodaj produkty lub określ preferencje diety.")

if page == "🎮 Grywalizacja":
    st.subheader("🎮 Twoje osiągnięcia")
    badges = [
        ("🥇", "7 dni bez marnowania"),
        ("🥈", "Uratowane 5 kg jedzenia"),
        ("🥉", "Zaoszczędzono 50 zł")
    ]
    for emoji, title in badges:
        st.markdown(f"{emoji} **{title}**")
    st.info("Zbieraj odznaki za swoje działania i ratuj planetę z klasą!")

if page == "📍 Mapa lodówek":
    st.subheader("📍 Społeczne lodówki i punkty oddawania")
    map = folium.Map(location=[52.2297, 21.0122], zoom_start=12)
    folium.Marker([52.23, 21.01], popup="Lodówka społeczna - Śródmieście").add_to(map)
    folium.Marker([52.24, 21.015], popup="NGO: Bank Żywności").add_to(map)
    folium_static(map)

if page == "📷 Skanowanie Paragonu":
    st.subheader("📷 Skanowanie paragonu")
    uploaded_file = st.file_uploader("Wybierz obraz", type=["png", "jpg", "jpeg"])
    if uploaded_file:
        image = Image.open(uploaded_file)
        st.image(image, caption="Wczytany obraz", use_column_width=True)
        text = pytesseract.image_to_string(image)
        st.text_area("Rozpoznany tekst", text)
        if st.button("Dodaj do listy"):
            for line in text.splitlines():
                if line.strip():
                    st.session_state.products.append({
                        "Nazwa": line.strip(),
                        "Ilość": 1.0,
                        "Jednostka": "szt.",
                        "Data ważności": today + datetime.timedelta(days=3),
                        "Dieta": []
                    })
            st.success("Dodano produkty z paragonu")
