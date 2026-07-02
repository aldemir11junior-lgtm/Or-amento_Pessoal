import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, date, timedelta
import json, hashlib, os, io

# ─── CONFIG ───────────────────────────────────────────────────────────────────
st.set_page_config(page_title="FinançasPro", layout="wide",
                   initial_sidebar_state="collapsed")

BASE_DIR       = os.path.dirname(os.path.abspath(__file__))
USERS_FILE     = os.path.join(BASE_DIR, "fp_usuarios.json")
DATA_FILE      = os.path.join(BASE_DIR, "fp_dados.json")
CATEGORIAS_FILE = os.path.join(BASE_DIR, "fp_categorias.json")

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

# ─── CATEGORIAS / DESCRIÇÕES (tabela de-para importável via Excel) ────────────
# Planilha padrão de Categoria x Descrição de Despesas, aplicada a todos os usuários
# até que cada um importe sua própria planilha personalizada na aba Descrições.
DESPESAS_PADRAO_BRUTO = [
    ("Casa", ["Aluguel", "Financiamento", "Condomínio", "IPTU", "Energia elétrica", "Água", "Gás", "Internet", "Telefone", "Manutenção", "Móveis", "Eletrodomésticos", "Material de limpeza", "Seguro residencial", "Decoração"]),
    ("Mercado", ["Alimentação", "Bebidas", "Higiene pessoal", "Produtos de limpeza", "Ração para pets", "Descartáveis"]),
    ("Carro", ["Combustível", "Seguro", "IPVA", "Licenciamento", "Manutenção", "Troca de óleo", "Pneus", "Lavagem", "Estacionamento", "Pedágio", "Multas", "Financiamento", "Acessórios"]),
    ("Moto", ["Combustível", "Seguro", "IPVA", "Licenciamento", "Manutenção", "Troca de óleo", "Pneus", "Lavagem", "Estacionamento", "Multas", "Financiamento", "Capacete e equipamentos"]),
    ("Saúde", ["Plano de saúde", "Consultas", "Exames", "Medicamentos", "Odontologia", "Óculos/Lentes", "Terapias", "Vacinas"]),
    ("Educação", ["Mensalidade", "Cursos", "Livros", "Material escolar", "Transporte", "Certificações"]),
    ("Lazer", ["Cinema", "Streaming", "Viagens", "Hotéis", "Passeios", "Bares", "Restaurantes", "Eventos", "Jogos", "Hobbies"]),
    ("Presentes", ["Aniversário", "Casamento", "Natal", "Dia das Mães", "Dia dos Pais", "Outros presentes"]),
    ("Investimentos", ["Reserva de emergência", "Tesouro", "CDB", "LCI/LCA", "Ações", "FIIs", "ETFs", "Criptomoedas", "Previdência privada"]),
    ("Pets", ["Veterinário", "Ração", "Banho e tosa", "Medicamentos", "Brinquedos", "Vacinas"]),
    ("Roupas", ["Roupas", "Calçados", "Acessórios", "Lavanderia"]),
    ("Impostos", ["IR", "Taxas", "Contabilidade"]),
    ("Trabalho", ["Ferramentas", "Equipamentos", "Software", "Cursos", "Deslocamento"]),
    ("Tecnologia", ["Celular", "Computador", "Periféricos", "Aplicativos", "Armazenamento em nuvem"]),
    ("Assinaturas", ["Música", "Vídeo", "Academia", "Jornais", "Softwares"]),
    ("Filhos", ["Escola", "Fraldas", "Roupas", "Brinquedos", "Material escolar", "Saúde"]),
    ("Doações", ["Instituições", "Igreja", "Campanhas"]),
    ("Financeiro", ["Tarifas bancárias", "Juros", "IOF", "Anuidade de cartão"]),
]

def _despesas_padrao():
    return [{"categoria": cat, "descricao": desc} for cat, descs in DESPESAS_PADRAO_BRUTO for desc in descs]

# Planilha padrão de Categoria x Descrição de Receitas, aplicada a todos os usuários
# até que cada um importe sua própria planilha personalizada na aba Descrições.
RECEITAS_PADRAO_BRUTO = [
    ("Trabalho", ["Salário", "13º Salário", "Férias", "Comissão", "Bônus", "PLR (Participação nos Lucros)", "Hora Extra", "Adicional Noturno", "Vale Alimentação/Refeição"]),
    ("Investimentos", ["Dividendos", "Juros sobre Capital Próprio", "Rendimento de Poupança", "Rendimento de CDB/Tesouro", "Aluguel Recebido", "Venda de Ações", "Venda de Imóvel", "Venda de Veículo"]),
    ("Freelance", ["Freelance", "Consultoria", "Serviços Prestados", "Comissão de Vendas"]),
    ("Extras", ["Restituição de Imposto de Renda", "Reembolso", "Prêmio/Sorteio", "Cashback", "Venda de Itens Usados"]),
    ("Outros", ["Presente Recebido", "Herança", "Empréstimo Recebido", "Pensão/Auxílio", "Renda Extra"]),
]

