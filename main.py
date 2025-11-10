import asyncio
from Instalador_bibliotecas import instalar_dependencias
from automatizacao_login_redacao import automatizar_login_redacao

async def main():
    await instalar_dependencias()
    dados = criar_janela_login()
    await automatizar_login_redacao(dados)

if __name__ == '__main__':
    asyncio.run(main())