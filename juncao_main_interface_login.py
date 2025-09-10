import customtkinter as ctk

# ----- Configuração global -----
ctk.set_appearance_mode('dark')

# Variáveis globais para guardar os dados digitados
dados_login = {"ra": "", "digito": "", "senha": ""}

# ----- Função para validar login -----
def validar_login(usuario_entry, senha_entry, resultado_login):
    usuario = usuario_entry.get()
    senha = senha_entry.get()

    # Salva os valores nas variáveis globais
    dados_login["ra"] = usuario[:-1]
    dados_login["digito"] = usuario[-1]
    dados_login["senha"] = senha

    resultado_login.configure(text='entrando na Sala do Futuro...',text_color='green')

    # Chama a automação depois do login
    asyncio.run(main())

# ----- Função para criar campos -----
def criar_campos(app):
    # Label sala do futuro
    label_titulo = ctk.CTkLabel(app,text='Login Sala do Futuro',
    font=('default',15,'bold'))
    label_titulo.pack(pady=(10,17))
    # Campo usuário
    entrada_usuario = ctk.CTkEntry(app, placeholder_text='Digite seu RA com dígito (ex: 123456x)',
    width=280)
    entrada_usuario.pack(pady=(0,22))

    # Campo senha
    entrada_senha = ctk.CTkEntry(app, placeholder_text='Digite sua senha',
    width=280)
    entrada_senha.pack()

    # resultado login
    resultado_login = ctk.CTkLabel(app, text='')
    resultado_login.pack(pady=10)

    # Botão login
    botao_login = ctk.CTkButton(
        app,
        text='Logar',
        command=lambda: validar_login(entrada_usuario, entrada_senha, resultado_login),
        border_width=3,border_color='#005180',
        width=280
    )
    botao_login.pack(pady=10)

# ---- checkbox ----


# ----- Função para criar a janela principal -----
def criar_janela():
    app = ctk.CTk()
    app.title('Login Automático')
    app.geometry('300x300')

    criar_campos(app)

    app.mainloop()

import asyncio
from playwright.async_api import async_playwright

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

    # Agora usa os dados no Playwright
    async with async_playwright() as pw:
        navegador = await pw.chromium.launch(headless=False)
        pagina = await navegador.new_page()
        await pagina.goto('https://saladofuturo.educacao.sp.gov.br/escolha-de-perfil')
        await preencher_dados_estudante(pagina, ra, digito, senha)
        await pagina.wait_for_timeout(10000)


# ----- Executa o programa -----
if __name__ == '__main__':
    criar_janela()