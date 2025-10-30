import os
import sys
import asyncio
from plyer import notification

def localizar_icone(nome_arquivo="icone.ico"):  # Mudado para .ico
    """Localiza o arquivo de ícone em vários diretórios possíveis"""
    try:
        # Lista de possíveis localizações do ícone
        candidatos = [
            os.path.join(sys._MEIPASS, nome_arquivo) if getattr(sys, "frozen", False) else None,
            os.path.join(os.path.dirname(os.path.abspath(__file__)), nome_arquivo),
            os.path.join(os.getcwd(), nome_arquivo)
        ]
        
        # Retorna o primeiro ícone válido encontrado
        for caminho in candidatos:
            if caminho and os.path.isfile(caminho):
                return caminho
                
        # Se não encontrar o .ico, tenta o fallback do Windows
        windows_ico = os.path.join(os.environ.get('SystemRoot', 'C:\\Windows'), 
                                 'System32\\imageres.dll,1')
        return windows_ico
    except Exception:
        return None

async def mostrar_notificacao(titulo, mensagem):
    """Exibe uma notificação usando plyer"""
    try:
        #mostra onde está procurando o ícone
        icone = localizar_icone()
        
        notification.notify(
            title=titulo,
            message=mensagem,
            app_name="Automação Redação",
            app_icon=icone,
            timeout=5,
            toast=True
        )
        
        await asyncio.sleep(0.2)
        
    except Exception as e:
        print(f"[DEBUG] Erro ao mostrar notificação com ícone: {e}")
        try:
            # Tenta sem ícone como fallback
            notification.notify(
                title=titulo,
                message=mensagem,
                app_name="Automação Redação",
                timeout=5,
                toast=True
            )
            await asyncio.sleep(0.2)
            
        except Exception as e2:
            print(f"[NOTIFICAÇÃO] {titulo}: {mensagem}")