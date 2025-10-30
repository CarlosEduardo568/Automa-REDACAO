import sys
import subprocess

def instalar_playwright_se_preciso():
    """
    Garante que o Playwright e os navegadores estejam instalados.
    Mesmo em PCs sem Python ou Playwright pré-instalados.
    """
    try:
        import playwright
        print("✅ Playwright já instalado.")
    except ImportError:
        print("🔄 Instalando Playwright...")
        try:
            subprocess.run([sys.executable, "-m", "pip", "install", "--upgrade", "playwright"], check=True)
            print("✅ Playwright instalado!")
        except Exception as e:
            print("❌ Erro ao instalar Playwright:", e)
            return

# Chamar antes de usar o Playwright
instalar_playwright_se_preciso()
