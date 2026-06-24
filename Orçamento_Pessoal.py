import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, date, timedelta
import json, hashlib, os

# ─── CONFIG ───────────────────────────────────────────────────────────────────
st.set_page_config(page_title="FinançasPro", layout="wide",
                   initial_sidebar_state="collapsed")

BASE_DIR   = os.path.dirname(os.path.abspath(__file__))
USERS_FILE = os.path.join(BASE_DIR, "fp_usuarios.json")
DATA_FILE  = os.path.join(BASE_DIR, "fp_dados.json")

# ─── CSS ──────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
header[data-testid="stHeader"] { display: none !important; }
section[data-testid="stSidebar"] { display: none !important; }
div[data-testid="stToolbar"] { display: none !important; }

.block-container {
  padding-top: 0rem !important;
  padding-bottom: 1rem !important;
  padding-left: 2rem !important;
  padding-right: 2rem !important;
}

@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Sans:wght@300;400;500;600&display=swap');

:root {
  --verde-escuro:#004f34; --verde-principal:#00704A; --verde-medio:#05C47A;
  --verde-claro:#4dc882;  --verde-menta:#a8f0c8;    --verde-fundo:#e8f7ef;
  --cinza-claro:#f4faf7;  --cinza-borda:#d0e8db;    --texto-escuro:#0d2b1e;
  --texto-medio:#00704A;
  --bg: #f4faf7; --card-bg: #fff; --border: #d0e8db;
  --text-main: #0d2b1e; --text-sub: #1a6645; --text-muted: #5d8a6e;
}
[data-theme="dark"] {
  --bg: #0d1f18; --card-bg: #122a1e; --border: #1e4033;
  --text-main: #e0f5ec; --text-sub: #a8f0c8; --text-muted: #6ebd95;
}

html, body, [class*="css"] {
  font-family: 'DM Sans', sans-serif;
  background: var(--bg) !important;
  color: var(--text-main) !important;
}

