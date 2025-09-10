import asyncio
from playwright.async_api import async_playwright
from interface_login import criar_janela

async def preencher_dados_estudante(pagina, ra, digito, senha):
    # Seleciona "Estudante"
    clicar_sou_estudante = pagina.get_by_text('Estudante', exact=True)
    await clicar_sou_estudante.click()

    # Preenche o RA
    ra_input = pagina.get_by_role('textbox', name='RA')
    await ra_input.fill(ra)

    # Preenche o dígito
    digito_input = pagina.get_by_role('textbox', name='Dígito')
    await digito_input.fill(digito)

    # Preenche a senha
    senha_input = pagina.get_by_role('textbox', name='Digite sua senha')
    await senha_input.fill(senha)

    # TODO: clicar no botão "Acessar"
    acessar_btn = pagina.get_by_role('button', name='Acessar')
    await acessar_btn.click()

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