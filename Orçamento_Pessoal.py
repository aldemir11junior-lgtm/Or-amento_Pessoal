import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, date
import json, hashlib, os

# ─── CONFIG ───────────────────────────────────────────────────────────────────
st.set_page_config(page_title="FinançasPro", page_icon="💰", layout="wide",
                   initial_sidebar_state="expanded")

BASE_DIR   = os.path.dirname(os.path.abspath(__file__))
USERS_FILE = os.path.join(BASE_DIR, "fp_usuarios.json")
DATA_FILE  = os.path.join(BASE_DIR, "fp_dados.json")

# ─── CSS ──────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Sans:wght@300;400;500;600&display=swap');
:root {
  --verde-escuro:#0d4a2f; --verde-principal:#1a7a4a; --verde-medio:#22a15e;
  --verde-claro:#4dc882;  --verde-menta:#a8f0c8;    --verde-fundo:#e8f7ef;
  --cinza-claro:#f4faf7;  --cinza-borda:#d0e8db;    --texto-escuro:#0d2b1e;
  --texto-medio:#3a6b53;
}
html,body,[class*="css"]{ font-family:'DM Sans',sans-serif; background:var(--cinza-claro); }

section[data-testid="stSidebar"] {
  background:linear-gradient(180deg,#0d4a2f 0%,#1a7a4a 60%,#22a15e 100%);
  border-right:2px solid rgba(77,200,130,0.2);
  min-width:210px!important; max-width:210px!important;
}
section[data-testid="stSidebar"] * { color:#e8f7ef!important; }
section[data-testid="stSidebar"] .stButton button {
  width:100%; background:rgba(255,255,255,0.07); border:none; border-radius:10px;
  color:#a8f0c8!important; font-family:'DM Sans',sans-serif; font-weight:600;
  font-size:0.84rem; padding:10px 14px; text-align:left; cursor:pointer;
  margin-bottom:4px; transition:all .18s;
}
section[data-testid="stSidebar"] .stButton button:hover {
  background:rgba(255,255,255,0.16); color:#fff!important;
}

.brand { font-family:'Syne',sans-serif; font-size:1.4rem; font-weight:800;
  color:#a8f0c8; text-align:center; padding:20px 0 4px; }
.brand span { color:#4dc882; }
.brand-sub { font-size:0.65rem; color:#22a15e; text-align:center;
  text-transform:uppercase; letter-spacing:1.2px; margin-bottom:20px; }

.kpi { background:#fff; border-radius:14px; padding:20px 22px;
  box-shadow:0 4px 24px rgba(13,74,47,.1); border:1.5px solid #d0e8db;
  border-top:4px solid; height:100%; }
.kpi.verde { border-top-color:#22a15e; }
.kpi.vermelho { border-top-color:#c0392b; }
.kpi.amarelo { border-top-color:#f39c12; }
.kpi.roxo { border-top-color:#8e44ad; }
.kpi-label { font-size:0.7rem; font-weight:600; text-transform:uppercase;
  letter-spacing:.8px; color:#3a6b53; margin-bottom:6px; }
.kpi-value { font-family:'Syne',sans-serif; font-size:1.9rem; font-weight:700;
  line-height:1.1; }
.kpi-value.pos { color:#1a7a4a; } .kpi-value.neg { color:#c0392b; }
.kpi-value.neu { color:#0d4a2f; }
.kpi-sub { font-size:0.72rem; color:#3a6b53; margin-top:4px; }

.section-title { font-family:'Syne',sans-serif; font-size:0.95rem; font-weight:700;
  color:#0d4a2f; border-left:4px solid #22a15e; padding-left:10px;
  margin:20px 0 12px; text-transform:uppercase; letter-spacing:.05em; }

.abc-item { border-radius:10px; padding:12px 16px; margin-bottom:8px;
  display:flex; justify-content:space-between; align-items:center; border:1.5px solid; }
.abc-a { background:#fdecea; border-color:#f5b7b1; }
.abc-b { background:#fef9e7; border-color:#f9e79f; }
.abc-c { background:#eafaf1; border-color:#a9dfbf; }
.abc-badge { font-size:0.7rem; font-weight:800; padding:2px 8px;
  border-radius:6px; display:inline-block; margin-bottom:3px; }
.abc-badge-a { background:#c0392b; color:#fff; }
.abc-badge-b { background:#d4ac0d; color:#fff; }
.abc-badge-c { background:#1e8449; color:#fff; }
.abc-name { font-size:0.88rem; font-weight:600; color:#0d2b1e; }
.abc-pct { font-size:0.72rem; color:#3a6b53; }
.abc-val { font-family:'Syne',sans-serif; font-size:1.05rem; font-weight:700; color:#0d2b1e; }

.login-box { max-width:420px; margin:60px auto; background:#fff;
  border-radius:20px; padding:40px; box-shadow:0 24px 80px rgba(0,0,0,.15); }
.login-title { font-family:'Syne',sans-serif; font-size:1.6rem; font-weight:800;
  color:#0d4a2f; margin-bottom:4px; }
.login-title span { color:#1a7a4a; }
.login-sub { font-size:0.72rem; color:#3a6b53; text-transform:uppercase;
  letter-spacing:1px; margin-bottom:24px; }

.divider { height:2px; background:linear-gradient(90deg,#22a15e,transparent);
  margin:18px 0; border-radius:2px; }

.badge { display:inline-block; padding:2px 9px; border-radius:20px;
  font-size:0.7rem; font-weight:700; }
.badge-receita   { background:#c8f7dc; color:#065f2e; }
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

.tag-pos { color:#1a7a4a; font-weight:700; font-family:'Syne',sans-serif; }
.tag-neg { color:#c0392b; font-weight:700; font-family:'Syne',sans-serif; }

.user-row { display:flex; align-items:center; gap:14px; padding:14px 18px;
  border-radius:12px; background:#f4faf7; border:1.5px solid #d0e8db;
  margin-bottom:8px; }
.user-ava { width:36px; height:36px; border-radius:50%; background:#1a7a4a;
  color:#fff; display:inline-flex; align-items:center; justify-content:center;
  font-family:'Syne',sans-serif; font-weight:700; font-size:14px; }
.user-ava-admin { background:#f39c12; }
</style>
""", unsafe_allow_html=True)

# ─── PERSISTÊNCIA ─────────────────────────────────────────────────────────────
def load_users():
    if os.path.exists(USERS_FILE):
        with open(USERS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    default = [{"usuario": "Aldemir", "senha": hash_pw("123"), "role": "admin"}]
    save_users(default)
    return default

def save_users(u):
    with open(USERS_FILE, "w", encoding="utf-8") as f:
        json.dump(u, f, ensure_ascii=False, indent=2)

def hash_pw(pw): return hashlib.sha256(pw.encode()).hexdigest()

def load_data(usuario):
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            all_data = json.load(f)
    else:
        all_data = {}
    key = usuario.lower()
    return (
        all_data.get(key, {}).get("lancamentos", []),
        all_data.get(key, {}).get("lixeira", []),
    )

def save_data(usuario, lancamentos, lixeira):
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            all_data = json.load(f)
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

# ══════════════════════════════════════════════════════════════════
# TELA DE LOGIN
# ══════════════════════════════════════════════════════════════════
if not st.session_state.logged_in:
    st.markdown("""
    <div style="text-align:center;padding:40px 0 10px">
      <div style="font-size:3rem">💰</div>
      <div style="font-family:Syne,sans-serif;font-size:1.8rem;font-weight:800;color:#0d4a2f;">
        Finanças<span style="color:#1a7a4a">Pro</span></div>
      <div style="font-size:0.75rem;color:#3a6b53;text-transform:uppercase;letter-spacing:1.2px;margin-top:4px;">
        Controle financeiro pessoal</div>
    </div>
    <div style="height:3px;background:linear-gradient(90deg,#22a15e,#e8f7ef);border-radius:2px;margin:18px auto 28px;max-width:280px"></div>
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
                        usuarios.append({"usuario": nu, "senha": hash_pw(p1), "role": "user"})
                        save_users(usuarios)
                        st.success("✅ Conta criada! Faça login.")
    st.stop()

# ─── A PARTIR DAQUI: USUÁRIO LOGADO ──────────────────────────────────────────
lancamentos = st.session_state.lancamentos
lixeira     = st.session_state.lixeira

def persistir():
    st.session_state.lancamentos = lancamentos
    st.session_state.lixeira     = lixeira
    save_data(st.session_state.username, lancamentos, lixeira)

# ─── SIDEBAR ──────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""<div class="brand">Finanças<span>Pro</span></div>
    <div class="brand-sub">Controle pessoal</div>""", unsafe_allow_html=True)

    pages = [("Dashboard","📊"), ("Lançamentos","➕"), ("Histórico","📋"),
             ("Apagados","🗑️")]
    if st.session_state.is_admin:
        pages.append(("Usuários","👥"))

    for pname, picon in pages:
        if st.button(f"{picon}  {pname}", key=f"nav_{pname}"):
            st.session_state.page = pname

    st.markdown("---")
    st.markdown(f'<div style="font-size:0.72rem;color:#a8f0c8!important;padding:0 0 2px;">👤 {st.session_state.username}'
                f'{"  👑" if st.session_state.is_admin else ""}</div>', unsafe_allow_html=True)

    if st.button("🚪 Sair", key="logout"):
        for k in list(st.session_state.keys()): del st.session_state[k]
        st.rerun()

current_page = st.session_state.page

# ══════════════════════════════════════════════════════════════════
# DASHBOARD
# ══════════════════════════════════════════════════════════════════
if current_page == "Dashboard":
    st.markdown('<div style="font-family:Syne,sans-serif;font-size:1.5rem;font-weight:800;color:#0d4a2f;margin-bottom:4px;">Visão <span style=\'color:#1a7a4a\'>Geral</span></div>', unsafe_allow_html=True)
    st.markdown(f'<div style="font-size:0.8rem;color:#3a6b53;">Atualizado em {datetime.now().strftime("%d/%m/%Y às %H:%M")}</div>', unsafe_allow_html=True)
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

    receitas  = [l for l in lancamentos if l["tipo"] == "Receita"]
    despesas  = [l for l in lancamentos if l["tipo"] != "Receita"]
    fixos     = [l for l in despesas    if l["tipo"] == "Fixo"]
    variaveis = [l for l in despesas    if l["tipo"] == "Variável"]

    total_r = sum(l["valor"] for l in receitas)
    total_d = sum(l["valor"] for l in despesas)
    total_f = sum(l["valor"] for l in fixos)
    total_v = sum(l["valor"] for l in variaveis)
    saldo   = total_r - total_d

    k1, k2, k3, k4 = st.columns(4)
    for col, cor, label, val, sub, cls in [
        (k1, "verde",    "Receitas",  total_r, f"{len(receitas)} lançamentos",  "pos"),
        (k2, "vermelho", "Despesas",  total_d, f"{len(despesas)} lançamentos",  "neg"),
        (k3, "amarelo",  "Fixos",     total_f, "Recorrente",                    "neu"),
        (k4, "roxo",     "Variáveis", total_v, "Pontual",                       "neu"),
    ]:
        with col:
            st.markdown(f"""<div class="kpi {cor}">
              <div class="kpi-label">{label}</div>
              <div class="kpi-value {cls}">{fmt_brl(val)}</div>
              <div class="kpi-sub">{sub}</div>
            </div>""", unsafe_allow_html=True)

    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

    # ── Gráfico Linha: Evolução Mensal ──
    if lancamentos:
        st.markdown('<div class="section-title">Evolução Mensal</div>', unsafe_allow_html=True)
        df = pd.DataFrame(lancamentos)
        df["mes"] = pd.to_datetime(df["data"]).dt.to_period("M").astype(str)
        gr = df.groupby(["mes","tipo"])["valor"].sum().reset_index()
        meses = sorted(df["mes"].unique())

        def mes_val(tipo):
            return [gr[(gr["mes"]==m) & (gr["tipo"]==tipo)]["valor"].sum() for m in meses]

        rec_v  = mes_val("Receita")
        desp_v = [sum(gr[(gr["mes"]==m) & (gr["tipo"]!="Receita")]["valor"]) for m in meses]
        sald_v = [r-d for r,d in zip(rec_v, desp_v)]
        labels = [m[2:] for m in meses]  # AAAA-MM → MM

        fig = go.Figure()
        for nome, vals, cor in [("Receita", rec_v, "#22a15e"),
                                 ("Despesa", desp_v, "#c0392b"),
                                 ("Saldo",   sald_v, "#f1c40f")]:
            fig.add_trace(go.Scatter(x=labels, y=vals, name=nome,
                mode="lines+markers", line=dict(color=cor, width=2.5),
                fill="tozeroy", fillcolor=cor.replace(")", ",0.07)").replace("rgb", "rgba") if "rgb" in cor else cor+"14",
                marker=dict(size=6, color=cor)))
        fig.update_layout(paper_bgcolor="white", plot_bgcolor="#f4faf7",
            height=260, margin=dict(t=10,b=30,l=10,r=10),
            font=dict(family="DM Sans"), legend=dict(orientation="h", y=-0.25),
            yaxis=dict(tickprefix="R$ ", gridcolor="#eef5f1"),
            xaxis=dict(gridcolor="#eef5f1"))
        st.plotly_chart(fig, use_container_width=True)

    # ── Análise ABC ──
    if despesas:
        st.markdown('<div class="section-title">Análise ABC de Despesas</div>', unsafe_allow_html=True)
        st.caption("**A** = maiores gastos (até 70%) · **B** = médios (até 90%) · **C** = menores (restante)")
        classe_map = {}
        for l in despesas:
            classe_map[l["classe"]] = classe_map.get(l["classe"], 0) + l["valor"]
        total_cls = sum(classe_map.values()) or 1
        sorted_cls = sorted(classe_map.items(), key=lambda x: -x[1])
        acum = 0
        for cls, val in sorted_cls:
            acum += val
            pct     = val / total_cls * 100
            acum_pct= acum / total_cls * 100
            cat     = "a" if acum_pct <= 70 else ("b" if acum_pct <= 90 else "c")
            st.markdown(f"""<div class="abc-item abc-{cat}">
              <div>
                <span class="abc-badge abc-badge-{cat}">{cat.upper()}</span>
                <div class="abc-name">{cls}</div>
                <div class="abc-pct">{pct:.1f}% do total</div>
              </div>
              <div class="abc-val">{fmt_brl(val)}</div>
            </div>""", unsafe_allow_html=True)

    # ── Gráficos: Barras por mês + Saldo ──
    col_g1, col_g2 = st.columns(2)
    with col_g1:
        st.markdown('<div class="section-title">Gastos por Mês</div>', unsafe_allow_html=True)
        if despesas:
            df_d = pd.DataFrame(despesas)
            df_d["mes"] = pd.to_datetime(df_d["data"]).dt.to_period("M").astype(str)
            bar_data = df_d.groupby("mes")["valor"].sum().tail(6).reset_index()
            bar_data["label"] = bar_data["mes"].str[5:]
            fig_b = px.bar(bar_data, x="label", y="valor",
                           color_discrete_sequence=["#1a7a4a"],
                           labels={"label":"Mês","valor":"R$"})
            fig_b.update_traces(marker_line_width=0)
            fig_b.update_layout(paper_bgcolor="white", plot_bgcolor="#f4faf7",
                height=220, margin=dict(t=10,b=20,l=10,r=10),
                showlegend=False, font=dict(family="DM Sans"),
                yaxis=dict(tickprefix="R$ ", gridcolor="#eef5f1"),
                xaxis=dict(gridcolor="rgba(0,0,0,0)"))
            st.plotly_chart(fig_b, use_container_width=True)
        else:
            st.info("Nenhuma despesa registrada.")

    with col_g2:
        st.markdown('<div class="section-title">Saldo Atual</div>', unsafe_allow_html=True)
        saldo_cor = "#1a7a4a" if saldo >= 0 else "#c0392b"
        saldo_sinal = "" if saldo >= 0 else "– "
        st.markdown(f"""<div style="background:#fff;border-radius:14px;padding:30px;
          box-shadow:0 4px 24px rgba(13,74,47,.1);border:1.5px solid #d0e8db;
          text-align:center;height:220px;display:flex;flex-direction:column;
          align-items:center;justify-content:center;">
          <div style="font-size:0.7rem;color:#3a6b53;text-transform:uppercase;
            letter-spacing:.8px;margin-bottom:8px;">Receitas – Despesas</div>
          <div style="font-family:Syne,sans-serif;font-size:2.2rem;font-weight:700;
            color:{saldo_cor};">{saldo_sinal}{fmt_brl(saldo)}</div>
        </div>""", unsafe_allow_html=True)

    # ── Gastos por Categoria ──
    if despesas:
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
                  box-shadow:0 2px 10px rgba(13,74,47,.08);border:1.5px solid #d0e8db;margin-bottom:10px;">
                  <div style="font-size:1.2rem;">{icons.get(cls,"📌")}</div>
                  <div style="font-size:0.68rem;font-weight:600;color:#3a6b53;
                    text-transform:uppercase;letter-spacing:.5px;">{cls}</div>
                  <div style="font-family:Syne,sans-serif;font-size:1.1rem;
                    font-weight:700;color:#0d4a2f;">{fmt_brl(val)}</div>
                  <div style="background:#d0e8db;border-radius:4px;height:3px;margin-top:6px;">
                    <div style="width:{pct}%;background:#1a7a4a;height:3px;border-radius:4px;"></div>
                  </div>
                </div>""", unsafe_allow_html=True)

    # ── Últimos Lançamentos ──
    st.markdown('<div class="section-title">Últimos Lançamentos</div>', unsafe_allow_html=True)
    if not lancamentos:
        st.info("Nenhum lançamento ainda.")
    else:
        ultimos = lancamentos[:10]
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
elif current_page == "Lançamentos":
    st.markdown('<div style="font-family:Syne,sans-serif;font-size:1.5rem;font-weight:800;color:#0d4a2f;margin-bottom:4px;">Novo <span style=\'color:#1a7a4a\'>Lançamento</span></div>', unsafe_allow_html=True)
    st.markdown('<div style="font-size:0.8rem;color:#3a6b53;margin-bottom:20px;">Informe data, valor e descrição — a categoria é detectada automaticamente.</div>', unsafe_allow_html=True)

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
                lancamentos.insert(0, novo)
                persistir()
                st.success(f"✅ Registrado: {ico} {cls} — {fmt_brl(valor_input)}")
                st.rerun()


# ══════════════════════════════════════════════════════════════════
# HISTÓRICO
# ══════════════════════════════════════════════════════════════════
elif current_page == "Histórico":
    st.markdown('<div style="font-family:Syne,sans-serif;font-size:1.5rem;font-weight:800;color:#0d4a2f;margin-bottom:4px;">Histórico <span style=\'color:#1a7a4a\'>Completo</span></div>', unsafe_allow_html=True)
    st.markdown('<div style="font-size:0.8rem;color:#3a6b53;margin-bottom:16px;">Todos os lançamentos registrados. Excluídos vão para Apagados.</div>', unsafe_allow_html=True)

    if not lancamentos:
        st.info("Nenhum lançamento registrado ainda.")
    else:
        filtro = st.radio("Filtrar:", ["Todos", "Fixo", "Variável", "Receita"],
                          horizontal=True, label_visibility="collapsed")
        lista = lancamentos if filtro == "Todos" else [l for l in lancamentos if l["tipo"] == filtro]

        for l in lista:
            d = l["data"].split("-"); data_fmt = f"{d[2]}/{d[1]}/{d[0]}"
            sinal = "+" if l["tipo"] == "Receita" else "-"
            cor_val = "#1a7a4a" if l["tipo"] == "Receita" else "#c0392b"
            col_info, col_val, col_btn = st.columns([5, 2, 1])
            with col_info:
                st.markdown(f"""<div style="background:#fff;border-radius:10px;padding:12px 16px;
                  border:1.5px solid #d0e8db;margin-bottom:6px;">
                  <div style="font-size:0.72rem;color:#3a6b53;">{data_fmt} · {badge_tipo(l['tipo'])} {badge_classe(l['classe'])}</div>
                  <div style="font-size:0.92rem;font-weight:600;color:#0d2b1e;margin-top:3px;">{l['icone']} {l['descricao']}</div>
                </div>""", unsafe_allow_html=True)
            with col_val:
                st.markdown(f'<div style="font-family:Syne,sans-serif;font-size:1.05rem;font-weight:700;color:{cor_val};padding:18px 0;">{sinal} {fmt_brl(l["valor"])}</div>', unsafe_allow_html=True)
            with col_btn:
                if st.button("🗑", key=f"del_{l['id']}", help="Mover para Apagados"):
                    l["apagadoEm"] = datetime.now().isoformat()
                    lixeira.insert(0, l)
                    lancamentos.remove(l)
                    persistir()
                    st.rerun()


# ══════════════════════════════════════════════════════════════════
# APAGADOS
# ══════════════════════════════════════════════════════════════════
elif current_page == "Apagados":
    st.markdown('<div style="font-family:Syne,sans-serif;font-size:1.5rem;font-weight:800;color:#0d4a2f;margin-bottom:4px;">Lançamentos <span style=\'color:#c0392b\'>Apagados</span></div>', unsafe_allow_html=True)
    st.markdown('<div style="font-size:0.8rem;color:#3a6b53;margin-bottom:16px;">Itens excluídos do histórico. Exclua definitivamente aqui.</div>', unsafe_allow_html=True)

    if not lixeira:
        st.info("Nenhum item apagado.")
    else:
        for l in lixeira:
            d = l["data"].split("-"); data_fmt = f"{d[2]}/{d[1]}/{d[0]}"
            col_info, col_val, col_btn = st.columns([5, 2, 1])
            with col_info:
                st.markdown(f"""<div style="background:#fdecea;border-radius:10px;padding:12px 16px;
                  border:1.5px solid #f5b7b1;margin-bottom:6px;opacity:0.85;">
                  <div style="font-size:0.72rem;color:#c0392b;">{data_fmt} · {badge_tipo(l['tipo'])} {badge_classe(l['classe'])}</div>
                  <div style="font-size:0.92rem;font-weight:600;color:#7b241c;margin-top:3px;">{l['icone']} {l['descricao']}</div>
                </div>""", unsafe_allow_html=True)
            with col_val:
                st.markdown(f'<div style="font-family:Syne,sans-serif;font-size:1.05rem;font-weight:700;color:#c0392b;padding:18px 0;">– {fmt_brl(l["valor"])}</div>', unsafe_allow_html=True)
            with col_btn:
                if st.button("✕", key=f"perm_{l['id']}", help="Excluir permanentemente"):
                    lixeira.remove(l)
                    persistir()
                    st.rerun()


# ══════════════════════════════════════════════════════════════════
# USUÁRIOS (ADMIN)
# ══════════════════════════════════════════════════════════════════
elif current_page == "Usuários":
    if not st.session_state.is_admin:
        st.error("Acesso restrito ao administrador.")
        st.stop()

    st.markdown('<div style="font-family:Syne,sans-serif;font-size:1.5rem;font-weight:800;color:#0d4a2f;margin-bottom:4px;">Gestão de <span style=\'color:#1a7a4a\'>Usuários</span></div>', unsafe_allow_html=True)
    st.markdown('<div style="font-size:0.8rem;color:#3a6b53;margin-bottom:20px;">Apenas administradores visualizam esta área.</div>', unsafe_allow_html=True)

    usuarios = load_users()
    for u in usuarios:
        is_admin_u = u.get("role") == "admin"
        is_me = u["usuario"].lower() == st.session_state.username.lower()
        role_label = "👑 Administrador" if is_admin_u else "👤 Usuário"
        col_u, col_btn = st.columns([5, 1])
        with col_u:
            ava_cls = "user-ava-admin" if is_admin_u else ""
            me_tag = ' <span style="font-size:10px;color:#1a7a4a">(você)</span>' if is_me else ""
            st.markdown(f"""<div class="user-row">
              <div class="user-ava {ava_cls}">{u['usuario'][0].upper()}</div>
              <div>
                <div style="font-weight:600;font-size:0.9rem;color:#0d2b1e;">{u['usuario']}{me_tag}</div>
                <div style="font-size:0.72rem;color:#3a6b53;">{role_label}</div>
              </div>
            </div>""", unsafe_allow_html=True)

    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    st.markdown('<div class="section-title">🔑 Trocar Senha</div>', unsafe_allow_html=True)

    nomes = [u["usuario"] for u in usuarios]
    sel_u = st.selectbox("Selecionar usuário:", nomes)
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
    f"<p style='text-align:center;color:#3a6b53;font-size:0.72rem;font-family:DM Sans;'>"
    f"💰 FinançasPro · Usuário: <b>{st.session_state.username}</b> · "
    f"{len(lancamentos)} lançamentos</p>",
    unsafe_allow_html=True
)