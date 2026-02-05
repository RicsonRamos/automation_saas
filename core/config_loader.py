import yaml
from pathlib import Path

# Caminho do arquivo de configuração
CONFIG_PATH = Path(__file__).resolve().parent.parent / "config.yaml"

# Carrega o YAML
with open(CONFIG_PATH, "r", encoding="utf-8") as f:
    cfg = yaml.safe_load(f)

# Raiz do projeto
PROJECT_ROOT = Path(cfg["project"]["root"]).resolve()

# Pastas principais
APP_DIR = PROJECT_ROOT / cfg["paths"]["app_dir"]
CORE_DIR = PROJECT_ROOT / cfg["paths"]["core_dir"]
DATA_DIR = PROJECT_ROOT / cfg["paths"]["data_dir"]
OUTPUT_DIR = PROJECT_ROOT / cfg["paths"]["output_dir"]
TEMPLATES_DIR = PROJECT_ROOT / cfg["paths"]["templates_dir"]

# Arquivos específicos
EXAMPLE_TEMPLATE = PROJECT_ROOT / cfg["files"]["example_template"]

# Função utilitária para criar pastas automaticamente
def ensure_dirs(*dirs):
    for d in dirs:
        d.mkdir(parents=True, exist_ok=True)
