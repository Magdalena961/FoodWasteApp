# DiaPlan – aplikacja do automatyzacji diety dla osób z cukrzycą

import streamlit as st
import pandas as pd
import datetime

st.set_page_config(page_title="DiaPlan", layout="wide")

st.markdown("""
    <style>
        .main-header {
            text-align: center;
            color: #388e3c;
            font-size: 3em;
            font-weight: bold;
            font-family: 'Georgia', serif;
            margin-top: 0.5em;
        }
        .sub-header {
            text-align: center;
            color: #6d4c41;
            font-size: 1.2em;
            font-style: italic;
        }
    </style>
""", unsafe_allow_html=True)

st.markdown("""
    <div class='main-header'>DiaPlan</div>
    <div class='sub-header'>Automatyzacja diety dla osób z cukrzycą</div>
    <br>
""", unsafe_allow_html=True)

if "meals" not in st.session_state:
    st.session_state.meals = []

with st.sidebar:
    st.header("🍽️ Dodaj posiłek")
    meal_name = st.text_input("Nazwa posiłku")
    carbs = st.number_input("Węglowodany [g]", min_value=0)
    proteins = st.number_input("Białka [g]", min_value=0)
    fats = st.number_input("Tłuszcze [g]", min_value=0)
    glycemic_index = st.number_input("Indeks glikemiczny", min_value=0)
    if st.button("Dodaj"):
        if meal_name:
            st.session_state.meals.append({
                "Posiłek": meal_name,
                "Węglowodany": carbs,
                "Białka": proteins,
                "Tłuszcze": fats,
                "IG": glycemic_index
            })
            st.success(f"Dodano: {meal_name}")

st.subheader("📋 Plan posiłków")
if st.session_state.meals:
    df = pd.DataFrame(st.session_state.meals)
    df.index += 1
    st.dataframe(df, use_container_width=True)
else:
    st.info("Brak dodanych posiłków. Dodaj coś z menu bocznego.")

st.markdown("""
    <hr>
    <p style='text-align: center; font-size: 0.8em;'>DiaPlan – wsparcie dietetyczne dla diabetyków</p>
""", unsafe_allow_html=True)

    <p style='text-align: center; font-size: 0.8em;'>DiaPlan – automatyzacja diety dla osób z cukrzycą – prototyp pracy dyplomowej</p>
""", unsafe_allow_html=True)

