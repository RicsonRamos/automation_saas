import streamlit as st
from datetime import datetime
from pathlib import Path

from core.config_loader import EXAMPLE_TEMPLATE, OUTPUT_DIR, ensure_dirs
from core.proposal_generator import generate_proposal
from core.db import initialize_db, get_connection

# ------------------------------
# Inicialização do DB e sessão
# ------------------------------
initialize_db()
if "tela" not in st.session_state:
    st.session_state.tela = "menu"
if "cliente_id" not in st.session_state:
    st.session_state.cliente_id = None

# ------------------------------
# Configuração da página
# ------------------------------
st.set_page_config(page_title="Mini SaaS - Propostas", layout="centered")
st.title("Mini SaaS de Propostas 📄")

# ------------------------------
# Função de Menu Inicial
# ------------------------------
def menu_inicial():
    st.header("Menu Principal")
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("Criar Cliente"):
            st.session_state.tela = "criar_cliente"
    with col2:
        if st.button("Clientes"):
            st.session_state.tela = "selecionar_cliente"
    with col3:
        if st.button("Histórico de Propostas"):
            st.session_state.tela = "historico"

# ------------------------------
# Tela de Criação de Cliente
# ------------------------------
def criar_cliente():
    st.header("Criar Novo Cliente")
    nome = st.text_input("Nome do Cliente")
    tipo = st.selectbox("Tipo de Cliente", ["PF", "PJ"])
    cpf_cnpj = st.text_input("CPF/CNPJ")
    email = st.text_input("Email")
    telefone = st.text_input("Telefone")

    if st.button("Salvar Cliente"):
        if not nome.strip():
            st.warning("Digite o nome do cliente!")
        else:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO clientes (nome, tipo, cpf_cnpj, email, telefone)
                VALUES (?, ?, ?, ?, ?)
            """, (nome, tipo, cpf_cnpj, email, telefone))
            conn.commit()
            conn.close()
            st.success(f"Cliente '{nome}' criado com sucesso!")
            st.session_state.tela = "menu"

    if st.button("Voltar ao Menu"):
        st.session_state.tela = "menu"

# ------------------------------
# Tela de Seleção de Cliente
# ------------------------------
def selecionar_cliente():
    st.header("Selecionar Cliente")
    
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, nome FROM clientes")
    clientes = cursor.fetchall()
    conn.close()

    cliente_options = {c[1]: c[0] for c in clientes}
    cliente_selecionado = st.selectbox("Escolha o Cliente", [""] + list(cliente_options.keys()))

    if cliente_selecionado:
        cliente_id = cliente_options[cliente_selecionado]
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT nome, tipo, cpf_cnpj, email, telefone FROM clientes WHERE id = ?", (cliente_id,))
        cliente_info = cursor.fetchone()
        conn.close()
        
        st.subheader("Informações do Cliente")
        st.write(f"**Nome:** {cliente_info[0]}")
        st.write(f"**Tipo:** {cliente_info[1]}")
        st.write(f"**CPF/CNPJ:** {cliente_info[2]}")
        st.write(f"**Email:** {cliente_info[3]}")
        st.write(f"**Telefone:** {cliente_info[4]}")
        
        if st.button("Criar Proposta"):
            st.session_state.cliente_id = cliente_id
            st.session_state.cliente_nome = cliente_info[0]
            st.session_state.cliente_tipo = cliente_info[1]
            st.session_state.tela = "form_proposta"

    if st.button("Voltar ao Menu"):
        st.session_state.tela = "menu"

# ------------------------------
# Função para exibir os botões de download
# ------------------------------
# Exemplo na função `exibir_botoes_download()`

def exibir_botoes_download():
    # Recupera as propostas do banco de dados
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT p.id, p.file_path 
        FROM propostas p
        WHERE p.cliente_id = ?
    """, (st.session_state.cliente_id,))
    propostas = cursor.fetchall()
    conn.close()

    if propostas:
        for i, p in enumerate(propostas):
            file_path = Path(p[1])  # Caminho do arquivo
            if file_path.exists():
                with open(file_path, "rb") as f:
                    st.download_button(
                        label=f" Baixar Proposta {i + 1}",
                        data=f,
                        file_name=file_path.name,
                        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                        key=f"proposta_{p[0]}"  # Chave única baseada no ID da proposta
                    )
            else:
                st.warning(f"Arquivo da Proposta {i + 1} não encontrado.")
    else:
        st.info("Nenhuma proposta disponível para este cliente.")


