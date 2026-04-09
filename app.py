import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as gobj
import plotly.express as px
from datetime import datetime, timedelta
import random

st.set_page_config(page_title="CrossPass", page_icon="⚡", layout="wide", initial_sidebar_state="collapsed")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&family=DM+Sans:wght@300;400;500;600&display=swap');
html,body,[class*="css"]{font-family:'DM Sans',sans-serif}
.hero{background:linear-gradient(135deg,#1e1548 0%,#0a0a0a 100%);border-radius:20px;padding:3rem 2rem;text-align:center;margin-bottom:2rem}
.hero-title{font-family:'Bebas Neue';font-size:72px;line-height:.88;color:#fafaf8;margin-bottom:1rem}
.hero-title span{color:#534AB7}
.hero-sub{font-size:16px;color:#aaa;line-height:1.65;max-width:520px;margin:0 auto 2rem}
.card{background:#111;border:1px solid #222;border-radius:14px;padding:1.2rem 1.4rem;margin-bottom:.75rem}
.card-dark{background:#0d0d0d;border:1px solid #1a1a1a;border-radius:14px;padding:1.2rem 1.4rem;margin-bottom:.75rem}
.stat-box{background:#111;border:1px solid #222;border-radius:12px;padding:1rem;text-align:center}
.stat-num{font-family:'Bebas Neue';font-size:36px;color:#534AB7;line-height:1}
.stat-lbl{font-size:10px;color:#888;text-transform:uppercase;letter-spacing:.08em;margin-top:3px}
.stat-sub{font-size:11px;color:#1D9E75;margin-top:4px}
.badge{display:inline-block;font-size:10px;font-weight:600;padding:3px 9px;border-radius:100px;margin:2px}
.badge-purple{background:#EEEDFE;color:#3C3489}
.badge-teal{background:#d0f0e4;color:#085041}
.badge-coral{background:#fce8e0;color:#712B13}
.badge-amber{background:#fef3cd;color:#633806}
.badge-dark{background:#1a1a1a;color:#888}
.pr-item{background:#111;border:1px solid #222;border-radius:10px;padding:12px 14px;display:flex;justify-content:space-between;align-items:center;margin-bottom:7px}
.pr-move{font-size:13px;font-weight:600;color:#fafaf8}
.pr-date{font-size:10px;color:#888;margin-top:2px}
.pr-val{font-family:'Bebas Neue';font-size:24px;color:#1D9E75}
.pr-prev{font-size:10px;color:#888;text-align:right;margin-top:2px}
.coach-card{background:#111;border:1px solid #222;border-radius:14px;padding:1.2rem;margin-bottom:.75rem}
.coach-name{font-size:15px;font-weight:600;color:#fafaf8;margin-bottom:2px}
.coach-spec{font-size:12px;color:#888;margin-bottom:8px}
.coach-price{font-family:'Bebas Neue';font-size:22px;color:#534AB7}
.rank-item{background:#111;border:1px solid #222;border-radius:10px;padding:10px 14px;display:flex;align-items:center;gap:12px;margin-bottom:6px}
.section-title{font-family:'Bebas Neue';font-size:22px;letter-spacing:.02em;color:#fafaf8;margin-bottom:.25rem}
.pill-metric{background:linear-gradient(135deg,#1a1230,#0d0d14);border:1px solid #2a2040;border-radius:12px;padding:.9rem 1rem;text-align:center}
.pill-val{font-family:'Bebas Neue';font-size:28px;color:#534AB7}
.pill-lbl{font-size:10px;color:#666;text-transform:uppercase;letter-spacing:.06em}
.wod-box{background:linear-gradient(135deg,#1a1040,#0a0a18);border:1px solid #2a2060;border-radius:14px;padding:1.2rem 1.4rem;margin-bottom:1rem}
.wod-title{font-family:'Bebas Neue';font-size:20px;color:#fafaf8;margin-bottom:.5rem}
.streak-bar{background:linear-gradient(90deg,#3C3489,#534AB7);border-radius:10px;padding:1rem 1.4rem;margin-bottom:1rem;display:flex;justify-content:space-between;align-items:center}
.topbar{position:sticky;top:0;z-index:999;background:#0a0a0a;border-bottom:1px solid #1a1a1a;padding:.5rem 1.5rem;display:flex;align-items:center;justify-content:space-between;margin-bottom:1.25rem;gap:1rem}
.topbar-logo{font-family:'Bebas Neue';font-size:22px;color:#534AB7;letter-spacing:.05em;white-space:nowrap}
.topbar-nav{display:flex;gap:4px;overflow-x:auto;flex:1;justify-content:center}
.topbar-btn{background:none;border:none;color:#666;padding:7px 14px;border-radius:8px;font-size:12px;font-weight:600;cursor:pointer;white-space:nowrap;transition:.15s;font-family:'DM Sans',sans-serif;letter-spacing:.02em}
.topbar-btn:hover{background:#1a1a1a;color:#fafaf8}
.topbar-btn.active{background:#534AB7;color:white}
.topbar-coins{display:flex;align-items:center;gap:6px;background:#1a1200;border:1px solid #3a2f00;border-radius:100px;padding:5px 14px;white-space:nowrap;flex-shrink:0}
.topbar-coin-val{font-family:'Bebas Neue';font-size:18px;color:#f59e0b;line-height:1}
section[data-testid="stSidebar"]{display:none}

.coins-bar{background:linear-gradient(90deg,#1a1200,#2a1f00);border:1px solid #3a2f00;border-radius:12px;padding:.7rem 1.2rem;display:flex;align-items:center;gap:10px;margin-bottom:1rem}
.coin-val{font-family:'Bebas Neue';font-size:28px;color:#f59e0b;line-height:1}
.product-card{background:#111;border:1px solid #222;border-radius:16px;overflow:hidden;margin-bottom:.75rem;transition:.15s}
.product-card:hover{border-color:#534AB7}
.product-img{width:100%;height:160px;display:flex;align-items:center;justify-content:center;font-size:56px}
.product-body{padding:1rem}
.product-name{font-size:14px;font-weight:600;color:#fafaf8;margin-bottom:3px}
.product-brand{font-size:11px;color:#888;margin-bottom:8px}
.product-price{font-family:'Bebas Neue';font-size:20px;color:#534AB7}
.product-coins{font-size:12px;color:#f59e0b;font-weight:600}
.coin-badge{display:inline-flex;align-items:center;gap:4px;background:#2a1f00;border:1px solid #3a2f00;color:#f59e0b;padding:3px 10px;border-radius:100px;font-size:11px;font-weight:600}
</style>
""", unsafe_allow_html=True)

# ── State ─────────────────────────────────────────────────────────────────────
DEFAULTS = {
    "page": "landing", "user": None, "checkins": 14,
    "coins": 850, "cart": [], "purchases": [],
    "challenge_progress": {"Outubro de Força": 14, "PR Challenge": 4, "Box Hopper": 3},
    "log_entries": [], "prs": {
        "Fran": {"val": "4:32", "prev": "5:10", "date": "3 dias atrás", "unit": "tempo"},
        "Clean & Jerk": {"val": "95", "prev": "90", "date": "1 semana atrás", "unit": "kg"},
        "Back Squat": {"val": "140", "prev": "132.5", "date": "2 semanas atrás", "unit": "kg"},
        "Cindy": {"val": "22", "prev": "19", "date": "1 mês atrás", "unit": "rounds"},
        "Dead Lift": {"val": "180", "prev": "172.5", "date": "1 mês atrás", "unit": "kg"},
        "Grace": {"val": "3:18", "prev": "3:55", "date": "2 meses atrás", "unit": "tempo"},
        "Snatch": {"val": "75", "prev": "70", "date": "3 semanas atrás", "unit": "kg"},
        "Helen": {"val": "8:42", "prev": "9:20", "date": "3 semanas atrás", "unit": "tempo"},
    }
}
for k, v in DEFAULTS.items():
    if k not in st.session_state:
        st.session_state[k] = v

def go(page):
    st.session_state.page = page
    st.rerun()

def badge(lbl, tipo="purple"):
    return f'<span class="badge badge-{tipo}">{lbl}</span>'

def stars(r):
    return "★" * int(r) + "☆" * (5 - int(r))

# ── Mock Data ─────────────────────────────────────────────────────────────────
COACHES = [
    {"id":1,"name":"Marcos Alves","spec":"Weightlifting & Competição","cert":"CF Level 3","rating":4.9,"reviews":87,"price":490,"students":34,"bio":"10 anos de experiência, 3x campeão estadual. Especialista em técnica de levantamento e programação de competição.","tags":["Competição","Levantamento","Programação"],"avatar":"MA"},
    {"id":2,"name":"Fernanda Costa","spec":"Fundamentos & Iniciantes","cert":"CF Level 2","rating":4.8,"reviews":64,"price":290,"students":28,"bio":"Especialista em ensinar CrossFit do zero. Método próprio de progressão para iniciantes com foco em movimento seguro.","tags":["Iniciantes","Técnica","Mobilidade"],"avatar":"FC"},
    {"id":3,"name":"Guilherme Ramos","spec":"Endurance & Metcons","cert":"CF Level 2 + USAW","rating":4.9,"reviews":112,"price":390,"students":51,"bio":"Ex-triatleta. Programação focada em capacidade aeróbica e metcons de alta intensidade. Atleta da temporada 2023.","tags":["Endurance","Metcon","Programação"],"avatar":"GR"},
    {"id":4,"name":"Patrícia Nunes","spec":"Mobilidade & Prevenção","cert":"CF Level 2 + Fisio","rating":5.0,"reviews":43,"price":450,"students":19,"bio":"Fisioterapeuta e coach CF Level 2. Trabalha recuperação de lesões e prevenção com foco em movimento funcional.","tags":["Mobilidade","Reabilitação","Força"],"avatar":"PN"},
    {"id":5,"name":"Diego Rocha","spec":"Força & Powerlifting","cert":"CF Level 2","rating":4.7,"reviews":55,"price":350,"students":22,"bio":"Background em powerlifting. Especialista em ciclos de força e periodização para atletas que querem ganhar carga.","tags":["Força","Ciclos","Periodização"],"avatar":"DR"},
]

PROGRAMS = [
    {"name":"8 Semanas de Força","coach":"Guilherme Ramos","price":197,"duration":"8 semanas","level":"Intermediário","description":"Ciclo completo de força com foco em squat, deadlift e press. Inclui vídeos de técnica e check-in semanal.","tags":["Força","Intermediário"]},
    {"name":"CrossFit do Zero","coach":"Fernanda Costa","price":97,"duration":"4 semanas","level":"Iniciante","description":"Programa de fundamentos para quem está começando. Aprenda os movimentos base com segurança e progressão.","tags":["Iniciante","Fundamentos"]},
    {"name":"Open Prep 2025","coach":"Marcos Alves","price":297,"duration":"12 semanas","level":"Avançado","description":"Preparação completa para o CrossFit Open. Programação dupla diária, simulados e análise de performance.","tags":["Competição","Avançado"]},
    {"name":"Mobilidade Diária","coach":"Patrícia Nunes","price":67,"duration":"Permanente","level":"Todos","description":"Protocolo diário de mobilidade e aquecimento. 15-20 min por dia para mover melhor e se lesionar menos.","tags":["Mobilidade","Prevenção"]},
]

PRODUCTS = [
    {"id":1,"cat":"Suplementos","name":"Whey Protein Isolado","brand":"Optimum Nutrition","emoji":"🥤","bg":"#1a2040","price_brl":189,"price_coins":1800,"stock":True,"desc":"2kg de whey isolado com 27g de proteína por dose. Sabor baunilha ou chocolate.","tags":["Proteína","Recuperação"]},
    {"id":2,"cat":"Suplementos","name":"Creatina Monohidratada","brand":"Growth Supplements","emoji":"⚡","bg":"#1a1040","price_brl":89,"price_coins":850,"stock":True,"desc":"300g de creatina pura. Aumento de força e potência nos treinos de alta intensidade.","tags":["Força","Performance"]},
    {"id":3,"cat":"Suplementos","name":"Pré-Treino ENERGY","brand":"Probiótica","emoji":"🔥","bg":"#2a1000","price_brl":129,"price_coins":1200,"stock":True,"desc":"Fórmula com cafeína, beta-alanina e citrulina. Foco e energia máxima para o WOD.","tags":["Energia","Foco"]},
    {"id":4,"cat":"Suplementos","name":"BCAA 2:1:1","brand":"Integral Médica","emoji":"💊","bg":"#0a2a1a","price_brl":79,"price_coins":750,"stock":True,"desc":"Aminoácidos essenciais para recuperação muscular. 60 doses por embalagem.","tags":["Recuperação","Músculo"]},
    {"id":5,"cat":"Roupas","name":"Shorts CrossFit Pro","brand":"CrossPass Wear","emoji":"🩳","bg":"#1a0a2a","price_brl":149,"price_coins":1400,"stock":True,"desc":"Shorts de compressão com tecnologia anti-odor. Ideal para WODs de alta intensidade. Tamanhos P ao GG.","tags":["Exclusivo","Performance"]},
    {"id":6,"cat":"Roupas","name":"Camiseta Dry-Fit","brand":"CrossPass Wear","emoji":"👕","bg":"#0a1a2a","price_brl":89,"price_coins":850,"stock":True,"desc":"Camiseta de treino com tecido respirável. Estampa CrossPass exclusiva. Unissex.","tags":["Exclusivo","Conforto"]},
    {"id":7,"cat":"Roupas","name":"Legging Compressão","brand":"CrossPass Wear","emoji":"🩱","bg":"#2a0a1a","price_brl":179,"price_coins":1700,"stock":False,"desc":"Legging de compressão feminina com bolso lateral. Tecido 4-way stretch.","tags":["Exclusivo","Feminino"]},
    {"id":8,"cat":"Roupas","name":"Meia Cano Alto","brand":"CrossPass Wear","emoji":"🧦","bg":"#1a1a0a","price_brl":49,"price_coins":450,"stock":True,"desc":"Pack com 3 meias cano alto para treino. Proteção contra o barbell.","tags":["Exclusivo","Proteção"]},
    {"id":9,"cat":"Equipamentos","name":"Jump Rope Speed Rope","brand":"RPM Speed","emoji":"🪢","bg":"#0a2a2a","price_brl":229,"price_coins":2200,"stock":True,"desc":"Corda de pular de alta velocidade. Cabo de aço com rolamento de precisão. Ideal para double-unders.","tags":["Ginástica","Velocidade"]},
    {"id":10,"cat":"Equipamentos","name":"Munhequeira WOD","brand":"RX Smart Gear","emoji":"🤸","bg":"#2a2a0a","price_brl":119,"price_coins":1100,"stock":True,"desc":"Munhequeira de couro para gymnastics e barbell. Proteção sem perder grip.","tags":["Proteção","Grip"]},
    {"id":11,"cat":"Equipamentos","name":"Knee Sleeves 7mm","brand":"SBD","emoji":"🦵","bg":"#1a0a0a","price_brl":289,"price_coins":2700,"stock":True,"desc":"Par de knee sleeves premium 7mm. Suporte e compressão para squats pesados.","tags":["Força","Proteção"]},
    {"id":12,"cat":"Equipamentos","name":"Chalk Magnésio 250g","brand":"Black Bear","emoji":"🤲","bg":"#1a1a1a","price_brl":39,"price_coins":370,"stock":True,"desc":"Magnésio em pó para grip em barbell, pull-ups e gymnastics. 250g.","tags":["Grip","Essential"]},
]

WOD_TODAY = {
    "name": "AMRAP 20",
    "movements": ["5 Pull-ups", "10 Push-ups", "15 Air Squats"],
    "score_type": "rounds",
    "rx_weight": None,
    "coach_tip": "Mantenha um ritmo sustentável desde o início. Mire em completar cada round em 1-1:30min.",
}

BOXES = [
    {"name":"CrossFit Itaim","loc":"SP","alunos":142,"churn":4.2,"ocupacao":71,"receita":46800,"rating":4.9},
    {"name":"CrossFit Leblon","loc":"RJ","alunos":98,"churn":5.1,"ocupacao":63,"receita":31200,"rating":4.8},
    {"name":"CrossFit Pinheiros","loc":"SP","alunos":87,"churn":3.8,"ocupacao":58,"receita":28400,"rating":4.7},
]

def gen_performance_data():
    dates = [datetime.now() - timedelta(days=x) for x in range(90, 0, -1)]
    base = 100
    data = []
    for d in dates:
        base += random.uniform(-2, 3)
        data.append({"date": d, "score": round(base, 1)})
    return pd.DataFrame(data)

def gen_volume_data():
    weeks = [f"S{i}" for i in range(1, 13)]
    return pd.DataFrame({
        "Semana": weeks,
        "Força": [random.randint(3, 8) for _ in weeks],
        "Metcon": [random.randint(4, 9) for _ in weeks],
        "Ginástica": [random.randint(1, 5) for _ in weeks],
    })

# ══════════════════════════════════════════════════════════════════════════════
# LANDING
# ══════════════════════════════════════════════════════════════════════════════
if st.session_state.page == "landing":
    st.markdown("""
    <div class="hero">
        <div class="hero-title">PERFORMANCE<br><span>SEM</span> TETO.</div>
        <p class="hero-sub">A plataforma de performance para atletas de CrossFit. Tracking de PRs, análise de evolução, coaches de elite e gestão para boxes — tudo em um lugar.</p>
    </div>
    """, unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown("""<div class="card" style="text-align:center;border-color:#2a2060">
            <div style="font-size:36px;margin-bottom:.5rem">📈</div>
            <div style="font-family:'Bebas Neue';font-size:18px;color:#fafaf8;margin-bottom:.3rem">Tracking de Performance</div>
            <div style="font-size:12px;color:#888">PRs, evolução, análise de volume e comparação com atletas do mesmo nível</div>
        </div>""", unsafe_allow_html=True)
    with c2:
        st.markdown("""<div class="card" style="text-align:center;border-color:#2a2060">
            <div style="font-size:36px;margin-bottom:.5rem">🏋️</div>
            <div style="font-family:'Bebas Neue';font-size:18px;color:#fafaf8;margin-bottom:.3rem">Coaches de Elite</div>
            <div style="font-size:12px;color:#888">Marketplace com coaches certificados e programas de treinamento personalizados</div>
        </div>""", unsafe_allow_html=True)
    with c3:
        st.markdown("""<div class="card" style="text-align:center;border-color:#2a2060">
            <div style="font-size:36px;margin-bottom:.5rem">🏢</div>
            <div style="font-family:'Bebas Neue';font-size:18px;color:#fafaf8;margin-bottom:.3rem">SaaS para Boxes</div>
            <div style="font-size:12px;color:#888">Gestão de turmas, analytics de alunos, CRM e retenção — tudo integrado</div>
        </div>""", unsafe_allow_html=True)

    st.markdown("---")
    c1, c2, c3, c4 = st.columns(4)
    with c1: st.markdown("<div class='stat-box'><div class='stat-num'>440</div><div class='stat-lbl'>Boxes parceiros</div></div>", unsafe_allow_html=True)
    with c2: st.markdown("<div class='stat-box'><div class='stat-num'>12k</div><div class='stat-lbl'>Atletas ativos</div></div>", unsafe_allow_html=True)
    with c3: st.markdown("<div class='stat-box'><div class='stat-num'>89</div><div class='stat-lbl'>Coaches certificados</div></div>", unsafe_allow_html=True)
    with c4: st.markdown("<div class='stat-box'><div class='stat-num'>4.9★</div><div class='stat-lbl'>Avaliação média</div></div>", unsafe_allow_html=True)

    st.markdown("")
    c1, c2, c3 = st.columns([1,2,1])
    with c2:
        st.markdown("### Escolha como entrar")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🏋️ Sou atleta", use_container_width=True, type="primary"):
                go("signup_athlete")
        with col2:
            if st.button("🏢 Tenho um box", use_container_width=True):
                go("signup_box")
        st.markdown("")
        if st.button("👤 Entrar com demo", use_container_width=True):
            st.session_state.user = {"name":"Rafael Santos","city":"São Paulo","plan":"Pro","tipo":"atleta","box":"CrossFit Itaim"}
            go("dashboard")

# ══════════════════════════════════════════════════════════════════════════════
# SIGNUP ATHLETE
# ══════════════════════════════════════════════════════════════════════════════
elif st.session_state.page == "signup_athlete":
    c1, c2, c3 = st.columns([1,2,1])
    with c2:
        st.markdown("### 🏋️ Cadastro do Atleta")
        st.caption("7 dias grátis em qualquer plano")

        with st.form("f_athlete"):
            name  = st.text_input("Nome completo", placeholder="Rafael Santos")
            email = st.text_input("E-mail", placeholder="rafael@email.com")
            senha = st.text_input("Senha", type="password")
            city  = st.selectbox("Cidade", ["São Paulo","Rio de Janeiro","Belo Horizonte","Curitiba","Porto Alegre"])
            box   = st.text_input("Box que você treina (opcional)", placeholder="CrossFit Itaim")
            nivel = st.select_slider("Nível", ["Iniciante","Intermediário","Avançado","Competidor"])

            st.markdown("**Escolha seu plano**")
            plan = st.radio("", [
                "Free — Gratuito (log de treinos e PRs básicos)",
                "Athlete — R$ 49/mês (analytics + ranking + comunidade)",
                "Pro — R$ 99/mês (coaching remoto + análise avançada + prioridade)",
            ], index=1)

            ok = st.form_submit_button("Criar conta →", use_container_width=True, type="primary")

        if ok:
            if not name:
                st.error("Digite seu nome.")
            else:
                st.session_state.user = {
                    "name": name, "city": city, "plan": plan.split("—")[0].strip(),
                    "tipo": "atleta", "nivel": nivel, "box": box or "Sem box fixo"
                }
                st.success(f"🎉 Bem-vindo, {name.split()[0]}!")
                st.balloons()
                go("dashboard")

        if st.button("← Voltar"):
            go("landing")

# ══════════════════════════════════════════════════════════════════════════════
# SIGNUP BOX
# ══════════════════════════════════════════════════════════════════════════════
elif st.session_state.page == "signup_box":
    c1, c2, c3 = st.columns([1,2,1])
    with c2:
        st.markdown("### 🏢 Cadastro do Box")
        st.caption("30 dias grátis, sem cartão de crédito")

        with st.form("f_box"):
            box_name  = st.text_input("Nome do box", placeholder="CrossFit Meu Box")
            owner     = st.text_input("Seu nome", placeholder="João Silva")
            email     = st.text_input("E-mail", placeholder="joao@meubox.com.br")
            city      = st.selectbox("Cidade", ["São Paulo","Rio de Janeiro","Belo Horizonte","Curitiba","Porto Alegre"])
            alunos    = st.number_input("Quantos alunos ativos?", 10, 500, 80)

            st.markdown("**Plano SaaS**")
            plan = st.radio("", [
                "Starter — R$ 199/mês (gestão básica, até 80 alunos)",
                "Growth — R$ 349/mês (analytics + CRM + até 200 alunos)",
                "Elite — R$ 599/mês (ilimitado + API + suporte dedicado)",
            ], index=1)

            ok = st.form_submit_button("Começar grátis →", use_container_width=True, type="primary")

        if ok:
            if not box_name:
                st.error("Digite o nome do box.")
            else:
                st.session_state.user = {
                    "name": owner, "box": box_name, "city": city,
                    "plan": plan.split("—")[0].strip(), "tipo": "box", "alunos": alunos
                }
                st.success(f"🎉 {box_name} cadastrado!")
                st.balloons()
                go("box_dashboard")

        if st.button("← Voltar"):
            go("landing")

# ══════════════════════════════════════════════════════════════════════════════
# ATHLETE DASHBOARD
# ══════════════════════════════════════════════════════════════════════════════
elif st.session_state.page == "dashboard":
    user = st.session_state.user or {"name":"Rafael Santos","city":"SP","plan":"Pro","tipo":"atleta","box":"CrossFit Itaim"}
    first = user["name"].split()[0]

    # ── Top nav bar ──
    if "nav_section" not in st.session_state:
        st.session_state.nav_section = "Dashboard"

    NAV_ITEMS = [
        ("🏠","Dashboard"),("📊","Performance"),("🏋️","WOD Log"),
        ("👨‍🏫","Coaches"),("🏆","Ranking"),("🛍️","Loja"),("⚙️","Config"),
    ]

    coins_now = st.session_state.coins
    btns_html = "".join([
        f'<span class="topbar-btn {"active" if st.session_state.nav_section==label else ""}" onclick="void(0)">{icon} {label}</span>'
        for icon,label in NAV_ITEMS
    ])
    st.markdown(f'''
    <div class="topbar">
        <div class="topbar-logo">⚡ CrossPass</div>
        <div class="topbar-nav" id="topnav"></div>
        <div class="topbar-coins">🪙 <span class="topbar-coin-val">{coins_now:,}</span><span style="font-size:10px;color:#888">moedas</span></div>
        <div style="font-size:12px;color:#888;white-space:nowrap">👤 {first}</div>
    </div>
    ''', unsafe_allow_html=True)

    # Use selectbox hidden-label as nav (reliable in Streamlit)
    nav_labels = [f"{icon} {label}" for icon,label in NAV_ITEMS]
    nav_choice = st.selectbox("Navegação", nav_labels,
        index=[label for _,label in NAV_ITEMS].index(st.session_state.nav_section),
        label_visibility="visible", key="topnav_select")
    st.session_state.nav_section = nav_choice.split(" ",1)[1] if " " in nav_choice else nav_choice
    section = st.session_state.nav_section

    col_sair = st.columns([8,1])[1]
    with col_sair:
        if st.button("Sair", use_container_width=True):
            go("landing")
    st.markdown("---")

    # ── DASHBOARD ──
    if section == "Dashboard":
        st.markdown(f"## Olá, {first} 👋")
        st.caption(f"📍 {user.get('box','Sem box')} · ⚡ Plano {user.get('plan','Free')}")

        st.markdown(f"""
        <div class="streak-bar">
            <div><div style="font-size:11px;color:rgba(255,255,255,.7);margin-bottom:3px">Sequência atual</div>
            <div style="font-family:'Bebas Neue';font-size:32px;color:white">🔥 14 dias</div></div>
            <div style="text-align:center"><div style="font-size:11px;color:rgba(255,255,255,.7);margin-bottom:3px">Moedas</div>
            <div style="font-family:'Bebas Neue';font-size:32px;color:#f59e0b">🪙 {st.session_state.coins:,}</div>
            <div style="font-size:10px;color:rgba(255,255,255,.6)">crosscoins</div></div>
            <div style="text-align:right"><div style="font-size:11px;color:rgba(255,255,255,.7);margin-bottom:3px">Este mês</div>
            <div style="font-family:'Bebas Neue';font-size:32px;color:white">{st.session_state.checkins}</div>
            <div style="font-size:10px;color:rgba(255,255,255,.6)">treinos</div></div>
        </div>
        """, unsafe_allow_html=True)

        c1, c2, c3, c4 = st.columns(4)
        metrics = [
            ("PRs este mês","4","↑ vs mês anterior"),
            ("Volume semanal","18 treinos","últimas 4 semanas"),
            ("Score de performance","147","↑ 8pts este mês"),
            ("Boxes visitados","3","SP + RJ"),
        ]
        for col, (lbl, val, sub) in zip([c1,c2,c3,c4], metrics):
            with col:
                st.markdown(f"<div class='stat-box'><div class='stat-num'>{val}</div><div class='stat-lbl'>{lbl}</div><div class='stat-sub'>{sub}</div></div>", unsafe_allow_html=True)

        st.markdown("---")
        col1, col2 = st.columns([3,2])

        with col1:
            st.markdown("#### Evolução de Performance (90 dias)")
            df = gen_performance_data()
            fig = gobj.Figure()
            fig.add_scatter(x=df["date"], y=df["score"], mode="lines",
                          line=dict(color="#534AB7", width=2.5),
                          fill="tozeroy", fillcolor="rgba(83,74,183,0.08)")
            fig.update_layout(height=240, margin=dict(t=10,b=10,l=10,r=10),
                            plot_bgcolor="#0d0d0d", paper_bgcolor="#0d0d0d",
                            xaxis=dict(showgrid=False, color="#444"),
                            yaxis=dict(showgrid=True, gridcolor="#1a1a1a", color="#444"),
                            font=dict(color="#888"))
            st.plotly_chart(fig, use_container_width=True)

        with col2:
            st.markdown("#### WOD de Hoje")
            st.markdown(f"""
            <div class="wod-box">
                <div class="wod-title">{WOD_TODAY['name']}</div>
                {''.join([f'<div style="font-size:13px;color:#ccc;margin-bottom:4px">• {m}</div>' for m in WOD_TODAY['movements']])}
                <div style="margin-top:.75rem;padding-top:.75rem;border-top:1px solid #2a2060">
                    <div style="font-size:10px;color:#534AB7;font-weight:600;text-transform:uppercase;margin-bottom:4px">💡 Dica do Coach</div>
                    <div style="font-size:11px;color:#aaa">{WOD_TODAY['coach_tip']}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            if st.button("📝 Registrar resultado", use_container_width=True, type="primary"):
                go("log_wod")

        st.markdown("---")
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("#### Últimos PRs")
            for move, pr in list(st.session_state.prs.items())[:4]:
                unit = pr["unit"]
                val_str = f"{pr['val']} {unit}" if unit not in ["tempo","rounds"] else pr["val"] + (" rds" if unit=="rounds" else "")
                st.markdown(f"""
                <div class="pr-item">
                    <div><div class="pr-move">{move}</div><div class="pr-date">{pr['date']}</div></div>
                    <div style="text-align:right"><div class="pr-val">{val_str}</div></div>
                </div>
                """, unsafe_allow_html=True)

        with col2:
            st.markdown("#### Coaches recomendados")
            for c in COACHES[:2]:
                st.markdown(f"""
                <div class="coach-card">
                    <div style="display:flex;align-items:center;gap:10px;margin-bottom:8px">
                        <div style="width:38px;height:38px;border-radius:50%;background:#534AB7;display:flex;align-items:center;justify-content:center;font-weight:700;font-size:13px;flex-shrink:0">{c['avatar']}</div>
                        <div><div class="coach-name">{c['name']}</div><div class="coach-spec">{c['spec']}</div></div>
                    </div>
                    <div style="display:flex;justify-content:space-between;align-items:center">
                        <div style="font-size:11px;color:#888">⭐ {c['rating']} · {c['reviews']} avaliações</div>
                        <div class="coach-price">R$ {c['price']}<span style="font-size:12px;color:#888">/mês</span></div>
                    </div>
                </div>
                """, unsafe_allow_html=True)

    # ── PERFORMANCE ──
    elif section == "Performance":
        st.markdown("## 📊 Análise de Performance")

        tab1, tab2, tab3 = st.tabs(["PRs & Evolução", "Volume de Treino", "Comparação"])

        with tab1:
            st.markdown("#### Todos os recordes pessoais")
            col1, col2 = st.columns(2)
            for i, (move, pr) in enumerate(st.session_state.prs.items()):
                with (col1 if i % 2 == 0 else col2):
                    unit = pr["unit"]
                    if unit == "kg":
                        diff = float(pr["val"]) - float(pr["prev"])
                        diff_str = f"+{diff:.1f}kg"
                    elif unit == "rounds":
                        diff = int(pr["val"].replace(" rds","")) - int(pr["prev"].replace(" rds",""))
                        diff_str = f"+{diff} rds"
                    else:
                        diff_str = "↑ PR"
                    st.markdown(f"""
                    <div class="pr-item" style="margin-bottom:8px">
                        <div>
                            <div class="pr-move">{move}</div>
                            <div class="pr-date">{pr['date']} · anterior: {pr['prev']} {unit if unit not in ['tempo','rounds'] else ''}</div>
                        </div>
                        <div style="text-align:right">
                            <div class="pr-val">{pr['val']} {unit if unit not in ['tempo','rounds'] else ''}</div>
                            <div style="font-size:10px;color:#1D9E75">{diff_str}</div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

            st.markdown("#### Adicionar novo PR")
            with st.form("new_pr"):
                c1, c2, c3, c4 = st.columns(4)
                with c1: move_new = st.text_input("Movimento", placeholder="Fran, Back Squat...")
                with c2: val_new  = st.text_input("Resultado", placeholder="4:32 ou 95")
                with c3: unit_new = st.selectbox("Unidade", ["kg","tempo","rounds","reps","m"])
                with c4: st.markdown(""); st.markdown("")
                ok = st.form_submit_button("✅ Salvar PR", use_container_width=True, type="primary")
            if ok and move_new and val_new:
                prev = st.session_state.prs.get(move_new, {}).get("val", "—")
                st.session_state.prs[move_new] = {"val": val_new, "prev": prev, "date": "agora", "unit": unit_new}
                st.success(f"🏆 PR em {move_new} registrado!")
                st.rerun()

        with tab2:
            st.markdown("#### Volume por semana (últimas 12 semanas)")
            df_vol = gen_volume_data()
            fig = gobj.Figure()
            for col, color in [("Força","#534AB7"),("Metcon","#1D9E75"),("Ginástica","#D85A30")]:
                fig.add_bar(name=col, x=df_vol["Semana"], y=df_vol[col], marker_color=color, opacity=0.85)
            fig.update_layout(barmode="stack", height=300, margin=dict(t=10,b=10,l=10,r=10),
                            plot_bgcolor="#0d0d0d", paper_bgcolor="#0d0d0d",
                            legend=dict(orientation="h", y=1.1, font=dict(color="#888")),
                            xaxis=dict(color="#444"), yaxis=dict(color="#444", gridcolor="#1a1a1a"))
            st.plotly_chart(fig, use_container_width=True)

            c1,c2,c3 = st.columns(3)
            with c1: st.markdown("<div class='stat-box'><div class='stat-num'>4.5</div><div class='stat-lbl'>Treinos/semana</div><div class='stat-sub'>média</div></div>", unsafe_allow_html=True)
            with c2: st.markdown("<div class='stat-box'><div class='stat-num'>62%</div><div class='stat-lbl'>Taxa de Força</div><div class='stat-sub'>vs 38% Metcon</div></div>", unsafe_allow_html=True)
            with c3: st.markdown("<div class='stat-box'><div class='stat-num'>14</div><div class='stat-lbl'>Sequência atual</div><div class='stat-sub'>dias consecutivos</div></div>", unsafe_allow_html=True)

        with tab3:
            st.markdown("#### Como você se compara")
            categories = ["Força","Ginástica","Endurance","Técnica","Consistência"]
            user_vals  = [78, 65, 82, 71, 90]
            avg_vals   = [65, 60, 68, 63, 72]

            fig = gobj.Figure()
            fig.add_scatterpolar(r=user_vals+[user_vals[0]], theta=categories+[categories[0]],
                fill='toself', name='Você', line_color='#534AB7', fillcolor='rgba(83,74,183,0.2)')
            fig.add_scatterpolar(r=avg_vals+[avg_vals[0]], theta=categories+[categories[0]],
                fill='toself', name='Média SP', line_color='#1D9E75', fillcolor='rgba(29,158,117,0.1)')
            fig.update_layout(polar=dict(bgcolor='#0d0d0d',
                radialaxis=dict(visible=True, range=[0,100], color="#444", gridcolor="#222"),
                angularaxis=dict(color="#888")),
                showlegend=True, height=350, margin=dict(t=20,b=20,l=20,r=20),
                paper_bgcolor="#0d0d0d", legend=dict(font=dict(color="#888")))
            st.plotly_chart(fig, use_container_width=True)

    # ── WOD LOG ──
    elif section == "WOD Log":
        st.markdown("## 🏋️ Registrar Treino")

        with st.form("wod_log"):
            c1, c2 = st.columns(2)
            with c1:
                tipo = st.selectbox("Tipo de treino", ["WOD do box","WOD personalizado","Força/Ciclo","Ginástica","Endurance"])
                wod_name = st.text_input("Nome do WOD", placeholder="Fran, Cindy, ou descreva...")
                score = st.text_input("Resultado / Score", placeholder="4:32 ou 15 rounds ou 95kg")
            with c2:
                data_treino = st.date_input("Data", datetime.now())
                rx = st.checkbox("RX (sem escalonamento)")
                feelings = st.select_slider("Como foi?", ["😫 Difícil","😤 Puxado","😐 Ok","😊 Bom","🔥 Ótimo"], value="😊 Bom")

            notes = st.text_area("Observações / Anotações", placeholder="Técnica, sensações, o que melhorar...", height=80)
            ok = st.form_submit_button("✅ Salvar treino", use_container_width=True, type="primary")

        if ok and wod_name:
            entry = {"tipo":tipo,"nome":wod_name,"score":score,"data":str(data_treino),"rx":rx,"feelings":feelings,"notes":notes}
            st.session_state.log_entries.insert(0, entry)
            st.session_state.checkins += 1
            st.success(f"💪 Treino '{wod_name}' registrado!")
            st.balloons()

        if st.session_state.log_entries:
            st.markdown("#### Histórico recente")
            for e in st.session_state.log_entries[:10]:
                rx_tag = badge("RX","teal") if e["rx"] else badge("Scaled","amber")
                st.markdown(f"""
                <div class="card">
                    <div style="display:flex;justify-content:space-between;align-items:center">
                        <div>
                            <div style="font-size:14px;font-weight:600;color:#fafaf8">{e['nome']}</div>
                            <div style="font-size:11px;color:#888;margin-top:2px">{e['data']} · {e['tipo']} · {e['feelings']}</div>
                        </div>
                        <div style="text-align:right">
                            <div style="font-family:'Bebas Neue';font-size:22px;color:#1D9E75">{e['score'] or '—'}</div>
                            <div>{rx_tag}</div>
                        </div>
                    </div>
                    {f'<div style="font-size:11px;color:#666;margin-top:8px;padding-top:8px;border-top:1px solid #1a1a1a">{e["notes"]}</div>' if e["notes"] else ''}
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("Nenhum treino registrado ainda. Comece agora!")

    # ── COACHES ──
    elif section == "Coaches":
        st.markdown("## 👨‍🏫 Coaches & Programas")

        tab1, tab2 = st.tabs(["Coaches 1:1", "Programas Online"])

        with tab1:
            c1, c2 = st.columns([2,1])
            with c1: q = st.text_input("", placeholder="Buscar por especialidade...", label_visibility="collapsed")
            with c2: spec_filter = st.selectbox("", ["Todos","Competição","Força","Iniciantes","Mobilidade","Endurance"], label_visibility="collapsed")

            coaches = COACHES.copy()
            if spec_filter != "Todos":
                coaches = [c for c in coaches if any(spec_filter.lower() in t.lower() for t in c["tags"])]
            if q:
                coaches = [c for c in coaches if q.lower() in c["name"].lower() or q.lower() in c["spec"].lower()]

            for c in coaches:
                tags_html = "".join([badge(t) for t in c["tags"]])
                col1, col2 = st.columns([3,1])
                with col1:
                    st.markdown(f"""
                    <div class="coach-card">
                        <div style="display:flex;align-items:center;gap:12px;margin-bottom:10px">
                            <div style="width:48px;height:48px;border-radius:50%;background:#534AB7;display:flex;align-items:center;justify-content:center;font-weight:700;font-size:16px;flex-shrink:0;border:2px solid #3C3489">{c['avatar']}</div>
                            <div>
                                <div class="coach-name">{c['name']}</div>
                                <div class="coach-spec">{c['spec']} · {c['cert']}</div>
                                <div style="font-size:11px;color:#f59e0b">{'★'*int(c['rating'])} {c['rating']} · {c['reviews']} avaliações · {c['students']} alunos ativos</div>
                            </div>
                        </div>
                        <div style="font-size:12px;color:#bbb;margin-bottom:8px">{c['bio']}</div>
                        <div>{tags_html}</div>
                        <div style="display:flex;justify-content:space-between;align-items:center;margin-top:10px">
                            <div class="coach-price">R$ {c['price']}<span style="font-size:12px;color:#888">/mês</span></div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                with col2:
                    st.markdown("")
                    st.markdown("")
                    if st.button("Contratar", key=f"hire_{c['id']}", use_container_width=True, type="primary"):
                        st.success(f"✅ Solicitação enviada para {c['name']}!")
                    if st.button("Ver perfil", key=f"view_{c['id']}", use_container_width=True):
                        st.info(f"Perfil completo de {c['name']} — em breve!")

        with tab2:
            for p in PROGRAMS:
                col1, col2 = st.columns([3,1])
                with col1:
                    tags_html = "".join([badge(t) for t in p["tags"]])
                    st.markdown(f"""
                    <div class="card">
                        <div style="display:flex;justify-content:space-between;align-items:flex-start;margin-bottom:8px">
                            <div>
                                <div style="font-size:15px;font-weight:600;color:#fafaf8">{p['name']}</div>
                                <div style="font-size:11px;color:#888;margin-top:2px">por {p['coach']} · {p['duration']} · {p['level']}</div>
                            </div>
                            <div style="font-family:'Bebas Neue';font-size:22px;color:#534AB7">R$ {p['price']}</div>
                        </div>
                        <div style="font-size:12px;color:#bbb;margin-bottom:8px">{p['description']}</div>
                        <div>{tags_html}</div>
                    </div>
                    """, unsafe_allow_html=True)
                with col2:
                    st.markdown("")
                    st.markdown("")
                    if st.button("Comprar", key=f"buy_{p['name']}", use_container_width=True, type="primary"):
                        st.success(f"✅ {p['name']} adicionado!")

    # ── RANKING ──
    elif section == "Ranking":
        st.markdown("## 🏆 Ranking & Comunidade")

        tab1, tab2 = st.tabs(["Ranking Geral", "Desafios"])

        with tab1:
            c1, c2 = st.columns([2,1])
            with c1: ranking_city = st.selectbox("", ["São Paulo","Rio de Janeiro","Belo Horizonte","Nacional"], label_visibility="collapsed")
            with c2: ranking_cat = st.selectbox("", ["Geral","Força","Metcon","Consistência"], label_visibility="collapsed")

            ranking_data = [
                {"pos":1,"name":"André Melo","box":"CF Itaim","score":3840,"badge":"🥇","streak":21},
                {"pos":2,"name":"Camila Freitas","box":"CF Pinheiros","score":3620,"badge":"🥈","streak":18},
                {"pos":3,"name":"Thiago Ramos","box":"CF Moema","score":3290,"badge":"🥉","streak":14},
                {"pos":4,"name":"Juliana Costa","box":"CF Itaim","score":2980,"badge":"","streak":11},
                {"pos":5,"name":"Pedro Alves","box":"CF Saúde","score":2750,"badge":"","streak":9},
                {"pos":6,"name":"Marina Lima","box":"CF Pinheiros","score":2640,"badge":"","streak":7},
                {"pos":7,"name":"Lucas Ferreira","box":"CF Moema","score":2510,"badge":"","streak":12},
            ]
            for r in ranking_data:
                pos_icon = r["badge"] if r["badge"] else f"#{r['pos']}"
                st.markdown(f"""
                <div class="rank-item">
                    <div style="font-family:'Bebas Neue';font-size:20px;width:32px;text-align:center;color:{'#f59e0b' if r['pos']==1 else '#aaa' if r['pos']==2 else '#cd7c4f' if r['pos']==3 else '#555'}">{pos_icon}</div>
                    <div style="flex:1"><div style="font-size:13px;font-weight:600;color:#fafaf8">{r['name']}</div><div style="font-size:10px;color:#888">{r['box']} · 🔥 {r['streak']} dias</div></div>
                    <div style="font-family:'Bebas Neue';font-size:18px;color:#534AB7">{r['score']:,}</div>
                </div>
                """, unsafe_allow_html=True)

            user = st.session_state.user or {}
            st.markdown(f"""
            <div style="margin-top:8px;padding:12px 14px;background:rgba(83,74,183,.15);border-radius:10px;border:1px solid #534AB7;display:flex;align-items:center;gap:12px">
                <div style="font-family:'Bebas Neue';font-size:20px;width:32px;text-align:center;color:#534AB7">#38</div>
                <div style="flex:1"><div style="font-size:13px;font-weight:600;color:#fafaf8">{user.get('name','Rafael Santos')} — você</div><div style="font-size:10px;color:#888">{user.get('box','CF Itaim')} · 🔥 14 dias</div></div>
                <div style="font-family:'Bebas Neue';font-size:18px;color:#534AB7">1.247</div>
            </div>
            <p style="font-size:10px;color:#444;text-align:center;margin-top:6px">Pontos = treinos × 80 + PRs × 120 + consistência × 50</p>
            """, unsafe_allow_html=True)

        with tab2:
            st.markdown("#### Desafios ativos")
            st.caption("🪙 Ganhe CrossCoins ao completar desafios — use na loja!")
            challenges = [
                {"key":"Outubro de Força","name":"Outubro de Força","desc":"Complete 20 treinos de força em outubro","total":20,"coins":500,"coins_top":1500,"ends":"15 dias","icon":"💪"},
                {"key":"PR Challenge","name":"PR Challenge","desc":"Bata 5 PRs em qualquer movimento este mês","total":5,"coins":300,"coins_top":1000,"ends":"8 dias","icon":"🏆"},
                {"key":"Box Hopper","name":"Box Hopper","desc":"Treine em 4 boxes diferentes este mês","total":4,"coins":200,"coins_top":700,"ends":"22 dias","icon":"🗺️"},
            ]
            for ch in challenges:
                prog = st.session_state.challenge_progress.get(ch["key"], 0)
                pct = min(prog / ch["total"], 1.0)
                done = pct >= 1.0
                col_ch, col_btn = st.columns([4,1])
                with col_ch:
                    st.markdown(f"""
                    <div class="card" style="border-color:{'#1D9E75' if done else '#222'}">
                        <div style="display:flex;justify-content:space-between;align-items:flex-start;margin-bottom:8px">
                            <div style="display:flex;gap:10px;align-items:flex-start">
                                <span style="font-size:22px">{ch['icon']}</span>
                                <div>
                                    <div style="font-size:14px;font-weight:600;color:#fafaf8">{ch['name']} {'✅' if done else ''}</div>
                                    <div style="font-size:11px;color:#888;margin-top:2px">{ch['desc']}</div>
                                </div>
                            </div>
                            <div style="text-align:right;flex-shrink:0">
                                <div style="font-size:10px;color:#888">Termina em</div>
                                <div style="font-size:13px;font-weight:600;color:#D85A30">{ch['ends']}</div>
                            </div>
                        </div>
                        <div style="display:flex;justify-content:space-between;font-size:11px;margin-bottom:6px">
                            <span style="color:#888">Progresso: {prog}/{ch['total']}</span>
                            <span style="color:#f59e0b;font-weight:600">🪙 {ch['coins']:,} ao completar · 🏆 {ch['coins_top']:,} se 1º lugar</span>
                        </div>
                        <div style="height:6px;background:#1a1a1a;border-radius:100px;overflow:hidden">
                            <div style="height:100%;width:{pct*100:.0f}%;background:{'#1D9E75' if done else '#534AB7'};border-radius:100px;transition:.4s"></div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                with col_btn:
                    st.markdown("")
                    st.markdown("")
                    if not done:
                        if st.button("+ Treino", key=f"ch_{ch['key']}", use_container_width=True):
                            st.session_state.challenge_progress[ch["key"]] = prog + 1
                            new_prog = prog + 1
                            if new_prog >= ch["total"]:
                                st.session_state.coins += ch["coins"]
                                st.success(f"🎉 Desafio '{ch['name']}' completo! +{ch['coins']:,} 🪙")
                            else:
                                st.rerun()
                    else:
                        st.markdown('<div style="font-size:11px;color:#1D9E75;text-align:center;padding-top:.5rem">Completo! ✅</div>', unsafe_allow_html=True)

            st.markdown("---")
            st.markdown("#### 🪙 Como ganhar CrossCoins")
            earning = [
                ("✅ Completar treino","+ 50 moedas"),
                ("🏆 Bater um PR","+ 120 moedas"),
                ("🥇 1º lugar no desafio mensal","+ 1.500 moedas"),
                ("🥈 2º lugar no desafio","+ 700 moedas"),
                ("🥉 3º lugar no desafio","+ 400 moedas"),
                ("🔥 Sequência de 30 dias","+ 500 moedas"),
                ("🗺️ Visitar novo box","+ 100 moedas"),
                ("⭐ Indicar um amigo","+ 200 moedas"),
            ]
            for label, val in earning:
                st.markdown(f"""<div style="display:flex;justify-content:space-between;padding:7px 0;border-bottom:1px solid #1a1a1a;font-size:13px">
                <span style="color:#ccc">{label}</span><span style="color:#f59e0b;font-weight:600">{val}</span></div>""", unsafe_allow_html=True)


    # ── LOJA ──
    elif section == "Loja":
        st.markdown("## 🛍️ Loja CrossPass")
        st.markdown(f"""
        <div class="coins-bar">
            <span style="font-size:22px">🪙</span>
            <div>
                <div class="coin-val">{st.session_state.coins:,} CrossCoins</div>
                <div style="font-size:10px;color:#888">Ganhe treinando, gaste na loja</div>
            </div>
            <div style="margin-left:auto;text-align:right">
                <div style="font-size:11px;color:#888">Compras realizadas</div>
                <div style="font-size:20px;font-weight:600;color:#f59e0b">{len(st.session_state.purchases)}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        col_search, col_cat = st.columns([2,1])
        with col_search: q_loja = st.text_input("", placeholder="Buscar produto...", label_visibility="collapsed", key="loja_q")
        with col_cat:
            cat_filter = st.selectbox("", ["Todos","Suplementos","Roupas","Equipamentos"], label_visibility="collapsed", key="loja_cat")

        pay_mode = st.radio("Forma de pagamento", ["💳 Pagar com R$", "🪙 Pagar com CrossCoins"], horizontal=True)

        prods = PRODUCTS.copy()
        if cat_filter != "Todos": prods = [p for p in prods if p["cat"] == cat_filter]
        if q_loja: prods = [p for p in prods if q_loja.lower() in p["name"].lower() or q_loja.lower() in p["brand"].lower()]

        if st.session_state.purchases:
            with st.expander(f"📦 Seus pedidos ({len(st.session_state.purchases)})"):
                for pur in st.session_state.purchases:
                    st.markdown(f"✅ **{pur['name']}** — {pur['paid']} — {pur['date']}")

        cols_loja = st.columns(3)
        for i, p in enumerate(prods):
            with cols_loja[i % 3]:
                tags_html = " ".join([f'<span class="badge badge-purple">{t}</span>' for t in p["tags"]])
                out_badge = '' if p["stock"] else '<span class="badge badge-coral">Esgotado</span>'
                price_display = f"R$ {p['price_brl']}" if "R$" in pay_mode else f"🪙 {p['price_coins']:,}"
                can_afford = (p["price_brl"] > 0) if "R$" in pay_mode else (st.session_state.coins >= p["price_coins"])
                st.markdown(f"""
                <div class="product-card">
                    <div class="product-img" style="background:linear-gradient(135deg,{p['bg']},#050505)">{p['emoji']}</div>
                    <div class="product-body">
                        <div class="product-name">{p['name']}</div>
                        <div class="product-brand">{p['brand']} {out_badge}</div>
                        <div style="font-size:11px;color:#888;margin-bottom:8px;line-height:1.5">{p['desc'][:80]}...</div>
                        <div>{tags_html}</div>
                        <div style="display:flex;justify-content:space-between;align-items:center;margin-top:.75rem">
                            <div>
                                <div class="product-price">{"R$ "+str(p['price_brl']) if "R$" in pay_mode else ""}</div>
                                <div class="product-coins">🪙 {p['price_coins']:,} moedas</div>
                            </div>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                if p["stock"]:
                    btn_label = f"Comprar — {'R$ '+str(p['price_brl']) if 'R$' in pay_mode else '🪙 '+str(p['price_coins'])}"
                    disabled = not can_afford
                    if st.button(btn_label, key=f"buy_{p['id']}", use_container_width=True,
                                 type="primary", disabled=disabled):
                        if "Coins" in pay_mode:
                            st.session_state.coins -= p["price_coins"]
                            paid_str = f"🪙 {p['price_coins']:,} moedas"
                        else:
                            paid_str = f"R$ {p['price_brl']}"
                        st.session_state.purchases.insert(0, {
                            "name": p["name"], "paid": paid_str,
                            "date": datetime.now().strftime("%d/%m %H:%M")
                        })
                        st.success(f"✅ {p['name']} comprado!")
                        st.rerun()
                    if not can_afford and "Coins" in pay_mode:
                        falta = p["price_coins"] - st.session_state.coins
                        st.caption(f"Faltam 🪙 {falta:,} moedas")
                else:
                    st.button("Esgotado", key=f"buy_{p['id']}", use_container_width=True, disabled=True)

    # ── SETTINGS ──
    elif section == "Config":
        user = st.session_state.user or {}
        st.markdown("## ⚙️ Configurações")
        c1, c2 = st.columns(2)
        with c1:
            st.markdown("#### Perfil")
            st.text_input("Nome", value=user.get("name",""))
            st.text_input("E-mail")
            st.selectbox("Cidade", ["São Paulo","Rio de Janeiro","Belo Horizonte","Curitiba"])
            st.select_slider("Nível", ["Iniciante","Intermediário","Avançado","Competidor"], value="Avançado")
        with c2:
            st.markdown("#### Plano atual")
            st.markdown(f"""
            <div class="card" style="border-color:#534AB7">
                <div style="font-family:'Bebas Neue';font-size:24px;color:#534AB7">Plano {user.get('plan','Pro')}</div>
                <div style="font-size:12px;color:#888;margin:.5rem 0">Próxima cobrança: 15 de novembro</div>
                {'<div style="font-size:12px;color:#1D9E75">✓ Analytics avançado</div><div style="font-size:12px;color:#1D9E75">✓ Ranking nacional</div><div style="font-size:12px;color:#1D9E75">✓ Coaching remoto</div>' if user.get('plan')=='Pro' else ''}
            </div>
            """, unsafe_allow_html=True)
            st.button("Trocar de plano", use_container_width=True)
            st.button("Cancelar assinatura", use_container_width=True)
        if st.button("Salvar alterações", type="primary"):
            st.success("✅ Perfil atualizado!")

# ══════════════════════════════════════════════════════════════════════════════
# LOG WOD (modal-like)
# ══════════════════════════════════════════════════════════════════════════════
elif st.session_state.page == "log_wod":
    st.markdown("## 📝 Registrar WOD de Hoje")
    st.markdown(f"""
    <div class="wod-box">
        <div class="wod-title">{WOD_TODAY['name']}</div>
        {''.join([f'<div style="font-size:13px;color:#ccc;margin-bottom:4px">• {m}</div>' for m in WOD_TODAY['movements']])}
    </div>
    """, unsafe_allow_html=True)

    with st.form("log_today"):
        c1, c2 = st.columns(2)
        with c1:
            score = st.text_input("Seu resultado (rounds + reps)", placeholder="ex: 15 rounds + 3 reps")
            rx = st.checkbox("RX completo")
        with c2:
            feelings = st.select_slider("Como foi?", ["😫","😤","😐","😊","🔥"], value="😊")
            notes = st.text_input("Observações", placeholder="O que funcionou? O que melhorar?")
        ok = st.form_submit_button("✅ Salvar", use_container_width=True, type="primary")

    if ok:
        entry = {"tipo":"WOD do box","nome":WOD_TODAY["name"],"score":score,"data":str(datetime.now().date()),"rx":rx,"feelings":feelings,"notes":notes}
        st.session_state.log_entries.insert(0, entry)
        st.session_state.checkins += 1
        st.success("💪 Treino registrado!")
        go("dashboard")

    if st.button("← Voltar ao dashboard"):
        go("dashboard")

# ══════════════════════════════════════════════════════════════════════════════
# BOX DASHBOARD (SaaS)
# ══════════════════════════════════════════════════════════════════════════════
elif st.session_state.page == "box_dashboard":
    user = st.session_state.user or {"name":"João","box":"CrossFit Demo","plan":"Growth","alunos":80}

    with st.sidebar:
        st.markdown(f"### 🏢 {user.get('box','Box')}")
        st.caption(f"Plano {user.get('plan','Growth')}")
        st.markdown("---")
        nav = st.radio("", ["📊 Visão Geral","👥 Alunos","📅 Turmas","💰 Financeiro","📈 Retenção"], label_visibility="collapsed")
        st.markdown("---")
        if st.button("← Sair"):
            go("landing")

    section = nav.split(" ",1)[1]

    if section == "Visão Geral":
        st.markdown(f"## 🏢 {user.get('box','Meu Box')}")
        st.caption(f"Plano {user.get('plan','Growth')} · {user.get('city','SP')}")

        alunos = user.get("alunos", 80)
        c1,c2,c3,c4 = st.columns(4)
        with c1: st.markdown(f"<div class='stat-box'><div class='stat-num'>{alunos}</div><div class='stat-lbl'>Alunos ativos</div><div class='stat-sub'>↑ 3 este mês</div></div>", unsafe_allow_html=True)
        with c2: st.markdown(f"<div class='stat-box'><div class='stat-num'>R$ {alunos*300//1000}k</div><div class='stat-lbl'>Receita mensal</div><div class='stat-sub'>↑ 5% vs mês ant.</div></div>", unsafe_allow_html=True)
        with c3: st.markdown("<div class='stat-box'><div class='stat-num'>4.2%</div><div class='stat-lbl'>Churn mensal</div><div class='stat-sub'>↓ 0.8% este mês</div></div>", unsafe_allow_html=True)
        with c4: st.markdown("<div class='stat-box'><div class='stat-num'>68%</div><div class='stat-lbl'>Ocupação média</div><div class='stat-sub'>↑ vs 63% anterior</div></div>", unsafe_allow_html=True)

        st.markdown("---")
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("#### Alunos por turma (hoje)")
            turmas = {"06:00":8,"07:00":12,"08:00":7,"12:00":5,"18:00":14,"19:00":15,"20:00":11}
            df_t = pd.DataFrame({"Horário":list(turmas.keys()),"Alunos":list(turmas.values())})
            fig = px.bar(df_t, x="Horário", y="Alunos", color_discrete_sequence=["#534AB7"])
            fig.update_layout(height=250, margin=dict(t=10,b=10,l=10,r=10),
                            plot_bgcolor="#0d0d0d", paper_bgcolor="#0d0d0d",
                            xaxis=dict(color="#444"), yaxis=dict(color="#444", gridcolor="#1a1a1a"))
            st.plotly_chart(fig, use_container_width=True)

        with col2:
            st.markdown("#### Retenção (últimos 6 meses)")
            meses = ["Mai","Jun","Jul","Ago","Set","Out"]
            retencao = [91, 88, 93, 89, 92, 96]
            fig2 = gobj.Figure()
            fig2.add_scatter(x=meses, y=retencao, mode="lines+markers",
                           line=dict(color="#1D9E75", width=2.5), marker=dict(size=7))
            fig2.add_hline(y=90, line_dash="dot", line_color="#534AB7", annotation_text="Meta 90%")
            fig2.update_layout(height=250, margin=dict(t=10,b=10,l=10,r=10),
                             plot_bgcolor="#0d0d0d", paper_bgcolor="#0d0d0d",
                             yaxis=dict(range=[80,100], color="#444", gridcolor="#1a1a1a"),
                             xaxis=dict(color="#444"))
            st.plotly_chart(fig2, use_container_width=True)

        st.markdown("#### Alertas de retenção")
        alertas = [
            {"nome":"Carlos Mendes","ultimo":"há 12 dias","risco":"Alto","turma":"19:00"},
            {"nome":"Ana Paula S.","ultimo":"há 8 dias","risco":"Médio","turma":"07:00"},
            {"nome":"Ricardo Lima","ultimo":"há 6 dias","risco":"Médio","turma":"18:00"},
        ]
        for a in alertas:
            cor = "#D85A30" if a["risco"]=="Alto" else "#BA7517"
            st.markdown(f"""
            <div class="card" style="border-left:3px solid {cor}">
                <div style="display:flex;justify-content:space-between;align-items:center">
                    <div><div style="font-size:13px;font-weight:600;color:#fafaf8">{a['nome']}</div>
                    <div style="font-size:11px;color:#888">Último treino: {a['ultimo']} · Turma das {a['turma']}</div></div>
                    <div style="font-size:12px;font-weight:600;color:{cor}">Risco {a['risco']}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)

    elif section == "Alunos":
        st.markdown("## 👥 Gestão de Alunos")
        alunos_data = pd.DataFrame({
            "Nome": ["Rafael Santos","Camila Freitas","André Melo","Julia Costa","Pedro Alves","Marina Lima","Lucas F.","Beatriz R."],
            "Turma": ["19:00","07:00","06:00","18:00","20:00","07:00","19:00","18:00"],
            "Plano": ["Premium","Premium","Lite","Premium","Lite","Premium","Premium","Lite"],
            "Check-ins/mês": [14,18,12,8,6,20,15,9],
            "Último treino": ["Hoje","Hoje","Ontem","Há 3 dias","Há 5 dias","Hoje","Ontem","Há 2 dias"],
            "Risco churn": ["Baixo","Baixo","Baixo","Médio","Alto","Baixo","Baixo","Médio"],
        })
        st.dataframe(alunos_data, use_container_width=True, hide_index=True)
        col1, col2 = st.columns(2)
        with col1:
            if st.button("📧 Enviar lembrete para inativos", use_container_width=True):
                st.success("✅ Mensagem enviada para 2 alunos!")
        with col2:
            if st.button("➕ Adicionar aluno", use_container_width=True, type="primary"):
                st.info("Formulário de cadastro em breve!")

    elif section == "Financeiro":
        st.markdown("## 💰 Financeiro")
        meses = ["Mai","Jun","Jul","Ago","Set","Out"]
        receita = [22400,23800,24100,25600,26800,28200]
        fig = gobj.Figure()
        fig.add_bar(x=meses, y=receita, marker_color="#534AB7", opacity=0.85)
        fig.update_layout(height=280, margin=dict(t=10,b=10,l=10,r=10),
                        plot_bgcolor="#0d0d0d", paper_bgcolor="#0d0d0d",
                        xaxis=dict(color="#444"), yaxis=dict(color="#444", gridcolor="#1a1a1a"))
        st.plotly_chart(fig, use_container_width=True)
        c1,c2,c3 = st.columns(3)
        with c1: st.markdown("<div class='stat-box'><div class='stat-num'>R$ 28k</div><div class='stat-lbl'>Receita outubro</div><div class='stat-sub'>↑ 5.2% vs set</div></div>", unsafe_allow_html=True)
        with c2: st.markdown("<div class='stat-box'><div class='stat-num'>R$ 312</div><div class='stat-lbl'>Ticket médio</div><div class='stat-sub'>por aluno/mês</div></div>", unsafe_allow_html=True)
        with c3: st.markdown("<div class='stat-box'><div class='stat-num'>R$ 1.8k</div><div class='stat-lbl'>Inadimplência</div><div class='stat-sub'>6 alunos em atraso</div></div>", unsafe_allow_html=True)

    else:
        st.markdown(f"## {nav}")
        st.info("Módulo em desenvolvimento — disponível na próxima versão.")
