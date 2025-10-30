import os
import sys
import asyncio
from winotify import Notification

def localizar_icone(nome_arquivo="icone.png"):  # Mudado para .png que é mais comum
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
                
        # Se não encontrar o ícone, retorna None (winotify usará ícone padrão)
        return None
    except Exception:
        return None

async def mostrar_notificacao(titulo, mensagem):
    """Exibe uma notificação usando winotify"""
    try:
        # Localiza o ícone
        icone = localizar_icone()
        
        # Cria a notificação
        notif = Notification(
            app_id="Automação Redação",
            title=titulo,
            msg=mensagem,
            duration="short",
            icon=icone if icone else None
        )
        
        # Exibe a notificação
        notif.show()
        
        # Pequena pausa para garantir que a notificação seja exibida
        await asyncio.sleep(0.2)
        
    except Exception as e:
        print(f"[DEBUG] Erro ao mostrar notificação: {e}")
        try:
            # Tenta sem ícone como fallback
            notif = Notification(
                app_id="Automação Redação",
                title=titulo,
                msg=mensagem,
                duration="short"
            )
            notif.show()
        except Exception as e:
            print(f"[DEBUG] Falha total ao mostrar notificação: {e}")