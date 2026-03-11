import streamlit as st
import requests

st.subheader("Prédiction de prix")

URL_PREDICT = "https://jiro99-getaround-api.hf.space/predict"

model_key_list = [
    "Alfa Romeo",
    "Audi",
    "BMW",
    "Citroen",
    "Ferrari",
    "Fiat",
    "Ford",
    "Honda",
    "KIA Motors",
    "Lamborghini",
    "Lexus",
    "Maserati",
    "Mazda",
    "Mercedes",
    "Mini",
    "Mitsubishi",
    "Nissan",
    "Opel",
    "PGO",
    "Peugeot",
    "Porsche",
    "Renault",
    "SEAT",
    "Subaru",
    "Suzuki",
    "Toyota",
    "Volkswagen",
    "Yamaha",
]
fuel_list = ["diesel", "electro", "hybrid_petrol", "petrol"]
paint_color_list = [
    "beige",
    "black",
    "blue",
    "brown",
    "green",
    "grey",
    "orange",
    "red",
    "silver",
    "white",
]
car_type_list = [
    "convertible",
    "coupe",
    "estate",
    "hatchback",
    "sedan",
    "subcompact",
    "suv",
    "van",
]


def predict(url=URL_PREDICT):
    data = {
        "input": [
            [
                st.session_state.model_key,
                st.session_state.mileage,
                st.session_state.engine_power,
                st.session_state.fuel,
                st.session_state.paint_color,
                st.session_state.car_type,
                st.session_state.private_parking_available,
                st.session_state.has_gps,
                st.session_state.has_air_conditioning,
                st.session_state.automatic_car,
                st.session_state.has_getaround_connect,
                st.session_state.has_speed_regulator,
                st.session_state.winter_tires,
            ]
        ]
    }

    response = requests.post(url, json=data)

    if response.status_code == 200:
        result = response.json()
        st.session_state.prediction = f"{result['prediction'][0]:.2f}€"

    else:
        st.error(f"Erreur lors de la requête : {response.status_code}")


with st.form("form", border=True):
    with st.container():
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.selectbox("Choisissez une marque", model_key_list, key="model_key")

        with col2:
            st.selectbox("Choisissez un carburant", fuel_list, key="fuel")

        with col3:
            st.selectbox("Choisissez une couleur", paint_color_list, key="paint_color")

        with col4:
            st.selectbox(
                "Choisissez un type de véhicule", car_type_list, key="car_type"
            )

    with st.container():
        col1, col2 = st.columns(2)

        with col1:
            st.number_input(
                "Saisissez le kilométrage",
                min_value=100,
                max_value=300_000,
                step=100,
                key="mileage",
            )

        with col2:
            st.number_input(
                "Saisissez la puissance du moteur",
                min_value=10,
                max_value=500,
                step=20,
                key="engine_power",
            )

    with st.container():
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.checkbox("Parking privé disponible", key="private_parking_available")
            st.checkbox("Getaround connect", key="has_getaround_connect")

        with col2:
            st.checkbox("Parking privé", key="has_gps")
            st.checkbox("Régulateur de vitesse", key="has_speed_regulator")

        with col3:
            st.checkbox("Climatisation", key="has_air_conditioning")
            st.checkbox("Pneus hiver", key="winter_tires")

        with col4:
            st.checkbox("Boîte automatique", key="automatic_car")

        st.markdown("<br><br>", unsafe_allow_html=True)

    with st.container():
        col1, col2, col3 = st.columns(3)

        with col2:
            st.form_submit_button("Prédire le prix", on_click=predict)

    with st.container():
        if "prediction" in st.session_state:
            st.success(f"Prix conseillé: {st.session_state.prediction}")