def _receitas_padrao():
    return [{"categoria": cat, "descricao": desc} for cat, descs in RECEITAS_PADRAO_BRUTO for desc in descs]

def load_categorias(usuario):
    if os.path.exists(CATEGORIAS_FILE):
        with open(CATEGORIAS_FILE, "r", encoding="utf-8") as f:
            try:
                all_data = json.load(f)
            except json.JSONDecodeError:
                all_data = {}
    else:
        all_data = {}
    bruto = all_data.get(usuario.lower(), {})
    if isinstance(bruto, list):  # formato antigo, anterior à separação Despesa/Receita
        despesa_lista = bruto if bruto else _despesas_padrao()
        return {"despesa": despesa_lista, "receita": _receitas_padrao()}
    despesa_lista = bruto.get("despesa", [])
    if not despesa_lista:
        despesa_lista = _despesas_padrao()  # planilha padrão até o usuário importar a sua própria
    receita_lista = bruto.get("receita", [])
    if not receita_lista:
        receita_lista = _receitas_padrao()  # planilha padrão até o usuário importar a sua própria
    return {"despesa": despesa_lista, "receita": receita_lista}

def save_categorias(usuario, mapa):
    if os.path.exists(CATEGORIAS_FILE):
        with open(CATEGORIAS_FILE, "r", encoding="utf-8") as f:
            try:
                all_data = json.load(f)
            except json.JSONDecodeError:
                all_data = {}
    else:
        all_data = {}
    all_data[usuario.lower()] = mapa
    with open(CATEGORIAS_FILE, "w", encoding="utf-8") as f:
        json.dump(all_data, f, ensure_ascii=False, indent=2)

def categorias_disponiveis(tipo_chave):
    lista = st.session_state.categorias_map.get(tipo_chave, [])
    return sorted({c["categoria"] for c in lista if c.get("categoria")})

def descricoes_disponiveis(tipo_chave, categoria):
    lista = st.session_state.categorias_map.get(tipo_chave, [])
    return sorted({c["descricao"] for c in lista
                    if c.get("categoria") == categoria and c.get("descricao")})

# ─── CLASSIFICAÇÃO AUTOMÁTICA (usada apenas na importação de extrato em lote) ──
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
    if tipo == "Receita":  return '<span class="badge badge-receita">Receita</span>'
    if tipo == "Fixo":     return '<span class="badge badge-fixo">Fixo</span>'
    if tipo == "Variável": return '<span class="badge badge-variavel">Variável</span>'
    return '<span class="badge badge-fixo">Despesa</span>'

# ─── SESSION STATE ────────────────────────────────────────────────────────────
def _ss(k, v):
    if k not in st.session_state: st.session_state[k] = v

_ss("logged_in", False); _ss("username", ""); _ss("is_admin", False)
_ss("page", "Dashboard")
_ss("lancamentos", []); _ss("lixeira", [])
_ss("categorias_map", {"despesa": [], "receita": []})
_ss("editando_lanc_id", None)
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
                        st.session_state.categorias_map = load_categorias(found["usuario"])
                        # Limpa itens apagados há mais de 30 dias ao fazer login
                        hoje_login = datetime.now()
                        st.session_state.lixeira = [
                            l for l in st.session_state.lixeira
                            if (hoje_login - datetime.fromisoformat(
                                l.get("apagadoEm", hoje_login.isoformat())
                            )).days <= 30
                        ]
                        save_data(found["usuario"], st.session_state.lancamentos, st.session_state.lixeira)
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

def persistir_categorias():
    save_categorias(st.session_state.username, st.session_state.categorias_map)

def limpar_lixeira_antiga():
    """Remove itens apagados há mais de 30 dias automaticamente."""
    if not st.session_state.lixeira:
        return
    hoje = datetime.now()
    antes = len(st.session_state.lixeira)
    st.session_state.lixeira = [
        l for l in st.session_state.lixeira
        if (hoje - datetime.fromisoformat(l.get("apagadoEm", hoje.isoformat()))).days <= 30
    ]
    depois = len(st.session_state.lixeira)
    if antes != depois:
        persistir()

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
pages = ["📊 Dashboard", "➕ Lançamentos", "📋 Histórico", "🏷️ Descrições", "⚙️ Conta"]
if st.session_state.is_admin:
    pages.append("👥 Usuários")

