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

# ============================================================
# STYLE GLOBAL
# ============================================================
st.markdown("""
<style>
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 3rem;
        max-width: 1200px;
    }
    h1 { font-weight: 600; color: #1a1a1a; }
    h2 { font-weight: 600; color: #1f3a68; margin-top: 1.5rem; }
    h3 { font-weight: 500; color: #2c5282; }
    .stMetric { background-color: #f8f7f3; padding: 12px; border-radius: 6px; }
    .source-note {
        font-size: 12px;
        color: #6b6b6b;
        font-style: italic;
        margin-top: 8px;
    }
    blockquote {
        border-left: 3px solid #1f3a68;
        padding-left: 16px;
        color: #4a4a4a;
        font-style: italic;
        margin: 16px 0;
    }
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
    st.markdown("*Mathématiques Appliquées à l'Économie et à la Finance*")
    st.markdown("---")
    st.markdown("**Institution**")
    st.markdown("Institut Supérieur de Génie Industriel (ISGI)")
    st.markdown("Nouakchott, Mauritanie")
    st.markdown("---")
    st.markdown("**Stage**")
    st.markdown("Agence Nationale de la Statistique")
    st.markdown("et de l'Analyse Démographique et Économique")
    st.markdown("*(ANSADE)*")

# ============================================================
# PAGE 1 - ACCUEIL
# ============================================================
if section == "Accueil":
    st.title("Prévision de l'Indice de la Production Industrielle")
    st.markdown("#### République Islamique de Mauritanie — Période 2011–2025")
    st.markdown("---")

    st.markdown("""
    ### Présentation du projet

    Ce travail s'inscrit dans le cadre du **Projet de Fin d'Études** de la
    **Licence Professionnelle en Mathématiques Appliquées à l'Économie et à la Finance (MAEF)**,
    dispensée à l'**Institut Supérieur de Génie Industriel (ISGI)** de Nouakchott.

    Il a été réalisé à l'**Agence Nationale de la Statistique et de l'Analyse Démographique
    et Économique (ANSADE)**, institution officielle de production statistique en Mauritanie.
    """)

    col1, col2 = st.columns([3, 2])

    with col1:
        st.markdown("""
        ### Problématique

        L'**Indice de la Production Industrielle (IPI)** constitue un indicateur économique
        majeur pour suivre l'activité du secteur industriel mauritanien.
        Sa prévision présente un intérêt opérationnel pour la planification publique,
        l'analyse conjoncturelle et la prise de décision économique.

        La problématique posée est la suivante :
        > *Comment modéliser de manière rigoureuse la dynamique de l'IPI mauritanien,
        > et en produire des prévisions fiables à court terme ?*

        ### Démarche méthodologique

        L'étude s'appuie sur la **méthodologie de Box-Jenkins** appliquée à une série
        chronologique trimestrielle de 60 observations couvrant la période 2011–2025 :

        - Analyse exploratoire de la série
        - Identification d'une tendance et d'une saisonnalité régulière
        - Spécification d'un modèle **SARIMA(0,1,2)(0,1,1)₄**
        - Estimation et validation du modèle
        - Production de prévisions ponctuelles et par intervalles pour l'année 2026
        """)

    with col2:
        st.markdown("### Indicateurs de performance")
        st.metric("MAPE", "3,77 %", help="Mean Absolute Percentage Error")
        st.metric("RMSE", "4,90", help="Root Mean Square Error")
        st.metric("AIC", "306,06", help="Critère d'information d'Akaike")
        st.metric("Observations", "60", help="Trimestres observés")

    st.markdown("---")
    st.markdown("""
    *Utilisez le menu de navigation à gauche pour parcourir les différentes sections du tableau de bord.*
    """)

# ============================================================
# PAGE 2 - ANALYSE ET RESULTATS
# ============================================================
elif section == "Analyse et résultats":
    st.title("Analyse de la série et résultats")
    st.markdown("Présentation graphique de la série historique, de sa décomposition et des prévisions issues du modèle SARIMA.")
    st.markdown("---")

    # ---- GRAPHIQUE 1 : SERIE + PREVISIONS ----
    st.markdown("## 1. Série historique et prévisions 2026")
    st.markdown("""
    Le graphique ci-dessous présente l'évolution trimestrielle de l'IPI mauritanien sur la période 2011–2025,
    ainsi que les prévisions issues du modèle SARIMA pour les quatre trimestres de l'année 2026.
    La zone en grisé rouge représente l'intervalle de confiance à 95 % autour de la prévision ponctuelle.
    """)

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
                               name='Intervalle de confiance 95 %'))
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
    > **Observation.** La série de l'IPI mauritanien présente une **tendance haussière** marquée à partir de 2018,
    > après une période de relative stagnation entre 2011 et 2017. Un creux significatif est observé au deuxième
    > trimestre 2021 (87,8 points), attribuable aux effets de la pandémie de Covid-19 sur l'activité industrielle.
    > Le profil saisonnier de la série est stable sur l'ensemble de la période : le deuxième trimestre est
    > systématiquement le plus faible, tandis que le quatrième trimestre constitue le pic annuel.
    """)

    st.markdown("---")

    # ---- DECOMPOSITION ----
    st.markdown("## 2. Décomposition de la série")
    st.markdown("""
    Avant d'appliquer le modèle SARIMA, la série a été décomposée en ses composantes structurelles
    selon le schéma additif **Y(t) = T(t) + S(t) + ε(t)**,
    où T(t) désigne la tendance, S(t) la composante saisonnière, et ε(t) le résidu.
    La décomposition repose sur une moyenne mobile centrée d'ordre 4.
    """)

    # Graphique 2a - Serie observee
    st.markdown("### 2.1 Série observée")
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

    # Graphique 2b - Tendance
    st.markdown("### 2.2 Composante de tendance")
    st.markdown("""
    La tendance, estimée par moyenne mobile centrée d'ordre 4, isole la dynamique de long terme
    en éliminant les fluctuations saisonnières et les chocs de court terme.
    """)
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
    st.markdown("""
    > La tendance révèle une croissance régulière à partir de 2018,
    > avec un léger fléchissement en fin de période (2025).
    """)

    # Graphique 2c - Saisonnalite
    st.markdown("### 2.3 Composante saisonnière")
    st.markdown("""
    La composante saisonnière mesure les variations cycliques régulières d'un trimestre à l'autre.
    Son amplitude stable confirme la pertinence d'une modélisation saisonnière.
    """)
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

    # Effet saisonnier moyen
    st.markdown("### 2.4 Effet saisonnier moyen par trimestre")
    st.markdown("Ce graphique synthétise l'écart moyen de chaque trimestre par rapport à la tendance.")
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
        yaxis_title="Écart à la moyenne (points d'indice)",
        xaxis=dict(showgrid=False),
        yaxis=dict(gridcolor='rgba(0,0,0,0.08)'),
        margin=dict(t=40, b=40, l=60, r=20)
    )
    st.plotly_chart(fig2d, use_container_width=True)

    st.markdown(f"""
    > **Lecture.** Le quatrième trimestre (T4) est structurellement le plus dynamique avec un effet positif de
    > **{seasonal[3]:+.2f} points** par rapport à la tendance, tandis que le deuxième trimestre (T2) est le plus faible
    > avec un effet de **{seasonal[1]:+.2f} points**. Cette saisonnalité régulière justifie pleinement le recours à un
    > modèle SARIMA, qui intègre explicitement la composante saisonnière par différenciation d'ordre 4.
    """)

    st.markdown("---")

    # ---- TABLEAU PREVISIONS ----
    st.markdown("## 3. Prévisions ponctuelles 2026")
    st.markdown("Le tableau ci-dessous présente les valeurs prédites pour chaque trimestre de 2026, accompagnées de leurs bornes de confiance à 95 %.")

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

    st.markdown("### Modèle retenu")
    st.markdown("**SARIMA(0,1,2)(0,1,1)₄** — *Seasonal AutoRegressive Integrated Moving Average*")
    st.markdown("""
    - 60 observations trimestrielles couvrant la période 2011 T1 → 2025 T4
    - Différenciation régulière d'ordre 1 (d=1) pour éliminer la tendance
    - Différenciation saisonnière d'ordre 1 (D=1) pour neutraliser la saisonnalité
    - Période saisonnière m = 4 (données trimestrielles)
    - Composantes moyennes mobiles régulière (q=2) et saisonnière (Q=1)
    """)

    csv = df.to_csv(index=False, sep=";").encode("utf-8")
    st.download_button("Télécharger les prévisions (CSV)", csv,
                       "previsions_IPI_2026.csv", "text/csv")

