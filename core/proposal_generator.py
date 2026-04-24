from docxtpl import DocxTemplate
from pathlib import Path
from datetime import datetime
from core.db import get_connection

def generate_proposal(client_id, data, template_path, output_dir):
    """
    Gera uma proposta profissional usando docxtpl (Jinja2).

    client_id: ID do cliente
    data: dict com placeholders a substituir (ex: {{ CLIENTE }})
    template_path: str ou Path do arquivo .docx
    output_dir: str ou Path da pasta de saída
    """
    template_path = Path(template_path)
    output_dir = Path(output_dir)

    if not template_path.exists():
        raise FileNotFoundError(f"Template não encontrado: {template_path}")

    # Carrega o template com docxtpl
    doc = DocxTemplate(template_path)
    
    # Renderiza os dados no template (Jinja2)
    doc.render(data)

    # Pasta do cliente
    client_folder = output_dir / f"cliente_{client_id}"
    client_folder.mkdir(parents=True, exist_ok=True)

    # Calcula versão para o NOME DO ARQUIVO (opcional, o DB controla a versão real)
    timestamp = datetime.now().strftime("%d%m%Y_%H%M%S")
    output_file = client_folder / f"proposta_{client_id}_{timestamp}.docx"

    # Salva documento
    doc.save(output_file)

    return output_file
