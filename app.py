"""
Dashboard PFE - Prevision de l'IPI mauritanien par modele SARIMA
Oumar Abou DIA - Licence Professionnelle MAEF, ISGI - Stage ANSADE
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go

st.set_page_config(
    page_title="PFE - IPI Mauritanie",
    page_icon=None,
    layout="wide"
)

st.markdown("""
<style>
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 3rem;
        max-width: 1200px;
    }
    h1 { font-weight: 600; }
    h2 { font-weight: 600; margin-top: 1.5rem; }
    h3 { font-weight: 500; }
</style>
""", unsafe_allow_html=True)

# ============================================================
# DONNEES
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
# DECOMPOSITION
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
    st.markdown("### Sommaire")
    section = st.radio(
        "Section",
        ["Accueil", "Analyse et résultats", "Conclusion et limites", "À propos"],
        label_visibility="collapsed"
    )
    st.markdown("---")
    st.markdown("**Projet de Fin d'Études**")
    st.markdown("Licence Professionnelle MAEF")
    st.markdown("---")
    st.markdown("**ISGI** — Nouakchott")
    st.markdown("**Stage** : ANSADE")

# ============================================================
# PAGE 1 - ACCUEIL
# ============================================================
if section == "Accueil":
    st.title("Prévision de l'Indice de la Production Industrielle")
    st.markdown("#### Mauritanie — Période 2011–2025")
    st.markdown("---")

    col1, col2 = st.columns([3, 2])

    with col1:
        st.markdown("""
        ### Le projet en bref

        Modélisation et prévision de l'**Indice de la Production Industrielle (IPI)**
        de la Mauritanie à partir des données trimestrielles de l'**ANSADE**.

        ### Méthode

        Modèle **SARIMA(0,1,2)(0,1,1)₄** appliqué à 60 observations trimestrielles
        (2011–2025), avec production de prévisions pour les 4 trimestres de 2026.

        ### Cadre

        Projet de Fin d'Études — Licence Professionnelle en Mathématiques Appliquées
        à l'Économie et à la Finance (**MAEF**), Institut Supérieur de Génie
        Industriel (**ISGI**) — Stage à l'**ANSADE**.
        """)

    with col2:
        st.markdown("### Indicateurs")
        st.metric("MAPE", "3,77 %")
        st.metric("RMSE", "4,90")
        st.metric("AIC", "306,06")
        st.metric("Observations", "60 trimestres")

# ============================================================
# PAGE 2 - ANALYSE ET RESULTATS
# ============================================================
elif section == "Analyse et résultats":
    st.title("Analyse et résultats")
    st.markdown("---")

    # ---- GRAPHIQUE 1 : SERIE + PREVISIONS ----
    st.markdown("## Série historique et prévisions 2026")
    st.markdown("Évolution trimestrielle de l'IPI avec projections SARIMA pour 2026 (intervalle de confiance à 95 %).")

    fig1 = go.Figure()
    fig1.add_trace(go.Scatter(x=PERIODS, y=IPI, mode='lines', name='IPI observé',
                               line=dict(color=NAVY, width=2.5)))
    fc_x = [PERIODS[-1]] + FC_PERIOD
    fc_y = [IPI[-1]] + FC_MEAN
    fc_lo = [IPI[-1]] + FC_LO
    fc_hi = [IPI[-1]] + FC_HI
    fig1.add_trace(go.Scatter(x=fc_x + fc_x[::-1], y=fc_hi + fc_lo[::-1],
                               fill='toself', fillcolor='rgba(139,38,53,0.15)',
                               line=dict(color='rgba(255,255,255,0)'),
                               name='Intervalle 95 %'))
    fig1.add_trace(go.Scatter(x=fc_x, y=fc_y, mode='lines+markers', name='Prévision 2026',
                               line=dict(color=BURGUNDY, width=2.5, dash='dash'),
                               marker=dict(size=9)))
    fig1.update_layout(
        height=500, hovermode='x unified', plot_bgcolor='white',
        yaxis_title="IPI (base 100 = 2017)",
        xaxis=dict(showgrid=False, tickangle=-45, nticks=15),
        yaxis=dict(gridcolor='rgba(0,0,0,0.08)'),
        legend=dict(orientation='h', y=1.08, x=0.5, xanchor='center'),
        margin=dict(t=40, b=80)
    )
    st.plotly_chart(fig1, use_container_width=True)

    col1, col2, col3, col4 = st.columns(4)
    mean_v = sum(IPI) / len(IPI)
    col1.metric("Moyenne", f"{mean_v:.1f}")
    col2.metric("Minimum", f"{min(IPI):.1f}", f"au {PERIODS[IPI.index(min(IPI))]}", delta_color="off")
    col3.metric("Maximum", f"{max(IPI):.1f}", f"au {PERIODS[IPI.index(max(IPI))]}", delta_color="off")
    col4.metric("Dernière valeur", f"{IPI[-1]:.1f}", f"au {PERIODS[-1]}", delta_color="off")

    st.markdown("""
    > Tendance haussière à partir de 2018, creux marqué au T2 2021 (effet Covid-19),
    > saisonnalité stable : **T2 bas, T4 haut**.
    """)

    st.markdown("---")

    # ---- DECOMPOSITION ----
    st.markdown("## Décomposition de la série")
    st.markdown("Décomposition additive : **Y(t) = Tendance + Saisonnalité + Résidu**.")

    st.markdown("### Série observée")
    fig2a = go.Figure()
    fig2a.add_trace(go.Scatter(x=PERIODS, y=IPI, mode='lines',
                                line=dict(color=NAVY, width=2.2), showlegend=False))
    fig2a.update_layout(
        height=320, plot_bgcolor='white',
        yaxis_title="IPI",
        xaxis=dict(showgrid=False, tickangle=-45, nticks=12),
        yaxis=dict(gridcolor='rgba(0,0,0,0.08)'),
        margin=dict(t=20, b=60, l=60, r=20)
    )
    st.plotly_chart(fig2a, use_container_width=True)

    st.markdown("### Tendance")
    fig2b = go.Figure()
    fig2b.add_trace(go.Scatter(x=PERIODS, y=trend, mode='lines',
                                line=dict(color=TEAL, width=2.2), showlegend=False))
    fig2b.update_layout(
        height=320, plot_bgcolor='white',
        yaxis_title="Tendance",
        xaxis=dict(showgrid=False, tickangle=-45, nticks=12),
        yaxis=dict(gridcolor='rgba(0,0,0,0.08)'),
        margin=dict(t=20, b=60, l=60, r=20)
    )
    st.plotly_chart(fig2b, use_container_width=True)
    st.markdown("> Croissance régulière à partir de 2018.")

    st.markdown("### Saisonnalité")
    fig2c = go.Figure()
    fig2c.add_trace(go.Scatter(x=PERIODS, y=seasonal_full, mode='lines',
                                line=dict(color=GOLD, width=2.2), showlegend=False))
    fig2c.update_layout(
        height=320, plot_bgcolor='white',
        yaxis_title="Saisonnalité",
        xaxis=dict(showgrid=False, tickangle=-45, nticks=12),
        yaxis=dict(gridcolor='rgba(0,0,0,0.08)'),
        margin=dict(t=20, b=60, l=60, r=20)
    )
    st.plotly_chart(fig2c, use_container_width=True)

    st.markdown("### Effet saisonnier moyen")
    fig2d = go.Figure()
    fig2d.add_trace(go.Bar(
        x=["T1 (Janv-Mars)", "T2 (Avr-Juin)", "T3 (Juil-Sept)", "T4 (Oct-Déc)"],
        y=seasonal,
        marker_color=[NAVY if v >= 0 else BURGUNDY for v in seasonal],
        text=[f"{v:+.2f}" for v in seasonal],
        textposition='outside', textfont=dict(size=14)
    ))
    fig2d.update_layout(
        height=380, plot_bgcolor='white',
        yaxis_title="Écart à la moyenne (points)",
        xaxis=dict(showgrid=False),
        yaxis=dict(gridcolor='rgba(0,0,0,0.08)'),
        margin=dict(t=40, b=40, l=60, r=20)
    )
    st.plotly_chart(fig2d, use_container_width=True)

    st.markdown(f"""
    > **T4** est le plus dynamique (**{seasonal[3]:+.2f} pts**), **T2** le plus faible
    > (**{seasonal[1]:+.2f} pts**). Cette saisonnalité justifie le choix d'un modèle SARIMA.
    """)

    st.markdown("---")

    # ---- TABLEAU PREVISIONS ----
    st.markdown("## Prévisions 2026")

    df = pd.DataFrame({
        "Trimestre": FC_PERIOD,
        "Prévision": FC_MEAN,
        "Borne inférieure (95 %)": FC_LO,
        "Borne supérieure (95 %)": FC_HI
    })

    st.dataframe(
        df.style.format({
            "Prévision": "{:.2f}",
            "Borne inférieure (95 %)": "{:.2f}",
            "Borne supérieure (95 %)": "{:.2f}"
        }),
        use_container_width=True, hide_index=True
    )

    st.markdown("**Modèle retenu** : SARIMA(0,1,2)(0,1,1)₄ — 60 observations, période saisonnière m = 4.")

    csv = df.to_csv(index=False, sep=";").encode("utf-8")
    st.download_button("Télécharger les prévisions (CSV)", csv,
                       "previsions_IPI_2026.csv", "text/csv")

# ============================================================
# PAGE 3 - CONCLUSION ET LIMITES
# ============================================================
elif section == "Conclusion et limites":
    st.title("Conclusion et limites")
    st.markdown("---")

    st.markdown("## Conclusion")
    st.markdown("""
    - Le modèle **SARIMA(0,1,2)(0,1,1)₄** capture bien la dynamique de l'IPI mauritanien.
    - **MAPE de 3,77 %** : bonne qualité d'ajustement.
    - Prévisions 2026 cohérentes avec le profil saisonnier observé (T2 bas, T4 haut).
    - Outil utile pour l'**analyse conjoncturelle** et la planification à court terme.
    """)

    st.markdown("## Limites")
    st.markdown("""
    - **Échantillon modeste** : 60 observations trimestrielles seulement.
    - **Approche univariée** : aucune variable exogène (pétrole, taux de change…).
    - **Horizon court** : prévisions fiables sur 4 trimestres maximum.
    - **Stabilité supposée** : ruptures structurelles possibles non prises en compte.
    """)

    st.markdown("## Perspectives")
    st.markdown("""
    - Étendre à un modèle **SARIMAX** avec variables exogènes.
    - Comparer avec d'autres méthodes (**Holt-Winters**, **ETS**).
    - **Mettre à jour** le modèle à mesure des nouvelles publications de l'ANSADE.
    """)

# ============================================================
# PAGE 4 - A PROPOS
# ============================================================
elif section == "À propos":
    st.title("À propos")
    st.markdown("---")

    st.markdown("### Auteur")
    st.markdown("""
    **Oumar Abou DIA**
    Étudiant en Licence Professionnelle MAEF — promotion 2025–2026.
    """)

    st.markdown("### Formation")
    st.markdown("""
    **Licence Professionnelle en Mathématiques Appliquées à l'Économie et à la Finance (MAEF)**
    Institut Supérieur de Génie Industriel (ISGI) — Nouakchott, Mauritanie.
    """)

    st.markdown("### Stage")
    st.markdown("""
    **Agence Nationale de la Statistique et de l'Analyse Démographique et Économique (ANSADE)**
    Institution officielle de production statistique en Mauritanie.
    """)

    st.markdown("### Encadrement")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("**Académique**")
        st.markdown("M. Merbe *(ISGI)*")
    with col2:
        st.markdown("**Professionnel**")
        st.markdown("M. Diop · M. Zeine *(ANSADE)*")

    st.markdown("### Ressources")
    st.markdown("""
    - Code source : [github.com/diaomar22/pfe-dashboard](https://github.com/diaomar22/pfe-dashboard)
    - Dashboard en ligne : [ipi-mauritanie.streamlit.app](https://ipi-mauritanie.streamlit.app)
    """)