# ============================================================
# PAGE 3 - CONCLUSION ET LIMITES
# ============================================================
elif section == "Conclusion et limites":
    st.title("Conclusion et limites de l'étude")
    st.markdown("---")

    st.markdown("## Conclusion")
    st.markdown("""
    Ce travail a permis de modéliser et de prévoir l'Indice de la Production Industrielle de la
    Mauritanie à partir d'une série trimestrielle de 60 observations couvrant la période 2011–2025.
    L'application de la **méthodologie de Box-Jenkins** a conduit à retenir un modèle
    **SARIMA(0,1,2)(0,1,1)₄**, qui prend en compte à la fois la tendance haussière de long terme
    et la saisonnalité trimestrielle régulière observée dans les données.

    Les principaux résultats obtenus sont les suivants :

    - Le modèle estimé présente une **erreur moyenne en pourcentage absolu (MAPE) de 3,77 %**,
      témoignant d'une bonne qualité d'ajustement aux données historiques.
    - L'erreur quadratique moyenne (RMSE) s'établit à **4,90 points d'indice**, ce qui reste
      faible au regard de la dispersion observée de la série.
    - Les **prévisions pour l'année 2026** indiquent un profil saisonnier conforme aux trimestres
      antérieurs, avec un point bas attendu au deuxième trimestre (111,2) et un pic au quatrième
      trimestre (116,7).
    - Les intervalles de confiance à 95 % s'élargissent progressivement avec l'horizon de
      prévision, traduisant l'incertitude croissante au-delà du court terme.

    Sur le plan opérationnel, ces prévisions peuvent constituer un **outil d'aide à la décision**
    pour les institutions économiques mauritaniennes (ANSADE, Ministère des Finances, Banque
    Centrale), en éclairant l'analyse conjoncturelle et la planification de court terme.
    """)

    st.markdown("---")
    st.markdown("## Limites de l'étude")
    st.markdown("""
    Malgré les résultats encourageants obtenus, plusieurs limites méritent d'être soulignées :

    **Taille de l'échantillon.** L'étude repose sur 60 observations trimestrielles, ce qui
    correspond à un horizon temporel de quinze années. Bien que suffisant pour une modélisation
    SARIMA, ce volume reste modeste et peut affecter la précision des estimations,
    notamment pour les paramètres saisonniers.

    **Approche univariée.** Le modèle SARIMA ne prend en compte que la dynamique propre de la
    série, sans intégrer de **variables explicatives exogènes** susceptibles d'influencer
    l'IPI (prix du pétrole, taux de change, demande mondiale, indices sectoriels).
    Une extension naturelle consisterait à mobiliser un modèle SARIMAX ou un modèle vectoriel
    autorégressif (VAR).

    **Hypothèse de stabilité structurelle.** Le modèle suppose que la dynamique observée sur
    la période 2011–2025 se prolonge en 2026. Or, l'économie mauritanienne est sensible à
    des chocs externes (pandémie, fluctuations des matières premières) qui peuvent provoquer
    des **ruptures structurelles** non capturées par le modèle.

    **Horizon de prévision limité.** Les prévisions ont été produites à un horizon de quatre
    trimestres. Au-delà, l'élargissement des intervalles de confiance réduit fortement la
    pertinence opérationnelle des projections.

    **Absence de comparaison multi-modèles.** Le modèle SARIMA a été retenu sur la base des
    critères d'information classiques (AIC, BIC) et de la qualité des résidus.
    Une comparaison systématique avec d'autres familles de modèles (Holt-Winters, ETS,
    lissage exponentiel, réseaux de neurones récurrents) permettrait d'évaluer plus rigoureusement
    son avantage relatif.
    """)

    st.markdown("---")
    st.markdown("## Perspectives")
    st.markdown("""
    Ce travail ouvre plusieurs pistes de prolongement :

    - **Enrichissement du modèle** par l'introduction de variables exogènes pertinentes pour
      l'économie mauritanienne (indices sectoriels, conjoncture régionale, prix internationaux).
    - **Mise à jour régulière du modèle** à mesure que de nouvelles observations trimestrielles
      deviennent disponibles, afin de maintenir sa pertinence prédictive.
    - **Comparaison avec d'autres approches** de prévision (modèles de lissage, méthodes
      d'apprentissage automatique) pour évaluer le rapport coût-précision de chaque méthode.
    - **Désagrégation sectorielle** : appliquer la même démarche aux sous-indices de production
      (industrie extractive, industries manufacturières, énergie) afin d'affiner l'analyse.
    """)

