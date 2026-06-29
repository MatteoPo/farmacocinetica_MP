import streamlit as st
import numpy as np
import plotly.graph_objects as go
from scipy.optimize import fsolve

st.title("Simulatore Medikinet XR")

# Parametri clinici
emivita = st.sidebar.slider("Emivita (h)", 1.0, 5.0, 2.5)
t_max = st.sidebar.slider("Tmax (h)", 0.5, 2.5, 1.5)
ritardo = st.sidebar.slider("Ritardo rilascio MR (h)", 2.0, 6.0, 4.0)

# Calcolo costanti: ke e ka (derivato da Tmax)
ke = np.log(2) / emivita
ka = fsolve(lambda k: (np.log(k/ke)/(k-ke)) - t_max, ke * 5)

def bateman(t, ka, ke, dose):
    # La formula classica di Bateman
    return dose * (ka / (ka - ke)) * (np.exp(-ke * t) - np.exp(-ka * t))

def get_profile(t, dose, t_assunzione):
    # IR: picco immediato
    ir = bateman(np.maximum(0, t - t_assunzione), ka, ke, dose * 0.5)
    # MR: picco ritardato
    mr = bateman(np.maximum(0, t - (t_assunzione + ritardo)), ka, ke, dose * 0.5)
    return ir + mr

# Input
d1, t1 = st.slider("Dose 1 (mg)", 0, 40, 20), st.slider("Ora 1", 6, 12, 7)
d2, t2 = st.slider("Dose 2 (mg)", 0, 40, 20), st.slider("Ora 2", 8, 20, 12)

t = np.linspace(6, 30, 300)
p1, p2 = get_profile(t, d1, t1), get_profile(t, d2, t2)
tot = p1 + p2

# Plot
fig = go.Figure()
fig.add_trace(go.Scatter(x=t, y=p1, name='Pasticca 1', fill='tozeroy', line=dict(dash='dash')))
fig.add_trace(go.Scatter(x=t, y=p2, name='Pasticca 2', fill='tozeroy', line=dict(dash='dash')))
fig.add_trace(go.Scatter(x=t, y=tot, name='Totale', line=dict(color='white', width=2)))

fig.update_layout(template="plotly_dark", xaxis_title="Ore", yaxis_title="Conc. Plasmatica")
st.plotly_chart(fig)
