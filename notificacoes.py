import os
import sys
from winotify import Notification

def mostrar_notificacao(titulo,mensagem):
    def resource_path(rel_path):
        # quando empacotado com PyInstaller, os arquivos são extraídos em sys._MEIPASS
        if getattr(sys, "frozen", False):
            base_path = sys._MEIPASS
        else:
            base_path = os.path.abspath(os.path.dirname(__file__))  # pasta do script
        return os.path.join(base_path, rel_path)

    # nome do arquivo de ícone (recomendo .ico)
    icone_file = resource_path("icone.png")

    # debug rápido: confirma que o arquivo existe
    if not os.path.exists(icone_file):
        raise FileNotFoundError(f"Ícone não encontrado: {icone_file}")

    notificacao = Notification(
        app_id="MinhaApp",
        title=titulo,
        msg=mensagem,
        icon=icone_file
    )