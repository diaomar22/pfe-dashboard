"""
Dashboard PFE — Prévision de l'IPI mauritanien par modèle SARIMA
Oumar Abou DIA — Licence MAEF, I.S.G.I. — Stage ANSADE
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

st.set_page_config(page_title="PFE — IPI Mauritanie", page_icon="📊", layout="wide")

# ============================================================
# DONNÉES
# ============================================================
IPI = [92.8, 84.2, 95.6, 96.8, 88.7, 93.8, 95.0, 106.2,
       106.0, 105.7, 102.0, 107.7, 106.7, 106.2, 103.5, 104.9,
       98.7, 98.0, 98.9, 103.7, 104.0, 94.7, 93.7, 102.7,
       108.4, 95.1, 103.1, 97.5, 95.2, 89.8, 96.5, 109.2,
       109.8, 101.6, 103.9, 113.9, 114.0, 108.7, 115.1, 112.9,
       103.3, 87.8, 93.3, 106.4, 116.9, 115.9, 113.5, 114.0,
       106.8, 117.8, 121.4, 119.0, 121.1, 118.6, 122.7, 117.8,
       114.1, 112.7, 113.7, 112.3]

PERIODS = [f"{y} T{q}" for y in range(2011, 2026) for q in range(1, 5)]
FC_PERIOD = ["2026 T1", "2026 T2", "2026 T3", "2026 T4"]
FC_MEAN = [113.02, 111.18, 113.43, 116.72]
FC_LO = [103.42, 100.59, 101.83, 104.14]
FC_HI = [122.62, 121.77, 125.03, 129.30]

NAVY = "#1f3a68"
BURGUNDY = "#8b2635"
TEAL = "#2d6a5f"
GOLD = "#b08742"

# ============================================================
# DÉCOMPOSITION
# ============================================================
def decompose(series):
    n = len(series)
    trend = [None] * n
    for i in range(2, n - 2):
        trend[i] = (0.5*series[i-2] + series[i-1] + series[i] + series[i+1] + 0.5*series[i+2]) / 4
    detr = [None if t is None else v - t for v, t in zip(series, trend)]
    q_sums = [0]*4; q_cnt = [0]*4
    for i, v in enumerate(detr):
        if v is not None:
            q_sums[i % 4] += v; q_cnt[i % 4] += 1
    q_avg = [s/c for s, c in zip(q_sums, q_cnt)]
    q_mean = sum(q_avg) / 4
    seasonal = [v - q_mean for v in q_avg]
    seasonal_full = [seasonal[i % 4] for i in range(n)]
    return trend, seasonal, seasonal_full

trend, seasonal, seasonal_full = decompose(IPI)

# ============================================================
# SIDEBAR
# ============================================================
with st.sidebar:
    st.markdown("### 📊 Menu")
    section = st.radio(
        "Section",
        ["🏠 Présentation", "📈 Série et prévisions", "🔍 Décomposition", "📋 Prévisions 2026"],
        label_visibility="collapsed"
    )
    st.markdown("---")
    st.markdown("**Projet de Fin d'Études**")
    st.markdown("Licence MAEF — I.S.G.I.")
    st.markdown("Stage : ANSADE")
    st.markdown("---")
    st.markdown("**Auteur**")
    st.markdown("Oumar Abou DIA")
    st.markdown("**Encadrants**")
    st.markdown("M. Merbe *(I.S.G.I.)*")
    st.markdown("M. Diop · M. Zeine *(ANSADE)*")

# ============================================================
# SECTION 1 — PRÉSENTATION
# ============================================================
if section == "🏠 Présentation":
    st.title("Prévision de l'Indice de la Production Industrielle")
    st.markdown("#### Mauritanie · 2011 – 2025 · Modèle SARIMA")
    st.markdown("---")

    col1, col2 = st.columns([2, 1])
    with col1:
        st.markdown("""
        ### 🎯 Objectif

        Modéliser et prévoir l'**Indice de la Production Industrielle (IPI)** de la
        Mauritanie à partir des données trimestrielles publiées par l'**ANSADE**,
        sur la période 2011 – 2025.

        ### 🧪 Démarche

        - Analyse de la série trimestrielle (60 observations)
        - Identification d'une tendance et d'une saisonnalité
        - Modélisation par un processus **SARIMA(0,1,2)(0,1,1)₄**
        - Production des prévisions pour les 4 trimestres de 2026

        ### 📈 Résultats

        - **MAPE** : 3,77 % — bonne précision du modèle
        - **RMSE** : 4,90 points d'indice
        - **AIC** : 306,06
        """)
    with col2:
        st.markdown("### Chiffres clés")
        st.metric("MAPE", "3,77 %")
        st.metric("RMSE", "4,90")
        st.metric("AIC", "306,06")
        st.metric("Observations", "60")

    st.markdown("---")
    st.info("👈 Utilisez le menu de gauche pour explorer le dashboard.")

# ============================================================
# SECTION 2 — SÉRIE ET PRÉVISIONS
# ============================================================
elif section == "📈 Série et prévisions":
    st.title("📈 Série historique et prévisions 2026")
    st.markdown("Évolution trimestrielle de l'IPI sur 15 ans, avec projections SARIMA pour 2026.")

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=PERIODS, y=IPI, mode='lines', name='IPI observé',
                              line=dict(color=NAVY, width=2.5)))

    fc_x = [PERIODS[-1]] + FC_PERIOD
    fc_y = [IPI[-1]] + FC_MEAN
    fc_lo = [IPI[-1]] + FC_LO
    fc_hi = [IPI[-1]] + FC_HI

    fig.add_trace(go.Scatter(x=fc_x + fc_x[::-1], y=fc_hi + fc_lo[::-1],
                              fill='toself', fillcolor='rgba(139,38,53,0.15)',
                              line=dict(color='rgba(255,255,255,0)'),
                              name='Intervalle 95%'))
    fig.add_trace(go.Scatter(x=fc_x, y=fc_y, mode='lines+markers', name='Prévision 2026',
                              line=dict(color=BURGUNDY, width=2.5, dash='dash'),
                              marker=dict(size=9)))

    fig.update_layout(
        height=500, hovermode='x unified', plot_bgcolor='white',
        yaxis_title="IPI (base 100 = 2017)",
        xaxis=dict(showgrid=False, tickangle=-45, nticks=15),
        yaxis=dict(gridcolor='rgba(0,0,0,0.08)'),
        legend=dict(orientation='h', y=1.08, x=0.5, xanchor='center'),
        margin=dict(t=40, b=80)
    )
    st.plotly_chart(fig, use_container_width=True)

    col1, col2, col3, col4 = st.columns(4)
    mean_v = sum(IPI) / len(IPI)
    col1.metric("Moyenne", f"{mean_v:.1f}")
    col2.metric("Minimum", f"{min(IPI):.1f}", f"au {PERIODS[IPI.index(min(IPI))]}")
    col3.metric("Maximum", f"{max(IPI):.1f}", f"au {PERIODS[IPI.index(max(IPI))]}")
    col4.metric("Dernière valeur", f"{IPI[-1]:.1f}", f"au {PERIODS[-1]}")

    st.markdown("""
    > **Observation.** La série montre une **tendance haussière** marquée à partir de 2018,
    > avec un creux notable au T2 2021 (effet de la pandémie). Le profil saisonnier est stable :
    > **T2 généralement bas, T4 généralement haut**.
    """)

# ============================================================
# SECTION 3 — DÉCOMPOSITION
# ============================================================
elif section == "🔍 Décomposition":
    st.title("🔍 Décomposition de la série")
    st.markdown("""
    Séparation de la série en **tendance** (évolution de long terme)
    et **saisonnalité** (effet trimestriel régulier).
    """)

    fig = make_subplots(
        rows=3, cols=1, shared_xaxes=True,
        subplot_titles=("Série observée", "Tendance", "Saisonnalité"),
        vertical_spacing=0.08
    )
    fig.add_trace(go.Scatter(x=PERIODS, y=IPI, line=dict(color=NAVY, width=1.8), showlegend=False), row=1, col=1)
    fig.add_trace(go.Scatter(x=PERIODS, y=trend, line=dict(color=TEAL, width=1.8), showlegend=False), row=2, col=1)
    fig.add_trace(go.Scatter(x=PERIODS, y=seasonal_full, line=dict(color=GOLD, width=1.8), showlegend=False), row=3, col=1)
    fig.update_layout(height=550, plot_bgcolor='white', margin=dict(t=40, b=40))
    fig.update_xaxes(showgrid=False, tickangle=-45, nticks=10)
    fig.update_yaxes(gridcolor='rgba(0,0,0,0.08)')
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("### Effet saisonnier moyen par trimestre")
    fig2 = go.Figure()
    fig2.add_trace(go.Bar(
        x=["T1", "T2", "T3", "T4"], y=seasonal,
        marker_color=[NAVY if v >= 0 else BURGUNDY for v in seasonal],
        text=[f"{v:+.2f}" for v in seasonal],
        textposition='outside', textfont=dict(size=14)
    ))
    fig2.update_layout(
        height=350, plot_bgcolor='white',
        yaxis_title="Écart à la moyenne",
        xaxis=dict(showgrid=False),
        yaxis=dict(gridcolor='rgba(0,0,0,0.08)')
    )
    st.plotly_chart(fig2, use_container_width=True)

    st.markdown("""
    > **Interprétation.** Le **T4** est le trimestre le plus fort en moyenne,
    > tandis que le **T2** est le plus faible.
    > Cette saisonnalité justifie l'utilisation d'un modèle SARIMA.
    """)

# ============================================================
# SECTION 4 — TABLEAU
# ============================================================
elif section == "📋 Prévisions 2026":
    st.title("📋 Prévisions ponctuelles 2026")
    st.markdown("Valeurs prédites pour chaque trimestre de 2026, avec intervalle de confiance à 95%.")

    df = pd.DataFrame({
        "Trimestre": FC_PERIOD,
        "Prévision": FC_MEAN,
        "Borne inférieure (95%)": FC_LO,
        "Borne supérieure (95%)": FC_HI
    })

    st.dataframe(
        df.style.format({"Prévision": "{:.2f}",
                          "Borne inférieure (95%)": "{:.2f}",
                          "Borne supérieure (95%)": "{:.2f}"}),
        use_container_width=True, hide_index=True
    )

    st.markdown("### Modèle utilisé")
    st.markdown("**SARIMA(0,1,2)(0,1,1)₄**")
    st.markdown("""
    - 60 observations trimestrielles (2011 T1 → 2025 T4)
    - Différenciation régulière et saisonnière
    - Période saisonnière m = 4 (données trimestrielles)
    """)

    csv = df.to_csv(index=False, sep=";").encode("utf-8")
    st.download_button("📥 Télécharger les prévisions (CSV)", csv,
                       "previsions_IPI_2026.csv", "text/csv")

    st.markdown("---")
    st.markdown("""
    **Projet de Fin d'Études — Licence MAEF · I.S.G.I.**
    Stage à l'ANSADE · Encadrement : M. Merbe (académique), M. Diop & M. Zeine (ANSADE)
    """)
