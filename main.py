import asyncio
from playwright.async_api import async_playwright
from interface_login import criar_janela

async def preencher_dados_estudante(pagina, ra, digito, senha):
    # Seleciona "Estudante"
    await pagina.get_by_text('Estudante', exact=True).click()

    # Preenche o RA
    await pagina.get_by_role('textbox', name='RA').fill(ra)

    # Preenche o dígito
    await pagina.get_by_role('textbox', name='Dígito').fill(digito)

    # Preenche a senha
    await pagina.get_by_role('textbox', name='Digite sua senha').fill(senha)

    # Clica no botão "Acessar"
    await pagina.get_by_role('button', name='Acessar').click()

async def main():
    # Primeiro abre a interface e pega os dados
    dados = criar_janela()
    ra = dados["ra"]
    digito = dados["digito"]
    senha = dados["senha"]

    # Agora usa os dados no Playwright
    async with async_playwright() as pw:
        navegador = await pw.chromium.launch(headless=False)
        pagina = await navegador.new_page()
        await pagina.goto('https://saladofuturo.educacao.sp.gov.br/escolha-de-perfil')
        await preencher_dados_estudante(pagina, ra, digito, senha)
        await pagina.wait_for_timeout(10000)

if __name__ == '__main__':
    asyncio.run(main())