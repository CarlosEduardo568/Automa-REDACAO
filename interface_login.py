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
    dados_login["ra"] = usuario[len(usuario)-1]
    dados_login["digito"] = usuario[-1]
    dados_login["senha"] = senha

    # verifica se o login é válido
    if not usuario or senha:
        resultado_login.configure(text='entrando na Sala do Futuro...',text_color='green')

    else:
        resultado_login.configure(text='login ou senha inválidos',text_color='red')

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
        border_width=3,
        border_color='#005180',
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


# ----- Executa o programa -----
if __name__ == '__main__':
    criar_janela()