# ============================================================
# PAGE 4 - A PROPOS
# ============================================================
elif section == "À propos":
    st.title("À propos")
    st.markdown("---")

    st.markdown("## L'auteur")
    st.markdown("""
    **Oumar Abou DIA**

    Étudiant en **Licence Professionnelle en Mathématiques Appliquées à l'Économie et à la
    Finance (MAEF)** à l'Institut Supérieur de Génie Industriel (ISGI) de Nouakchott,
    promotion 2025–2026.

    Ce projet constitue mon **Projet de Fin d'Études** (PFE), réalisé dans le cadre d'un
    stage de fin de cycle à l'Agence Nationale de la Statistique et de l'Analyse
    Démographique et Économique (ANSADE).

    Mes domaines d'intérêt couvrent la **statistique appliquée**, l'**économétrie des séries
    temporelles**, la **finance quantitative** et la **science des données** appliquée aux
    problématiques économiques.
    """)

    st.markdown("---")
    st.markdown("## L'établissement de formation")
    st.markdown("""
    **Institut Supérieur de Génie Industriel (ISGI)**

    L'ISGI, anciennement Institut Universitaire Professionnel (IUP), est un établissement
    d'enseignement supérieur situé à Nouakchott, en Mauritanie. Il propose des formations
    professionnalisantes en sciences appliquées, en gestion et en mathématiques appliquées.

    La **Licence Professionnelle MAEF** offre une formation pluridisciplinaire à l'intersection
    des mathématiques, de la statistique, de l'économie et de la finance. Elle prépare ses
    diplômés aux métiers d'analyste statistique, de chargé d'études économiques, ou à la
    poursuite d'études en master de statistique, d'économétrie ou de finance quantitative.
    """)

    st.markdown("---")
    st.markdown("## La structure d'accueil")
    st.markdown("""
    **Agence Nationale de la Statistique et de l'Analyse Démographique et Économique (ANSADE)**

    L'ANSADE est l'**institution officielle en charge de la production statistique** en
    République Islamique de Mauritanie. Elle assure la collecte, le traitement, l'analyse
    et la diffusion des données statistiques nationales dans les domaines économique,
    démographique et social.

    À ce titre, l'ANSADE produit notamment l'**Indice de la Production Industrielle (IPI)**,
    objet de la présente étude, ainsi que les principaux indicateurs macroéconomiques du pays.
    """)

    st.markdown("---")
    st.markdown("## Encadrement du projet")

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("**Encadrement académique**")
        st.markdown("**M. Merbe**")
        st.markdown("*Institut Supérieur de Génie Industriel (ISGI)*")
        st.markdown("Encadrant pédagogique et superviseur méthodologique du projet de fin d'études.")

    with col2:
        st.markdown("**Encadrement professionnel**")
        st.markdown("**M. Diop** · **M. Zeine**")
        st.markdown("*Agence Nationale de la Statistique et de l'Analyse Démographique et Économique (ANSADE)*")
        st.markdown("Encadrants professionnels lors du stage à l'ANSADE.")

    st.markdown("---")
    st.markdown("## Ressources du projet")
    st.markdown("""
    Le code source de ce tableau de bord est disponible publiquement sur GitHub :
    [github.com/diaomar22/pfe-dashboard](https://github.com/diaomar22/pfe-dashboard)

    Le tableau de bord est hébergé sur Streamlit Community Cloud :
    [ipi-mauritanie.streamlit.app](https://ipi-mauritanie.streamlit.app)
    """)

    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; color: #6b6b6b; font-size: 13px; padding: 20px 0;'>
    Tableau de bord réalisé dans le cadre du Projet de Fin d'Études<br>
    Licence Professionnelle en Mathématiques Appliquées à l'Économie et à la Finance — Promotion 2025–2026<br>
    Institut Supérieur de Génie Industriel · Nouakchott, Mauritanie
    </div>
    """, unsafe_allow_html=True)