/* ── Top bar ── */
.top-bar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  background: linear-gradient(90deg, #004f34 0%, #00704A 60%, #029158 100%);
  padding: 0.7rem 2rem;
  border-radius: 0;
  border-bottom: 2px solid #05C47A;
  margin-bottom: 0;
}
.top-brand {
  font-family: 'Syne', sans-serif;
  font-size: 1.3rem;
  font-weight: 800;
  color: #a8f0c8;
}
.top-brand span { color: #4dc882; }
.top-user {
  font-size: 0.72rem;
  color: #a8f0c8;
}

/* ── Abas de navegação abaixo do título ── */
.stTabs [data-baseweb="tab-list"] {
  background: var(--card-bg);
  border-bottom: 2px solid var(--border);
  border-radius: 0;
  gap: 0;
  padding: 0 1.5rem;
}
.stTabs [data-baseweb="tab"] {
  background: transparent !important;
  color: var(--text-sub) !important;
  font-family: 'DM Sans', sans-serif;
  font-weight: 600;
  font-size: 0.85rem;
  padding: 0.75rem 1.2rem;
  border-bottom: 3px solid transparent;
  transition: all 0.15s;
}
.stTabs [aria-selected="true"] {
  color: #00704A !important;
  border-bottom: 3px solid #05C47A !important;
}
.stTabs [data-baseweb="tab-panel"] {
  padding: 1.2rem 0.5rem;
}

.kpi { background: var(--card-bg); border-radius:14px; padding:10px 16px;
  box-shadow:0 4px 24px rgba(0,112,74,.1); border:1.5px solid var(--border);
  border-top:4px solid; height:100%; }
.kpi.verde { border-top-color:#05C47A; }
.kpi.vermelho { border-top-color:#c0392b; }
.kpi.amarelo { border-top-color:#f39c12; }
.kpi.roxo { border-top-color:#8e44ad; }
.kpi-label {
  font-size: 0.62rem; font-weight: 600; text-transform: uppercase;
  letter-spacing: .8px; color: var(--text-sub); margin-bottom: 4px;
}
.kpi-value {
  font-family: 'Syne', sans-serif; font-size: 1.45rem;
  font-weight: 700; line-height: 1.1;
}
.kpi-value.pos { color:#00704A; } .kpi-value.neg { color:#c0392b; }
.kpi-value.neu { color:#00704A; }
.kpi-sub { font-size:0.72rem; color: var(--text-sub); margin-top:4px; }

.section-title { font-family:'Syne',sans-serif; font-size:0.95rem; font-weight:700;
  color:#004f34; border-left:4px solid #05C47A; padding-left:10px;
  margin:20px 0 12px; text-transform:uppercase; letter-spacing:.05em; }

.login-box { max-width:420px; margin:60px auto; background: var(--card-bg);
  border-radius:20px; padding:40px; box-shadow:0 24px 80px rgba(0,0,0,.15); }
.login-title { font-family:'Syne',sans-serif; font-size:1.6rem; font-weight:800;
  color:#00704A; margin-bottom:4px; }
.login-sub { font-size:0.72rem; color:#00704A; text-transform:uppercase;
  letter-spacing:1px; margin-bottom:24px; }

.divider { height:2px; background:linear-gradient(90deg,#05C47A,transparent);
  margin:18px 0; border-radius:2px; }

.badge { display:inline-block; padding:2px 9px; border-radius:20px;
  font-size:0.7rem; font-weight:700; }
.badge-receita   { background:#c8f7dc; color:#00704A; }
.badge-fixo      { background:#dff5ea; color:#0d7a3e; }
.badge-variavel  { background:#fff0e0; color:#c05e00; }
.badge-aliment   { background:#e3f2fd; color:#1565c0; }
.badge-transport { background:#fce4ec; color:#880e4f; }
.badge-moradia   { background:#e8eaf6; color:#283593; }
.badge-saude     { background:#e0f7fa; color:#006064; }
.badge-lazer     { background:#fff9c4; color:#f57f17; }
.badge-educacao  { background:#f3e5f5; color:#6a1b9a; }
.badge-servicos  { background:#e8f5e9; color:#2e7d32; }
.badge-outros    { background:#fafafa; color:#555; border:1px solid #ddd; }

.tag-pos { color:#00704A; font-weight:700; font-family:'Syne',sans-serif; }
.tag-neg { color:#c0392b; font-weight:700; font-family:'Syne',sans-serif; }

.user-row { display:flex; align-items:center; gap:14px; padding:14px 18px;
  border-radius:12px; background: var(--card-bg); border:1.5px solid var(--border);
  margin-bottom:8px; }
.user-ava { width:36px; height:36px; border-radius:50%; background:#00704A;
  color:#fff; display:inline-flex; align-items:center; justify-content:center;
  font-family:'Syne',sans-serif; font-weight:700; font-size:14px; }
.user-ava-admin { background:#f39c12; }

.insight-box {
  background: linear-gradient(135deg, #004f34 0%, #00704A 100%);
  border-radius: 14px; padding: 16px 20px; color: #e8f7ef;
  margin-bottom: 10px; border: 1.5px solid rgba(77,200,130,0.2);
}
.insight-label {
  font-size: 0.62rem; font-weight: 700; text-transform: uppercase;
  letter-spacing: 1px; color: #a8f0c8; margin-bottom: 4px;
}
.insight-value {
  font-family: 'Syne', sans-serif; font-size: 1.2rem; font-weight: 700; color: #fff;
}
.insight-sub { font-size: 0.72rem; color: #a8f0c8; margin-top: 2px; }

/* upload excel preview */
.excel-row { background: var(--card-bg); border: 1.5px solid var(--border);
  border-radius:10px; padding:12px 16px; margin-bottom:6px; }
.excel-row-ok  { border-left: 4px solid #05C47A; }
.excel-row-rev { border-left: 4px solid #f39c12; }
</style>
""", unsafe_allow_html=True)

# ─── PERSISTÊNCIA ─────────────────────────────────────────────────────────────
def load_users():
    if os.path.exists(USERS_FILE):
        with open(USERS_FILE, "r", encoding="utf-8") as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                pass
    default = [{"usuario": "Aldemir", "senha": hash_pw("123"), "role": "admin"}]
    save_users(default)
    return default

def save_users(u):
    with open(USERS_FILE, "w", encoding="utf-8") as f:
        json.dump(u, f, ensure_ascii=False, indent=2)

def hash_pw(pw): 
    return hashlib.sha256(pw.encode()).hexdigest()

def load_data(usuario):
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            try:
                all_data = json.load(f)
            except json.JSONDecodeError:
                all_data = {}
    else:
        all_data = {}
    key = usuario.lower()
    user_section = all_data.get(key, {})
    return user_section.get("lancamentos", []), user_section.get("lixeira", [])

def save_data(usuario, lancamentos, lixeira):
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            try:
                all_data = json.load(f)
            except json.JSONDecodeError:
                all_data = {}
    else:
        all_data = {}
    key = usuario.lower()
    all_data[key] = {"lancamentos": lancamentos, "lixeira": lixeira}
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(all_data, f, ensure_ascii=False, indent=2)

# ─── CLASSIFICAÇÃO AUTOMÁTICA ─────────────────────────────────────────────────
REGRAS = [
    {"palavras": ["salário","salario","pagamento","freelance","renda","receita","honorário","honorario","pró-labore","prolabore","dividendo"],
     "tipo": "Receita", "classe": "Receita", "icone": "💵"},
    {"palavras": ["aluguel","condomínio","condominio","iptu","financiamento","prestação casa"],
     "tipo": "Fixo", "classe": "Moradia", "icone": "🏠"},
    {"palavras": ["luz","energia","enel","cpfl","elektro","água","agua","saneamento","sabesp"],
     "tipo": "Fixo", "classe": "Moradia", "icone": "🏠"},
    {"palavras": ["internet","wi-fi","wifi","claro","vivo","tim","oi","net","telefone","celular","mensalidade"],
     "tipo": "Fixo", "classe": "Serviços", "icone": "📡"},
    {"palavras": ["netflix","amazon prime","disney","hbo","spotify","youtube premium"],
     "tipo": "Fixo", "classe": "Lazer", "icone": "🎬"},
    {"palavras": ["seguro","plano de saúde","plano saude","unimed","amil"],
     "tipo": "Fixo", "classe": "Saúde", "icone": "🏥"},
    {"palavras": ["supermercado","mercado","padaria","açougue","feira","ifood","rappi","delivery","restaurante","lanche","pizza","hamburguer","refeição","refeicao","almoço","almoco","jantar","café","cafe","comida"],
     "tipo": "Variável", "classe": "Alimentação", "icone": "🍽️"},
    {"palavras": ["uber","99","taxi","combustível","combustivel","gasolina","etanol","pedágio","pedagio","estacionamento","ônibus","onibus","metrô","metro"],
     "tipo": "Variável", "classe": "Transporte", "icone": "🚗"},
    {"palavras": ["farmácia","farmacia","remédio","remedio","médico","medico","consulta","exame","dentista","hospital","clínica","clinica"],
     "tipo": "Variável", "classe": "Saúde", "icone": "💊"},
    {"palavras": ["faculdade","escola","curso","mensalidade escola","livro","udemy","alura","coursera"],
     "tipo": "Fixo", "classe": "Educação", "icone": "📚"},
    {"palavras": ["cinema","teatro","show","ingresso","viagem","hotel","passeio","academia","jogo","game"],
     "tipo": "Variável", "classe": "Lazer", "icone": "🎉"},
    {"palavras": ["roupa","calçado","calcado","sapato","tênis","tenis","camisa","vestido","shopping"],
     "tipo": "Variável", "classe": "Vestuário", "icone": "👗"},
]

def classificar(desc):
    import unicodedata
    d = unicodedata.normalize("NFD", desc.lower())
    d = "".join(c for c in d if unicodedata.category(c) != "Mn")
    for r in REGRAS:
        for p in r["palavras"]:
            pn = unicodedata.normalize("NFD", p.lower())
            pn = "".join(c for c in pn if unicodedata.category(c) != "Mn")
            if pn in d:
                return r["tipo"], r["classe"], r["icone"]
    return "Variável", "Outros", "📌"

# ─── HELPERS ──────────────────────────────────────────────────────────────────
def fmt_brl(v):
    return f"R$ {abs(v):,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

def badge_classe(cls):
    mapa = {"Alimentação":"aliment","Transporte":"transport","Moradia":"moradia",
            "Saúde":"saude","Lazer":"lazer","Educação":"educacao",
            "Serviços":"servicos","Receita":"receita","Vestuário":"outros","Outros":"outros"}
    return f'<span class="badge badge-{mapa.get(cls,"outros")}">{cls}</span>'

def badge_tipo(tipo):
    if tipo == "Receita": return '<span class="badge badge-receita">Receita</span>'
    if tipo == "Fixo":    return '<span class="badge badge-fixo">Fixo</span>'
    return '<span class="badge badge-variavel">Variável</span>'

# ─── SESSION STATE ────────────────────────────────────────────────────────────
def _ss(k, v):
    if k not in st.session_state: st.session_state[k] = v

_ss("logged_in", False); _ss("username", ""); _ss("is_admin", False)
_ss("page", "Dashboard")
_ss("lancamentos", []); _ss("lixeira", [])
_ss("tema_escuro", False)

# ══════════════════════════════════════════════════════════════════
# TELA DE LOGIN
# ══════════════════════════════════════════════════════════════════
if not st.session_state.logged_in:
    st.markdown("""
    <div style="text-align:center;padding:15px 0 10px">
      <div style="font-size:3rem"></div>
      <div style="font-family:Syne,sans-serif;font-size:1.8rem;font-weight:800;color:#004f34;">
        Finanças<span style="color:#00704A">Pro</span></div>
      <div style="font-size:0.75rem;color:#1a6645;text-transform:uppercase;letter-spacing:1.2px;margin-top:4px;">
        Controle financeiro pessoal</div>
    </div>
    <div style="height:3px;background:linear-gradient(90deg,#05C47A,#e8f7ef);border-radius:2px;margin:5px auto 28px;max-width:280px"></div>
    """, unsafe_allow_html=True)

    _, col, _ = st.columns([1, 1.2, 1])
    with col:
        aba = st.radio("", ["Entrar", "Criar conta"], horizontal=True, label_visibility="collapsed")

        if aba == "Entrar":
            user_in = st.text_input("👤 Usuário", key="li_u")
            pass_in = st.text_input("🔒 Senha", type="password", key="li_p")
            if st.button("✦ Entrar", use_container_width=True, type="primary"):
                if not user_in or not pass_in:
                    st.error("Preencha todos os campos.")
                else:
                    usuarios = load_users()
                    found = next((u for u in usuarios
                                  if u["usuario"].lower() == user_in.lower()
                                  and u["senha"] == hash_pw(pass_in)), None)
                    if not found:
                        st.error("Usuário ou senha incorretos.")
                    elif found.get("status", "aprovado") == "pendente":
                        st.warning("⏳ Sua conta foi criada, mas ainda aguarda a aprovação do Aldemir.")
                    elif found.get("status") == "desativado":
                        st.error("🚫 Sua conta foi desativada. Entre em contato com o administrador.")
                    else:
                        st.session_state.logged_in = True
                        st.session_state.username  = found["usuario"]
                        st.session_state.is_admin  = found.get("role") == "admin"
                        lanc, lix = load_data(found["usuario"])
                        st.session_state.lancamentos = lanc
                        st.session_state.lixeira     = lix
                        st.rerun()
        else:
            nu = st.text_input("👤 Novo usuário", key="reg_u")
            p1 = st.text_input("🔒 Senha", type="password", key="reg_p1")
            p2 = st.text_input("🔒 Confirmar senha", type="password", key="reg_p2")
            if st.button("✦ Criar conta", use_container_width=True, type="primary"):
                if not nu or not p1 or not p2: st.warning("Preencha todos os campos.")
                elif len(nu) < 3: st.warning("Usuário: mínimo 3 caracteres.")
                elif len(p1) < 3: st.warning("Senha: mínimo 3 caracteres.")
                elif p1 != p2: st.error("As senhas não conferem.")
                else:
                    usuarios = load_users()
                    if any(u["usuario"].lower() == nu.lower() for u in usuarios):
                        st.error("Esse usuário já existe.")
                    else:
                        usuarios.append({
                            "usuario": nu, 
                            "senha": hash_pw(p1), 
                            "role": "user",
                            "status": "pendente" 
                        })
                        save_users(usuarios)
                        st.success("✅ Conta solicitada com sucesso! Aguarde a aprovação do Aldemir.")
    st.stop()

# ─── A PARTIR DAQUI: USUÁRIO LOGADO ──────────────────────────────────────────
lancamentos = st.session_state.lancamentos
lixeira     = st.session_state.lixeira

def persistir():
    save_data(
        st.session_state.username, 
        st.session_state.lancamentos, 
        st.session_state.lixeira
    )

# ─── DARK MODE CSS DINÂMICO ───────────────────────────────────────────────────
if st.session_state.tema_escuro:
    st.markdown("""
    <style>
    html, body, [class*="css"], .block-container { background: #0d1f18 !important; color: #e0f5ec !important; }
    .stTabs [data-baseweb="tab-list"] { background: #122a1e !important; border-color: #1e4033 !important; }
    .stTabs [data-baseweb="tab-panel"] { background: #0d1f18 !important; }
    .kpi { background: #122a1e !important; border-color: #1e4033 !important; }
    .kpi-label, .kpi-sub { color: #a8f0c8 !important; }
    .section-title { color: #4dc882 !important; }
    .user-row { background: #122a1e !important; border-color: #1e4033 !important; }
    div[data-testid="stForm"] { background: #122a1e !important; border-color: #1e4033 !important; }
    .stTextInput input, .stNumberInput input, .stSelectbox div, .stDateInput input {
      background: #0d1f18 !important; color: #e0f5ec !important; border-color: #1e4033 !important;
    }
    .stDataFrame { background: #122a1e !important; }
    div[data-testid="stDataFrameResizable"] { background: #122a1e !important; }
    </style>
    """, unsafe_allow_html=True)

# ─── TOP BAR ──────────────────────────────────────────────────────────────────
btn_tema_label = "☀️ Claro" if st.session_state.tema_escuro else "🌙 Escuro"
col_brand, col_user, col_tema, col_sair = st.columns([5, 2, 1, 1])
with col_brand:
    st.markdown(f"""
    <div class="top-bar">
      <div class="top-brand">Finanças<span>Pro</span></div>
    </div>
    """, unsafe_allow_html=True)
with col_user:
    st.markdown(f"<div style='padding-top:0.9rem;font-size:0.78rem;color:#1a6645;'>👤 <b>{st.session_state.username}</b>{'  👑' if st.session_state.is_admin else ''}</div>", unsafe_allow_html=True)
with col_tema:
    st.markdown("<div style='height:0.5rem'></div>", unsafe_allow_html=True)
    if st.button(btn_tema_label, key="btn_tema", use_container_width=True):
        st.session_state.tema_escuro = not st.session_state.tema_escuro
        st.rerun()
with col_sair:
    st.markdown("<div style='height:0.5rem'></div>", unsafe_allow_html=True)
    if st.button("🚪 Sair", key="logout", use_container_width=True):
        for k in list(st.session_state.keys()): del st.session_state[k]
        st.rerun()

# ─── NAVEGAÇÃO POR ABAS ───────────────────────────────────────────────────────
pages = ["📊 Dashboard", "➕ Lançamentos", "📋 Histórico"]
if st.session_state.is_admin:
    pages.append("👥 Usuários")

# Mapeia label da aba para nome de página interno
PAGE_MAP = {
    "📊 Dashboard": "Dashboard",
    "➕ Lançamentos": "Lançamentos",
    "📋 Histórico": "Histórico",
    "👥 Usuários": "Usuários",
}
# Descobre índice atual
page_labels = list(PAGE_MAP.keys())[:len(pages)]
current_label = next((k for k, v in PAGE_MAP.items() if v == st.session_state.page), page_labels[0])
default_idx = page_labels.index(current_label) if current_label in page_labels else 0

selected_tab = st.tabs(pages)
# Controlamos qual aba renderizar via session_state.page
# Cada aba vai verificar se é a ativa
_active_page = st.session_state.page

current_page = _active_page

# ══════════════════════════════════════════════════════════════════
# DASHBOARD
# ══════════════════════════════════════════════════════════════════
with selected_tab[0]:  # Dashboard
    st.markdown('<div style="font-family:Syne,sans-serif;font-size:1.5rem;font-weight:800;color:#00704A;margin-bottom:4px;">Visão <span style=\'color:#00704A\'>Geral</span></div>', unsafe_allow_html=True)
    st.markdown(f'<div style="font-size:0.8rem;color:#1a6645;">Atualizado em {datetime.now().strftime("%d/%m/%Y às %H:%M")}</div>', unsafe_allow_html=True)
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

    # ── FILTRO DE DATA (acima dos cards) ──
    # Usa keys intermediárias (_val) para os atalhos não conflitarem com os widgets já renderizados
    st.markdown('<div class="section-title">🗓️ Filtrar Período de Análise</div>', unsafe_allow_html=True)

    if lancamentos:
        datas_existentes = [datetime.strptime(l["data"], "%Y-%m-%d").date() for l in lancamentos]
        data_min_dados = min(datas_existentes)
    else:
        data_min_dados = date.today().replace(day=1)

    # Inicializa as keys intermediárias apenas uma vez
    if "filtro_inicio_val" not in st.session_state:
        st.session_state.filtro_inicio_val = data_min_dados
    if "filtro_fim_val" not in st.session_state:
        st.session_state.filtro_fim_val = date.today()

    # Atalhos ficam ANTES dos widgets — alteram só as keys intermediárias
    col_d1, col_d2, col_d3 = st.columns([2, 2, 3])
    with col_d3:
        st.markdown('<div style="padding-top:8px;font-size:0.72rem;color:#1a6645;font-weight:600;text-transform:uppercase;letter-spacing:.5px;margin-bottom:4px;">Atalhos rápidos</div>', unsafe_allow_html=True)
        col_at1, col_at2, col_at3 = st.columns(3)
        with col_at1:
            if st.button("Este mês", key="at_mes", use_container_width=True):
                st.session_state.filtro_inicio_val = date.today().replace(day=1)
                st.session_state.filtro_fim_val    = date.today()
                st.rerun()
        with col_at2:
            if st.button("Últ. 3 meses", key="at_3m", use_container_width=True):
                st.session_state.filtro_inicio_val = date.today() - timedelta(days=90)
                st.session_state.filtro_fim_val    = date.today()
                st.rerun()
        with col_at3:
            if st.button("Este ano", key="at_ano", use_container_width=True):
                st.session_state.filtro_inicio_val = date.today().replace(month=1, day=1)
                st.session_state.filtro_fim_val    = date.today()
                st.rerun()

    # Widgets leem value= das keys intermediárias (sem key= própria para evitar conflito)
    with col_d1:
        data_inicio = st.date_input(
            "📅 Data inicial",
            value=st.session_state.filtro_inicio_val,
            min_value=date(2000, 1, 1),
            max_value=date.today(),
            format="DD/MM/YYYY"
        )
        st.session_state.filtro_inicio_val = data_inicio
    with col_d2:
        data_fim = st.date_input(
            "📅 Data final",
            value=st.session_state.filtro_fim_val,
            min_value=date(2000, 1, 1),
            max_value=date.today(),
            format="DD/MM/YYYY"
        )
        st.session_state.filtro_fim_val = data_fim

    if data_inicio > data_fim:
        st.warning("⚠️ A data inicial não pode ser maior que a data final.")
        st.stop()

    # Filtra lançamentos pelo período selecionado
    def no_periodo(l):
        d = datetime.strptime(l["data"], "%Y-%m-%d").date()
        return data_inicio <= d <= data_fim

    lanc_filtrados = [l for l in lancamentos if no_periodo(l)]

    receitas  = [l for l in lanc_filtrados if l["tipo"] == "Receita"]
    despesas  = [l for l in lanc_filtrados if l["tipo"] != "Receita"]
    fixos     = [l for l in despesas       if l["tipo"] == "Fixo"]
    variaveis = [l for l in despesas       if l["tipo"] == "Variável"]

    total_r = sum(l["valor"] for l in receitas)
    total_d = sum(l["valor"] for l in despesas)
    saldo   = total_r - total_d

    periodo_label = f"{data_inicio.strftime('%d/%m/%Y')} → {data_fim.strftime('%d/%m/%Y')}"
    st.markdown(f'<div style="font-size:0.75rem;color:#1a6645;margin:6px 0 14px;">📌 Período: <b>{periodo_label}</b> · {len(lanc_filtrados)} lançamentos encontrados</div>', unsafe_allow_html=True)

    # ── KPI Cards (Receitas, Despesas, Saldo) ──
    saldo_cor = "pos" if saldo >= 0 else "neg"
    saldo_bor = "verde" if saldo >= 0 else "vermelho"

    k1, k2, k3 = st.columns(3)
    for col, cor, label, val, sub, cls in [
        (k1, "verde",   "Receitas",  total_r, f"{len(receitas)} lançamentos", "pos"),
        (k2, "vermelho","Despesas",  total_d, f"{len(despesas)} lançamentos", "neg"),
        (k3, saldo_bor, "Saldo",     saldo,   "Receitas – Despesas",          saldo_cor),
    ]:
        with col:
            st.markdown(f"""<div class="kpi {cor}">
              <div class="kpi-label">{label}</div>
              <div class="kpi-value {cls}">{fmt_brl(val)}</div>
              <div class="kpi-sub">{sub}</div>
            </div>""", unsafe_allow_html=True)

    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

    # ── Gráfico de Linha Suavizada: Evolução Mensal ──
    if lanc_filtrados:
        st.markdown('<div class="section-title">Evolução Mensal</div>', unsafe_allow_html=True)
        df = pd.DataFrame(lanc_filtrados)
        df["mes_periodo"] = pd.to_datetime(df["data"]).dt.to_period("M")
        df["mes_str"]     = df["mes_periodo"].astype(str)

        # Agrega por mês
        gr = df.groupby(["mes_str", "tipo"])["valor"].sum().reset_index()
        meses = sorted(df["mes_str"].unique())

        def mes_val(tipo):
            return [gr[(gr["mes_str"] == m) & (gr["tipo"] == tipo)]["valor"].sum() for m in meses]

        rec_v  = mes_val("Receita")
        desp_v = [sum(gr[(gr["mes_str"] == m) & (gr["tipo"] != "Receita")]["valor"]) for m in meses]
        sald_v = [r - d for r, d in zip(rec_v, desp_v)]

        # Labels: "Jan/25", "Fev/25" etc.
        meses_nomes = ["Jan","Fev","Mar","Abr","Mai","Jun","Jul","Ago","Set","Out","Nov","Dez"]
        def formatar_mes(m_str):
            ano, mes = m_str.split("-")
            return f"{meses_nomes[int(mes)-1]}/{ano[2:]}"
        labels = [formatar_mes(m) for m in meses]

        fig = go.Figure()
        for nome, vals, cor, fill_cor in [
            ("Receita", rec_v,  "#05C47A", "rgba(5,196,122,0.12)"),
            ("Despesa", desp_v, "#c0392b", "rgba(192,57,43,0.10)"),
            ("Saldo",   sald_v, "#f1c40f", "rgba(241,196,15,0.10)"),
        ]:
            fig.add_trace(go.Scatter(
                x=labels,
                y=vals,
                name=nome,
                mode="lines+markers",
                line=dict(color=cor, width=3, shape="spline", smoothing=1.2),
                fill="tozeroy",
                fillcolor=fill_cor,
                marker=dict(size=8, color=cor, line=dict(width=2, color="#fff")),
                hovertemplate=f"<b>{nome}</b><br>%{{x}}<br>R$ %{{y:,.2f}}<extra></extra>"
            ))

        fig.update_layout(
            paper_bgcolor="white",
            plot_bgcolor="#f4faf7",
            height=280,
            margin=dict(t=10, b=40, l=10, r=10),
            font=dict(family="DM Sans"),
            legend=dict(orientation="h", y=-0.28, x=0.5, xanchor="center",
                        font=dict(size=12)),
            yaxis=dict(tickprefix="R$ ", gridcolor="#eef5f1", zeroline=True,
                       zerolinecolor="#d0e8db"),
            xaxis=dict(gridcolor="rgba(0,0,0,0)", tickfont=dict(size=11)),
            hovermode="x unified"
        )
        st.plotly_chart(fig, use_container_width=True)

    # ── Gráfico de Pareto de Despesas por Categoria ──
    if despesas:
        st.markdown('<div class="section-title">Análise de Pareto — Despesas por Categoria</div>', unsafe_allow_html=True)
        st.caption("As barras mostram o valor absoluto por categoria; a linha amarela indica o percentual acumulado.")

        classe_map = {}
        for l in despesas:
            classe_map[l["classe"]] = classe_map.get(l["classe"], 0) + l["valor"]

        total_cls = sum(classe_map.values()) or 1
        sorted_cls = sorted(classe_map.items(), key=lambda x: -x[1])
        cats_pareto    = [c[0] for c in sorted_cls]
        vals_pareto    = [c[1] for c in sorted_cls]
        acumulado      = []
        soma = 0
        for v in vals_pareto:
            soma += v / total_cls * 100
            acumulado.append(round(soma, 2))

        # Gradiente de verde mais escuro para mais claro
        n = len(cats_pareto)
        cores_barras = [f"rgba({0 + int(i * (5-0)/max(n-1,1))}, {112 + int(i * (196-112)/max(n-1,1))}, {74 + int(i * (122-74)/max(n-1,1))}, 0.9)" for i in range(n)]

        fig_pareto = go.Figure()
        fig_pareto.add_trace(go.Bar(
            x=cats_pareto,
            y=vals_pareto,
            name="Valor (R$)",
            marker_color=cores_barras,
            marker_line_width=0,
            hovertemplate="<b>%{x}</b><br>R$ %{y:,.2f}<extra></extra>"
        ))
        fig_pareto.add_trace(go.Scatter(
            x=cats_pareto,
            y=acumulado,
            name="% Acumulado",
            mode="lines+markers",
            yaxis="y2",
            line=dict(color="#FFD700", width=3, shape="spline"),
            marker=dict(size=8, color="#f1c40f", line=dict(width=2, color="#fff")),
            hovertemplate="<b>%{x}</b><br>Acum: %{y:.1f}%<extra></extra>"
        ))

        # Linha de referência 80%
        fig_pareto.add_shape(
            type="line", xref="paper", yref="y2",
            x0=0, x1=1, y0=80, y1=80,
            line=dict(color="#c0392b", width=1.5, dash="dot")
        )
        fig_pareto.add_annotation(
            xref="paper", yref="y2",
            x=1.01, y=80, text="80%",
            showarrow=False, font=dict(color="#c0392b", size=10)
        )

        fig_pareto.update_layout(
            paper_bgcolor="white",
            plot_bgcolor="#f4faf7",
            height=300,
            margin=dict(t=10, b=30, l=10, r=50),
            font=dict(family="DM Sans"),
            legend=dict(orientation="h", y=-0.25, x=0.5, xanchor="center"),
            yaxis=dict(tickprefix="R$ ", gridcolor="#eef5f1", title=""),
            yaxis2=dict(overlaying="y", side="right", range=[0, 110],
                        ticksuffix="%", showgrid=False, title=""),
            xaxis=dict(gridcolor="rgba(0,0,0,0)"),
            bargap=0.25
        )
        st.plotly_chart(fig_pareto, use_container_width=True)

    # ── Gráfico de Barras: Top Despesas por Descrição (gradiente vermelho) ──
    if despesas:
        st.markdown('<div class="section-title">Top Itens de Despesa</div>', unsafe_allow_html=True)
        col_top, col_limitar = st.columns([4, 1])
        with col_limitar:
            top_n = st.selectbox("Mostrar top:", [5, 10, 15, 20], index=0, key="top_n_desp", label_visibility="collapsed")

        desc_map = {}
        for l in despesas:
            chave = f"{l['icone']} {l['descricao']}"
            desc_map[chave] = desc_map.get(chave, 0) + l["valor"]
        sorted_desc = sorted(desc_map.items(), key=lambda x: -x[1])[:top_n]

        if sorted_desc:
            itens_top  = [s[0] for s in sorted_desc]
            vals_top   = [s[1] for s in sorted_desc]
            n_top      = len(itens_top)

            # Gradiente vermelho: do mais escuro (#7b0000) ao mais claro (#f5b7b1)
            def red_gradient(i, total):
                r_start, g_start, b_start = 123, 0, 0      # escuro
                r_end,   g_end,   b_end   = 245, 183, 177  # claro
                t = i / max(total - 1, 1)
                r = int(r_start + t * (r_end - r_start))
                g = int(g_start + t * (g_end - g_start))
                b = int(b_start + t * (b_end - b_start))
                return f"rgb({r},{g},{b})"

            cores_red = [red_gradient(i, n_top) for i in range(n_top)]

            fig_top = go.Figure(go.Bar(
                y=itens_top[::-1],
                x=vals_top[::-1],
                orientation="h",
                marker_color=cores_red[::-1],
                marker_line_width=0,
                hovertemplate="<b>%{y}</b><br>R$ %{x:,.2f}<extra></extra>"
            ))
            fig_top.update_layout(
                paper_bgcolor="white",
                plot_bgcolor="#f4faf7",
                height=max(220, n_top * 32),
                margin=dict(t=10, b=20, l=10, r=10),
                font=dict(family="DM Sans"),
                xaxis=dict(tickprefix="R$ ", gridcolor="#eef5f1"),
                yaxis=dict(gridcolor="rgba(0,0,0,0)", tickfont=dict(size=11)),
                showlegend=False
            )
            st.plotly_chart(fig_top, use_container_width=True)

    # ── Linha divisória ──
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

    # ── Gráfico: Composição Fixo vs Variável (Donut) + Receita vs Despesa ──
    if despesas or receitas:
        col_donut1, col_donut2 = st.columns(2)

        with col_donut1:
            st.markdown('<div class="section-title">Composição das Despesas</div>', unsafe_allow_html=True)
            total_f = sum(l["valor"] for l in fixos)
            total_v = sum(l["valor"] for l in variaveis)
            if total_f + total_v > 0:
                fig_donut1 = go.Figure(go.Pie(
                    labels=["Fixos", "Variáveis"],
                    values=[total_f, total_v],
                    hole=0.6,
                    marker_colors=["#00704A", "#f39c12"],
                    textinfo="percent+label",
                    hovertemplate="<b>%{label}</b><br>R$ %{value:,.2f}<br>%{percent}<extra></extra>"
                ))
                fig_donut1.add_annotation(
                    text=f"<b>{fmt_brl(total_f + total_v)}</b>",
                    x=0.5, y=0.5, showarrow=False,
                    font=dict(size=13, family="Syne", color="#004f34")
                )
                fig_donut1.update_layout(
                    paper_bgcolor="white", height=240,
                    margin=dict(t=10, b=10, l=10, r=10),
                    showlegend=True,
                    legend=dict(orientation="h", y=-0.1, x=0.5, xanchor="center"),
                    font=dict(family="DM Sans")
                )
                st.plotly_chart(fig_donut1, use_container_width=True)

        with col_donut2:
            st.markdown('<div class="section-title">Receita vs Despesa</div>', unsafe_allow_html=True)
            if total_r + total_d > 0:
                fig_donut2 = go.Figure(go.Pie(
                    labels=["Receitas", "Despesas"],
                    values=[total_r, total_d],
                    hole=0.6,
                    marker_colors=["#05C47A", "#c0392b"],
                    textinfo="percent+label",
                    hovertemplate="<b>%{label}</b><br>R$ %{value:,.2f}<br>%{percent}<extra></extra>"
                ))
                saldo_txt = fmt_brl(saldo)
                saldo_cor_ann = "#00704A" if saldo >= 0 else "#c0392b"
                fig_donut2.add_annotation(
                    text=f"<b>{saldo_txt}</b>",
                    x=0.5, y=0.5, showarrow=False,
                    font=dict(size=12, family="Syne", color=saldo_cor_ann)
                )
                fig_donut2.update_layout(
                    paper_bgcolor="white", height=240,
                    margin=dict(t=10, b=10, l=10, r=10),
                    showlegend=True,
                    legend=dict(orientation="h", y=-0.1, x=0.5, xanchor="center"),
                    font=dict(family="DM Sans")
                )
                st.plotly_chart(fig_donut2, use_container_width=True)

    # ── Gráfico: Gastos por Dia da Semana ──
    if despesas:
        st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
        st.markdown('<div class="section-title">Padrão de Gastos — Dia da Semana</div>', unsafe_allow_html=True)

        df_sem = pd.DataFrame(despesas)
        df_sem["data_dt"]    = pd.to_datetime(df_sem["data"])
        df_sem["dia_semana"] = df_sem["data_dt"].dt.dayofweek  # 0=seg, 6=dom
        dias_nomes = ["Seg", "Ter", "Qua", "Qui", "Sex", "Sáb", "Dom"]
        agg_sem = df_sem.groupby("dia_semana")["valor"].sum().reindex(range(7), fill_value=0)
        vals_sem = agg_sem.values.tolist()

        cores_sem = []
        max_sem = max(vals_sem) if max(vals_sem) > 0 else 1
        for v in vals_sem:
            intensidade = v / max_sem
            r = int(13  + intensidade * (26 - 13))
            g = int(74  + intensidade * (161 - 74))
            b = int(47  + intensidade * (94 - 47))
            cores_sem.append(f"rgba({r},{g},{b},0.85)")

        fig_sem = go.Figure(go.Bar(
            x=dias_nomes,
            y=vals_sem,
            marker_color=cores_sem,
            marker_line_width=0,
            hovertemplate="<b>%{x}</b><br>R$ %{y:,.2f}<extra></extra>"
        ))
        fig_sem.update_layout(
            paper_bgcolor="white", plot_bgcolor="#f4faf7",
            height=220, margin=dict(t=10, b=20, l=10, r=10),
            showlegend=False, font=dict(family="DM Sans"),
            yaxis=dict(tickprefix="R$ ", gridcolor="#eef5f1"),
            xaxis=dict(gridcolor="rgba(0,0,0,0)")
        )
        st.plotly_chart(fig_sem, use_container_width=True)

    # ── Gráfico: Evolução do Saldo Acumulado (linha saúde financeira) ──
    if lanc_filtrados:
        st.markdown('<div class="section-title">Saúde Financeira — Saldo Acumulado</div>', unsafe_allow_html=True)

        df_sal = pd.DataFrame(lanc_filtrados)
        df_sal["data_dt"] = pd.to_datetime(df_sal["data"])
        df_sal["valor_signed"] = df_sal.apply(
            lambda r: r["valor"] if r["tipo"] == "Receita" else -r["valor"], axis=1
        )
        df_sal_sorted = df_sal.sort_values("data_dt")
        df_sal_sorted["saldo_acum"] = df_sal_sorted["valor_signed"].cumsum()
        df_sal_sorted["data_fmt"]   = df_sal_sorted["data_dt"].dt.strftime("%d/%m/%Y")
        df_sal_sorted["mes_ano"]    = df_sal_sorted["data_dt"].dt.strftime("%b/%y")

        # Agrega por dia para limpar sobreposições
        df_daily = df_sal_sorted.groupby("data_dt").agg(
            saldo_acum=("saldo_acum", "last"),
            data_fmt=("data_fmt", "last")
        ).reset_index()

        cor_linha = "#05C47A" if df_daily["saldo_acum"].iloc[-1] >= 0 else "#c0392b"
        fill_acum = "rgba(5,196,122,0.12)" if df_daily["saldo_acum"].iloc[-1] >= 0 else "rgba(192,57,43,0.10)"

        fig_acum = go.Figure()
        fig_acum.add_trace(go.Scatter(
            x=df_daily["data_fmt"],
            y=df_daily["saldo_acum"],
            mode="lines",
            line=dict(color=cor_linha, width=2.5, shape="spline", smoothing=0.8),
            fill="tozeroy",
            fillcolor=fill_acum,
            hovertemplate="<b>%{x}</b><br>Saldo: R$ %{y:,.2f}<extra></extra>"
        ))
        fig_acum.add_shape(
            type="line", xref="paper", yref="y",
            x0=0, x1=1, y0=0, y1=0,
            line=dict(color="#1a6645", width=1, dash="dot")
        )
        fig_acum.update_layout(
            paper_bgcolor="white", plot_bgcolor="#f4faf7",
            height=220, margin=dict(t=10, b=20, l=10, r=10),
            showlegend=False, font=dict(family="DM Sans"),
            yaxis=dict(tickprefix="R$ ", gridcolor="#eef5f1", zeroline=False),
            xaxis=dict(gridcolor="rgba(0,0,0,0)", nticks=8)
        )
        st.plotly_chart(fig_acum, use_container_width=True)

    # ── Gastos por Categoria (cards com barra) ──
    if despesas:
        st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
        st.markdown('<div class="section-title">Gastos por Categoria</div>', unsafe_allow_html=True)
        cats = sorted(classe_map.items(), key=lambda x: -x[1])
        max_val = cats[0][1] if cats else 1
        icons = {"Alimentação":"🍽️","Transporte":"🚗","Moradia":"🏠","Saúde":"💊",
                 "Lazer":"🎉","Educação":"📚","Serviços":"📡","Vestuário":"👗","Outros":"📌"}
        cols = st.columns(min(4, len(cats)))
        for i, (cls, val) in enumerate(cats):
            with cols[i % 4]:
                pct = int(val/max_val*100)
                st.markdown(f"""<div style="background:#fff;border-radius:12px;padding:14px 16px;
                  box-shadow:0 2px 10px rgba(0,112,74,.08);border:1.5px solid #b8e8d4;margin-bottom:10px;">
                  <div style="font-size:1.2rem;">{icons.get(cls,"📌")}</div>
                  <div style="font-size:0.68rem;font-weight:600;color:#1a6645;
                    text-transform:uppercase;letter-spacing:.5px;">{cls}</div>
                  <div style="font-family:Syne,sans-serif;font-size:1.1rem;
                    font-weight:700;color:#004f34;">{fmt_brl(val)}</div>
                  <div style="background:#d0e8db;border-radius:4px;height:3px;margin-top:6px;">
                    <div style="width:{pct}%;background:#00704A;height:3px;border-radius:4px;"></div>
                  </div>
                </div>""", unsafe_allow_html=True)

    # ── Últimos Lançamentos ──
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Últimos Lançamentos no Período</div>', unsafe_allow_html=True)
    if not lanc_filtrados:
        st.info("Nenhum lançamento no período selecionado.")
    else:
        ultimos = lanc_filtrados[:10]
        rows = []
        for l in ultimos:
            d = l["data"].split("-"); data_fmt = f"{d[2]}/{d[1]}/{d[0]}"
            sinal = "+" if l["tipo"] == "Receita" else "-"
            rows.append({"Data": data_fmt, "Descrição": f"{l['icone']} {l['descricao']}",
                         "Tipo": l["tipo"], "Categoria": l["classe"],
                         "Valor": f"{sinal} {fmt_brl(l['valor'])}"})
        st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)

# ══════════════════════════════════════════════════════════════════
# LANÇAMENTOS
# ══════════════════════════════════════════════════════════════════
with selected_tab[1]:  # Lançamentos
    st.markdown('<div style="font-family:Syne,sans-serif;font-size:1.5rem;font-weight:800;color:#00704A;margin-bottom:4px;">Novo <span style=\'color:#00704A\'>Lançamento</span></div>', unsafe_allow_html=True)
    st.markdown('<div style="font-size:0.8rem;color:#1a6645;margin-bottom:20px;">Informe data, valor e descrição — a categoria é detectada automaticamente.</div>', unsafe_allow_html=True)

    aba_lanc = st.tabs(["✏️ Lançamento Manual", "📂 Importar Excel"])

    # ── Manual ──
    with aba_lanc[0]:
        with st.form("form_lancamento", clear_on_submit=True):
            c1, c2 = st.columns(2)
            with c1:
                data_input = st.date_input("📅 Data", value=date.today())
            with c2:
                valor_input = st.number_input("💰 Valor (R$)", min_value=0.01, step=0.01, format="%.2f")
            desc_input = st.text_input("📝 Descrição", placeholder="Ex: Conta de luz, Supermercado, Salário...")

            if desc_input and len(desc_input) >= 3:
                tipo_det, cls_det, ico_det = classificar(desc_input)
                st.info(f"{ico_det} Detectado automaticamente: **{cls_det}** · {tipo_det}")

            submitted = st.form_submit_button("✦ Registrar Lançamento", type="primary", use_container_width=True)
            if submitted:
                if not desc_input:
                    st.error("Preencha a descrição.")
                else:
                    tipo, cls, ico = classificar(desc_input)
                    novo = {
                        "id": int(datetime.now().timestamp() * 1000),
                        "data": str(data_input),
                        "valor": float(valor_input),
                        "descricao": desc_input.strip(),
                        "tipo": tipo, "classe": cls, "icone": ico,
                    }
                    st.session_state.lancamentos.insert(0, novo)
                    persistir()
                    st.success(f"✅ Registrado: {ico} {cls} — {fmt_brl(valor_input)}")
                    st.rerun()

    # ── Importar Excel ──
    with aba_lanc[1]:
        st.markdown('<div class="section-title">📂 Importar planilha Excel</div>', unsafe_allow_html=True)
        st.markdown("""
        <div style="font-size:0.8rem;color:#1a6645;margin-bottom:12px;">
        Envie um arquivo <b>.xlsx</b> ou <b>.xls</b>. O sistema tentará identificar automaticamente
        as colunas de <b>data</b>, <b>valor</b> e <b>descrição</b>.
        Linhas não identificadas serão listadas para preenchimento manual.
        </div>
        """, unsafe_allow_html=True)

        arquivo_excel = st.file_uploader("Selecionar arquivo Excel", type=["xlsx", "xls"], key="excel_uploader")

        if arquivo_excel:
            try:
                df_excel = pd.read_excel(arquivo_excel)
            except Exception as e:
                st.error(f"❌ Erro ao ler o arquivo: {e}")
                df_excel = None

            if df_excel is not None and not df_excel.empty:
                st.markdown(f'<div style="font-size:0.75rem;color:#1a6645;margin-bottom:8px;">📄 {len(df_excel)} linhas encontradas · Colunas: {", ".join(df_excel.columns.tolist())}</div>', unsafe_allow_html=True)

                def encontrar_col(df, palavras):
                    for c in df.columns:
                        cn = c.lower().strip()
                        if any(p in cn for p in palavras):
                            return c
                    return None

                col_data_x  = encontrar_col(df_excel, ["data","date","dt","dia"])
                col_valor_x = encontrar_col(df_excel, ["valor","value","quantia","montante","vl","amount","total"])
                col_desc_x  = encontrar_col(df_excel, ["descri","desc","historico","hist","memo","observ","detalhe","título","titulo","nome"])

                linhas_ok_x  = []
                linhas_rev_x = []

                for idx, row in df_excel.iterrows():
                    d_val = row[col_data_x]  if col_data_x  else None
                    v_val = row[col_valor_x] if col_valor_x else None
                    s_val = row[col_desc_x]  if col_desc_x  else None

                    d_ok, d_parsed = False, None
                    if d_val is not None and not (isinstance(d_val, float) and pd.isna(d_val)):
                        try:
                            d_parsed = pd.to_datetime(d_val, dayfirst=True).date()
                            d_ok = True
                        except Exception:
                            pass

                    v_ok, v_parsed = False, None
                    if v_val is not None and not (isinstance(v_val, float) and pd.isna(v_val)):
                        try:
                            v_parsed = float(str(v_val).replace("R$","").replace(".","").replace(",",".").strip())
                            if v_parsed > 0:
                                v_ok = True
                        except Exception:
                            pass

                    s_ok, s_parsed = False, ""
                    if s_val is not None and not (isinstance(s_val, float) and pd.isna(s_val)):
                        s_parsed = str(s_val).strip()
                        if len(s_parsed) >= 2:
                            s_ok = True

                    if d_ok and v_ok and s_ok:
                        linhas_ok_x.append({"idx": idx, "data": d_parsed, "valor": v_parsed, "desc": s_parsed})
                    else:
                        linhas_rev_x.append({"idx": idx, "d_ok": d_ok, "d_val": d_parsed or d_val,
                                             "v_ok": v_ok, "v_val": v_parsed or v_val,
                                             "s_ok": s_ok, "s_val": s_parsed or s_val})

                if linhas_ok_x:
                    st.markdown(f'<div class="section-title">✅ {len(linhas_ok_x)} linha(s) prontas para importar</div>', unsafe_allow_html=True)
                    for item in linhas_ok_x[:5]:
                        tipo_p, cls_p, ico_p = classificar(item["desc"])
                        st.markdown(f"""<div class="excel-row excel-row-ok">
                          <span style="font-size:0.72rem;color:#1a6645;">{item['data'].strftime('%d/%m/%Y')} · {badge_tipo(tipo_p)} {badge_classe(cls_p)}</span><br>
                          <span style="font-size:0.9rem;font-weight:600;">{ico_p} {item['desc']}</span>
                          <span style="float:right;font-family:Syne,sans-serif;color:#00704A;font-weight:700;">{fmt_brl(item['valor'])}</span>
                        </div>""", unsafe_allow_html=True)
                    if len(linhas_ok_x) > 5:
                        st.caption(f"… e mais {len(linhas_ok_x) - 5} linha(s).")

                if linhas_rev_x:
                    st.markdown(f'<div class="section-title">⚠️ {len(linhas_rev_x)} linha(s) precisam de revisão</div>', unsafe_allow_html=True)
                    st.markdown('<div style="font-size:0.78rem;color:#c05e00;margin-bottom:10px;">Preencha apenas os campos com ⚠️ que não puderam ser identificados automaticamente.</div>', unsafe_allow_html=True)

                    if "excel_revisao" not in st.session_state:
                        st.session_state.excel_revisao = {}

                    for item in linhas_rev_x:
                        idx = item["idx"]
                        titulo_exp = str(item["s_val"])[:40] if item["s_val"] else f"Linha {idx+1} (sem descrição)"
                        with st.expander(f"Linha {idx + 1} — {titulo_exp}", expanded=True):
                            r1, r2, r3 = st.columns(3)
                            with r1:
                                label_d = "📅 Data" + ("" if item["d_ok"] else " ⚠️")
                                val_d = item["d_val"] if isinstance(item["d_val"], date) else date.today()
                                data_rev = st.date_input(label_d, value=val_d, key=f"rev_d_{idx}", disabled=item["d_ok"])
                            with r2:
                                label_v = "💰 Valor" + ("" if item["v_ok"] else " ⚠️")
                                val_v = float(item["v_val"]) if item["v_ok"] and item["v_val"] else 0.01
                                valor_rev = st.number_input(label_v, min_value=0.01, value=max(float(val_v), 0.01), step=0.01, format="%.2f", key=f"rev_v_{idx}", disabled=item["v_ok"])
                            with r3:
                                label_s = "📝 Descrição" + ("" if item["s_ok"] else " ⚠️")
                                desc_rev = st.text_input(label_s, value=str(item["s_val"]) if item["s_val"] else "", key=f"rev_s_{idx}", disabled=item["s_ok"])

                            d_final = item["d_val"] if item["d_ok"] else data_rev
                            v_final = item["v_val"] if item["v_ok"] else valor_rev
                            s_final = item["s_val"] if item["s_ok"] else desc_rev

                            if s_final and len(str(s_final)) >= 2:
                                t_p, c_p, i_p = classificar(str(s_final))
                                st.caption(f"{i_p} Categoria detectada: **{c_p}** · {t_p}")

                            st.session_state.excel_revisao[idx] = {"data": d_final, "valor": v_final, "desc": s_final}

                if linhas_ok_x or linhas_rev_x:
                    st.markdown("<div style='height:0.5rem'></div>", unsafe_allow_html=True)
                    if st.button("✦ Importar todos os lançamentos", type="primary", use_container_width=True, key="btn_importar_excel"):
                        importados = 0
                        erros = 0
                        ts_base = int(datetime.now().timestamp() * 1000)

                        for i, item in enumerate(linhas_ok_x):
                            tipo_i, cls_i, ico_i = classificar(item["desc"])
                            st.session_state.lancamentos.insert(0, {
                                "id": ts_base + i,
                                "data": str(item["data"]),
                                "valor": float(item["valor"]),
                                "descricao": item["desc"],
                                "tipo": tipo_i, "classe": cls_i, "icone": ico_i,
                            })
                            importados += 1

                        for j, item in enumerate(linhas_rev_x):
                            idx = item["idx"]
                            rev = st.session_state.get("excel_revisao", {}).get(idx, {})
                            d_f = item["d_val"] if item["d_ok"] else rev.get("data")
                            v_f = item["v_val"] if item["v_ok"] else rev.get("valor")
                            s_f = item["s_val"] if item["s_ok"] else rev.get("desc")
                            if d_f and v_f and s_f and len(str(s_f)) >= 2:
                                try:
                                    tipo_j, cls_j, ico_j = classificar(str(s_f))
                                    d_str = str(d_f) if isinstance(d_f, date) else str(d_f)[:10]
                                    st.session_state.lancamentos.insert(0, {
                                        "id": ts_base + len(linhas_ok_x) + j,
                                        "data": d_str, "valor": float(v_f),
                                        "descricao": str(s_f).strip(),
                                        "tipo": tipo_j, "classe": cls_j, "icone": ico_j,
                                    })
                                    importados += 1
                                except Exception:
                                    erros += 1
                            else:
                                erros += 1

                        persistir()
                        if "excel_revisao" in st.session_state:
                            del st.session_state.excel_revisao
                        msg = f"✅ {importados} lançamento(s) importado(s)!"
                        if erros:
                            msg += f" · {erros} linha(s) ignorada(s) por dados incompletos."
                        st.success(msg)
                        st.rerun()

# ══════════════════════════════════════════════════════════════════
# HISTÓRICO — com aba "Apagados" embutida
# ══════════════════════════════════════════════════════════════════
with selected_tab[2]:  # Histórico
    st.markdown('<div style="font-family:Syne,sans-serif;font-size:1.5rem;font-weight:800;color:#00704A;margin-bottom:4px;">Histórico <span style=\'color:#00704A\'>& Apagados</span></div>', unsafe_allow_html=True)
    st.markdown('<div style="font-size:0.8rem;color:#1a6645;margin-bottom:16px;">Gerencie seus lançamentos e itens excluídos em um só lugar.</div>', unsafe_allow_html=True)

    aba_hist = st.tabs(["📋 Lançamentos Ativos", "🗑️ Apagados"])

    # ── Aba: Lançamentos Ativos ──
    with aba_hist[0]:
        if not lancamentos:
            st.info("Nenhum lançamento registrado ainda.")
        else:
            filtro = st.radio("Filtrar:", ["Todos", "Fixo", "Variável", "Receita"],
                              horizontal=True, label_visibility="collapsed")
            lista = lancamentos if filtro == "Todos" else [l for l in lancamentos if l["tipo"] == filtro]

            for l in lista:
                d = l["data"].split("-"); data_fmt = f"{d[2]}/{d[1]}/{d[0]}"
                sinal = "+" if l["tipo"] == "Receita" else "-"
                cor_val = "#00704A" if l["tipo"] == "Receita" else "#c0392b"
                col_info, col_val, col_btn = st.columns([5, 2, 1])
                with col_info:
                    st.markdown(f"""<div style="background:#fff;border-radius:10px;padding:12px 16px;
                      border:1.5px solid #b8e8d4;margin-bottom:6px;">
                      <div style="font-size:0.72rem;color:#1a6645;">{data_fmt} · {badge_tipo(l['tipo'])} {badge_classe(l['classe'])}</div>
                      <div style="font-size:0.92rem;font-weight:600;color:#0d2b1e;margin-top:3px;">{l['icone']} {l['descricao']}</div>
                    </div>""", unsafe_allow_html=True)
                with col_val:
                    st.markdown(f'<div style="font-family:Syne,sans-serif;font-size:1.05rem;font-weight:700;color:{cor_val};padding:18px 0;">{sinal} {fmt_brl(l["valor"])}</div>', unsafe_allow_html=True)
                with col_btn:
                    if st.button("🗑", key=f"del_{l['id']}", help="Mover para Apagados"):
                        l["apagadoEm"] = datetime.now().isoformat()
                        st.session_state.lixeira.insert(0, l)
                        st.session_state.lancamentos.remove(l)
                        persistir()
                        st.rerun()

    # ── Aba: Apagados ──
    with aba_hist[1]:
        st.markdown('<div style="font-size:0.8rem;color:#1a6645;margin-bottom:12px;">Itens excluídos do histórico. Restaure ou exclua definitivamente.</div>', unsafe_allow_html=True)

        if not lixeira:
            st.info("Nenhum item apagado.")
        else:
            for l in lixeira:
                d = l["data"].split("-"); data_fmt = f"{d[2]}/{d[1]}/{d[0]}"
                col_info, col_val, col_rest, col_del = st.columns([5, 2, 0.7, 0.7])
                with col_info:
                    st.markdown(f"""<div style="background:#fdecea;border-radius:10px;padding:12px 16px;
                      border:1.5px solid #f5b7b1;margin-bottom:6px;opacity:0.85;">
                      <div style="font-size:0.72rem;color:#c0392b;">{data_fmt} · {badge_tipo(l['tipo'])} {badge_classe(l['classe'])}</div>
                      <div style="font-size:0.92rem;font-weight:600;color:#7b241c;margin-top:3px;">{l['icone']} {l['descricao']}</div>
                    </div>""", unsafe_allow_html=True)
                with col_val:
                    st.markdown(f'<div style="font-family:Syne,sans-serif;font-size:1.05rem;font-weight:700;color:#c0392b;padding:18px 0;">– {fmt_brl(l["valor"])}</div>', unsafe_allow_html=True)
                with col_rest:
                    if st.button("↩️", key=f"rest_{l['id']}", help="Restaurar para Lançamentos"):
                        st.session_state.lancamentos.insert(0, {k: v for k, v in l.items() if k != "apagadoEm"})
                        st.session_state.lixeira.remove(l)
                        persistir()
                        st.success(f"✅ '{l['descricao']}' restaurado!")
                        st.rerun()
                with col_del:
                    if st.button("✕", key=f"perm_{l['id']}", help="Excluir permanentemente"):
                        lixeira.remove(l)
                        persistir()
                        st.rerun()

# ══════════════════════════════════════════════════════════════════
# USUÁRIOS (ADMIN)
# ══════════════════════════════════════════════════════════════════
with selected_tab[3] if len(selected_tab) > 3 else selected_tab[0]:  # Usuários (admin)
    if not st.session_state.is_admin:
        st.error("Acesso restrito ao administrador.")
    else:
        st.markdown('<div style="font-family:Syne,sans-serif;font-size:1.5rem;font-weight:800;color:#00704A;margin-bottom:4px;">Gestão de <span style=\'color:#00704A\'>Usuários</span></div>', unsafe_allow_html=True)
        st.markdown('<div style="font-size:0.8rem;color:#1a6645;margin-bottom:20px;">Painel de controle de acessos e aprovações.</div>', unsafe_allow_html=True)

        usuarios = load_users()

        st.markdown('<div class="section-title">⏳ Aguardando Aprovação</div>', unsafe_allow_html=True)
        pendentes = [u for u in usuarios if u.get("status") == "pendente"]

        if not pendentes:
            st.info("Não há nenhuma solicitação de acesso pendente.")
        else:
            for u in pendentes:
                col_u, col_btn1, col_btn2 = st.columns([5, 1, 1])
                with col_u:
                    st.markdown(f"""<div class="user-row" style="border-color: #f39c12;">
                      <div class="user-ava" style="background: #f39c12;">{u['usuario'][0].upper()}</div>
                      <div>
                        <div style="font-weight:600;font-size:0.9rem;color:#0d2b1e;">{u['usuario']}</div>
                        <div style="font-size:0.72rem;color:#d35400;">Aguardando liberação</div>
                      </div>
                    </div>""", unsafe_allow_html=True)
                with col_btn1:
                    if st.button("✓ Aprovar", key=f"aprov_{u['usuario']}", type="primary", use_container_width=True):
                        u["status"] = "aprovado"
                        save_users(usuarios)
                        st.success(f"Acesso liberado para {u['usuario']}!")
                        st.rerun()
                with col_btn2:
                    if st.button("✕ Recusar", key=f"recus_{u['usuario']}", use_container_width=True):
                        usuarios.remove(u)
                        save_users(usuarios)
                        st.warning(f"Solicitação de {u['usuario']} removida.")
                        st.rerun()

        st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

        st.markdown('<div class="section-title">👥 Usuários Cadastrados</div>', unsafe_allow_html=True)
        st.markdown('<div style="font-size:0.75rem;color:#1a6645;margin-bottom:10px;">Use os botões para ativar ou desativar o acesso de cada usuário. Você não pode desativar sua própria conta.</div>', unsafe_allow_html=True)

        # Todos exceto pendentes (já tratados acima)
        cadastrados = [u for u in usuarios if u.get("status") != "pendente"]

        for u in cadastrados:
            is_admin_u = u.get("role") == "admin"
            is_me = u["usuario"].lower() == st.session_state.username.lower()
            esta_ativo = u.get("status", "aprovado") == "aprovado"
            role_label = "👑 Administrador" if is_admin_u else "👤 Usuário"
            status_cor  = "#1a6645" if esta_ativo else "#c0392b"
            status_txt  = "✅ Ativo" if esta_ativo else "🚫 Desativado"

            col_u, col_toggle = st.columns([5, 1.4])
            with col_u:
                ava_cls = "user-ava-admin" if is_admin_u else ""
                me_tag  = ' <span style="font-size:10px;color:#00704A">(você)</span>' if is_me else ""
                card_bg  = "#fff" if esta_ativo else "#fdecea"
                card_bdr = "#d0e8db" if esta_ativo else "#f5b7b1"
                st.markdown(f"""<div style="display:flex;align-items:center;gap:14px;padding:12px 16px;
                  border-radius:12px;background:{card_bg};border:1.5px solid {card_bdr};margin-bottom:6px;">
                  <div class="user-ava {ava_cls}" style="opacity:{'1' if esta_ativo else '0.5'}">{u['usuario'][0].upper()}</div>
                  <div>
                    <div style="font-weight:600;font-size:0.9rem;color:#0d2b1e;">{u['usuario']}{me_tag}</div>
                    <div style="font-size:0.72rem;color:{status_cor};">{role_label} · {status_txt}</div>
                  </div>
                </div>""", unsafe_allow_html=True)
            with col_toggle:
                st.markdown("<div style='height:0.45rem'></div>", unsafe_allow_html=True)
                if is_me:
                    st.button("🔒 Você", key=f"tog_{u['usuario']}", disabled=True, use_container_width=True)
                elif esta_ativo:
                    if st.button("🚫 Desativar", key=f"tog_{u['usuario']}", use_container_width=True):
                        u["status"] = "desativado"
                        save_users(usuarios)
                        st.warning(f"Acesso de {u['usuario']} desativado.")
                        st.rerun()
                else:
                    if st.button("✅ Ativar", key=f"tog_{u['usuario']}", type="primary", use_container_width=True):
                        u["status"] = "aprovado"
                        save_users(usuarios)
                        st.success(f"Acesso de {u['usuario']} reativado!")
                        st.rerun()

        st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
        st.markdown('<div class="section-title">🔑 Trocar Senha</div>', unsafe_allow_html=True)

        ativos = [u for u in usuarios if u.get("status", "aprovado") == "aprovado"]
        nomes_ativos = [u["usuario"] for u in ativos]
        sel_u = st.selectbox("Selecionar usuário:", nomes_ativos)
        nova_s = st.text_input("Nova senha:", type="password", key="adm_nova")
        conf_s = st.text_input("Confirmar senha:", type="password", key="adm_conf")

        if st.button("💾 Salvar nova senha", type="primary"):
            if not nova_s or not conf_s: st.warning("Preencha os dois campos.")
            elif len(nova_s) < 3: st.warning("Mínimo 3 caracteres.")
            elif nova_s != conf_s: st.error("As senhas não conferem.")
            else:
                for u in usuarios:
                    if u["usuario"] == sel_u:
                        u["senha"] = hash_pw(nova_s)
                save_users(usuarios)
                st.success(f"✅ Senha de {sel_u} alterada com sucesso!")

# ─── FOOTER ───────────────────────────────────────────────────────────────────
st.markdown("---")
st.markdown(
    f"<p style='text-align:center;color:#1a6645;font-size:0.72rem;font-family:DM Sans;'>"
    f" FinançasPro · Usuário: <b>{st.session_state.username}</b> · "
    f"{len(lancamentos)} lançamentos</p>",
    unsafe_allow_html=True
)