import streamlit as st

st.set_page_config(page_title="GetAround dashboard", layout="wide")

st.title("GetAround dashboard")

adjust_threshold_checkin_type_page = st.Page(
    "adjust_threshold_checkin_type.py", title="Ajustement des seuils et type de checkin"
)
price_pred_page = st.Page("price_prediction.py", title="Prédiction de prix")

pg = st.navigation([adjust_threshold_checkin_type_page, price_pred_page])

pg.run()
