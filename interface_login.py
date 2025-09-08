def interface_login():
    import customtkinter as ctk


    # configuração da aparência
    ctk.set_appearance_mode('dark')
    # criação da janela prncipal
    app = ctk.CTk()
    app.title('Login Sala do Futuro')
    app.geometry('300x300')


    # ----- criação das funções de funcionalidades -----
    def validar_login():
        # validar login
        usuario =  entrada_ra.get()
        senha = entrada_senha.get()

        # verificar usuário e senha
        if usuario == 'Carlos' and senha == '1234':
            resultado_login.configure(text='Seja bem vindo Carlos bonitão😉',text_color='green')

        else:
            resultado_login.configure(text='Login ou senha inválidos!',text_color='red')

    #----- criação dos campos -----
    #campo usuário
    ctk.CTkLabel(app,text='Usuário(RA):').pack(pady=10)
    entrada_ra = ctk.CTkEntry(app,placeholder_text='Digite seu RA')
    entrada_ra.pack(pady=10)

    #campo senha
    ctk.CTkLabel(app,text='Senha:').pack(pady=10)
    entrada_senha = ctk.CTkEntry(app,placeholder_text='Digite sua senha')
    entrada_senha.pack(pady=10)

    #botão de logar
    botao_login = ctk.CTkButton(app,text='Logar',command=validar_login)
    botao_login.pack(pady=10)

    # campo do feedback do login
    resultado_login = ctk.CTkLabel(app,text='')
    resultado_login.pack(pady=10)


    # inicia o loop da aplicação
    app.mainloop()

# chamar função
interface_login()