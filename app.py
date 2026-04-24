import streamlit as st
import pandas as pd
from datetime import datetime
from pathlib import Path

from core.config_loader import EXAMPLE_TEMPLATE, OUTPUT_DIR, ensure_dirs
from core.proposal_generator import generate_proposal
from core.db import initialize_db, get_connection

# ------------------------------
# Inicialização
# ------------------------------
initialize_db()
ensure_dirs(OUTPUT_DIR)

if "tela" not in st.session_state:
    st.session_state.tela = "Dashboard"
if "cliente_id" not in st.session_state:
    st.session_state.cliente_id = None

# ------------------------------
# Configuração da página
# ------------------------------
st.set_page_config(page_title="Gestão SaaS - Automação", layout="wide", page_icon="🚀")

# CSS customizado para melhorar a estética
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .stMetric { background-color: #ffffff; padding: 20px; border-radius: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.05); }
    .stButton>button { width: 100%; border-radius: 5px; }
    </style>
""", unsafe_allow_html=True)

# ------------------------------
# Sidebar - Navegação
# ------------------------------
with st.sidebar:
    st.title("🚀 Menu Principal")
    st.markdown("---")
    if st.button("📊 Dashboard"): st.session_state.tela = "Dashboard"
    if st.button("👥 Clientes"): st.session_state.tela = "Clientes"
    if st.button("📑 Propostas & Contratos"): st.session_state.tela = "Projetos"
    if st.button("💰 Financeiro"): st.session_state.tela = "Financeiro"
    st.markdown("---")
    st.caption("Versão 1.0 - Sprint Zero Expanded")

# ------------------------------
# Funções Auxiliares de DB
# ------------------------------
def get_metrics():
    conn = get_connection()
    try:
        # Receita Gerada (Soma de tudo que foi pago no financeiro)
        gerada = pd.read_sql("SELECT SUM(valor) as total FROM financeiro WHERE status = 'Pago'", conn)["total"].iloc[0] or 0
        # Receita Esperada (Soma de tudo que está pendente no financeiro)
        esperada = pd.read_sql("SELECT SUM(valor) as total FROM financeiro WHERE status = 'Pendente'", conn)["total"].iloc[0] or 0
        # Projetos Ativos (Status = 'Contrato')
        ativos = pd.read_sql("SELECT COUNT(*) as total FROM propostas WHERE status = 'Contrato'", conn)["total"].iloc[0] or 0
    except:
        gerada, esperada, ativos = 0, 0, 0
    conn.close()
    return gerada, esperada, ativos

# ------------------------------
# TELA: Dashboard
# ------------------------------
def tela_dashboard():
    st.title("📊 Dashboard de Performance")
    gerada, esperada, ativos = get_metrics()

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Receita Gerada", f"R$ {gerada:,.2f}")
    col2.metric("Receita Esperada", f"R$ {esperada:,.2f}")
    col3.metric("Contratos Ativos", ativos)
    col4.metric("Total em Negociação", f"R$ {gerada + esperada:,.2f}")

    st.markdown("---")
    
    col_left, col_right = st.columns(2)
    
    with col_left:
        st.subheader("📈 Volume de Vendas")
        conn = get_connection()
        try:
            df_vendas = pd.read_sql("SELECT date_created, valor FROM propostas", conn)
            if not df_vendas.empty:
                df_vendas['date_created'] = pd.to_datetime(df_vendas['date_created'])
                df_grouped = df_vendas.set_index('date_created').resample('D').sum().reset_index()
                st.area_chart(df_grouped.set_index('date_created'))
            else:
                st.info("Sem dados de vendas para exibir no gráfico.")
        except:
            st.error("Erro ao carregar dados do gráfico.")
        conn.close()

    with col_right:
        st.subheader("🔔 Próximos Vencimentos")
        conn = get_connection()
        try:
            df_venc = pd.read_sql("""
                SELECT p.servico, f.valor, f.data_vencimento 
                FROM financeiro f 
                JOIN propostas p ON f.proposta_id = p.id 
                WHERE f.status = 'Pendente' 
                ORDER BY f.data_vencimento ASC LIMIT 5
            """, conn)
            if not df_venc.empty:
                st.table(df_venc)
            else:
                st.success("Nenhum pagamento pendente para os próximos dias!")
        except:
            st.info("Aguardando dados financeiros.")
        conn.close()

# ------------------------------
# TELA: Clientes
# ------------------------------
def tela_clientes():
    st.title("👥 Gestão de Clientes")
    
    tabs = st.tabs(["Listar Clientes", "Cadastrar Novo"])
    
    with tabs[1]:
        with st.form("novo_cliente"):
            nome = st.text_input("Nome/Razão Social")
            tipo = st.selectbox("Tipo", ["PJ", "PF"])
            doc = st.text_input("CPF/CNPJ")
            email = st.text_input("E-mail")
            tel = st.text_input("Telefone")
            if st.form_submit_button("Salvar"):
                if nome:
                    conn = get_connection()
                    cursor = conn.cursor()
                    cursor.execute("INSERT INTO clientes (nome, tipo, cpf_cnpj, email, telefone) VALUES (?,?,?,?,?)", 
                                 (nome, tipo, doc, email, tel))
                    conn.commit()
                    conn.close()
                    st.success("Cliente cadastrado!")
                else:
                    st.error("Nome é obrigatório.")

    with tabs[0]:
        conn = get_connection()
        df_clientes = pd.read_sql("SELECT * FROM clientes", conn)
        conn.close()
        st.dataframe(df_clientes, use_container_width=True)

# ------------------------------
# TELA: Projetos / Propostas
# ------------------------------
def tela_projetos():
    st.title("📑 Propostas e Contratos")
    
    conn = get_connection()
    clientes = pd.read_sql("SELECT id, nome FROM clientes", conn)
    conn.close()
    
    with st.expander("➕ Gerar Nova Proposta"):
        if clientes.empty:
            st.warning("Cadastre um cliente primeiro.")
        else:
            cliente_map = dict(zip(clientes['nome'], clientes['id']))
            c_nome = st.selectbox("Selecione o Cliente", clientes['nome'])
            servico = st.text_input("Serviço")
            desc = st.text_area("Descrição do Escopo")
            valor = st.number_input("Valor Total (R$)", min_value=0.0)
            prazo = st.text_input("Prazo (ex: 15 dias)")
            vencimento = st.date_input("Data de Vencimento da Proposta")
            
            if st.button("Gerar e Salvar"):
                data_doc = {
                    "CLIENTE": c_nome,
                    "DATA": datetime.now().strftime("%d/%m/%Y"),
                    "SERVICO": servico,
                    "DESCRICAO": desc,
                    "VALOR": f"R$ {valor:,.2f}",
                    "PRAZO": prazo
                }
                c_id = cliente_map[c_nome]
                try:
                    path = generate_proposal(c_id, data_doc, EXAMPLE_TEMPLATE, OUTPUT_DIR)
                    
                    conn = get_connection()
                    cursor = conn.cursor()
                    cursor.execute("""
                        INSERT INTO propostas (cliente_id, servico, descricao, prazo, valor, file_path, status, data_vencimento)
                        VALUES (?, ?, ?, ?, ?, ?, 'Orçamento', ?)
                    """, (c_id, servico, desc, prazo, valor, str(path), vencimento))
                    conn.commit()
                    conn.close()
                    st.success(f"Proposta salva! Arquivo: {path}")
                except Exception as e:
                    st.error(f"Erro ao gerar proposta: {e}")

    st.markdown("### 📋 Lista de Documentos")
    conn = get_connection()
    query = """
        SELECT p.id, c.nome as Cliente, p.servico, p.valor, p.status, p.data_vencimento, p.nf_emitida, p.file_path
        FROM propostas p JOIN clientes c ON p.cliente_id = c.id
    """
    df_p = pd.read_sql(query, conn)
    conn.close()

    for i, row in df_p.iterrows():
        with st.expander(f"{row['Cliente']} - {row['servico']} ({row['status']})"):
            col1, col2, col3 = st.columns([2, 1, 1])
            col1.write(f"**Valor:** R$ {row['valor']:,.2f} | **Vencimento:** {row['data_vencimento']}")
            col2.write(f"**NF:** {'✅ Emitida' if row['nf_emitida'] else '❌ Pendente'}")
            
            c1, c2, c3, c4 = st.columns(4)
            with c1:
                if row['status'] == 'Orçamento':
                    if st.button("Aprovar (Contrato)", key=f"apr_{row['id']}"):
                        conn = get_connection()
                        cursor = conn.cursor()
                        cursor.execute("UPDATE propostas SET status = 'Contrato' WHERE id = ?", (row['id'],))
                        cursor.execute("INSERT INTO financeiro (proposta_id, valor, data_vencimento, status) VALUES (?,?,?, 'Pendente')",
                                     (row['id'], row['valor'], row['data_vencimento']))
                        conn.commit()
                        conn.close()
                        st.rerun()
            with c2:
                if row['status'] == 'Contrato':
                    if st.button("Concluir", key=f"concl_{row['id']}"):
                        conn = get_connection()
                        cursor = conn.cursor()
                        cursor.execute("UPDATE propostas SET status = 'Concluído' WHERE id = ?", (row['id'],))
                        conn.commit()
                        conn.close()
                        st.rerun()
            with c3:
                if not row['nf_emitida']:
                    if st.button("Marcar NF Emitida", key=f"nf_{row['id']}"):
                        conn = get_connection()
                        cursor = conn.cursor()
                        cursor.execute("UPDATE propostas SET nf_emitida = 1 WHERE id = ?", (row['id'],))
                        conn.commit()
                        conn.close()
                        st.rerun()
            with c4:
                file_path = Path(row['file_path'])
                if file_path.exists():
                    with open(file_path, "rb") as f:
                        st.download_button("Download DOCX", f, file_name=file_path.name, key=f"dl_{row['id']}")

# ------------------------------
# TELA: Financeiro
# ------------------------------
def tela_financeiro():
    st.title("💰 Controle Financeiro")
    
    conn = get_connection()
    try:
        query = """
            SELECT f.id, c.nome as Cliente, p.servico, f.valor, f.data_vencimento, f.status, f.data_pagamento
            FROM financeiro f
            JOIN propostas p ON f.proposta_id = p.id
            JOIN clientes c ON p.cliente_id = c.id
        """
        df_f = pd.read_sql(query, conn)
    except:
        df_f = pd.DataFrame()
    conn.close()

    if df_f.empty:
        st.info("Nenhum registro financeiro encontrado. Aprove uma proposta para gerar faturamento.")
    else:
        st.dataframe(df_f, use_container_width=True)
        
        st.markdown("### 🛠️ Ações Financeiras")
        for i, row in df_f.iterrows():
            if row['status'] == 'Pendente':
                if st.button(f"Confirmar Pagamento: {row['Cliente']} - R$ {row['valor']}", key=f"pag_{row['id']}"):
                    conn = get_connection()
                    cursor = conn.cursor()
                    cursor.execute("UPDATE financeiro SET status = 'Pago', data_pagamento = ? WHERE id = ?", 
                                 (datetime.now().strftime("%Y-%m-%d"), row['id']))
                    conn.commit()
                    conn.close()
                    st.success("Pagamento confirmado!")
                    st.rerun()

# ------------------------------
# Roteamento
# ------------------------------
if st.session_state.tela == "Dashboard": tela_dashboard()
elif st.session_state.tela == "Clientes": tela_clientes()
elif st.session_state.tela == "Projetos": tela_projetos()
elif st.session_state.tela == "Financeiro": tela_financeiro()