# Mapeia label da aba para nome de página interno
PAGE_MAP = {
    "📊 Dashboard": "Dashboard",
    "➕ Lançamentos": "Lançamentos",
    "📋 Histórico": "Histórico",
    "🏷️ Descrições": "Descrições",
    "⚙️ Conta": "Conta",
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
            text=[f"R$ {v:,.0f}".replace(",","X").replace(".",",").replace("X",".") for v in vals_pareto],
            textposition="outside",
            textfont=dict(size=10, family="DM Sans"),
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

            vals_rev = vals_top[::-1]
            fig_top = go.Figure(go.Bar(
                y=itens_top[::-1],
                x=vals_rev,
                orientation="h",
                marker_color=cores_red[::-1],
                marker_line_width=0,
                text=[f"R$ {v:,.2f}".replace(",","X").replace(".",",").replace("X",".") for v in vals_rev],
                textposition="outside",
                textfont=dict(size=10, family="DM Sans"),
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
            text=[f"R$ {v:,.0f}".replace(",","X").replace(".",",").replace("X",".") if v > 0 else "" for v in vals_sem],
            textposition="outside",
            textfont=dict(size=10, family="DM Sans"),
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

    # ── Gastos por Categoria/Veículo (segmentação extra, ex: Moto) ──
    despesas_com_cat_extra = [l for l in despesas if l.get("categoria_extra")]
    if despesas_com_cat_extra:
        st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
        st.markdown('<div class="section-title">🏷️ Gastos por Categoria/Veículo</div>', unsafe_allow_html=True)
        st.caption("Segmentação extra informada nos lançamentos (ex: Moto, Carro, Casa).")

        cat_extra_map = {}
        for l in despesas_com_cat_extra:
            cat_extra_map[l["categoria_extra"]] = cat_extra_map.get(l["categoria_extra"], 0) + l["valor"]

        sorted_cat_extra = sorted(cat_extra_map.items(), key=lambda x: -x[1])
        nomes_cat_extra = [c[0] for c in sorted_cat_extra]
        vals_cat_extra  = [c[1] for c in sorted_cat_extra]

        fig_cat_extra = go.Figure(go.Bar(
            x=nomes_cat_extra,
            y=vals_cat_extra,
            marker_color="#00704A",
            marker_line_width=0,
            text=[f"R$ {v:,.0f}".replace(",","X").replace(".",",").replace("X",".") for v in vals_cat_extra],
            textposition="outside",
            textfont=dict(size=10, family="DM Sans"),
            hovertemplate="<b>%{x}</b><br>R$ %{y:,.2f}<extra></extra>"
        ))
        fig_cat_extra.update_layout(
            paper_bgcolor="white", plot_bgcolor="#f4faf7",
            height=260, margin=dict(t=10, b=20, l=10, r=10),
            showlegend=False, font=dict(family="DM Sans"),
            yaxis=dict(tickprefix="R$ ", gridcolor="#eef5f1"),
            xaxis=dict(gridcolor="rgba(0,0,0,0)")
        )
        st.plotly_chart(fig_cat_extra, use_container_width=True)

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
                         "Categoria/Veículo": l.get("categoria_extra", "") or "—",
                         "Valor": f"{sinal} {fmt_brl(l['valor'])}"})
        st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)

