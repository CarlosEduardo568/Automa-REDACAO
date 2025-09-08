def interface_login():
    import customtkinter as ctk

    # configuração da aparência
    ctk.set_appearance_mode('dark')
    # criação da janela prncipal
    app = ctk.CTk()
    app.title('Login Sala do Futuro')
    app.geometry('300x300')

    # criaçã das funções de funcionalidades
    def validar_login():
        usuario =  entrada_usuario.get()
        senha = entrada_senha.get()

        # verificar usuário e senha
        if usuario == 'Carlos' and senha == '1234':
            resultado_login.configure(text='Seja bem vindo Carlos bonitão😉',text_color='green')

        else:
            resultado_login.configure(text='Login ou senha inválidos!',text_color='red')

    # criação dos campos
    # label
    label_usuario = ctk.CTkLabel(app,text='Usuário(RA):')
    label_usuario.pack(pady = 10)
    # entry
    entrada_usuario = ctk.CTkEntry(app,placeholder_text='Digite seu RA')
    entrada_usuario.pack(pady=10)
    # label
    label_senha = ctk.CTkLabel(app,text='Senha:')
    label_senha.pack(pady = 10)
    # entry
    entrada_senha = ctk.CTkEntry(app,placeholder_text='Digite sua senha')
    entrada_senha.pack(pady=10)
    #button
    botao = ctk.CTkButton(app,text='Logar',command=validar_login)
    botao.pack(pady=10)

    # campo do feedback do login
    resultado_login = ctk.CTkLabel(app,text='')
    resultado_login.pack(pady=10)

    # inicia o loop da aplicação
    app.mainloop()