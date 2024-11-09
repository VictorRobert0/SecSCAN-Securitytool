import subprocess
import tkinter as tk
import numpy as np
from tkinter import *
from tkinter import filedialog, messagebox, simpledialog



janela = Tk()
janela.title("SecSCAN")
janela.attributes("-fullscreen", False)


class SecProject:
    def __init__(self, janela_principal):

        self.janela_principal = janela_principal  

        self.resultado_label = Label(self.janela_principal, text=" ", font="Arial 16", bg="#F5F5F5")
        self.resultado_label.pack(side=TOP, padx=10, pady=10)


        #Inicializar as variaveis
        self.tree = None
        self.table = None 
        self.filename = ""

        self.cria_widgets()
        # Não execute a função aqui, só inicialize
        # self.executar_comandos_nmap()

    def executar_comandos_nmap(self):
        """Abre um novo terminal para executar comandos Nmap."""
        def executar_comando():
            parametros = terminal_output.get("1.0", "end-1c")
            
            if parametros :
                comando = f"sudo nmap {parametros}"
            else:
                terminal_output.insert(tk.END, "Por favor insira um comando ou IP valido. \n", 'red')
                return 
            try:
                resultado = subprocess.run(comando, shell=True, capture_output=True, text=True)
                terminal_output.insert(tk.END, resultado.stdout)
                
                
                if resultado.stderr:
                    terminal_output.insert(tk.END, resultado.stderr, 'red')  # Exibe erros em vermelh
                
            except subprocess.CalledProcessError as e:
                terminal_output.insert(tk.END, f"Erro ao executar o comando: {e}", 'red')

        terminal_window = tk.Toplevel(self.janela_principal)
        terminal_window.title("Terminal Nmap")

        terminal_output = tk.Text(terminal_window, height=20, width=80)
        terminal_output.tag_config('red', foreground='red')
        terminal_output.pack(fill="both", expand=True)

        botao_executar = tk.Button(terminal_window, text="Executar", command=executar_comando)
        botao_executar.pack()

    def cria_widgets(self):

        #Cria o menu "Arquivo"
        menu_bar = tk.Menu(self.janela_principal)

        menu_arquivos = tk.Menu(menu_bar, tearoff=0)

        menu_arquivos.add_command(label="Abrir", command=janela.destroy)
        menu_arquivos.add_separator()

        menu_arquivos.add_command(label="Salvar como", command=janela.destroy)
        menu_arquivos.add_separator()

        menu_arquivos.add_command(label="Sair", command=janela.destroy)
        menu_arquivos.add_separator()

        menu_bar.add_cascade(label="Arquivo", menu=menu_arquivos)
        
        #------------------------------------------------------------------------------------------------
        #Cria o menu "Netcat"

        menu_netcat = tk.Menu(menu_bar, tearoff=0)

        # Corrigido: passamos a referência do método
        menu_netcat.add_command(label="Visualizar", command=self.executar_comandos_nmap)

        menu_bar.add_cascade(label="NMap", menu=menu_netcat)
        
        #Define a barra de menu como a barra de menu da janela principal
        self.janela_principal.config(menu=menu_bar)


# Criação da janela principal e da instância da classe SecProject
editor = SecProject(janela)

# Executa o loop principal da interface gráfica
janela.mainloop()