# ══════════════════════════════════════════════════════════════════
# LANÇAMENTOS
# ══════════════════════════════════════════════════════════════════
with selected_tab[1]:  # Lançamentos
    st.markdown('<div style="font-family:Syne,sans-serif;font-size:1.5rem;font-weight:800;color:#00704A;margin-bottom:4px;">Novo <span style=\'color:#00704A\'>Lançamento</span></div>', unsafe_allow_html=True)
    st.markdown('<div style="font-size:0.8rem;color:#1a6645;margin-bottom:20px;">Informe data e valor, e escolha a Categoria (visão macro) e a Descrição (detalhe) cadastradas na aba 🏷️ Descrições.</div>', unsafe_allow_html=True)

    aba_lanc = st.tabs(["✏️ Lançamento Manual", "📂 Importar Excel"])

    # ── Manual ──
    # Fora de st.form de propósito: Categoria e Descrição são amarradas (a 2ª depende da 1ª),
    # e formulários do Streamlit só atualizam ao enviar — os selects precisam reagir na hora.
    with aba_lanc[0]:
        c1, c2 = st.columns(2)
        with c1:
            data_input = st.date_input("📅 Data", value=date.today(), key="ml_data")
        with c2:
            valor_input = st.number_input("💰 Valor (R$)", min_value=0.01, step=0.01, format="%.2f", key="ml_valor")

        tipo_input_lbl = st.radio("Tipo", ["💵 Receita", "💸 Despesa"], horizontal=True, key="ml_tipo")
        TIPO_LBL_MAP = {"💵 Receita": "Receita", "💸 Despesa": "Despesa"}
        tipo_final = TIPO_LBL_MAP[tipo_input_lbl]
        tipo_chave = "receita" if tipo_final == "Receita" else "despesa"

        categorias_opts = categorias_disponiveis(tipo_chave)
        categoria_input, descricao_input = None, None
        if not categorias_opts:
            st.warning(f"⚠️ Nenhuma categoria de {tipo_final} cadastrada ainda. Vá até a aba **🏷️ Descrições** e importe a planilha correspondente antes de registrar um lançamento manual.")
        else:
            cc1, cc2 = st.columns(2)
            with cc1:
                categoria_input = st.selectbox("🏷️ Categoria", categorias_opts, key=f"ml_categoria_{tipo_chave}")
            with cc2:
                desc_opts = descricoes_disponiveis(tipo_chave, categoria_input)
                if desc_opts:
                    descricao_input = st.selectbox("📝 Descrição", desc_opts, key=f"ml_descricao_{tipo_chave}")
                else:
                    st.warning("Nenhuma descrição cadastrada para essa categoria na planilha.")

        if st.button("✦ Registrar Lançamento", type="primary", use_container_width=True, key="ml_submit"):
            if not categoria_input or not descricao_input:
                st.error("Selecione uma Categoria e uma Descrição válidas.")
            else:
                icone_final = {"Receita": "💵", "Despesa": "💸"}[tipo_final]
                novo = {
                    "id": int(datetime.now().timestamp() * 1000),
                    "data": str(data_input),
                    "valor": float(valor_input),
                    "descricao": descricao_input,
                    "categoria_extra": "",
                    "tipo": tipo_final, "classe": categoria_input, "icone": icone_final,
                }
                st.session_state.lancamentos.insert(0, novo)
                persistir()
                st.success(f"✅ Registrado: {icone_final} {categoria_input} · {descricao_input} — {fmt_brl(valor_input)}")
                if "ml_valor" in st.session_state:
                    del st.session_state["ml_valor"]
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

        tipo_import_excel = st.radio(
            "O que você está importando?",
            ["💰 Receitas", "💸 Despesas"],
            horizontal=True, key="tipo_import_excel"
        )
        eh_receita_import = tipo_import_excel == "💰 Receitas"

        arquivo_excel = st.file_uploader("Selecionar arquivo Excel", type=["xlsx", "xls"], key="excel_uploader")

        if arquivo_excel:
            try:
                try:
                    import openpyxl  # noqa: F401
                except ImportError:
                    import subprocess, sys
                    subprocess.check_call([sys.executable, "-m", "pip", "install", "openpyxl", "--quiet"])
                    import openpyxl  # noqa: F401
                df_excel = pd.read_excel(arquivo_excel, engine="openpyxl")
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

                col_data_auto  = encontrar_col(df_excel, ["data","date","dt","dia"])
                col_valor_auto = encontrar_col(df_excel, ["valor","value","quantia","montante","vl","amount","total","preço","preco","price"])
                col_desc_auto  = encontrar_col(df_excel, ["descri","desc","historico","hist","memo","observ","detalhe","título","titulo","nome"])

                colunas_disp = df_excel.columns.tolist()

                st.markdown('<div style="font-size:0.78rem;color:#1a6645;margin:6px 0 4px;">📌 Colunas detectadas automaticamente. Ajuste abaixo se algo estiver errado:</div>', unsafe_allow_html=True)
                cc1, cc2, cc3 = st.columns(3)
                with cc1:
                    col_data_x = st.selectbox(
                        "📅 Coluna de Data",
                        colunas_disp,
                        index=colunas_disp.index(col_data_auto) if col_data_auto in colunas_disp else 0,
                        key="col_data_x_sel"
                    )
                with cc2:
                    col_valor_x = st.selectbox(
                        "💰 Coluna de Valor",
                        colunas_disp,
                        index=colunas_disp.index(col_valor_auto) if col_valor_auto in colunas_disp else 0,
                        key="col_valor_x_sel"
                    )
                with cc3:
                    col_desc_x = st.selectbox(
                        "📝 Coluna de Descrição",
                        colunas_disp,
                        index=colunas_disp.index(col_desc_auto) if col_desc_auto in colunas_disp else 0,
                        key="col_desc_x_sel"
                    )

                usar_cat_extra_despesa = False
                col_cat_extra_x = None
                if not eh_receita_import:
                    usar_cat_extra_despesa = st.checkbox(
                        "Usar uma coluna como Categoria/Veículo (ex: Moto) para poder segmentar os gastos depois",
                        key="usar_cat_extra_despesa_check"
                    )
                    if usar_cat_extra_despesa:
                        col_cat_extra_x = st.selectbox(
                            "🏷️ Coluna que representa a Categoria/Veículo",
                            colunas_disp,
                            index=0,
                            key="col_cat_extra_x_sel",
                            help="Essa informação fica salva separada da descrição, permitindo somar/filtrar depois (ex: total gasto com Moto)."
                        )

                linhas_ok_x  = []
                linhas_rev_x = []

                for idx, row in df_excel.iterrows():
                    d_val = row[col_data_x]  if col_data_x  else None
                    v_val = row[col_valor_x] if col_valor_x else None
                    s_val = row[col_desc_x]  if col_desc_x  else None
                    cat_extra_val = ""
                    if usar_cat_extra_despesa and col_cat_extra_x:
                        cev = row[col_cat_extra_x]
                        try:
                            cat_extra_val = str(cev).strip() if not pd.isna(cev) else ""
                        except (TypeError, ValueError):
                            cat_extra_val = str(cev).strip() if cev is not None else ""

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
                            if isinstance(v_val, (int, float)):
                                v_parsed = float(v_val)
                            else:
                                v_str = str(v_val).replace("R$", "").strip()
                                if "," in v_str:
                                    # Formato BR: ponto = milhar, vírgula = decimal
                                    v_str = v_str.replace(".", "").replace(",", ".")
                                v_parsed = float(v_str)
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
                        linhas_ok_x.append({"idx": idx, "data": d_parsed, "valor": v_parsed, "desc": s_parsed, "cat_extra": cat_extra_val})
                    else:
                        linhas_rev_x.append({"idx": idx, "d_ok": d_ok, "d_val": d_parsed or d_val,
                                             "v_ok": v_ok, "v_val": v_parsed or v_val,
                                             "s_ok": s_ok, "s_val": s_parsed or s_val, "cat_extra": cat_extra_val})

                if linhas_ok_x:
                    st.markdown(f'<div class="section-title">✅ {len(linhas_ok_x)} linha(s) prontas para importar</div>', unsafe_allow_html=True)
                    for item in linhas_ok_x[:5]:
                        if eh_receita_import:
                            tipo_p, cls_p, ico_p = "Receita", "Receita", "💵"
                        else:
                            tipo_p, cls_p, ico_p = classificar(item["desc"])
                            if tipo_p == "Receita":
                                tipo_p, cls_p, ico_p = "Variável", "Outros", "📌"
                        cat_extra_tag = f' · 🏷️ {item["cat_extra"]}' if item.get("cat_extra") else ""
                        st.markdown(f"""<div class="excel-row excel-row-ok">
                          <span style="font-size:0.72rem;color:#1a6645;">{item['data'].strftime('%d/%m/%Y')} · {badge_tipo(tipo_p)} {badge_classe(cls_p)}{cat_extra_tag}</span><br>
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
                                if eh_receita_import:
                                    t_p, c_p, i_p = "Receita", "Receita", "💵"
                                else:
                                    t_p, c_p, i_p = classificar(str(s_final))
                                    if t_p == "Receita":
                                        t_p, c_p, i_p = "Variável", "Outros", "📌"
                                st.caption(f"{i_p} Categoria detectada: **{c_p}** · {t_p}")

                            st.session_state.excel_revisao[idx] = {"data": d_final, "valor": v_final, "desc": s_final}

                if linhas_ok_x or linhas_rev_x:
                    st.markdown("<div style='height:0.5rem'></div>", unsafe_allow_html=True)
                    total_para_importar = len(linhas_ok_x) + len(linhas_rev_x)
                    st.markdown(f'<div style="font-size:0.78rem;color:#1a6645;margin-bottom:8px;">📋 <b>{total_para_importar}</b> linha(s) serão processadas ({len(linhas_ok_x)} prontas, {len(linhas_rev_x)} com revisão).</div>', unsafe_allow_html=True)

                    # Exibe resultado da importação anterior (se houver) ANTES do botão
                    if st.session_state.get("msg_importacao"):
                        msg_tipo, msg_txt = st.session_state.msg_importacao
                        if msg_tipo == "success":
                            st.success(msg_txt)
                        elif msg_tipo == "warning":
                            st.warning(msg_txt)
                        else:
                            st.error(msg_txt)
                        # Limpa após exibir para não repetir
                        del st.session_state["msg_importacao"]

                    if st.button("✦ Importar todos os lançamentos", type="primary", use_container_width=True, key="btn_importar_excel"):
                        importados = 0
                        erros = 0
                        ts_base = int(datetime.now().timestamp() * 1000)

                        for i, item in enumerate(linhas_ok_x):
                            if eh_receita_import:
                                tipo_i, cls_i, ico_i = "Receita", "Receita", "💵"
                            else:
                                tipo_i, cls_i, ico_i = classificar(item["desc"])
                                if tipo_i == "Receita":
                                    tipo_i, cls_i, ico_i = "Variável", "Outros", "📌"
                            st.session_state.lancamentos.insert(0, {
                                "id": ts_base + i,
                                "data": str(item["data"]),
                                "valor": float(item["valor"]),
                                "descricao": item["desc"],
                                "categoria_extra": item.get("cat_extra", ""),
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
                                    if eh_receita_import:
                                        tipo_j, cls_j, ico_j = "Receita", "Receita", "💵"
                                    else:
                                        tipo_j, cls_j, ico_j = classificar(str(s_f))
                                        if tipo_j == "Receita":
                                            tipo_j, cls_j, ico_j = "Variável", "Outros", "📌"
                                    d_str = str(d_f) if isinstance(d_f, date) else str(d_f)[:10]
                                    st.session_state.lancamentos.insert(0, {
                                        "id": ts_base + len(linhas_ok_x) + j,
                                        "data": d_str, "valor": float(v_f),
                                        "descricao": str(s_f).strip(),
                                        "categoria_extra": item.get("cat_extra", ""),
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

                        # Guarda mensagem no session_state — será exibida APÓS o rerun
                        if importados > 0 and erros == 0:
                            st.session_state.msg_importacao = ("success",
                                f"✅ Importação concluída! {importados} lançamento(s) adicionado(s) ao histórico.")
                        elif importados > 0 and erros > 0:
                            st.session_state.msg_importacao = ("warning",
                                f"⚠️ Importação parcial: {importados} importado(s), {erros} linha(s) ignorada(s) por dados incompletos.")
                        else:
                            st.session_state.msg_importacao = ("error",
                                f"❌ Nenhum lançamento importado. {erros} linha(s) com dados incompletos. Verifique data, valor e descrição.")

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
            filtro = st.radio("Filtrar:", ["Todos", "Receita", "Despesa", "Fixo", "Variável"],
                              horizontal=True, label_visibility="collapsed")
            lista = lancamentos if filtro == "Todos" else [l for l in lancamentos if l["tipo"] == filtro]

            categorias_extra_disp = sorted({l.get("categoria_extra", "") for l in lista if l.get("categoria_extra")})
            if categorias_extra_disp:
                filtro_cat_extra = st.selectbox(
                    "🏷️ Filtrar por Categoria/Veículo:",
                    ["Todas"] + categorias_extra_disp,
                    key="filtro_cat_extra_lanc"
                )
                if filtro_cat_extra != "Todas":
                    lista = [l for l in lista if l.get("categoria_extra", "") == filtro_cat_extra]

            for l in lista:
                d = l["data"].split("-"); data_fmt = f"{d[2]}/{d[1]}/{d[0]}"
                sinal = "+" if l["tipo"] == "Receita" else "-"
                cor_val = "#00704A" if l["tipo"] == "Receita" else "#c0392b"
                cat_extra_tag = f' · 🏷️ {l["categoria_extra"]}' if l.get("categoria_extra") else ""
                col_info, col_val, col_edit, col_btn = st.columns([5, 2, 0.8, 0.8])
                with col_info:
                    st.markdown(f"""<div style="background:#fff;border-radius:10px;padding:12px 16px;
                      border:1.5px solid #b8e8d4;margin-bottom:6px;">
                      <div style="font-size:0.72rem;color:#1a6645;">{data_fmt} · {badge_tipo(l['tipo'])} {badge_classe(l['classe'])}{cat_extra_tag}</div>
                      <div style="font-size:0.92rem;font-weight:600;color:#0d2b1e;margin-top:3px;">{l['icone']} {l['descricao']}</div>
                    </div>""", unsafe_allow_html=True)
                with col_val:
                    st.markdown(f'<div style="font-family:Syne,sans-serif;font-size:1.05rem;font-weight:700;color:{cor_val};padding:18px 0;">{sinal} {fmt_brl(l["valor"])}</div>', unsafe_allow_html=True)
                with col_edit:
                    if st.button("✏️", key=f"edit_{l['id']}", help="Editar lançamento"):
                        st.session_state.editando_lanc_id = l['id']
                        st.rerun()
                with col_btn:
                    if st.button("🗑", key=f"del_{l['id']}", help="Mover para Apagados"):
                        l["apagadoEm"] = datetime.now().isoformat()
                        st.session_state.lixeira.insert(0, l)
                        st.session_state.lancamentos.remove(l)
                        persistir()
                        st.rerun()

                if st.session_state.get("editando_lanc_id") == l["id"]:
                    ICONE_TIPO_EDIT = {"Receita": "💵", "Despesa": "💸"}
                    tipos_edit_opts = ["Receita", "Despesa"]

                    st.markdown(f'<div class="section-title">✏️ Editando lançamento</div>', unsafe_allow_html=True)
                    try:
                        data_val_edit = datetime.strptime(l["data"], "%Y-%m-%d").date()
                    except Exception:
                        data_val_edit = date.today()
                    ec1, ec2 = st.columns(2)
                    with ec1:
                        data_edit = st.date_input("📅 Data", value=data_val_edit, key=f"edit_d_{l['id']}")
                        valor_edit = st.number_input("💰 Valor", min_value=0.01, value=max(float(l["valor"]), 0.01), step=0.01, format="%.2f", key=f"edit_v_{l['id']}")
                    with ec2:
                        # Lançamentos antigos podem ter tipo "Fixo"/"Variável"; tratamos como Despesa por padrão.
                        idx_tipo_edit = 0 if l["tipo"] == "Receita" else 1
                        tipo_edit = st.selectbox("Tipo", tipos_edit_opts, index=idx_tipo_edit, key=f"edit_t_{l['id']}")
                        tipo_chave_edit = "receita" if tipo_edit == "Receita" else "despesa"

                        # Categoria/Descrição amarradas: precisam ficar fora de st.form para reagir na hora.
                        categorias_opts_edit = categorias_disponiveis(tipo_chave_edit)
                        if l["classe"] not in categorias_opts_edit:
                            categorias_opts_edit = sorted(set(categorias_opts_edit) | {l["classe"]})
                        classe_edit = st.selectbox("🏷️ Categoria", categorias_opts_edit,
                                                    index=categorias_opts_edit.index(l["classe"]),
                                                    key=f"edit_c_{l['id']}_{tipo_chave_edit}")

                    desc_opts_edit = descricoes_disponiveis(tipo_chave_edit, classe_edit)
                    if l["descricao"] not in desc_opts_edit:
                        desc_opts_edit = sorted(set(desc_opts_edit) | {l["descricao"]})
                    desc_edit = st.selectbox("📝 Descrição", desc_opts_edit,
                                              index=desc_opts_edit.index(l["descricao"]),
                                              key=f"edit_s_{l['id']}_{tipo_chave_edit}_{classe_edit}")
                    cat_extra_edit = st.text_input("🏷️ Categoria/Veículo (opcional)", value=l.get("categoria_extra", ""),
                                                    placeholder="Ex: Moto, Carro, Casa...", key=f"edit_cat_{l['id']}")

                    col_save_e, col_cancel_e = st.columns(2)
                    with col_save_e:
                        salvar_edit = st.button("💾 Salvar alterações", type="primary", use_container_width=True, key=f"edit_save_{l['id']}")
                    with col_cancel_e:
                        cancelar_edit = st.button("✕ Cancelar", use_container_width=True, key=f"edit_cancel_{l['id']}")

                    if salvar_edit:
                        l["data"] = str(data_edit)
                        l["valor"] = float(valor_edit)
                        l["descricao"] = desc_edit
                        l["tipo"] = tipo_edit
                        l["classe"] = classe_edit
                        l["categoria_extra"] = cat_extra_edit.strip()
                        l["icone"] = ICONE_TIPO_EDIT.get(tipo_edit, "💸")
                        persistir()
                        st.session_state.editando_lanc_id = None
                        st.success("✅ Lançamento atualizado com sucesso!")
                        st.rerun()
                    if cancelar_edit:
                        st.session_state.editando_lanc_id = None
                        st.rerun()

    # ── Aba: Apagados ──
    with aba_hist[1]:
        st.markdown('<div style="font-size:0.8rem;color:#1a6645;margin-bottom:8px;">Itens excluídos do histórico. Restaure ou exclua definitivamente.</div>', unsafe_allow_html=True)
        st.markdown('<div style="font-size:0.75rem;color:#c05e00;background:#fef9e7;border:1px solid #f9e79f;border-radius:8px;padding:8px 12px;margin-bottom:12px;">⏳ Itens ficam disponíveis por <b>30 dias</b> após a exclusão. Após esse prazo são removidos automaticamente.</div>', unsafe_allow_html=True)

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
                    # Calcular dias restantes
                    try:
                        apagado_em = datetime.fromisoformat(l.get("apagadoEm", datetime.now().isoformat()))
                        dias_restantes = 30 - (datetime.now() - apagado_em).days
                        dias_restantes = max(0, dias_restantes)
                    except Exception:
                        dias_restantes = 30
                    cor_dias = "#c0392b" if dias_restantes <= 3 else ("#d97706" if dias_restantes <= 7 else "#1a6645")
                    st.markdown(f'<div style="font-size:0.68rem;color:{cor_dias};font-weight:600;padding:4px 0;text-align:center;">🗓 {dias_restantes}d restantes</div>', unsafe_allow_html=True)
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
# DESCRIÇÕES (tabela de-para Categoria x Descrição, importável via Excel)
# ══════════════════════════════════════════════════════════════════
with selected_tab[3]:  # Descrições
    st.markdown('<div style="font-family:Syne,sans-serif;font-size:1.5rem;font-weight:800;color:#00704A;margin-bottom:4px;">Categorias <span style=\'color:#00704A\'>& Descrições</span></div>', unsafe_allow_html=True)
    st.markdown('<div style="font-size:0.8rem;color:#1a6645;margin-bottom:20px;">Categoria é a visão macro usada nos relatórios (ex: Alimentação). Descrição é o detalhe (ex: Mercado, Restaurante). Há uma planilha separada para Despesas e outra para Receitas. Baixe, ajuste no Excel e importe de volta — lançamentos já registrados mantêm a categoria/descrição do momento em que foram feitos.</div>', unsafe_allow_html=True)

    def _bloco_categorias(tipo_chave, titulo, cor_icone):
        lista_atual = st.session_state.categorias_map.get(tipo_chave, [])
        df_map = pd.DataFrame(lista_atual) if lista_atual else pd.DataFrame(columns=["categoria", "descricao"])

        col_dl, col_up = st.columns(2)
        with col_dl:
            st.markdown(f'<div class="section-title">⬇️ Baixar planilha de {titulo}</div>', unsafe_allow_html=True)
            st.caption("Baixe, ajuste as categorias/descrições no Excel e importe novamente.")
            df_export = df_map.rename(columns={"categoria": "Categoria", "descricao": "Descrição"})
            if df_export.empty:
                df_export = pd.DataFrame(columns=["Categoria", "Descrição"])
            buffer_cat = io.BytesIO()
            with pd.ExcelWriter(buffer_cat, engine="openpyxl") as writer:
                df_export.to_excel(writer, index=False, sheet_name=titulo)
            st.download_button(
                f"📥 Baixar {titulo}.xlsx",
                data=buffer_cat.getvalue(),
                file_name=f"Descricoes_{titulo}.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                use_container_width=True,
                key=f"dl_{tipo_chave}",
            )

        with col_up:
            st.markdown(f'<div class="section-title">⬆️ Importar planilha de {titulo}</div>', unsafe_allow_html=True)
            st.caption("Envie um .xlsx com as colunas Categoria e Descrição.")
            arq_cat = st.file_uploader("Selecionar arquivo", type=["xlsx", "xls"], key=f"upload_categorias_{tipo_chave}")

            if arq_cat:
                try:
                    try:
                        import openpyxl  # noqa: F401
                    except ImportError:
                        import subprocess, sys
                        subprocess.check_call([sys.executable, "-m", "pip", "install", "openpyxl", "--quiet"])
                        import openpyxl  # noqa: F401
                    df_up = pd.read_excel(arq_cat, engine="openpyxl")
                except Exception as e:
                    st.error(f"❌ Erro ao ler o arquivo: {e}")
                    df_up = None

                if df_up is not None and not df_up.empty:
                    cols_lower = {str(c).lower().strip(): c for c in df_up.columns}
                    col_cat  = next((cols_lower[c] for c in cols_lower if "categ" in c), None)
                    col_desc = next((cols_lower[c] for c in cols_lower if "descri" in c), None)

                    if not col_cat or not col_desc:
                        st.error("A planilha precisa ter uma coluna de Categoria e uma de Descrição.")
                    else:
                        nova_lista, vistos = [], set()
                        for _, row in df_up.iterrows():
                            cat_v  = str(row[col_cat]).strip()  if pd.notna(row[col_cat])  else ""
                            desc_v = str(row[col_desc]).strip() if pd.notna(row[col_desc]) else ""
                            if cat_v and desc_v:
                                chave = (cat_v.lower(), desc_v.lower())
                                if chave not in vistos:
                                    vistos.add(chave)
                                    nova_lista.append({"categoria": cat_v, "descricao": desc_v})

                        st.info(f"📄 {len(nova_lista)} combinações de Categoria/Descrição prontas para importar.")
                        st.dataframe(
                            pd.DataFrame(nova_lista).rename(columns={"categoria": "Categoria", "descricao": "Descrição"}),
                            use_container_width=True, hide_index=True,
                        )
                        if st.button("✅ Confirmar importação", type="primary", use_container_width=True, key=f"confirmar_import_{tipo_chave}"):
                            st.session_state.categorias_map[tipo_chave] = nova_lista
                            persistir_categorias()
                            st.success(f"✅ {len(nova_lista)} combinações de {titulo} importadas com sucesso!")
                            st.rerun()

        st.markdown(f'<div class="section-title">📋 Categorias e Descrições de {titulo} cadastradas</div>', unsafe_allow_html=True)
        if df_map.empty:
            st.info(f"Nenhuma categoria de {titulo} cadastrada ainda. Importe uma planilha acima para começar.")
        else:
            st.dataframe(
                df_map.rename(columns={"categoria": "Categoria", "descricao": "Descrição"})
                      .sort_values(["Categoria", "Descrição"]),
                use_container_width=True, hide_index=True,
            )

    aba_desc = st.tabs(["💸 Despesas", "💵 Receitas"])
    with aba_desc[0]:
        _bloco_categorias("despesa", "Despesas", "#c0392b")
    with aba_desc[1]:
        _bloco_categorias("receita", "Receitas", "#00704A")

# ══════════════════════════════════════════════════════════════════
# CONTA
# ══════════════════════════════════════════════════════════════════
with selected_tab[4] if len(selected_tab) > 4 else selected_tab[0]:  # Conta
    st.markdown('<div style="font-family:Syne,sans-serif;font-size:1.5rem;font-weight:800;color:#00704A;margin-bottom:4px;">Minha <span style=\'color:#00704A\'>Conta</span></div>', unsafe_allow_html=True)
    st.markdown('<div style="font-size:0.8rem;color:#1a6645;margin-bottom:20px;">Altere sua senha de acesso quando quiser.</div>', unsafe_allow_html=True)

    st.markdown('<div class="section-title">🔑 Alterar Senha</div>', unsafe_allow_html=True)
    with st.form("form_trocar_senha"):
        senha_atual = st.text_input("🔒 Senha atual", type="password", key="conta_atual")
        senha_nova1 = st.text_input("🔒 Nova senha", type="password", key="conta_nova1")
        senha_nova2 = st.text_input("🔒 Confirmar nova senha", type="password", key="conta_nova2")
        if st.form_submit_button("💾 Salvar nova senha", type="primary", use_container_width=True):
            if not senha_atual or not senha_nova1 or not senha_nova2:
                st.warning("Preencha todos os campos.")
            elif len(senha_nova1) < 3:
                st.warning("A nova senha deve ter pelo menos 3 caracteres.")
            elif senha_nova1 != senha_nova2:
                st.error("As novas senhas não conferem.")
            else:
                usuarios_conta = load_users()
                u_conta = next((u for u in usuarios_conta if u["usuario"].lower() == st.session_state.username.lower()), None)
                if not u_conta or u_conta["senha"] != hash_pw(senha_atual):
                    st.error("Senha atual incorreta.")
                else:
                    u_conta["senha"] = hash_pw(senha_nova1)
                    save_users(usuarios_conta)
                    st.success("✅ Senha alterada com sucesso!")

with selected_tab[5] if len(selected_tab) > 5 else selected_tab[0]:  # Usuários (admin)
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