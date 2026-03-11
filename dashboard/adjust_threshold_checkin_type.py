from time import sleep

import pandas as pd
import plotly.express as px
import streamlit as st

all_checkin_type = ["All", "Connect", "Mobile"]
DATA_URL = "df_with_next_rental.csv"


@st.cache_data
def load_data(nrows=None):
    sleep(3)
    data = pd.read_csv(DATA_URL, nrows=nrows)
    return data


data_load_state = st.text("Loading data...")
data = load_data()
data_load_state.text("")

# initialise les valeurs par defaut
if "selection_checkin_type" not in st.session_state:
    st.session_state.selection_checkin_type = all_checkin_type[0]

if "selection_threshold" not in st.session_state:
    st.session_state.selection_threshold = 0


def checkin_change():
    # reinitialise le threshold a 0
    st.session_state.selection_threshold = 0

    init_df_delay()

    st.session_state.nb_retard = len(st.session_state.df_delay)


def init_df_delay():
    selection = st.session_state.get("selection_checkin_type")

    if selection is None:
        return

    selection_threshold = st.session_state.get("selection_threshold", 0)

    checkin_list = (
        [c.lower() for c in all_checkin_type[1:]]
        if selection == "All"
        else [selection.lower()]
    )

    df_delayz = data[
        (data["delay_at_checkout_in_minutes"] - selection_threshold > 0)
        & (data["checkin_type"].isin(checkin_list))
    ].copy()

    st.session_state.df_delay = df_delayz


if "nb_retard" not in st.session_state:
    checkin_change()

st.subheader("Ajustement des seuils et type de checkin")

with st.container(border=True):
    selection_checkin_type = st.selectbox(
        "Type de Checkin",
        all_checkin_type,
        # default=all_checkin_type[0],
        key="selection_checkin_type",
        on_change=checkin_change,
    )

    selection_threshold = st.slider(
        "Délai minimum avant la prochaine location en minutes",
        min_value=0,
        max_value=360,
        step=15,
        key="selection_threshold",
        on_change=init_df_delay,
    )


with st.container(border=True):
    st.subheader(
        "Part du chiffre d’affaires des propriétaires affectée par le seuil et le périmètre"
    )

df_delay = st.session_state.df_delay

with st.container(border=True):
    st.subheader("Nombre de retards")

    fig = px.histogram(
        df_delay.assign(fake_var=1),
        x="fake_var",
        title=f"{len(df_delay)} retards > {selection_threshold} min",
        color="checkin_type",
        barmode="group",
        color_discrete_map={"mobile": "red", "connect": "blue"},
        category_orders={"checkin_type": ["connect", "mobile"]},
        hover_data={
            "fake_var": False,
        },
    )
    fig.update_xaxes(type="category", title="")
    fig.update_layout(bargap=0.9)

    st.plotly_chart(fig, width="stretch")


with st.container(border=True):
    st.subheader("Combien de cas problématiques sont ils résolus ?")

    nb_retard = st.session_state.nb_retard
    resolved = nb_retard - len(df_delay)
    pct = (resolved / nb_retard) * 100

    st.write(
        f"Après application du seuil à **{selection_threshold}** min  \nRetards corrigés : **{nb_retard - len(df_delay)}**, soit **{pct}%**"
    )
