import subprocess
import tkinter as tk
import urllib.request
import webbrowser
from tkinter import *
from tkinter import filedialog, messagebox, simpledialog
from tkinter.ttk import Progressbar
import os
import requests

janela = Tk()
janela.title("SecSCAN")
#janela.attributes("-fullscrean", False)
janela.geometry("700x300")


class SecProject:
    def __init__(self, janela_principal):
        self.janela_principal = janela_principal  

        self.resultado_label = Label(self.janela_principal, text="SecSCAN", font="Arial 16", bg="#F5F5F5")
        self.resultado_label.pack(side=TOP, padx=10, pady=10)

        # Inicializar as variáveis
        self.tree = None
        self.table = None 
        self.filename = ""

        self.cria_widgets()

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
                    terminal_output.insert(tk.END, resultado.stderr, 'red')  # Exibe erros em vermelho
                
            except subprocess.CalledProcessError as e:
                terminal_output.insert(tk.END, f"Erro ao executar o comando: {e}", 'red')

        terminal_window = tk.Toplevel(self.janela_principal)
        terminal_window.title("Terminal Nmap")

        terminal_output = tk.Text(terminal_window, height=20, width=80)
        terminal_output.tag_config('red', foreground='red')
        terminal_output.pack(fill="both", expand=True)

        botao_executar = tk.Button(terminal_window, text="Executar", command=executar_comando)
        botao_executar.pack()
    
    # Função para abrir a documentação do Nmap
    def help_nmap(self):
        url= "https://nmap.org/man/pt_BR/"
        webbrowser.open(url)

    def install_nmap_windows(self):
        """Baixa e instala o Nmap no Windows com barra de progresso."""
        # Função para atualizar a barra de progresso durante o download
        def update_progress(blocknum, blocksize, totalsize):
            downloaded = blocknum * blocksize
            if totalsize > 0:
                percent = int((downloaded / totalsize) * 100)
                progress_bar['value'] = percent
                progress_label.config(text=f"Progresso: {percent}%")
                janela.update_idletasks()  # Atualiza a interface gráfica

        # Criando uma janela de progresso
        progress_window = Toplevel(self.janela_principal)
        progress_window.title("Instalando Nmap")
        progress_window.geometry("400x150")

        progress_label = Label(progress_window, text="Baixando o instalador do Nmap...", font="Arial 12")
        progress_label.pack(pady=10)

        progress_bar = Progressbar(progress_window, length=300, orient=HORIZONTAL, mode='determinate')
        progress_bar.pack(pady=20)

        # Baixa o instalador do Nmap
        nmap_installer_url = "https://nmap.org/dist/nmap-7.94-setup.exe"
        nmap_installer_path = "nmap-setup.exe"
        
        try:
            # Baixando o arquivo e atualizando o progresso
            urllib.request.urlretrieve(nmap_installer_url, nmap_installer_path, reporthook=update_progress)

            # Atualizando o progresso para "Instalando o Nmap"
            progress_label.config(text="Instalando o Nmap...")
            
            # Inicia a instalação silenciosa
            subprocess.run([nmap_installer_path, '/S'], check=True)  # Instalação silenciosa
            progress_label.config(text="Instalação concluída!")
            progress_bar['value'] = 100

        except Exception as e:
            progress_label.config(text=f"Erro: {e}")
            progress_bar['value'] = 0

        # Fecha a janela de progresso após 3 segundos
        progress_window.after(3000, progress_window.destroy)


    def download_and_install_metasploit(self):
        """Baixa e instala o Metasploit no Windows com barra de progresso."""
        def update_progress(blocknum, blocksize, totalsize):
            downloaded = blocknum * blocksize
            if totalsize > 0:
                percent = int((downloaded / totalsize) * 100)
                progress_bar['value'] = percent
                progress_label.config(text=f"Progresso: {percent}%")
                janela.update_idletasks()  # Atualiza a interface gráfica

        # Criando uma janela de progresso
        progress_window = Toplevel(self.janela_principal)
        progress_window.title("Instalando Metasploit")
        progress_window.geometry("400x150")

        progress_label = Label(progress_window, text="Baixando o instalador do Metasploit...", font="Arial 12")
        progress_label.pack(pady=10)

        progress_bar = Progressbar(progress_window, length=300, orient=HORIZONTAL, mode='determinate')
        progress_bar.pack(pady=20)

        # Baixa o instalador do Metasploit
        download_url = "https://windows.metasploit.com/metasploitframework-latest.msi"
        download_location = os.path.join(os.getenv("APPDATA"), "Metasploit")
        install_location = "C:\\Tools"
        installer_path = os.path.join(download_location, "metasploit.msi")

        # Verifica se os diretórios existem e cria se não
        if not os.path.exists(download_location):
            os.makedirs(download_location)
        if not os.path.exists(install_location):
            os.makedirs(install_location)

        try:
            # Baixando o arquivo e atualizando o progresso
            urllib.request.urlretrieve(download_url, installer_path, reporthook=update_progress)

            # Executando o instalador
            progress_label.config(text="Instalando o Metasploit...")
            subprocess.run([installer_path, '/q', f"/log={os.path.join(download_location, 'install.log')}", f"INSTALLLOCATION={install_location}"], check=True)
            progress_label.config(text="Instalação concluída!")
            progress_bar['value'] = 100

        except Exception as e:
            progress_label.config(text=f"Erro: {e}")
            progress_bar['value'] = 0

        # fecha a janela de progresso após 3 segundos
        progress_window.after(3000, progress_window.destroy)

    def cria_widgets(self):
        # Cria o menu "Arquivo"
        menu_bar = tk.Menu(self.janela_principal)

        menu_arquivos = tk.Menu(menu_bar, tearoff=0)

        menu_arquivos.add_command(label="Sair", command=janela.destroy)

        menu_bar.add_cascade(label="Menu", menu=menu_arquivos)
        
        #------------------------------------------------------------------------------------------------
        # Cria o menu "NMap"
        menu_netcat = tk.Menu(menu_bar, tearoff=0)

        menu_netcat.add_command(label="Executar Nmap", command=self.executar_comandos_nmap)
        menu_netcat.add_separator()
        menu_netcat.add_command(label="Instalar no Windows", command=self.install_nmap_windows)  # Sem parênteses
        menu_netcat.add_separator()
        menu_netcat.add_command(label="Documentação", command=self.help_nmap)

        menu_bar.add_cascade(label="NMap", menu=menu_netcat)
        
        #------------------------------------------------------------------------------------------------
        # Cria o menu "MetaSploit"
        menu_metasploit = tk.Menu(menu_bar, tearoff=0)
        
        menu_metasploit.add_command(label="Executar MetaSploit", command="")  # Defina uma função para isso mais tarde
        menu_metasploit.add_separator()
        menu_metasploit.add_command(label="Instalar no Windows", command=self.download_and_install_metasploit)  # A função que você deseja chamar
        
        menu_bar.add_cascade(label="MetaSploit",menu=menu_metasploit)
        # Define a barra de menu como a barra de menu da janela principal
        self.janela_principal.config(menu=menu_bar)

# Criação da janela principal e da instância da classe SecProject
editor = SecProject(janela)

# Executa o loop principal da interface gráfica
janela.mainloop()
