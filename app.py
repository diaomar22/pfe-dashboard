"""
Dashboard PFE - Prevision de l'IPI mauritanien par modele SARIMA
Oumar Abou DIA - Licence Professionnelle MAEF, ISGI - Stage ANSADE
Soutenance : Juillet 2026
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go

st.set_page_config(
    page_title="PFE - IPI Mauritanie",
    page_icon=None,
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================
# STYLE GLOBAL
# ============================================================
st.markdown("""
<style>
    .main .block-container {
        padding-top: 1.5rem;
        padding-bottom: 3rem;
        max-width: 1300px;
    }
    h1 {
        font-weight: 700;
        color: #0d1b2a;
        letter-spacing: -0.5px;
    }
    h2 {
        font-weight: 600;
        color: #1f3a68;
        margin-top: 2rem;
        padding-bottom: 0.5rem;
        border-bottom: 2px solid #e8ecf3;
    }
    h3 {
        font-weight: 600;
        color: #2c4566;
    }

    /* En-tete institutionnel */
    .institutional-header {
        background: #ffffff;
        border-radius: 12px;
        border: 1px solid #e8ecf3;
        padding: 1.1rem 1.4rem;
        margin-bottom: 1.5rem;
        box-shadow: 0 2px 8px rgba(0,0,0,0.04);
    }
    .institutional-row {
        display: flex;
        align-items: center;
        gap: 18px;
        padding-bottom: 12px;
        border-bottom: 1px solid #e8ecf3;
        margin-bottom: 12px;
    }
    .institutional-text-block { flex: 1; }
    .institutional-eyebrow {
        font-size: 10.5px;
        color: #6b7280;
        letter-spacing: 1.5px;
        margin: 0;
        font-weight: 600;
    }
    .institutional-line {
        font-size: 13px;
        color: #0d1b2a;
        margin: 3px 0 0;
        font-weight: 500;
    }
    .institutional-right {
        text-align: right;
        font-size: 11px;
        color: #6b7280;
    }
    .institutional-right p { margin: 2px 0; }
    .institutional-title {
        margin: 0;
        font-size: 24px;
        font-weight: 700;
        color: #0d1b2a;
        letter-spacing: -0.3px;
        line-height: 1.2;
    }
    .institutional-tagline {
        margin: 6px 0 0;
        color: #4a5d75;
        font-size: 14px;
        font-style: italic;
    }

    /* Bandeau resultat principal */
    .result-banner {
        background: linear-gradient(135deg, #ffffff 0%, #f5f9ff 100%);
        border-radius: 12px;
        border: 1px solid #d6e3f5;
        padding: 1.4rem 1.6rem;
        margin-bottom: 1.5rem;
        box-shadow: 0 2px 12px rgba(31, 58, 104, 0.08);
        display: flex;
        align-items: center;
        gap: 24px;
        flex-wrap: wrap;
    }
    .result-banner-text { flex: 1; min-width: 280px; }
    .result-banner-eyebrow {
        font-size: 11px;
        color: #1f3a68;
        letter-spacing: 1.5px;
        margin: 0 0 8px;
        font-weight: 700;
    }
    .result-banner-main {
        font-size: 26px;
        font-weight: 600;
        margin: 0 0 6px;
        color: #0d1b2a;
        line-height: 1.25;
    }
    .result-banner-main .accent {
        color: #1f3a68;
        font-weight: 700;
    }
    .result-banner-sub {
        font-size: 14px;
        color: #5a6473;
        margin: 0;
    }
    .quarter-pills {
        display: flex;
        gap: 14px;
        padding: 12px 16px;
        background: #eef4fc;
        border-radius: 10px;
        border: 1px solid #d6e3f5;
    }
    .quarter-pill { text-align: center; padding: 0 4px; }
    .quarter-pill-label {
        font-size: 10px;
        color: #1f3a68;
        margin: 0 0 4px;
        letter-spacing: 1.2px;
        font-weight: 700;
    }
    .quarter-pill-value {
        font-size: 18px;
        font-weight: 700;
        margin: 0;
        color: #1f3a68;
    }

    /* Cartes KPI a degrade */
    .kpi-card {
        background: linear-gradient(135deg, #1f3a68 0%, #2c5282 100%);
        padding: 1.5rem;
        border-radius: 12px;
        color: white;
        box-shadow: 0 4px 20px rgba(31, 58, 104, 0.25);
        text-align: left;
        height: 100%;
    }
    .kpi-card.gold {
        background: linear-gradient(135deg, #b08742 0%, #d4a157 100%);
        box-shadow: 0 4px 20px rgba(176, 135, 66, 0.25);
    }
    .kpi-card.burgundy {
        background: linear-gradient(135deg, #8b2635 0%, #b8344a 100%);
        box-shadow: 0 4px 20px rgba(139, 38, 53, 0.25);
    }
    .kpi-card.teal {
        background: linear-gradient(135deg, #2d6a5f 0%, #3d8a7a 100%);
        box-shadow: 0 4px 20px rgba(45, 106, 95, 0.25);
    }
    .kpi-card .kpi-label {
        font-size: 11px;
        text-transform: uppercase;
        letter-spacing: 1.5px;
        opacity: 0.9;
        margin-bottom: 0.5rem;
        font-weight: 600;
        color: white;
    }
    .kpi-card .kpi-value {
        font-size: 2.2rem;
        font-weight: 700;
        line-height: 1;
        margin-bottom: 0.3rem;
        color: white;
    }
    .kpi-card .kpi-sub {
        font-size: 12px;
        opacity: 0.85;
        font-style: italic;
        color: white;
    }

    /* Stats secondaires */
    .stat-card {
        background: white;
        padding: 1.1rem;
        border-radius: 10px;
        border-left: 4px solid #1f3a68;
        box-shadow: 0 2px 8px rgba(0,0,0,0.06);
        height: 100%;
    }
    .stat-card.min { border-left-color: #8b2635; }
    .stat-card.max { border-left-color: #2d6a5f; }
    .stat-card.last { border-left-color: #b08742; }
    .stat-card .stat-label {
        font-size: 10.5px;
        text-transform: uppercase;
        letter-spacing: 1px;
        color: #6b7280;
        font-weight: 700;
        margin-bottom: 0.4rem;
    }
    .stat-card .stat-value {
        font-size: 1.7rem;
        font-weight: 700;
        color: #0d1b2a;
        line-height: 1;
    }
    .stat-card .stat-sub {
        font-size: 12px;
        color: #6b7280;
        margin-top: 0.3rem;
        font-style: italic;
    }

    /* Bandeau d'info */
    .info-banner {
        background: linear-gradient(90deg, #f5f7fb 0%, #eef2f8 100%);
        border-left: 4px solid #1f3a68;
        padding: 1rem 1.5rem;
        border-radius: 8px;
        margin: 1.5rem 0;
        color: #2c4566;
        font-size: 14px;
        line-height: 1.6;
    }
    .info-banner strong { color: #0d1b2a; }

    /* Sidebar */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #f5f7fb 0%, #eef2f8 100%);
    }
</style>
""", unsafe_allow_html=True)

# ============================================================
# DRAPEAU MAURITANIEN (SVG)
# ============================================================
FLAG_SVG = """
<svg width="50" height="34" viewBox="0 0 300 200" xmlns="http://www.w3.org/2000/svg"
     style="border-radius: 3px; border: 1px solid #e8ecf3; display: block; flex-shrink: 0;">
    <rect width="300" height="200" fill="#00A95C"/>
    <rect width="300" height="20" fill="#D01C1F"/>
    <rect y="180" width="300" height="20" fill="#D01C1F"/>
    <polygon points="150,75 156.3,93.5 175.8,93.5 160.1,105 166.4,123.5 150,112 133.6,123.5 139.9,105 124.2,93.5 143.7,93.5" fill="#FFD700"/>
    <path d="M 80 110 Q 150 200 220 110 Q 150 165 80 110 Z" fill="#FFD700"/>
</svg>
"""

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
FC_AVG = sum(FC_MEAN) / 4  # 113.59

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
# COMPOSANTS HTML
# ============================================================
def institutional_header():
    return f"""
    <div class="institutional-header">
        <div class="institutional-row">
            {FLAG_SVG}
            <div class="institutional-text-block">
                <p class="institutional-eyebrow">RÉPUBLIQUE ISLAMIQUE DE MAURITANIE</p>
                <p class="institutional-line">ANSADE · ISGI · Licence Professionnelle MAEF</p>
            </div>
            <div class="institutional-right">
                <p><strong style="color:#0d1b2a;">PFE 2025–2026</strong></p>
                <p>Soutenance · Juillet 2026</p>
            </div>
        </div>
        <h1 class="institutional-title">Prévision de l'Indice de la Production Industrielle</h1>
        <p class="institutional-tagline">Outil d'aide à la décision conjoncturelle — Modèle SARIMA(0,1,2)(0,1,1)₄</p>
    </div>
    """

def result_banner():
    return f"""
    <div class="result-banner">
        <div class="result-banner-text">
            <p class="result-banner-eyebrow">RÉSULTAT PRINCIPAL · ANNÉE 2026</p>
            <p class="result-banner-main">IPI moyen attendu de <span class="accent">{FC_AVG:.1f} pts</span></p>
            <p class="result-banner-sub">avec un pic au quatrième trimestre à 116,7 points</p>
        </div>
        <div class="quarter-pills">
            <div class="quarter-pill"><p class="quarter-pill-label">T1</p><p class="quarter-pill-value">113,0</p></div>
            <div class="quarter-pill"><p class="quarter-pill-label">T2</p><p class="quarter-pill-value">111,2</p></div>
            <div class="quarter-pill"><p class="quarter-pill-label">T3</p><p class="quarter-pill-value">113,4</p></div>
            <div class="quarter-pill"><p class="quarter-pill-label">T4</p><p class="quarter-pill-value">116,7</p></div>
        </div>
    </div>
    """

def kpi_card(label, value, sub, variant=""):
    return f"""
    <div class="kpi-card {variant}">
        <div class="kpi-label">{label}</div>
        <div class="kpi-value">{value}</div>
        <div class="kpi-sub">{sub}</div>
    </div>
    """

def stat_card(label, value, sub, variant=""):
    return f"""
    <div class="stat-card {variant}">
        <div class="stat-label">{label}</div>
        <div class="stat-value">{value}</div>
        <div class="stat-sub">{sub}</div>
    </div>
    """

# ============================================================
# CONFIG GRAPHIQUES
# ============================================================
def style_fig(fig, height=500, y_title=""):
    fig.update_layout(
        height=height,
        plot_bgcolor='white',
        paper_bgcolor='white',
        font=dict(family="sans-serif", size=12, color="#2c4566"),
        yaxis_title=y_title,
        xaxis=dict(
            showgrid=False, tickangle=-45, nticks=12,
            tickfont=dict(size=11, color="#6b7280"),
            linecolor="#e8ecf3", linewidth=1
        ),
        yaxis=dict(
            gridcolor='#e8ecf3', tickfont=dict(size=11, color="#6b7280"),
            linecolor="#e8ecf3", zeroline=False
        ),
        margin=dict(t=30, b=70, l=60, r=30),
        hovermode='x unified'
    )
    return fig

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
    st.markdown("---")
    st.markdown("*Soutenance : Juillet 2026*")

# ============================================================
# PAGE 1 - ACCUEIL
# ============================================================
if section == "Accueil":
    st.markdown(institutional_header(), unsafe_allow_html=True)
    st.markdown(result_banner(), unsafe_allow_html=True)

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown(kpi_card("MAPE", "3,77 %", "Précision du modèle"), unsafe_allow_html=True)
    with c2:
        st.markdown(kpi_card("RMSE", "4,90", "Erreur quadratique", "teal"), unsafe_allow_html=True)
    with c3:
        st.markdown(kpi_card("AIC", "306,06", "Critère d'Akaike", "burgundy"), unsafe_allow_html=True)
    with c4:
        st.markdown(kpi_card("Observations", "60", "Trimestres 2011–2025", "gold"), unsafe_allow_html=True)

    st.markdown("")
    st.markdown("")

    col1, col2 = st.columns([3, 2])
    with col1:
        st.markdown("## Le projet en bref")
        st.markdown("""
        Modélisation et prévision de l'**Indice de la Production Industrielle (IPI)**
        de la Mauritanie à partir des données trimestrielles publiées par l'**ANSADE**.

        ### Méthode
        Modèle **SARIMA(0,1,2)(0,1,1)₄** appliqué à 60 observations trimestrielles
        (2011–2025), avec production de prévisions pour les 4 trimestres de 2026.

        ### Cadre académique
        Projet de Fin d'Études — **Licence Professionnelle en Mathématiques Appliquées
        à l'Économie et à la Finance (MAEF)**, Institut Supérieur de Génie Industriel
        (**ISGI**) — Stage à l'**ANSADE**.
        """)

    with col2:
        st.markdown("## En quelques chiffres")
        st.markdown(stat_card("Période d'étude", "15 ans", "2011 T1 → 2025 T4"), unsafe_allow_html=True)
        st.markdown("")
        st.markdown(stat_card("Horizon de prévision", "4 trimestres", "Année 2026 complète", "max"), unsafe_allow_html=True)
        st.markdown("")
        st.markdown(stat_card("Fréquence", "Trimestrielle", "m = 4 (saisonnalité)", "last"), unsafe_allow_html=True)

# ============================================================
# PAGE 2 - ANALYSE ET RESULTATS
# ============================================================
elif section == "Analyse et résultats":
    st.title("Analyse et résultats")
    st.markdown("")

    # ---- GRAPHIQUE 1 : SERIE + PREVISIONS AVEC ANNOTATIONS ----
    st.markdown("## Série historique et prévisions 2026")
    st.markdown("Évolution trimestrielle de l'IPI avec annotations contextuelles. La zone orange marque la période Covid-19, la zone bleue marque la phase de prévision.")

    fig1 = go.Figure()

    # Zone Covid (avril 2020 - decembre 2021 : indices 37 a 43 environ)
    fig1.add_vrect(
        x0="2020 T1", x1="2021 T4",
        fillcolor="rgba(216, 90, 48, 0.10)",
        line_width=0,
        annotation_text="Période Covid-19",
        annotation_position="top",
        annotation=dict(font=dict(size=11, color="#993C1D", family="sans-serif"))
    )

    # Zone prevision
    fig1.add_vrect(
        x0=PERIODS[-1], x1=FC_PERIOD[-1],
        fillcolor="rgba(31, 58, 104, 0.08)",
        line_width=0,
        annotation_text="Prévisions SARIMA",
        annotation_position="top",
        annotation=dict(font=dict(size=11, color="#1f3a68", family="sans-serif"))
    )

    # Ligne verticale "AUJOURD'HUI"
    fig1.add_vline(
        x=PERIODS[-1],
        line=dict(color="#6b7280", width=1.5, dash="dash"),
        annotation_text="AUJOURD'HUI",
        annotation_position="top right",
        annotation=dict(font=dict(size=10, color="#6b7280", family="sans-serif"))
    )

    # Serie observee
    fig1.add_trace(go.Scatter(
        x=PERIODS, y=IPI, mode='lines', name='IPI observé',
        line=dict(color=NAVY, width=3),
        fill='tozeroy', fillcolor='rgba(31,58,104,0.06)'
    ))

    # Intervalle de confiance et prevision
    fc_x = [PERIODS[-1]] + FC_PERIOD
    fc_y = [IPI[-1]] + FC_MEAN
    fc_lo = [IPI[-1]] + FC_LO
    fc_hi = [IPI[-1]] + FC_HI

    fig1.add_trace(go.Scatter(
        x=fc_x + fc_x[::-1], y=fc_hi + fc_lo[::-1],
        fill='toself', fillcolor='rgba(139,38,53,0.18)',
        line=dict(color='rgba(255,255,255,0)'),
        name='Intervalle 95 %'
    ))
    fig1.add_trace(go.Scatter(
        x=fc_x, y=fc_y, mode='lines+markers', name='Prévision 2026',
        line=dict(color=BURGUNDY, width=3, dash='dash'),
        marker=dict(size=11, color=BURGUNDY, line=dict(color='white', width=2))
    ))

    # Annotation : creux Covid (T2 2021)
    fig1.add_annotation(
        x="2021 T2", y=87.8,
        ax=0, ay=60,
        text="<b>Creux Covid-19</b><br>87,8 points",
        showarrow=True, arrowhead=2, arrowsize=1, arrowwidth=1.5,
        arrowcolor="#8b2635",
        font=dict(size=11, color="#8b2635", family="sans-serif"),
        bgcolor="rgba(255,255,255,0.9)",
        bordercolor="#8b2635", borderwidth=1, borderpad=4
    )

    # Annotation : maximum historique
    fig1.add_annotation(
        x="2024 T3", y=122.7,
        ax=0, ay=-50,
        text="<b>Maximum historique</b><br>122,7 points",
        showarrow=True, arrowhead=2, arrowsize=1, arrowwidth=1.5,
        arrowcolor="#2d6a5f",
        font=dict(size=11, color="#2d6a5f", family="sans-serif"),
        bgcolor="rgba(255,255,255,0.9)",
        bordercolor="#2d6a5f", borderwidth=1, borderpad=4
    )

    fig1 = style_fig(fig1, height=540, y_title="IPI (base 100 = 2017)")
    fig1.update_layout(
        yaxis=dict(range=[75, 138], gridcolor='#e8ecf3', tickfont=dict(size=11, color="#6b7280")),
        legend=dict(orientation='h', y=-0.15, x=0.5, xanchor='center',
                    bgcolor='rgba(255,255,255,0.9)', borderwidth=0)
    )
    st.plotly_chart(fig1, use_container_width=True)

    # Stats sous le graphique
    st.markdown("")
    mean_v = sum(IPI) / len(IPI)
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown(stat_card("Moyenne", f"{mean_v:.1f}", "Niveau central"), unsafe_allow_html=True)
    with c2:
        st.markdown(stat_card("Minimum", f"{min(IPI):.1f}", f"au {PERIODS[IPI.index(min(IPI))]}", "min"), unsafe_allow_html=True)
    with c3:
        st.markdown(stat_card("Maximum", f"{max(IPI):.1f}", f"au {PERIODS[IPI.index(max(IPI))]}", "max"), unsafe_allow_html=True)
    with c4:
        st.markdown(stat_card("Dernière valeur", f"{IPI[-1]:.1f}", f"au {PERIODS[-1]}", "last"), unsafe_allow_html=True)

    st.markdown("""
    <div class="info-banner">
    <strong>Lecture.</strong> Tendance haussière marquée à partir de 2018,
    creux significatif au T2 2021 (effet Covid-19), saisonnalité stable :
    <strong>T2 systématiquement bas, T4 systématiquement haut</strong>.
    </div>
    """, unsafe_allow_html=True)

    # ---- DECOMPOSITION ----
    st.markdown("## Décomposition de la série")
    st.markdown("Décomposition additive : **Y(t) = Tendance + Saisonnalité + Résidu**.")

    st.markdown("### Série observée")
    fig2a = go.Figure()
    fig2a.add_trace(go.Scatter(
        x=PERIODS, y=IPI, mode='lines',
        line=dict(color=NAVY, width=2.5),
        fill='tozeroy', fillcolor='rgba(31,58,104,0.08)',
        showlegend=False
    ))
    fig2a = style_fig(fig2a, height=320, y_title="IPI")
    fig2a.update_layout(yaxis=dict(range=[80, 130], gridcolor='#e8ecf3', tickfont=dict(size=11, color="#6b7280")))
    st.plotly_chart(fig2a, use_container_width=True)

    st.markdown("### Tendance")
    fig2b = go.Figure()
    fig2b.add_trace(go.Scatter(
        x=PERIODS, y=trend, mode='lines',
        line=dict(color=TEAL, width=3),
        fill='tozeroy', fillcolor='rgba(45,106,95,0.08)',
        showlegend=False
    ))
    fig2b = style_fig(fig2b, height=320, y_title="Tendance")
    fig2b.update_layout(yaxis=dict(range=[95, 120], gridcolor='#e8ecf3', tickfont=dict(size=11, color="#6b7280")))
    st.plotly_chart(fig2b, use_container_width=True)

    st.markdown("""
    <div class="info-banner">
    Croissance régulière à partir de 2018, après une période de stagnation 2011–2017.
    </div>
    """, unsafe_allow_html=True)

    st.markdown("### Saisonnalité")
    fig2c = go.Figure()
    fig2c.add_trace(go.Scatter(
        x=PERIODS, y=seasonal_full, mode='lines',
        line=dict(color=GOLD, width=2.5),
        showlegend=False
    ))
    fig2c = style_fig(fig2c, height=320, y_title="Saisonnalité")
    st.plotly_chart(fig2c, use_container_width=True)

    st.markdown("### Effet saisonnier moyen par trimestre")
    fig2d = go.Figure()
    colors_bars = [NAVY if v >= 0 else BURGUNDY for v in seasonal]
    fig2d.add_trace(go.Bar(
        x=["T1 (Janv-Mars)", "T2 (Avr-Juin)", "T3 (Juil-Sept)", "T4 (Oct-Déc)"],
        y=seasonal,
        marker=dict(color=colors_bars, line=dict(color='white', width=2)),
        text=[f"{v:+.2f}" for v in seasonal],
        textposition='outside',
        textfont=dict(size=15, color="#2c4566", family="sans-serif"),
        width=0.6
    ))
    fig2d = style_fig(fig2d, height=400, y_title="Écart à la moyenne (points)")
    fig2d.update_layout(
        xaxis=dict(showgrid=False, tickfont=dict(size=12, color="#2c4566"), linecolor="#e8ecf3")
    )
    st.plotly_chart(fig2d, use_container_width=True)

    st.markdown(f"""
    <div class="info-banner">
    <strong>T4</strong> est le plus dynamique ({seasonal[3]:+.2f} pts),
    <strong>T2</strong> le plus faible ({seasonal[1]:+.2f} pts).
    Cette saisonnalité justifie le choix d'un modèle SARIMA.
    </div>
    """, unsafe_allow_html=True)

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
    st.markdown("")

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
    st.markdown("")

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
        st.markdown("Dr. Benioug Merbe *(ISGI)*")
    with col2:
        st.markdown("**Professionnel**")
        st.markdown("M. Ezyn SEGNANE · M. Mamadou DIOP *(ANSADE)*")

    st.markdown("### Ressources")
    st.markdown("""
    - Code source : [github.com/diaomar22/pfe-dashboard](https://github.com/diaomar22/pfe-dashboard)
    - Dashboard en ligne : [ipi-mauritanie.streamlit.app](https://ipi-mauritanie.streamlit.app)
    """)
