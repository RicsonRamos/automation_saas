from docxtpl import DocxTemplate
from pathlib import Path
from datetime import date


def generate_proposal(data: dict) -> str:
    template_path = Path("templates/proposta.docx")
    
    doc = DocxTemplate(template_path)

    doc.render(data)

    today = date.today().isoformat()
    client_folder = Path("output") / data["cliente_nome"]
    client_folder.mkdir(parents=True, exist_ok=True)

    output_path = client_folder / f"proposta_v1_{today}.docx"
    doc.save(output_path)

    return str(output_path)
