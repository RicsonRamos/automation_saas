from core.db import get_connection
from docx import Document
from pathlib import Path
from datetime import datetime

def generate_proposal(client_id, data, template_path, output_dir):
    """
    Gera uma proposta baseada em template e dados do cliente.

    client_id: ID do cliente
    data: dict com placeholders a substituir
    template_path: str ou Path do arquivo .docx
    output_dir: str ou Path da pasta de saída
    """
    template_path = Path(template_path)
    output_dir = Path(output_dir)

    if not template_path.exists():
        raise FileNotFoundError(f"Template não encontrado: {template_path}")

    doc = Document(template_path)

    # Substitui placeholders no template
    if data:
        for p in doc.paragraphs:
            for key, value in data.items():
                p.text = p.text.replace(f"{{{key}}}", str(value))

    # Pasta do cliente
    today = datetime.now().strftime("%d%m%Y_%H%M%S")
    client_folder = output_dir / f"cliente_{client_id}"
    client_folder.mkdir(parents=True, exist_ok=True)

    # Calcula versão automaticamente
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT MAX(version) FROM propostas WHERE cliente_id = ?", (client_id,))
    row = cursor.fetchone()
    version = (row[0] or 0) + 1
    conn.close()

    # Caminho final do arquivo
    output_file = client_folder / f"proposta_{client_id}_{today}_v{version}.docx"

    # Salva documento
    doc.save(output_file)

    # Salva no banco de dados
    save_proposal_to_db(client_id, data, output_file, version)

    return output_file


def save_proposal_to_db(client_id, data, file_path, version):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO propostas (cliente_id, date_created, servico, descricao, prazo, valor, file_path, version)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        client_id,
        datetime.now(),
        data.get("servico"),
        data.get("descricao"),
        data.get("prazo"),
        data.get("valor"),
        str(file_path),
        version
    ))
    conn.commit()
    conn.close()
