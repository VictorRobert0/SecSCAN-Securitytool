import requests
import urllib.request
import webbrowser
import threading
import tkinter as tk
from tkinter import scrolledtext, messagebox
from tkinter import ttk
import subprocess
from PIL import Image, ImageTk  # Importa as bibliotecas necessárias

class SecProject:
    def __init__(self, janela_principal):
        self.janela_principal = janela_principal
        self.processos = []  # Lista para armazenar processos em execução

        # Carrega e configura a imagem de fundo
        self.imagem_fundo_original = Image.open("/home/dzklab/interface-SecSCAN/img/secscan.jpg")
        self.imagem_fundo = ImageTk.PhotoImage(self.imagem_fundo_original)
        self.fundo_label = tk.Label(self.janela_principal, image=self.imagem_fundo)
        self.fundo_label.place(relwidth=1, relheight=1, x=0, y=0)

        # Configuração do label de título
        self.resultado_label = tk.Label(self.janela_principal, text="SecSCAN", font="Courier 16", fg="lime", bg="black")
        self.resultado_label.pack(side=tk.TOP, padx=10, pady=10)

        self.cria_widgets()

        # Redimensiona a imagem ao redimensionar a janela
        self.janela_principal.bind("<Configure>", self.redimensionar_imagem)

    def redimensionar_imagem(self, event):
        """Redimensiona a imagem de fundo de acordo com o tamanho da janela."""
        nova_imagem = self.imagem_fundo_original.resize((event.width, event.height), Image.ANTIALIAS)
        self.imagem_fundo = ImageTk.PhotoImage(nova_imagem)
        self.fundo_label.configure(image=self.imagem_fundo)

    def executar_comandos_nmap(self):
        """Executa o Nmap em uma thread separada e atualiza a interface com a saída."""
        
        def executar_comando():
            # Obtém o IP e os parâmetros do usuário
            ip_alvo = ip_entry.get().strip()
            parametros = parametros_input.get("1.0", "end-1c").strip()

            if not ip_alvo:
                terminal_output.insert(tk.END, "Por favor, insira um IP válido.\n", 'red')
                return

            comando = f"nmap {parametros} {ip_alvo}"

            # Executa o comando em uma nova thread
            def run_nmap():
                try:
                    processo = subprocess.Popen(
                        comando, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
                    )
                    self.processos.append(processo)

                    # Exibe a saída do processo no campo de output
                    for linha in processo.stdout:
                        terminal_output.insert(tk.END, linha)
                        terminal_output.yview(tk.END)

                    erro = processo.stderr.read()
                    if erro:
                        terminal_output.insert(tk.END, erro, 'red')
                        terminal_output.yview(tk.END)

                except Exception as e:
                    terminal_output.insert(tk.END, f"Erro ao executar o comando: {e}\n", 'red')

                finally:
                    # Remove o indicador de carregamento
                    loading_label.pack_forget()
                    self.processos.remove(processo)

            # Exibe indicador de carregamento
            loading_label.pack(side=tk.BOTTOM, pady=5)
            
            # Inicia a thread para execução do comando
            threading.Thread(target=run_nmap).start()

        def cancelar_comando():
            """Cancela o último comando em execução."""
            if self.processos:
                processo = self.processos[-1]
                processo.terminate()  # Interrompe o subprocesso em execução
                terminal_output.insert(tk.END, "\nComando cancelado.\n", 'red')
                self.processos.pop()  # Remove o processo da lista
                parametros_input.focus()  # Foca no campo de entrada para novos comandos

        # Configuração da interface do terminal
        terminal_window = tk.Toplevel(self.janela_principal)
        terminal_window.title("Terminal Nmap")

        # Campo de entrada para IP alvo
        ip_label = tk.Label(terminal_window, text="IP Alvo:")
        ip_label.pack(anchor="w", padx=10, pady=2)
        ip_entry = tk.Entry(terminal_window, width=30)
        ip_entry.pack(fill="x", padx=10)

        # Campo de entrada para parâmetros de comando
        parametros_label = tk.Label(terminal_window, text="Parâmetros de scan:")
        parametros_label.pack(anchor="w", padx=10, pady=2)
        parametros_input = tk.Text(terminal_window, height=2, width=80)
        parametros_input.pack(fill="x", padx=10, pady=5)

        # Área de saída do terminal
        terminal_output = scrolledtext.ScrolledText(terminal_window, height=20, width=80)
        terminal_output.tag_config('red', foreground='red')
        terminal_output.pack(fill="both", expand=True)

        # Combobox de comandos prontos e sua seleção
        comandos_comuns = [
            "scan rápido: -T4 -F",
            "scan completo: -sS -sV -O",
            "scan de portas específicas: -p 80,443",
            "scan de rede: 192.168.1.0/24",
            "scan de vulnerabilidades: --script vuln"
        ]

        def seleciona_comando(event):
            comando_selecionado = comando_combobox.get()
            parametros_input.delete("1.0", tk.END)
            parametros_input.insert(tk.END, comando_selecionado.split(": ")[1])

        comando_combobox = ttk.Combobox(terminal_window, values=comandos_comuns)
        comando_combobox.bind("<<ComboboxSelected>>", seleciona_comando)
        comando_combobox.pack(padx=10, pady=5)

        # Botões para executar e cancelar
        botao_executar = tk.Button(terminal_window, text="Executar", command=executar_comando, bg="black", fg="lime")
        botao_executar.pack(side=tk.LEFT, padx=10)

        botao_cancelar = tk.Button(terminal_window, text="Cancelar", command=cancelar_comando, bg="black", fg="red")
        botao_cancelar.pack(side=tk.RIGHT, padx=10)

        # Indicador de carregamento
        loading_label = tk.Label(terminal_window, text="Executando...", fg="orange", bg="black")

        ip_entry.focus()  # Foca no campo de entrada de IP inicialmente

    def install_nmap_windows(self):
        """Baixa e instala o Nmap no Windows com barra de progresso."""
        def update_progress(blocknum, blocksize, totalsize):
            downloaded = blocknum * blocksize
            if totalsize > 0:
                percent = int((downloaded / totalsize) * 100)
                progress_bar['value'] = percent
                progress_label.config(text=f"Progresso: {percent}%")
                janela.update_idletasks()  # Atualiza a interface gráfica

        # Criando uma janela de progresso
        progress_window = tk.Toplevel(self.janela_principal)
        progress_window.title("Instalando Nmap")
        progress_window.geometry("400x150")

        progress_label = tk.Label(progress_window, text="Baixando o instalador do Nmap...", font="Arial 12")
        progress_label.pack(pady=10)

        progress_bar = ttk.Progressbar(progress_window, length=300, orient=tk.HORIZONTAL, mode='determinate')
        progress_bar.pack(pady=20)

        # Baixa o instalador do Nmap
        nmap_installer_url = "https://nmap.org/dist/nmap-7.94-setup.exe"
        nmap_installer_path = "nmap-setup.exe"
        
        try:
            # Baixando o arquivo e atualizando o progresso
            urllib.request.urlretrieve(nmap_installer_url, nmap_installer_path, reporthook=update_progress)

            # Inicia a instalação silenciosa
            progress_label.config(text="Instalando o Nmap...")
            subprocess.run([nmap_installer_path, '/S'], check=True)  # Instalação silenciosa
            progress_label.config(text="Instalação concluída!")
            progress_bar['value'] = 100

        except Exception as e:
            progress_label.config(text=f"Erro: {e}")
            progress_bar['value'] = 0

        # Fecha a janela de progresso após 3 segundos
        progress_window.after(3000, progress_window.destroy)

    def help_nmap(self):
        """Abre a documentação do Nmap no navegador."""
        url = "https://nmap.org/man/pt_BR/"
        webbrowser.open(url)

    def executar_metasploit(self):
        """Executa o Metasploit em uma thread separada e atualiza a interface com a saída."""
        terminal_output = tk.Toplevel(self.janela_principal)
        terminal_output.title("Metasploit Terminal")
        terminal_output.geometry("600x400")
        
        terminal_text = scrolledtext.ScrolledText(terminal_output, height=20, width=80)
        terminal_text.pack(fill="both", expand=True)

        def run_msfconsole():
            try:
                processo = subprocess.Popen(
                    "msfconsole", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
                )
                self.processos.append(processo)
                
                # Leitura da saída do processo
                for linha in processo.stdout:
                    terminal_text.insert(tk.END, linha)
                    terminal_text.yview(tk.END)

                erro = processo.stderr.read()
                if erro:
                    terminal_text.insert(tk.END, erro, 'red')
                    terminal_text.yview(tk.END)

            except Exception as e:
                terminal_text.insert(tk.END, f"Erro ao executar o Metasploit: {e}\n", 'red')

        # Inicia a execução do Metasploit
        threading.Thread(target=run_msfconsole).start()

    def instalar_metasploit_windows(self):
        """Instala o Metasploit Framework no Windows"""
        url = "https://metasploit.help.rapid7.com/docs/installing-the-metasploit-framework"
        webbrowser.open(url)

    def help_metasploit(self):
        """Abre a documentação do Metasploit no navegador"""
        url = "https://www.metasploit.com/docs"
        webbrowser.open(url)

    def cria_widgets(self):
        """Configuração de widgets na janela principal."""
        
        # Criando um frame para centralizar os botões
        central_frame = tk.Frame(self.janela_principal, bg="black")
        central_frame.pack(pady=50)

        # Adicionando os botões centralizados
        botao_nmap = tk.Button(central_frame, text="Terminal Nmap", command=self.executar_comandos_nmap, bg="black", fg="lime")
        botao_nmap.pack(padx=10, pady=5)

        # Criando o menu suspenso para Nmap
        nmap_menu = tk.Menu(self.janela_principal, tearoff=0)
        nmap_menu.add_command(label="Instalar Nmap", command=self.install_nmap_windows)
        nmap_menu.add_command(label="Help Nmap", command=self.help_nmap)

        # Criando o menu suspenso para Metasploit
        metasploit_menu = tk.Menu(self.janela_principal, tearoff=0)
        metasploit_menu.add_command(label="Executar Metasploit", command=self.executar_metasploit)
        metasploit_menu.add_command(label="Instalar Metasploit", command=self.instalar_metasploit_windows)
        metasploit_menu.add_command(label="Help Metasploit", command=self.help_metasploit)

        menu_bar = tk.Menu(self.janela_principal)
        menu_bar.add_cascade(label="Nmap", menu=nmap_menu)
        menu_bar.add_cascade(label="Metasploit", menu=metasploit_menu)

        # Configuração da barra de menus
        self.janela_principal.config(menu=menu_bar)

        botao_metasploit = tk.Button(central_frame, text="Terminal Metasploit", command=self.executar_metasploit, bg="black", fg="lime")
        botao_metasploit.pack(padx=10, pady=5)

        botao_help_metasploit = tk.Button(central_frame, text="Help Metasploit", command=self.help_metasploit, bg="black", fg="orange")
        botao_help_metasploit.pack(padx=10, pady=5)


# Inicialização da interface Tkinter
janela = tk.Tk()
janela.title("SecProject")
janela.geometry("800x496")
janela.config(bg="black")

app = SecProject(janela)
janela.mainloop()
