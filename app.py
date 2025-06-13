# FoodWasteApp - Pełna wersja aplikacji Streamlit z dodatkowymi funkcjami

import streamlit as st
import pandas as pd
import datetime
import os
from PIL import Image
import pytesseract
import plotly.express as px
import folium
from streamlit_folium import folium_static

# Ustawienia aplikacji
st.set_page_config(page_title="FoodWasteApp", layout="wide")

# Ładowanie i zapisywanie danych CSV
DATA_PATH = "produkty.csv"

def load_data():
    if os.path.exists(DATA_PATH):
        return pd.read_csv(DATA_PATH, parse_dates=["Data waznosci"])
    return pd.DataFrame(columns=["Nazwa", "Ilosc", "Jednostka", "Data waznosci", "Cena"])

def save_data(df):
    df.to_csv(DATA_PATH, index=False)

# Inicjalizacja danych
if "products" not in st.session_state:
    st.session_state.products = load_data()

today = datetime.date.today()

# Stylizacja
st.markdown("""
<style>
    .main-header {
        text-align: center;
        color: #2e7d32;
        font-size: 3em;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

st.markdown("<div class='main-header'>FoodWasteApp</div>", unsafe_allow_html=True)

# Sidebar - dodawanie produktu
with st.sidebar:
    st.header("Dodaj produkt")
    name = st.text_input("Nazwa produktu")
    quantity = st.number_input("Ilosc", min_value=0.0, value=1.0)
    unit = st.selectbox("Jednostka", ["szt.", "g", "kg", "ml", "l"])
    expiry = st.date_input("Data waznosci", min_value=today)
    price = st.number_input("Cena (zł)", min_value=0.0, value=0.0)
    if st.button("Dodaj") and name:
        new_row = pd.DataFrame([[name, quantity, unit, expiry, price]], columns=st.session_state.products.columns)
        st.session_state.products = pd.concat([st.session_state.products, new_row], ignore_index=True)
        save_data(st.session_state.products)
        st.success(f"Dodano: {name}")

# Zakladki
page = st.selectbox("Sekcja", ["Produkty", "Statystyki", "Przepisy", "Mapa lodowek", "Paragon", "Eurostat"])

if page == "Produkty":
    st.subheader("Twoje produkty")
    df = st.session_state.products
    if not df.empty:
        df["Status"] = df["Data waznosci"].apply(lambda x: "Dzisiaj" if pd.to_datetime(x).date() == today else ("Wkrótce" if pd.to_datetime(x).date() <= today + datetime.timedelta(days=2) else "OK"))
        st.dataframe(df)

        if st.button("Wyczysc wszystkie"):
            st.session_state.products = pd.DataFrame(columns=df.columns)
            save_data(st.session_state.products)
            st.success("Wyczyszczono")

        csv = df.to_csv(index=False).encode("utf-8")
        st.download_button("Pobierz CSV", csv, "produkty.csv", "text/csv")
    else:
        st.info("Brak danych. Dodaj produkt w panelu bocznym.")

elif page == "Statystyki":
    st.subheader("Statystyki i oszczędności")
    df = st.session_state.products
    total = len(df)
    soon = sum(pd.to_datetime(df["Data waznosci"]).dt.date <= today + datetime.timedelta(days=2))
    value = df["Cena"].sum()
    co2_saved = total * 2.5  # Średnia wartość emisji CO2 w kg za produkt

    st.metric("Liczba produktów", total)
    st.metric("Wkrótce wygasa", soon)
    st.metric("Łączna wartość", f"{value:.2f} zł")
    st.metric("Oszczędzony CO2", f"{co2_saved:.1f} kg")

    chart = px.histogram(df, x="Data waznosci", nbins=20, title="Produkty wg daty wazności")
    st.plotly_chart(chart)

elif page == "Przepisy":
    st.subheader("Propozycje przepisów")
    skladniki = df["Nazwa"].str.lower().tolist()
    przepisy = {
        "jajka": "Omlet z warzywami",
        "banany": "Chlebek bananowy",
        "pomidor": "Zupa pomidorowa",
        "ziemniaki": "Frytki pieczone"
    }
    znalezione = [przepisy[s] for s in przepisy if s in skladniki]
    if znalezione:
        for r in znalezione:
            st.success(f"✅ {r}")
    else:
        st.info("Brak dopasowanych przepisów")

elif page == "Mapa lodowek":
    st.subheader("Mapa lodówek społecznych")
    mapa = folium.Map(location=[52.2297, 21.0122], zoom_start=6)
    punkty = [
        {"nazwa": "Warszawa - Jadłodzielnia", "lat": 52.2297, "lon": 21.0122},
        {"nazwa": "Kraków - Punkt dzielenia się", "lat": 50.0647, "lon": 19.9450},
        {"nazwa": "Gdańsk - Lodówka", "lat": 54.3520, "lon": 18.6466}
    ]
    for p in punkty:
        folium.Marker(location=[p["lat"], p["lon"]], popup=p["nazwa"]).add_to(mapa)
    folium_static(mapa)

elif page == "Paragon":
    st.subheader("Skanowanie paragonu")
    upload = st.file_uploader("Dodaj obraz", type=["png", "jpg", "jpeg"])
    if upload:
        img = Image.open(upload)
        st.image(img, use_column_width=True)
        text = pytesseract.image_to_string(img)
        st.text_area("Odczytany tekst", text)

        if st.button("Dodaj z paragonu"):
            for line in text.splitlines():
                if line.strip():
                    new_row = pd.DataFrame([[line.strip(), 1.0, "szt.", today, 0.0]], columns=df.columns)
                    st.session_state.products = pd.concat([st.session_state.products, new_row], ignore_index=True)
            save_data(st.session_state.products)
            st.success("Dodano z paragonu")

elif page == "Eurostat":
    st.subheader("Dane Eurostat")
    st.markdown("""
    - Gospodarstwa domowe odpowiadają za **54%** marnowanej żywności w UE (ok. **72 kg/osoba/rok**).
    - Całkowite marnotrawstwo żywności w UE: **132 kg/osoba/rok**.
    - Najczęściej marnowane: warzywa, pieczywo, owoce.
    - Ślad węglowy marnotrawstwa: **8-10% emisji globalnych gazów cieplarnianych**.
    """)
    fig = px.pie(names=["Gospodarstwa domowe", "Gastronomia", "Handel", "Przemysł"],
                 values=[54, 11, 8, 27],
                 title="Udział sektorów w marnotrawstwie żywności w UE")
    st.plotly_chart(fig)

# Koniec aplikacji

