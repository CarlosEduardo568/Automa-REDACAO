import asyncio
from Instalador_bibliotecas import instalar_dependencias
from notificacoes import mostrar_notificacao

async def main():
    # mostrar notificação de aviso
    await mostrar_notificacao('Aguarde⌛','O aplicativo abrirá em breve.')

    # 1️⃣  instalar as dependências necessárias
    await instalar_dependencias()

    # 2️⃣ criar a janela de login e obter dados
    from interface_login import criar_janela_login
    dados = criar_janela_login()

    # 3️⃣ automatizar o login e preencher a redação
    from automatizacao_login_redacao import automatizar_login_redacao
    await automatizar_login_redacao(dados)
"-----------------------------------------------------------------------------"

if __name__ == '__main__':
    asyncio.run(main())