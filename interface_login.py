import customtkinter as ctk

# ----- Configuração global -----
ctk.set_appearance_mode('dark')


# ----- Função para validar login -----
def validar_login(usuario_entry, senha_entry, resultado_label):
    usuario = usuario_entry.get()
    senha = senha_entry.get()

    if usuario == 'Carlos' and senha == '1234':
        resultado_label.configure(text='Seja bem vindo Carlos bonitão😉', text_color='green')
    else:
        resultado_label.configure(text='Login ou senha inválidos!', text_color='red')


# ----- Função para criar widgets -----
def criar_widgets(app):
    # Campo usuário
    ctk.CTkLabel(app, text='Usuário(RA):').pack(pady=10)
    entrada_usuario = ctk.CTkEntry(app, placeholder_text='Digite seu RA')
    entrada_usuario.pack(pady=10)

    # Campo senha
    ctk.CTkLabel(app, text='Senha:').pack(pady=10)
    entrada_senha = ctk.CTkEntry(app, placeholder_text='Digite sua senha', show='*')
    entrada_senha.pack(pady=10)

    # resultado login
    resultado_login = ctk.CTkLabel(app, text='')
    resultado_login.pack(pady=10)

    # Botão login
    botao_login = ctk.CTkButton(
        app,
        text='Logar',
        command=lambda: validar_login(entrada_usuario, entrada_senha, resultado_login)
    )
    botao_login.pack(pady=10)


# ----- Função para criar a janela principal -----
def criar_janela():
    app = ctk.CTk()
    app.title('Login Sala do Futuro')
    app.geometry('300x300')

    criar_widgets(app)

    app.mainloop()


# ----- Executa o programa -----
if __name__ == '__main__':
    criar_janela()