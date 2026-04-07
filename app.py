import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots

st.set_page_config(
    page_title="CrossPass — Modelo de Negócio",
    page_icon="🏋️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Palette ───────────────────────────────────────────────────────────────────
PURPLE = "#534AB7"
PURPLE_DARK = "#3C3489"
PURPLE_LIGHT = "#EEEDFE"
TEAL = "#1D9E75"
CORAL = "#D85A30"
AMBER = "#BA7517"
GRAY = "#888780"

# ── CSS ───────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
    .metric-card {
        background: #f7f6fe;
        border-radius: 10px;
        padding: 1rem 1.2rem;
        border-left: 4px solid #534AB7;
    }
    .metric-label { font-size: 12px; color: #888780; margin-bottom: 4px; }
    .metric-value { font-size: 24px; font-weight: 600; color: #3C3489; }
    .metric-sub   { font-size: 11px; color: #888780; margin-top: 2px; }
    .section-title {
        font-size: 13px; font-weight: 600; color: #534AB7;
        text-transform: uppercase; letter-spacing: .06em; margin-bottom: .5rem;
    }
    .pitch-box {
        background: #f7f6fe; border-radius: 10px;
        padding: 1.2rem 1.4rem; border-left: 4px solid #534AB7;
        line-height: 1.75;
    }
    .tag {
        display: inline-block; background: #EEEDFE; color: #3C3489;
        border-radius: 6px; padding: 2px 10px; font-size: 12px;
        margin: 2px;
    }
    [data-testid="stSidebar"] { background: #3C3489; }
    [data-testid="stSidebar"] * { color: white !important; }
    [data-testid="stSidebar"] .stSlider > div > div { background: #534AB7; }
    h1 { color: #3C3489; }
    h2 { color: #534AB7; border-bottom: 1px solid #EEEDFE; padding-bottom: .3rem; }
    h3 { color: #3C3489; }
</style>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# SIDEBAR — inputs globais
# ══════════════════════════════════════════════════════════════════════════════
with st.sidebar:
    st.markdown("## 🏋️ CrossPass")
    st.markdown("### Premissas do Modelo")
    st.markdown("---")

    st.markdown("**Mercado**")
    n_boxes    = st.slider("Boxes ativos no Brasil", 300, 600, 440, 10)
    alunos_box = st.slider("Alunos por box", 50, 250, 175, 5)

    st.markdown("**Modelo CrossPass**")
    mensalidade = st.slider("Mensalidade (R$/mês)", 200, 500, 300, 10)
    take_rate   = st.slider("Take rate (%)", 15, 35, 25, 1) / 100
    adopt_y5    = st.slider("Adoção máx. Ano 5 (% TAM)", 3, 20, 10, 1) / 100
    saas_price  = st.slider("SaaS por box (R$/mês)", 100, 500, 250, 10)
    cac         = st.slider("CAC (R$/usuário)", 50, 500, 150, 10)
    churn_m     = st.slider("Churn mensal (%)", 2, 12, 5, 1) / 100
    salary      = st.slider("Salário médio CLT (R$/mês)", 6000, 15000, 9000, 500)

    st.markdown("**Valuation**")
    wacc  = st.slider("WACC / Hurdle rate (%)", 15, 45, 25, 1) / 100
    g_per = st.slider("Crescimento perpetuidade (%)", 1, 6, 3, 1) / 100

    st.markdown("**Captação**")
    seed    = st.number_input("Seed (R$)", 500_000, 5_000_000, 2_000_000, 100_000, format="%d")
    serie_a = st.number_input("Série A (R$, Ano 2)", 0, 15_000_000, 5_000_000, 500_000, format="%d")

# ══════════════════════════════════════════════════════════════════════════════
# CÁLCULOS CENTRAIS
# ══════════════════════════════════════════════════════════════════════════════
tam = n_boxes * alunos_box

# Growth fractions (Ano 0..5)
g_frac   = [0, 0.04, 0.14, 0.35, 0.65, 1.0]
pboxes   = [0, 22, 60, 120, 200, 300]
sboxes   = [0, 8, 22, 50, 100, 170]
hc       = [3, 6, 11, 18, 26, 35]
infra_a  = [50_000, 60_000, 120_000, 200_000, 300_000, 420_000]
comm_a   = [80_000, 120_000, 200_000, 300_000, 400_000, 500_000]
capex_a  = [50_000, 30_000, 30_000, 40_000, 50_000, 60_000]
capsoft  = [200_000, 80_000, 60_000, 40_000, 30_000, 20_000]

anos = ["Ano 0", "Ano 1", "Ano 2", "Ano 3", "Ano 4", "Ano 5"]

users    = [round(tam * adopt_y5 * f) for f in g_frac]
rev_b2c  = [u * mensalidade * 12 for u in users]
rev_saas = [sb * saas_price * 12 for sb in sboxes]
rev_net  = [b * take_rate + s for b, s in zip(rev_b2c, rev_saas)]

# Custos
team_cost = [h * salary * 12 for h in hc]
new_users = [max(0, users[i] - users[i-1]) if i > 0 else users[0] for i in range(6)]
mkt_cost  = [n * cac for n in new_users]
total_cost = [team_cost[i] + mkt_cost[i] + infra_a[i] + comm_a[i] for i in range(6)]

ebitda = [rev_net[i] - total_cost[i] for i in range(6)]

# D&A simplificado
amort = [capsoft[0]/3] + [sum(capsoft[max(0,i-2):i+1])/3 for i in range(1,6)]
ebit  = [ebitda[i] - amort[i] for i in range(6)]

# Impostos e Lucro Líquido
tax_rate = 0.34
ir = [max(0, -e * tax_rate) for e in ebit]
net_income = [ebit[i] - ir[i] for i in range(6)]

# Caixa acumulado
cum_burn = []
cb = 0
for e in ebitda:
    cb += min(0, e)
    cum_burn.append(cb)
max_burn = abs(min(cum_burn))

# FCO / FCI / FCF
fco = [net_income[i] + amort[i] for i in range(6)]
fci = [-(capex_a[i] + capsoft[i]) for i in range(6)]
fcf_fin = [seed if i == 0 else (serie_a if i == 2 else 0) for i in range(6)]
delta_cash = [fco[i] + fci[i] + fcf_fin[i] for i in range(6)]
cash = []
c = 0
for d in delta_cash:
    c += d
    cash.append(c)

# FCFF para DCF
nopat = [max(0, ebit[i]) * (1 - tax_rate) for i in range(6)]
fcff  = [nopat[i] + amort[i] - capex_a[i] - capsoft[i] for i in range(6)]

pv_fcff = sum(fcff[i+1] / (1+wacc)**(i+1) for i in range(5))
tv = fcff[5] * (1 + g_per) / (wacc - g_per) if wacc > g_per else 0
pv_tv = tv / (1+wacc)**5
npv = pv_fcff + pv_tv

# IRR
irr_flows = [-seed] + fcff[1:5] + [fcff[5] + tv]
try:
    from numpy_financial import irr as np_irr
    irr_val = np_irr(irr_flows)
except:
    # manual IRR approx
    irr_val = None

# Unit Economics
mrr_net   = mensalidade * take_rate
ltv       = mrr_net / churn_m
ltv_cac   = ltv / cac
payback_m = cac / mrr_net
churn_annual = 1 - (1 - churn_m)**12
retention = (1 - churn_m)**12

# Break-even
bey = next((i for i, e in enumerate(ebitda) if e > 0), None)

# ══════════════════════════════════════════════════════════════════════════════
# PÁGINAS
# ══════════════════════════════════════════════════════════════════════════════
page = st.sidebar.radio(
    "Navegação",
    ["Visão Geral", "Mercado", "Modelo Financeiro",
     "Valuation & DCF", "Unit Economics", "Cenários",
     "Business Canvas", "Pitch"],
    label_visibility="collapsed"
)

def fmt_brl(v, suffix=""):
    if abs(v) >= 1_000_000:
        return f"R$ {v/1_000_000:.1f}M{suffix}"
    if abs(v) >= 1_000:
        return f"R$ {v/1_000:.0f}k{suffix}"
    return f"R$ {v:.0f}{suffix}"

def metric(label, value, sub=""):
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">{label}</div>
        <div class="metric-value">{value}</div>
        <div class="metric-sub">{sub}</div>
    </div>""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
if page == "Visão Geral":
# ══════════════════════════════════════════════════════════════════════════════
    st.title("🏋️ CrossPass")
    st.markdown("##### Marketplace de CrossFit — Modelo de Negócio Integrado")
    st.markdown("---")

    c1, c2, c3, c4 = st.columns(4)
    with c1: metric("Usuários Ano 5", f"{users[5]:,.0f}", f"{adopt_y5*100:.0f}% do TAM")
    with c2: metric("Receita Líq. Ano 5", fmt_brl(rev_net[5]), "B2C + SaaS")
    with c3: metric("Capital Necessário", fmt_brl(max_burn), "pico de queima")
    with c4: metric("Break-even", f"Ano {bey}" if bey else "Após Y5", "1º EBITDA positivo")

    st.markdown("---")
    c1, c2 = st.columns(2)

    with c1:
        st.subheader("EBITDA x Receita Líquida")
        fig = go.Figure()
        fig.add_bar(x=anos, y=[r/1e6 for r in rev_net],
                    name="Receita Líquida", marker_color=PURPLE, opacity=0.85)
        fig.add_scatter(x=anos, y=[e/1e6 for e in ebitda],
                        name="EBITDA", line=dict(color=TEAL, width=2.5),
                        mode="lines+markers", marker=dict(size=7))
        fig.add_hline(y=0, line_dash="dot", line_color=CORAL, line_width=1)
        fig.update_layout(height=320, margin=dict(t=10,b=10,l=10,r=10),
                          legend=dict(orientation="h", y=1.1),
                          yaxis_title="R$ milhões",
                          plot_bgcolor="white", paper_bgcolor="white")
        st.plotly_chart(fig, use_container_width=True)

    with c2:
        st.subheader("Caixa Acumulado")
        colors = [TEAL if c >= 0 else CORAL for c in cash]
        fig2 = go.Figure()
        fig2.add_bar(x=anos, y=[c/1e6 for c in cash],
                     marker_color=colors, opacity=0.85)
        fig2.add_hline(y=0, line_dash="dot", line_color=GRAY, line_width=1)
        fig2.update_layout(height=320, margin=dict(t=10,b=10,l=10,r=10),
                           yaxis_title="R$ milhões",
                           plot_bgcolor="white", paper_bgcolor="white")
        st.plotly_chart(fig2, use_container_width=True)

    st.markdown("---")
    c1, c2, c3, c4 = st.columns(4)
    with c1: metric("TAM", f"{tam:,.0f} praticantes", f"{n_boxes} boxes × {alunos_box} alunos")
    with c2: metric("LTV / CAC", f"{ltv_cac:.1f}x", "Meta: > 3x")
    with c3: metric("VPL (NPV)", fmt_brl(npv), f"WACC {wacc*100:.0f}%")
    with c4: metric("Margem EBITDA Y5", f"{ebitda[5]/rev_net[5]*100:.0f}%" if rev_net[5]>0 else "—", "Ano 5")

# ══════════════════════════════════════════════════════════════════════════════
elif page == "Mercado":
# ══════════════════════════════════════════════════════════════════════════════
    st.title("Análise de Mercado")

    c1, c2, c3 = st.columns(3)
    with c1: metric("TAM", f"{tam:,.0f}", f"{n_boxes} boxes × {alunos_box} alunos/box")
    with c2: metric("SAM (5 capitais)", f"{int(tam*0.63):,.0f}", "SP, RJ, BH, CWB, POA — 63% dos boxes")
    with c3: metric("SOM (Ano 5)", f"{users[5]:,.0f}", f"{adopt_y5*100:.0f}% de penetração")

    st.markdown("---")
    c1, c2 = st.columns(2)

    with c1:
        st.subheader("Funil TAM / SAM / SOM")
        fig = go.Figure(go.Funnel(
            y=["TAM — CrossFit BR", "SAM — 5 capitais", "SOM — Ano 5"],
            x=[tam, int(tam*0.63), users[5]],
            marker_color=[PURPLE_DARK, PURPLE, TEAL],
            textinfo="value+percent initial",
        ))
        fig.update_layout(height=320, margin=dict(t=10,b=10,l=10,r=10),
                          plot_bgcolor="white", paper_bgcolor="white")
        st.plotly_chart(fig, use_container_width=True)

    with c2:
        st.subheader("Crescimento de Usuários")
        fig2 = go.Figure()
        fig2.add_bar(x=anos, y=users, marker_color=PURPLE, opacity=0.85, name="Usuários")
        fig2.update_layout(height=320, margin=dict(t=10,b=10,l=10,r=10),
                           yaxis_title="Usuários ativos",
                           plot_bgcolor="white", paper_bgcolor="white")
        st.plotly_chart(fig2, use_container_width=True)

    st.markdown("---")
    st.subheader("Distribuição de Boxes por Estado (amostra)")
    estados = {"SP": 180, "RJ": 97, "MG": 40, "PR": 30, "RS": 25,
               "DF": 15, "CE": 12, "GO": 12, "SC": 10, "BA": 10, "Outros": 19}
    df_estados = pd.DataFrame({"Estado": list(estados.keys()),
                                "Boxes": list(estados.values())})
    fig3 = px.bar(df_estados, x="Estado", y="Boxes",
                  color_discrete_sequence=[PURPLE])
    fig3.update_layout(height=280, margin=dict(t=10,b=10,l=10,r=10),
                       plot_bgcolor="white", paper_bgcolor="white")
    st.plotly_chart(fig3, use_container_width=True)
    st.caption("Fonte: crossfit.com/gyms/brazil (mar/2026). SP inclui cidade e interior.")

    st.markdown("---")
    st.subheader("Benchmarks de Mercado")
    bm = {
        "Mercado global CrossFit (USD)": "US$ 2,8–4,0 bilhões",
        "Crescimento anual projetado": "7–12% a.a.",
        "ClassPass — receita esperada 2024": "US$ 500M (+20% YoY)",
        "Ocupação média de academia": "37% da capacidade (ClassPass, 2026)",
        "Crescimento de reservas fitness 2025": "+36% YoY (ClassPass, 2026)",
        "CrossFit Open 2024 — participantes BR": "3º país em inscritos globais",
    }
    for k, v in bm.items():
        cols = st.columns([2,3])
        cols[0].markdown(f"**{k}**")
        cols[1].markdown(v)

# ══════════════════════════════════════════════════════════════════════════════
elif page == "Modelo Financeiro":
# ══════════════════════════════════════════════════════════════════════════════
    st.title("Modelo Financeiro")

    tab1, tab2, tab3 = st.tabs(["DRE", "Fluxo de Caixa", "Balanço Resumido"])

    with tab1:
        st.subheader("Demonstração do Resultado (R$)")
        repasse = [-r * (1 - take_rate) for r in rev_b2c]
        taxas   = [-r * 0.02 for r in rev_b2c]
        rec_liq = [rev_b2c[i] + repasse[i] + taxas[i] + rev_saas[i] for i in range(6)]
        marg_b  = [rec_liq[i] / (rev_b2c[i] + rev_saas[i]) * 100
                   if (rev_b2c[i]+rev_saas[i]) > 0 else 0 for i in range(6)]

        df_dre = pd.DataFrame({
            "Item": [
                "Usuários ativos", "Receita Bruta B2C", "Receita SaaS",
                "Receita Bruta Total", "(-) Repasse aos boxes",
                "(-) Taxa processadora (2%)", "Receita Líquida",
                "(-) Time", "(-) Marketing (CAC)", "(-) Infra + Cloud",
                "(-) Custo comercial", "EBITDA", "Margem EBITDA %",
                "(-) D&A", "EBIT", "Lucro Líquido"
            ]
        })
        for i, ano in enumerate(anos):
            df_dre[ano] = [
                f"{users[i]:,.0f}",
                fmt_brl(rev_b2c[i]),
                fmt_brl(rev_saas[i]),
                fmt_brl(rev_b2c[i]+rev_saas[i]),
                fmt_brl(repasse[i]),
                fmt_brl(taxas[i]),
                fmt_brl(rec_liq[i]),
                fmt_brl(-team_cost[i]),
                fmt_brl(-mkt_cost[i]),
                fmt_brl(-infra_a[i]),
                fmt_brl(-comm_a[i]),
                fmt_brl(ebitda[i]),
                f"{ebitda[i]/rec_liq[i]*100:.1f}%" if rec_liq[i]>0 else "—",
                fmt_brl(-amort[i]),
                fmt_brl(ebit[i]),
                fmt_brl(net_income[i]),
            ]

        st.dataframe(df_dre.set_index("Item"), use_container_width=True)

        st.subheader("Composição da Receita")
        fig = go.Figure()
        fig.add_bar(x=anos, y=[r/1e6 for r in rev_b2c],
                    name="B2C (bruto)", marker_color=PURPLE, opacity=0.8)
        fig.add_bar(x=anos, y=[r/1e6 for r in rev_saas],
                    name="SaaS", marker_color=TEAL, opacity=0.8)
        fig.add_scatter(x=anos, y=[e/1e6 for e in ebitda],
                        name="EBITDA", line=dict(color=CORAL, width=2),
                        mode="lines+markers")
        fig.update_layout(barmode="stack", height=320,
                          yaxis_title="R$ milhões",
                          margin=dict(t=10,b=10,l=10,r=10),
                          legend=dict(orientation="h", y=1.1),
                          plot_bgcolor="white", paper_bgcolor="white")
        st.plotly_chart(fig, use_container_width=True)

    with tab2:
        st.subheader("Fluxo de Caixa (R$)")
        df_cf = pd.DataFrame({"Item": [
            "FCO — Lucro Líquido", "FCO — D&A (não-caixa)",
            "Caixa Operacional (FCO)",
            "(-) Capex hardware", "(-) Software capitalizado",
            "Caixa Investimentos (FCI)",
            "(+) Captação Seed", "(+) Captação Série A",
            "Caixa Financiamentos (FCF)",
            "Variação Líquida de Caixa", "CAIXA FINAL"
        ]})
        for i, ano in enumerate(anos):
            df_cf[ano] = [
                fmt_brl(net_income[i]),
                fmt_brl(amort[i]),
                fmt_brl(fco[i]),
                fmt_brl(-capex_a[i]),
                fmt_brl(-capsoft[i]),
                fmt_brl(fci[i]),
                fmt_brl(seed if i==0 else 0),
                fmt_brl(serie_a if i==2 else 0),
                fmt_brl(fcf_fin[i]),
                fmt_brl(delta_cash[i]),
                fmt_brl(cash[i]),
            ]
        st.dataframe(df_cf.set_index("Item"), use_container_width=True)

        fig2 = go.Figure()
        fig2.add_bar(x=anos, y=[f/1e6 for f in fco], name="FCO", marker_color=TEAL)
        fig2.add_bar(x=anos, y=[f/1e6 for f in fci], name="FCI", marker_color=CORAL)
        fig2.add_bar(x=anos, y=[f/1e6 for f in fcf_fin], name="FCF", marker_color=AMBER)
        fig2.add_scatter(x=anos, y=[c/1e6 for c in cash],
                         name="Caixa final", line=dict(color=PURPLE, width=2.5),
                         mode="lines+markers")
        fig2.update_layout(barmode="relative", height=320,
                           yaxis_title="R$ milhões",
                           margin=dict(t=10,b=10,l=10,r=10),
                           legend=dict(orientation="h", y=1.1),
                           plot_bgcolor="white", paper_bgcolor="white")
        st.plotly_chart(fig2, use_container_width=True)

    with tab3:
        st.subheader("Balanço Resumido (R$)")
        ar  = [rev_b2c[i] * 15/360 for i in range(6)]
        sw  = [sum(capsoft[:i+1]) - sum(amort[:i+1]) for i in range(6)]
        ap  = [rev_b2c[i] * (1-take_rate) * 30/360 for i in range(6)]
        cap_social = [seed + (serie_a if i >= 2 else 0) for i in range(6)]
        retain = [sum(net_income[:i+1]) for i in range(6)]
        pl  = [cap_social[i] + retain[i] for i in range(6)]

        df_bs = pd.DataFrame({"Item": [
            "Caixa", "Contas a Receber", "Software Líquido",
            "TOTAL ATIVO",
            "Contas a Pagar", "TOTAL PASSIVO",
            "Capital Social", "Lucros/Prejuízos Acum.",
            "PATRIMÔNIO LÍQUIDO",
            "TOTAL P + PL"
        ]})
        for i, ano in enumerate(anos):
            total_at = cash[i] + ar[i] + max(0, sw[i])
            total_pas = ap[i]
            df_bs[ano] = [
                fmt_brl(cash[i]), fmt_brl(ar[i]), fmt_brl(max(0,sw[i])),
                fmt_brl(total_at),
                fmt_brl(ap[i]), fmt_brl(total_pas),
                fmt_brl(cap_social[i]), fmt_brl(retain[i]),
                fmt_brl(pl[i]),
                fmt_brl(total_pas + pl[i]),
            ]
        st.dataframe(df_bs.set_index("Item"), use_container_width=True)

# ══════════════════════════════════════════════════════════════════════════════
elif page == "Valuation & DCF":
# ══════════════════════════════════════════════════════════════════════════════
    st.title("Valuation & DCF")

    c1, c2, c3 = st.columns(3)
    with c1: metric("VPL (NPV)", fmt_brl(npv), f"WACC {wacc*100:.0f}%, g {g_per*100:.0f}%")
    with c2: metric("Valor Terminal", fmt_brl(tv), f"Gordon Growth — g={g_per*100:.0f}%")
    with c3: metric("EV/Receita Ano 5", f"{npv/rev_net[5]:.1f}x" if rev_net[5]>0 else "—",
                    "múltiplo sobre receita líquida")

    st.markdown("---")
    c1, c2 = st.columns(2)

    with c1:
        st.subheader("FCFF por Ano")
        colors_fcff = [TEAL if f >= 0 else CORAL for f in fcff]
        fig = go.Figure()
        fig.add_bar(x=anos, y=[f/1e6 for f in fcff],
                    marker_color=colors_fcff, opacity=0.85)
        fig.add_hline(y=0, line_dash="dot", line_color=GRAY)
        fig.update_layout(height=300, yaxis_title="R$ milhões",
                          margin=dict(t=10,b=10,l=10,r=10),
                          plot_bgcolor="white", paper_bgcolor="white")
        st.plotly_chart(fig, use_container_width=True)

    with c2:
        st.subheader("Composição do VPL")
        labels = ["PV FCFFs (Y1-Y5)", "PV Valor Terminal"]
        values = [pv_fcff, pv_tv]
        colors_ = [PURPLE, TEAL]
        fig2 = go.Figure(go.Pie(labels=labels, values=values,
                                 marker_colors=colors_, hole=0.5,
                                 textinfo="label+percent"))
        fig2.update_layout(height=300, margin=dict(t=10,b=10,l=30,r=30),
                           showlegend=True)
        st.plotly_chart(fig2, use_container_width=True)

    st.markdown("---")
    st.subheader("Tabela de Sensibilidade — VPL (R$ M) vs WACC × g")
    wacc_range = [0.20, 0.25, 0.30, 0.35, 0.40]
    g_range    = [0.02, 0.03, 0.04, 0.05]

    sens_data = []
    for gv in g_range:
        row_s = []
        for wv in wacc_range:
            if wv <= gv:
                row_s.append(float("nan"))
                continue
            pv_f = sum(fcff[i+1]/(1+wv)**(i+1) for i in range(5))
            tv_s = fcff[5]*(1+gv)/(wv-gv)/(1+wv)**5
            row_s.append(round((pv_f + tv_s)/1e6, 1))
        sens_data.append(row_s)

    df_sens = pd.DataFrame(sens_data,
                           index=[f"g={int(g*100)}%" for g in g_range],
                           columns=[f"WACC={int(w*100)}%" for w in wacc_range])

    fig3 = go.Figure(go.Heatmap(
        z=df_sens.values,
        x=df_sens.columns.tolist(),
        y=df_sens.index.tolist(),
        colorscale=[[0, CORAL],[0.5, "#EEEDFE"],[1, TEAL]],
        text=[[f"R${v:.1f}M" if not np.isnan(v) else "N/A"
               for v in row] for row in df_sens.values],
        texttemplate="%{text}",
        showscale=True,
    ))
    fig3.update_layout(height=280, margin=dict(t=10,b=10,l=80,r=10))
    st.plotly_chart(fig3, use_container_width=True)

    # IRR calc via numpy
    st.markdown("---")
    st.subheader("TIR (IRR) e Múltiplos")
    c1, c2, c3 = st.columns(3)

    irr_flows_arr = np.array([-seed] + fcff[1:5] + [fcff[5]+tv])
    try:
        coeffs = np.poly1d(irr_flows_arr[::-1])
        roots = np.roots(coeffs)
        real_roots = [r.real for r in roots if abs(r.imag) < 1e-6 and r.real > 0]
        irr_est = min(real_roots) - 1 if real_roots else None
    except:
        irr_est = None

    with c1:
        irr_str = f"{irr_est*100:.1f}%" if irr_est and 0 < irr_est < 5 else "Calcular no Excel"
        metric("TIR (IRR)", irr_str, "sobre investimento inicial")
    with c2:
        metric("EV/EBITDA Ano 5",
               f"{npv/ebitda[5]:.1f}x" if ebitda[5]>0 else "N/A",
               "múltiplo EV/EBITDA")
    with c3:
        metric("Payback Simples",
               f"{seed/max(1,cash[5]/5):.1f} anos",
               "estimativa sobre caixa gerado")

# ══════════════════════════════════════════════════════════════════════════════
elif page == "Unit Economics":
# ══════════════════════════════════════════════════════════════════════════════
    st.title("Unit Economics")

    c1, c2, c3, c4 = st.columns(4)
    with c1: metric("MRR líquido / usuário", f"R$ {mrr_net:.0f}/mês", "mensalidade × take rate")
    with c2: metric("LTV", fmt_brl(ltv), f"vida média {1/churn_m:.0f} meses")
    with c3: metric("CAC", f"R$ {cac:,.0f}", "custo de aquisição")
    with c4:
        color = TEAL if ltv_cac >= 3 else CORAL
        metric("LTV / CAC", f"{ltv_cac:.1f}x", "meta: acima de 3x")

    st.markdown("---")
    c1, c2 = st.columns(2)

    with c1:
        st.subheader("Curva de Recuperação do CAC")
        months = list(range(1, 37))
        cum_rev = [mrr_net * m for m in months]
        cac_line = [cac] * len(months)
        payback_month = next((m for m, r in zip(months, cum_rev) if r >= cac), None)

        fig = go.Figure()
        fig.add_scatter(x=months, y=cum_rev, name="Receita acumulada",
                        line=dict(color=TEAL, width=2.5), fill="tozeroy",
                        fillcolor="rgba(29,158,117,0.1)")
        fig.add_scatter(x=months, y=cac_line, name="CAC",
                        line=dict(color=CORAL, width=2, dash="dash"))
        if payback_month:
            fig.add_vline(x=payback_month, line_dash="dot",
                          line_color=PURPLE, annotation_text=f"Payback: {payback_month}m")
        fig.update_layout(height=300, xaxis_title="Meses",
                          yaxis_title="R$",
                          margin=dict(t=10,b=10,l=10,r=10),
                          legend=dict(orientation="h", y=1.1),
                          plot_bgcolor="white", paper_bgcolor="white")
        st.plotly_chart(fig, use_container_width=True)

    with c2:
        st.subheader("Curva de Retenção de Cohort")
        months_r = list(range(0, 25))
        retention_curve = [(1-churn_m)**m for m in months_r]

        fig2 = go.Figure()
        fig2.add_scatter(x=months_r, y=[r*100 for r in retention_curve],
                         fill="tozeroy", line=dict(color=PURPLE, width=2.5),
                         fillcolor="rgba(83,74,183,0.1)")
        fig2.add_hline(y=50, line_dash="dot", line_color=GRAY,
                       annotation_text="50% restantes")
        fig2.update_layout(height=300, xaxis_title="Meses após aquisição",
                           yaxis_title="% usuários retidos",
                           margin=dict(t=10,b=10,l=10,r=10),
                           plot_bgcolor="white", paper_bgcolor="white")
        st.plotly_chart(fig2, use_container_width=True)

    st.markdown("---")
    st.subheader("Sensibilidade LTV/CAC vs Take Rate × Churn")
    takes = [0.15, 0.20, 0.25, 0.30, 0.35]
    churns = [0.03, 0.05, 0.07, 0.10, 0.12]
    matrix = [[round((mensalidade*t/c)/cac, 1) for t in takes] for c in churns]
    df_ltv = pd.DataFrame(matrix,
                          index=[f"Churn {int(c*100)}%/mês" for c in churns],
                          columns=[f"Take {int(t*100)}%" for t in takes])

    def color_ltvcac(val):
        if val >= 5: return f"background-color: {TEAL}; color: white"
        elif val >= 3: return f"background-color: {PURPLE_LIGHT}; color: {PURPLE_DARK}"
        else: return f"background-color: #fce8e8; color: {CORAL}"

    st.dataframe(df_ltv.style.applymap(color_ltvcac), use_container_width=True)
    st.caption("Verde = excelente (>5x) | Roxo = saudável (3-5x) | Vermelho = abaixo do mínimo (<3x)")

    st.markdown("---")
    st.subheader("Cohort — Receita Acumulada por Coorte")
    ret_annual = (1 - churn_m)**12
    cohort_data = {}
    for cy in range(1, 6):
        nu = new_users[cy]
        row_r = []
        for obs in range(6):
            age = obs - cy
            if age < 0:
                row_r.append(0)
            else:
                retained = nu * ret_annual**age
                row_r.append(retained * mensalidade * take_rate * 12)
        cohort_data[f"Coorte Ano {cy}"] = row_r

    df_cohort = pd.DataFrame(cohort_data, index=anos).T
    fig3 = px.bar(df_cohort, barmode="stack",
                  color_discrete_sequence=[PURPLE_DARK, PURPLE, "#7F77DD", "#AFA9EC", PURPLE_LIGHT])
    fig3.update_layout(height=300, yaxis_title="Receita líquida (R$)",
                       xaxis_title="Ano de observação",
                       margin=dict(t=10,b=10,l=10,r=10),
                       legend=dict(orientation="h", y=1.15),
                       plot_bgcolor="white", paper_bgcolor="white")
    st.plotly_chart(fig3, use_container_width=True)

# ══════════════════════════════════════════════════════════════════════════════
elif page == "Cenários":
# ══════════════════════════════════════════════════════════════════════════════
    st.title("Análise de Cenários")

    scenarios = {
        "Pessimista": {"adopt": 0.05, "take": 0.20, "cac": 300, "churn": 0.08},
        "Base":       {"adopt": adopt_y5, "take": take_rate, "cac": cac, "churn": churn_m},
        "Otimista":   {"adopt": 0.18, "take": 0.30, "cac": 90,  "churn": 0.03},
    }

    results = {}
    for name, p in scenarios.items():
        u5 = round(tam * p["adopt"])
        rev5 = u5 * mensalidade * 12 * p["take"] + 170 * saas_price * 12
        team5 = 35 * salary * 12
        mkt5 = u5 * p["cac"]
        eb5 = rev5 - team5 - mkt5 - infra_a[5] - comm_a[5]
        ltv5 = mensalidade * p["take"] / p["churn"]
        lc5 = ltv5 / p["cac"]
        results[name] = {
            "Usuários Ano 5": u5,
            "Receita Líq. Ano 5 (R$)": rev5,
            "EBITDA Ano 5 (R$)": eb5,
            "Margem EBITDA %": eb5/rev5*100 if rev5 > 0 else 0,
            "LTV/CAC": lc5,
        }

    colors_s = {
        "Pessimista": CORAL,
        "Base": PURPLE,
        "Otimista": TEAL,
    }

    c1, c2, c3 = st.columns(3)
    for col, (name, res) in zip([c1,c2,c3], results.items()):
        with col:
            st.markdown(f"### {name}")
            for k, v in res.items():
                if isinstance(v, float) and k.endswith("%"):
                    metric(k, f"{v:.1f}%")
                elif isinstance(v, float) and "LTV" in k:
                    metric(k, f"{v:.1f}x")
                elif isinstance(v, int):
                    metric(k, f"{v:,.0f}")
                else:
                    metric(k, fmt_brl(v))
                st.markdown("")

    st.markdown("---")
    st.subheader("Comparação de EBITDA Ano 5")
    names = list(results.keys())
    ebitdas = [results[n]["EBITDA Ano 5 (R$)"] / 1e6 for n in names]
    fig = go.Figure(go.Bar(
        x=names, y=ebitdas,
        marker_color=[colors_s[n] for n in names],
        text=[f"R$ {v:.1f}M" for v in ebitdas],
        textposition="outside",
    ))
    fig.add_hline(y=0, line_dash="dot", line_color=GRAY)
    fig.update_layout(height=320, yaxis_title="R$ milhões",
                      margin=dict(t=30,b=10,l=10,r=10),
                      plot_bgcolor="white", paper_bgcolor="white")
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("Premissas por Cenário")
    df_prem = pd.DataFrame({
        "Premissa": ["Adoção máx. Ano 5", "Take rate", "CAC (R$)", "Churn mensal"],
        "Pessimista": ["5%", "20%", "R$ 300", "8%"],
        "Base": [f"{adopt_y5*100:.0f}%", f"{take_rate*100:.0f}%",
                 f"R$ {cac}", f"{churn_m*100:.0f}%"],
        "Otimista": ["18%", "30%", "R$ 90", "3%"],
    })
    st.dataframe(df_prem.set_index("Premissa"), use_container_width=True)

# ══════════════════════════════════════════════════════════════════════════════
elif page == "Business Canvas":
# ══════════════════════════════════════════════════════════════════════════════
    st.title("Business Model Canvas")

    canvas = {
        "Parceiros-Chave": [
            "Boxes de CrossFit e estúdios funcionais",
            "Empresas (RH / benefícios corporativos)",
            "Influenciadores fitness",
            "Provedores de pagamento",
        ],
        "Atividades-Chave": [
            "Desenvolvimento e manutenção da plataforma",
            "Parcerias com boxes",
            "Captação de usuários",
            "Gestão de pagamentos e billing",
            "Quality assurance dos boxes",
        ],
        "Proposta de Valor (Usuário)": [
            "Acesso flexível a múltiplos boxes",
            "Variedade sem fidelização a um local",
            "Experiência gamificada (PRs, rankings)",
            f"Mensalidade de R$ {mensalidade}/mês",
        ],
        "Proposta de Valor (Box)": [
            "Aumento de ocupação em horários ociosos",
            "Aquisição de novos alunos sem marketing",
            "Ferramentas de gestão (agenda, CRM)",
            "Receita incremental sem custo fixo",
        ],
        "Segmentos": [
            "Praticantes de CrossFit e funcional",
            "Boxes independentes (440 no BR)",
            "Pessoas que querem flexibilidade",
            "Empresas com benefício de bem-estar",
        ],
        "Canais": [
            "App mobile (canal principal)",
            "Parceria com boxes (aquisição local)",
            "Instagram e TikTok fitness",
            "Vendas B2B diretas (empresas)",
        ],
        "Recursos-Chave": [
            "Aplicativo e plataforma",
            "Rede de boxes parceiros",
            "Time de parcerias e suporte",
            "Algoritmo de pricing e ocupação",
        ],
        "Fontes de Receita": [
            f"Assinatura B2C: R$ {mensalidade}/mês ({take_rate*100:.0f}% take rate)",
            f"SaaS para boxes: R$ {saas_price}/mês",
            "Plano corporativo por funcionário",
        ],
        "Estrutura de Custos": [
            "Desenvolvimento de software",
            "Infraestrutura cloud e APIs",
            "Marketing e CAC",
            f"Time ({hc[3]} pessoas no Ano 3)",
            "Suporte ao cliente e comercial",
        ],
    }

    cols1 = st.columns(3)
    cols2 = st.columns(3)
    cols3 = st.columns(3)

    for col, (title, items) in zip(cols1 + cols2 + cols3, canvas.items()):
        with col:
            st.markdown(f'<div class="section-title">{title}</div>', unsafe_allow_html=True)
            for item in items:
                st.markdown(f"- {item}")

    st.markdown("---")
    st.markdown(f"""
    <div class="pitch-box">
    <b>Diferencial central:</b> efeito de rede local — mais boxes parceiros geram mais opções para o atleta,
    o que gera mais check-ins e mais receita para o box. O CrossPass só vence quando os dois lados vencem.
    </div>
    """, unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
elif page == "Pitch":
# ══════════════════════════════════════════════════════════════════════════════
    st.title("Pitch & Textos")

    tab1, tab2, tab3 = st.tabs(["Pitch 2 minutos", "Análise Completa", "Exportar"])

    with tab1:
        st.subheader("Pitch de 2 minutos")
        st.markdown(f"""
        <div class="pitch-box">
        O Brasil é o segundo país com mais boxes de CrossFit no mundo, com {n_boxes} unidades ativas
        e cerca de {tam:,.0f} praticantes. É uma comunidade apaixonada, que paga bem e treina com frequência.
        Mas tem um problema que ninguém resolveu ainda: falta flexibilidade. O atleta que viaja, que mora longe
        do trabalho ou que quer treinar em outro bairro não tem opção, ou falta ou paga duas mensalidades.
        <br><br>
        O CrossPass resolve isso. É um marketplace de assinatura mensal de R$ {mensalidade} que dá acesso
        a múltiplos boxes de CrossFit. O usuário assina uma vez e treina onde quiser, quando quiser.
        Para o box, é receita incremental em horário ocioso, sem custo de marketing próprio.
        <br><br>
        O modelo financeiro é saudável. Retemos {take_rate*100:.0f}% de cada assinatura e repassamos
        {(1-take_rate)*100:.0f}% aos boxes por check-in. Com CAC de R$ {cac} e churn mensal de {churn_m*100:.0f}%,
        o LTV/CAC chega a {ltv_cac:.1f}x, bem acima do mínimo de 3x que o mercado aceita.
        A projeção é atingir break-even no {"Ano " + str(bey) if bey else "Ano 3–4"} com capital
        necessário de aproximadamente {fmt_brl(max_burn)}.
        <br><br>
        O principal concorrente é o ClassPass, que é genérico e não tem nenhuma feature para a comunidade
        CrossFit. Esse é nosso diferencial: gamificação, PRs, rankings, tudo pensado para quem respira CrossFit.
        <br><br>
        A estratégia de lançamento é hiperlocal. Começamos em São Paulo, fechamos 20 boxes parceiros antes
        de abrir para usuários, e crescemos cidade por cidade. O próprio coach do box é nosso canal de
        aquisição, o que mantém o CAC baixo.
        <br><br>
        O mercado é de nicho, mas é um nicho com identidade, dinheiro e problema real. E ninguém está resolvendo direito.
        </div>
        """, unsafe_allow_html=True)

    with tab2:
        sections = {
            "Segmentação do público-alvo": f"""
O CrossPass atende três segmentos. O principal é o praticante de CrossFit urbano entre 25 e 40 anos
que paga em torno de R$ {mensalidade}/mês e valoriza performance e variedade. Dentro desse grupo,
o perfil mais valioso é o nômade urbano: profissional que trabalha longe de casa, viaja com frequência
ou enjoa de treinar sempre no mesmo lugar.

O segundo segmento são os boxes independentes com ocupação abaixo de 70%, que têm horários ociosos
e carecem de ferramentas de gestão. O terceiro, endereçável a partir do Ano 2, são empresas que
oferecem benefício de bem-estar e buscam alternativas ao Gympass para funcionários com perfil de alta performance.
""",
            "Dimensionamento do público-alvo": f"""
Com base em contagem direta do diretório crossfit.com/gyms/brazil em março de 2026, o Brasil tem
{n_boxes} boxes ativos. Usando a premissa de {alunos_box} alunos por box, o mercado total é de
aproximadamente {tam:,.0f} praticantes. O mercado endereçável se concentra nas cinco maiores capitais,
que respondem por 63% dos boxes, cerca de {int(tam*0.63):,.0f} praticantes.

A meta é atingir {adopt_y5*100:.0f}% desse universo em 5 anos, aproximadamente {users[5]:,.0f}
usuários pagantes, com EBITDA positivo a partir do {"Ano " + str(bey) if bey else "Ano 3–4"}.
""",
            "Precificação": f"""
O CrossPass cobra R$ {mensalidade}/mês, na paridade com a mensalidade média de um box nas capitais.
O argumento de venda é conveniência, não preço. Dos R$ {mensalidade}, {take_rate*100:.0f}% ficam com
o CrossPass e {(1-take_rate)*100:.0f}% são repassados aos boxes por check-in.

Existe também um plano SaaS de R$ {saas_price}/mês para boxes com mais de 80 alunos.
Com churn de {churn_m*100:.0f}% e CAC de R$ {cac}, o LTV/CAC é de {ltv_cac:.1f}x.
""",
        }

        for title, text in sections.items():
            st.markdown(f"### {title}")
            st.markdown(f'<div class="pitch-box">{text}</div>', unsafe_allow_html=True)
            st.markdown("")

    with tab3:
        st.subheader("Exportar dados do modelo")

        df_export = pd.DataFrame({
            "Ano": anos,
            "Usuários": users,
            "Receita Bruta B2C (R$)": rev_b2c,
            "Receita SaaS (R$)": rev_saas,
            "Receita Liquida (R$)": rev_net,
            "EBITDA (R$)": ebitda,
            "Caixa Final (R$)": cash,
            "FCFF (R$)": fcff,
        })

        csv = df_export.to_csv(index=False).encode("utf-8")
        st.download_button(
            label="Baixar CSV com projeções",
            data=csv,
            file_name="crosspass_projecoes.csv",
            mime="text/csv",
        )

        st.markdown("---")
        st.subheader("Resumo das premissas atuais")
        df_prem = pd.DataFrame({
            "Premissa": [
                "Boxes ativos", "Alunos por box", "TAM",
                "Mensalidade", "Take rate", "Adoção Ano 5",
                "SaaS/box", "CAC", "Churn mensal",
                "WACC", "g perpet.", "Seed", "Série A",
            ],
            "Valor": [
                n_boxes, alunos_box, tam,
                f"R$ {mensalidade}", f"{take_rate*100:.0f}%", f"{adopt_y5*100:.0f}%",
                f"R$ {saas_price}", f"R$ {cac}", f"{churn_m*100:.0f}%",
                f"{wacc*100:.0f}%", f"{g_per*100:.0f}%",
                fmt_brl(seed), fmt_brl(serie_a),
            ]
        })
        st.dataframe(df_prem.set_index("Premissa"), use_container_width=True)