# ------------------------------
# Tela de Formulário de Proposta
# ------------------------------
def form_proposta():
    cliente_id = st.session_state.cliente_id
    if not cliente_id:
        st.warning("Selecione um cliente primeiro.")
        st.session_state.tela = "selecionar_cliente"
        return

    cliente_nome = st.session_state.cliente_nome
    cliente_tipo = st.session_state.cliente_tipo

    st.header(f"Gerar Proposta para {cliente_nome}")

    # Se a proposta for duplicada, preenche os dados da proposta anterior
    servico = st.text_input("Serviço", value=st.session_state.servico)
    descricao = st.text_area("Descrição", value=st.session_state.descricao)
    prazo = st.text_input("Prazo de entrega", value=st.session_state.prazo)
    valor = st.text_input("Valor (R$)", value=st.session_state.valor)

    with st.form("proposta_form"):
        submitted = st.form_submit_button("Gerar Proposta")

    if submitted:
    if not cliente_nome.strip() or not servico.strip() or not valor.strip():
        st.warning("Todos os campos são obrigatórios!")
    else:
        with st.spinner("Gerando proposta..."):
            try:
                ensure_dirs(OUTPUT_DIR)
                data_atual = datetime.now().strftime("%d%m%Y_%H%M%S")
                versao = st.session_state.versao

                # Gerar o arquivo da proposta
                path = generate_proposal(
                    client_id=cliente_id,
                    data={
                        "CLIENTE": cliente_nome,
                        "DATA": datetime.now().strftime("%d/%m/%Y"),
                        "VERSAO": versao,
                        "SERVICO": servico,
                        "DESCRICAO": descricao,
                        "PRAZO": prazo,
                        "VALOR": valor
                    },
                    template_path=EXAMPLE_TEMPLATE,
                    output_dir=OUTPUT_DIR
                )

                # Inserir dados no banco
                conn = get_connection()
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT INTO propostas (cliente_id, servico, descricao, prazo, valor, file_path, version)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                """, (cliente_id, servico, descricao, prazo, valor, str(path), versao))

                conn.commit()
                conn.close()

                st.success(f"Proposta gerada com sucesso! 📄 \nArquivo salvo em: `{path}`", icon="✅")
            except Exception as e:
                st.error(f"Ocorreu um erro ao gerar a proposta: {e}", icon="🚨")
            # Exibe os botões de download para as propostas deste cliente
            exibir_botoes_download()

    if st.button("Voltar ao Menu"):
        st.session_state.tela = "menu"


# ------------------------------
# Tela de Histórico de Propostas
# ------------------------------
def historico_propostas():
    st.header("Histórico de Propostas")

    conn = get_connection()
    cursor = conn.cursor()

    # Busca os clientes
    cursor.execute("SELECT id, nome FROM clientes")
    clientes = cursor.fetchall()
    cliente_options = {c[1]: c[0] for c in clientes}

    cliente_selected = st.selectbox("Filtrar por Cliente", ["Todos"] + list(cliente_options.keys()))
    servico_filtro = st.text_input("Pesquisar por Serviço")
    data_filtro = st.text_input("Pesquisar por Data (dd/mm/yyyy)")

    # Query para buscar propostas
    query = """
        SELECT p.id, c.nome, p.servico, p.descricao, p.prazo, p.valor, p.version, p.file_path, p.date_created
        FROM propostas p
        JOIN clientes c ON p.cliente_id = c.id
        WHERE 1=1
    """
    params = []

    if cliente_selected != "Todos":
        query += " AND c.id = ?"
        params.append(cliente_options[cliente_selected])

    if servico_filtro.strip():
        query += " AND p.servico LIKE ?"
        params.append(f"%{servico_filtro.strip()}%")

    if data_filtro.strip():
        query += " AND DATE(p.date_created) = DATE(?)"
        params.append(data_filtro.strip())

    # Executa a query
    cursor.execute(query, params)
    propostas = cursor.fetchall()
    conn.close()

    if propostas:
        for p in propostas:
            st.markdown("---")
            st.subheader(f"{p[1]} | Serviço: {p[2] or 'Não especificado'} | Data: {p[8]} | v{p[6]}")
            descricao = p[3] if p[3] else 'Não especificada'
            prazo = p[4] if p[4] else 'Não especificado'
            valor = f"R$ {p[5]:.2f}" if p[5] else 'Não especificado'
            
            st.write(f"**Descrição:** {descricao}")
            st.write(f"**Prazo:** {prazo}")
            st.write(f"**Valor:** {valor}")

            file_path = Path(p[7])

            # Botão de duplicação da proposta
            if st.button(f"Duplicar Proposta {p[0]}", key=f"duplicar_{p[0]}"):
                # Preencher o formulário com dados da proposta selecionada
                st.session_state.cliente_id = p[1]
                st.session_state.cliente_nome = p[1]
                st.session_state.cliente_tipo = p[2]

                # Preenche os campos com os dados da proposta
                st.session_state.servico = p[2]
                st.session_state.descricao = p[3]
                st.session_state.prazo = p[4]
                st.session_state.valor = p[5]
                st.session_state.versao = f"v{int(p[6]) + 1}"  # Nova versão da proposta

                st.session_state.tela = "form_proposta"
                
            # Botão de download
            if file_path.exists():
                with open(file_path, "rb") as f:
                    st.download_button(
                        label=f"⬇️ Baixar Proposta {p[0]}",
                        data=f,
                        file_name=file_path.name,
                        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                        key=f"download_{p[0]}"  # Chave única baseada no ID da proposta
                    )

            # Botão de exclusão
            if st.button(f"Excluir Proposta {p[0]}", key=f"excluir_{p[0]}"):
                if st.confirmation_dialog("Você tem certeza de que deseja excluir esta proposta?"):
                    excluir_proposta(p[0], file_path)
    else:
        st.info("Nenhuma proposta encontrada para os filtros aplicados.")



# ------------------------------
# Função para Excluir Proposta do DB
# ------------------------------
def excluir_proposta(proposta_id, file_path):
    conn = get_connection()
    cursor = conn.cursor()

    # Exclui a proposta do banco de dados
    cursor.execute("DELETE FROM propostas WHERE id = ?", (proposta_id,))
    conn.commit()

    # Verifica se o arquivo da proposta existe e o remove
    if file_path.exists():
        file_path.unlink()  # Exclui o arquivo da proposta

    conn.close()
    st.success(f"Proposta {proposta_id} excluída com sucesso.")
    st.experimental_rerun()  # Atualiza a tela após a exclusão



# ------------------------------
# Controle de Navegação
# ------------------------------
if st.session_state.tela == "menu":
    menu_inicial()
elif st.session_state.tela == "criar_cliente":
    criar_cliente()
elif st.session_state.tela == "selecionar_cliente":
    selecionar_cliente()
elif st.session_state.tela == "form_proposta":
    form_proposta()
elif st.session_state.tela == "historico":
    historico_propostas()
