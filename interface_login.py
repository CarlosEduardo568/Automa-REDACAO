import customtkinter as ctk
import pyautogui
import os

ctk.set_appearance_mode('dark')
dados_login = {}

def validar_login(usuario_entry, senha_entry, redacao_textbox,resultado_login, app):
    usuario = usuario_entry.get().strip()
    senha = senha_entry.get().strip()
    redacao = redacao_textbox.get("1.0", "end-1c").strip()  # pega todoo o texto da redação

    if "-" in usuario:
        ra, digito = usuario.split("-")

    if len(senha) >= 6 and 15 >= len(usuario) >= 10:
            ra, digito = usuario[:-1], usuario[-1]
            dados_login["ra"] = ra
            dados_login["digito"] = digito
            dados_login["senha"] = senha
            dados_login["redacao"] = redacao  # armazena a redação

            resultado_login.configure(text='Entrando na Sala do Futuro...',text_color='green')

            app.destroy()

    else:
        resultado_login.configure(text='Login ou senha inválidos',text_color='red')

def configurar_janela():
    app = ctk.CTk()
    app.title('Automa Redação')
    app.iconbitmap(os.path.join(os.path.dirname(os.path.abspath(__file__)), "icone.png"))
    # guardar altura e largura e uma variável
    largura_janela = 400
    altura_janela = 500

    #---------- centralizar interface ------------

    # Pega o tamanho da tela
    largura_tela, altura_tela = pyautogui.size()

    # Calcula a posição x e y
    x = int((largura_tela / 2) - (largura_janela / 2))
    y = int((altura_tela / 2) - (altura_janela / 2))

    # Definir geometria já centralizada
    app.geometry(f"{largura_janela}x{altura_janela}+{x}+{y}")
    return app
    #------------------------------------------------------------------

def criar_campos(app):
    # Título
    ctk.CTkLabel(app, text='Login Sala do Futuro', font=('default', 15, 'bold')).pack(pady=(10, 17))

    # RA + dígito
    entrada_usuario = ctk.CTkEntry(app, placeholder_text='RA com dígito (ex: 1234567-8)', width=280)
    entrada_usuario.pack(pady=(0, 10))

    # Senha
    entrada_senha = ctk.CTkEntry(app, placeholder_text='Digite sua senha', show="*", width=280)
    entrada_senha.pack(pady=(0, 20))

    # msotrar senha
    def mostrar_senha():
        if var_check.get():  # True se marcado
            entrada_senha.configure(show='')
        else:
            entrada_senha.configure(show='*')

    # Checkbox
    var_check = ctk.BooleanVar()
    checkbox = ctk.CTkCheckBox(master=app,
                               text="Mostrar senha",
                               variable=var_check,
                               onvalue=True,
                               offvalue=False,
                               command=mostrar_senha)
    checkbox.pack(pady=(0, 10), anchor='w', padx=30)

    # Redação
    ctk.CTkLabel(app, text='Digite sua Redação:', font=('default', 12, 'bold')).pack(pady=(0,5))
    redacao_textbox = ctk.CTkTextbox(app, width=350, height=200)
    redacao_textbox.pack(pady=(0, 10))


    # Botão login
    ctk.CTkButton(app, text='Entrar',
                  command= lambda:validar_login(entrada_usuario, entrada_senha, redacao_textbox, resultado_login, app),
                  border_width=2, border_color='#005180', width=280).pack()

    # resulado login
    resultado_login = ctk.CTkLabel(app,text='')
    resultado_login.pack(pady=10)

"----------------------------------------------------------------"
def criar_janela_login():
    app = configurar_janela()
    criar_campos(app)
    app.mainloop()
    return dados_login
