import requests
import urllib.request
import webbrowser
import threading
import tkinter as tk
from tkinter import scrolledtext, messagebox
from tkinter import ttk
import subprocess

class SecProject:
    def __init__(self, janela_principal):
        self.janela_principal = janela_principal
        self.processos = []  # Lista para armazenar processos em execução
        self.resultado_label = tk.Label(self.janela_principal, text="SecSCAN", font="Courier 16", fg="lime", bg="black")
        self.resultado_label.pack(side=tk.TOP, padx=10, pady=10)
        self.cria_widgets()

    def executar_comandos_nmap(self):
        """Executa o Nmap em uma thread separada e atualiza a interface com a saída."""
        
        def executar_comando():
            # Pega o comando a ser executado do campo de texto
            parametros = terminal_input.get("1.0", "end-1c").strip()
            if not parametros:
                terminal_output.insert(tk.END, "Por favor, insira um comando ou IP válido.\n", 'red')
                return

            comando = f"nmap {parametros}"

            # Executa o comando em uma nova thread
            def run_nmap():
                try:
                    processo = subprocess.Popen(
                        comando, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
                    )
                    self.processos.append(processo)
                    
                    # Leitura da saída e atualização da interface
                    for linha in processo.stdout:
                        terminal_output.insert(tk.END, linha)
                        terminal_output.yview(tk.END)

                    # Checar erros
                    erro = processo.stderr.read()
                    if erro:
                        terminal_output.insert(tk.END, erro, 'red')
                        terminal_output.yview(tk.END)

                except Exception as e:
                    terminal_output.insert(tk.END, f"Erro ao executar o comando: {e}\n", 'red')

                finally:
                    # Remover indicador de carregamento
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
                terminal_input.focus()  # Foca no campo de entrada para novos comandos

        # Configuração da interface do terminal
        terminal_window = tk.Toplevel(self.janela_principal)
        terminal_window.title("Terminal Nmap")

        terminal_output = scrolledtext.ScrolledText(terminal_window, height=20, width=80)
        terminal_output.tag_config('red', foreground='red')
        terminal_output.pack(fill="both", expand=True)

        terminal_input = tk.Text(terminal_window, height=2, width=80)
        terminal_input.pack(fill="x", padx=10, pady=10)

        # Comandos prontos e seleção
        comandos_comuns = [
            "scan rápido: -T4 -F",
            "scan completo: -sS -sV -O",
            "scan de portas específicas: -p 80,443",
            "scan de rede: 192.168.1.0/24",
            "scan de vulnerabilidades: --script vuln"
        ]

        def seleciona_comando(event):
            comando_selecionado = comando_combobox.get()
            terminal_input.delete("1.0", tk.END)
            terminal_input.insert(tk.END, comando_selecionado.split(": ")[1])

        comando_combobox = ttk.Combobox(terminal_window, values=comandos_comuns)
        comando_combobox.bind("<<ComboboxSelected>>", seleciona_comando)
        comando_combobox.pack(padx=10, pady=5)

        botao_executar = tk.Button(terminal_window, text="Executar", command=executar_comando, bg="black", fg="lime")
        botao_executar.pack(side=tk.LEFT, padx=10)

        botao_cancelar = tk.Button(terminal_window, text="Cancelar", command=cancelar_comando, bg="black", fg="red")
        botao_cancelar.pack(side=tk.RIGHT, padx=10)

        loading_label = tk.Label(terminal_window, text="Executando...", fg="orange", bg="black")

        terminal_input.focus()

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
                
                # Leitura da saída e atualização da interface
                for linha in processo.stdout:
                    terminal_text.insert(tk.END, linha)
                    terminal_text.yview(tk.END)

                # Checar erros
                erro = processo.stderr.read()
                if erro:
                    terminal_text.insert(tk.END, erro, 'red')
                    terminal_text.yview(tk.END)

            except Exception as e:
                terminal_text.insert(tk.END, f"Erro ao executar o comando: {e}\n", 'red')

        # Inicia a thread para execução do Metasploit
        threading.Thread(target=run_msfconsole).start()

    def instalar_metasploit_windows(self):
        """Baixa e instala o Metasploit no Windows com barra de progresso."""
        messagebox.showinfo("Instalação do Metasploit", "Para instalar o Metasploit, visite o site oficial:\nhttps://www.rapid7.com/products/metasploit/download/")
        
    def help_metasploit(self):
        """Abre a documentação do Metasploit no navegador."""
        url = "https://docs.metasploit.com/"
        webbrowser.open(url)

    def cria_widgets(self):
        # Menu superior
        menu_bar = tk.Menu(self.janela_principal)

        # Menu "Arquivo"
        menu_arquivos = tk.Menu(menu_bar, tearoff=0)
        menu_arquivos.add_command(label="Sair", command=self.janela_principal.quit)
        menu_bar.add_cascade(label="Menu", menu=menu_arquivos)

        # Menu "NMap"
        menu_nmap = tk.Menu(menu_bar, tearoff=0)
        menu_nmap.add_command(label="Executar Nmap", command=self.executar_comandos_nmap)
        menu_nmap.add_separator()
        menu_nmap.add_command(label="Instalar no Windows", command=self.install_nmap_windows)
        menu_nmap.add_separator()
        menu_nmap.add_command(label="Documentação", command=self.help_nmap)
        menu_bar.add_cascade(label="NMap", menu=menu_nmap)

        # Menu "Metasploit"
        menu_metasploit = tk.Menu(menu_bar, tearoff=0)
        menu_metasploit.add_command(label="Executar Metasploit", command=self.executar_metasploit)
        menu_metasploit.add_separator()
        menu_metasploit.add_command(label="Instalar no Windows", command=self.instalar_metasploit_windows)
        menu_metasploit.add_separator()
        menu_metasploit.add_command(label="Documentação", command=self.help_metasploit)
        menu_bar.add_cascade(label="Metasploit", menu=menu_metasploit)

        self.janela_principal.config(menu=menu_bar)


# Criação da janela principal e da instância da classe SecProject
janela = tk.Tk()
janela.title("SecSCAN")
janela.geometry("600x400")
janela.config(bg="black")  # Cor de fundo escura para estilo hacker

editor = SecProject(janela)

# Executa o loop principal da interface gráfica
janela.mainloop()
