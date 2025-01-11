import requests
import urllib.request
import threading
import tkinter as tk
from tkinter import scrolledtext, messagebox
from tkinter import ttk
import subprocess
import ctypes
import sys
import os
import webbrowser
from PIL import Image, ImageTk

class SecProject:
    def __init__(self, janela_principal):
        self.janela_principal = janela_principal
        self.processos = []

        # Inicializa msf_path como None
        self.msf_path = None

        # Configuração de imagem de fundo (verificando o ambiente)
        if getattr(sys, 'frozen', False):  # Se for um executável compilado
            caminho_imagem = os.path.join(sys._MEIPASS, "img", "secscan.jpg")
        else:
            caminho_imagem = "./img/secscan.jpg"  # Para ambiente de desenvolvimento

        self.imagem_fundo_original = Image.open(caminho_imagem)
        self.imagem_fundo = ImageTk.PhotoImage(self.imagem_fundo_original)
        self.fundo_label = tk.Label(self.janela_principal, image=self.imagem_fundo)
        self.fundo_label.place(relwidth=1, relheight=1, x=0, y=0)

        # Label de título
        self.resultado_label = tk.Label(self.janela_principal, text="SecSCAN - Security Tool", font="Courier 16", fg="lime", bg="black")
        self.resultado_label.pack(side=tk.TOP, padx=10, pady=10)

        # Criação de menu
        self.menu_bar = tk.Menu(self.janela_principal)
        self.criar_menu()
        self.janela_principal.config(menu=self.menu_bar)

        self.cria_widgets()
        self.janela_principal.geometry("700x500")
        self.janela_principal.resizable(False, False)

        # Adicionando assinatura no canto inferior direito
        self.assinatura_label = tk.Label(self.janela_principal, text="Desenvolvido por Victor RobertoS", font="Arial 10", fg="white", bg="black")
        self.assinatura_label.place(x=511, y=476)

        # Variável para controlar o estado de execução do scan
        self.scan_thread = None
        self.terminar_scan = False



#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
                           # METASPLOIT SESSION - TERMINAL
#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
 
    def doc_metasploit(self):
        webbrowser.open("https://docs.metasploit.com/docs/pentesting/metasploit-guide-setting-module-options.html")



    def buscar_msfconsole(self, raiz="C:\\"):
        """Busca recursivamente o msfconsole.bat no sistema"""
        for root, dirs, files in os.walk(raiz):
            if "msfconsole.bat" in files:
                return os.path.join(root, "msfconsole.bat")
        return None

    def verificar_instalacao_metasploit(self):
        """Verifica se o Metasploit está instalado em algum local do sistema"""
        # Verifica se o caminho já foi armazenado
        if self.msf_path and os.path.isfile(self.msf_path):
            return True

        # Tenta localizar o msfconsole
        drives = [f"{chr(x)}:\\" for x in range(65, 91) if os.path.exists(f"{chr(x)}:\\")]
        for drive in drives:
            self.msf_path = self.buscar_msfconsole(drive)
            if self.msf_path:
                return True

        return False

    def executar_terminal_metasploit(self):
        """Abre um terminal interativo apenas se o Metasploit estiver instalado"""
        if not self.verificar_instalacao_metasploit():
            messagebox.showerror("Erro", "Metasploit Framework não está instalado no sistema.")
            return

        # Cria a janela para o terminal
        terminal_window = tk.Toplevel(self.janela_principal)
        terminal_window.title("Terminal Metasploit")
        terminal_window.geometry("600x400")

        # Caixa de texto para saída
        terminal_output = tk.Text(terminal_window, wrap="word", state="disabled", bg="black", fg="white")
        terminal_output.pack(fill="both", expand=True, padx=10, pady=10)

        # Entrada para comandos
        command_frame = tk.Frame(terminal_window)
        command_frame.pack(fill="x", padx=10, pady=5)

        tk.Label(command_frame, text="Comando:").pack(side="left")
        command_entry = tk.Entry(command_frame)
        command_entry.pack(side="left", fill="x", expand=True, padx=5)
        send_button = tk.Button(command_frame, text="Executar", command=lambda: self.executar_comando_metasploit(command_entry, terminal_output))
        send_button.pack(side="right")

        # Inicia o msfconsole em um subprocess
        self.msf_process = subprocess.Popen(
            [self.msf_path],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1
        )

        # Atualiza a saída do terminal com os logs do msfconsole
        threading.Thread(target=self.atualizar_terminal, args=(terminal_output,), daemon=True).start()

    def executar_comando_metasploit(self, command_entry, terminal_output):
        """Envia um comando para o msfconsole"""
        command = command_entry.get().strip()
        if self.msf_process and command:
            self.msf_process.stdin.write(command + "\n")
            self.msf_process.stdin.flush()
            command_entry.delete(0, tk.END)

    def atualizar_terminal(self, terminal_output):
        """Atualiza o terminal com a saída do msfconsole"""
        while self.msf_process and self.msf_process.poll() is None:
            output = self.msf_process.stdout.readline()
            if output:
                terminal_output.config(state="normal")
                terminal_output.insert("end", output)
                terminal_output.config(state="disabled")
                terminal_output.see("end")
 
 
 
 
 
 
 
 
 
 
 
 
    def install_metasploit(self):
        """Função de instalação do Metasploit no Windows"""
        progress_window = tk.Toplevel(self.janela_principal)
        progress_window.title("Instalação do Metasploit")

        progress_label = tk.Label(progress_window, text="Baixando o instalador do Metasploit...", font="Arial 12")
        progress_label.pack(pady=10)

        progress_bar = ttk.Progressbar(progress_window, length=300, orient=tk.HORIZONTAL, mode='determinate')
        progress_bar.pack(pady=20)

        metasploit_installer_url = "https://windows.metasploit.com/metasploitframework-latest.msi"
        metasploit_installer_path = "metasploitframework-latest.msi"

        try:
            # Atualiza o progresso do download
            def update_progress(block_num, block_size, total_size):
                progress = block_num * block_size / total_size * 100
                progress_bar['value'] = progress
                progress_window.update_idletasks()

            # Baixa o instalador
            urllib.request.urlretrieve(metasploit_installer_url, metasploit_installer_path, reporthook=update_progress)

            # Atualiza o label para indicar o próximo passo
            progress_label.config(text="Instalando o Metasploit...")

            # Executa o instalador .msi como administrador
            self.run_msi_as_admin(metasploit_installer_path)

            # Confirma a conclusão
            progress_label.config(text="Instalação concluída!")
            progress_bar['value'] = 100

            # Adiciona o Metasploit ao PATH do sistema
            self.adicionar_metasploit_ao_path()

        except Exception as e:
            progress_label.config(text="Erro ao baixar ou instalar o Metasploit.")
            print(f"Erro: {e}")
            progress_bar['value'] = 0

    def run_msi_as_admin(self, msi_path):
        """Executa um arquivo MSI como administrador"""
        try:
            # Executa o comando msiexec com privilégios elevados
            cmd = f'powershell -Command "Start-Process msiexec.exe -ArgumentList \'/i \\"{msi_path}\\" /quiet /norestart\' -Verb RunAs"'
            subprocess.run(cmd, shell=True, check=True)
            print(f"Instalador {msi_path} executado com sucesso.")
        except subprocess.CalledProcessError as e:
            print(f"Erro ao executar o instalador: {e}")
        except Exception as e:
            print(f"Erro inesperado ao executar o instalador: {e}")

    def adicionar_metasploit_ao_path(self):
        """Adiciona o Metasploit ao PATH do sistema"""
        metasploit_install_path = r"C:\Program Files (x86)\metasploit-framework"
        if metasploit_install_path not in os.environ.get('PATH', ''):
            os.environ['PATH'] += os.pathsep + metasploit_install_path
            try:
                subprocess.run(f'setx PATH "%PATH%;{metasploit_install_path}"', shell=True, check=True)
                print("Metasploit adicionado ao PATH com sucesso. :)")
            except subprocess.CalledProcessError as e:
                print(f"Erro ao adicionar Metasploit ao PATH: {e}")


#------------------------------------------------------------------------------------------------------------------------------------------------------------  
                                #COMANDOS NMAP
#------------------------------------------------------------------------------------------------------------------------------------------------------------
    def verificar_instalacao(self, terminal_output):
        nmap_path = r"C:\Program Files (x86)\Nmap\nmap.exe"
        if not os.path.isfile(nmap_path):
            terminal_output.insert(tk.END, "Nmap não encontrado. Por favor, instale o Nmap primeiro.\n", 'red')
            terminal_output.yview(tk.END)
            return False
        return True

    def adicionar_nmap_ao_path(self):
        nmap_install_path = r"C:\Program Files (x86)\Nmap"
        if nmap_install_path not in os.environ.get('PATH', ''):
            os.environ['PATH'] += os.pathsep + nmap_install_path
            subprocess.run(f'setx PATH "%PATH%;{nmap_install_path}"', shell=True)
            print("Nmap adicionado ao PATH com sucesso.")

    def executar_comandos_nmap(self):
        terminal_window = tk.Toplevel(self.janela_principal)
        terminal_window.title("Terminal Nmap")

        ip_label = tk.Label(terminal_window, text="IP Alvo:")
        ip_label.pack(anchor="w", padx=10, pady=2)
        ip_entry = tk.Entry(terminal_window, width=30)
        ip_entry.pack(fill="x", padx=10)

        parametros_label = tk.Label(terminal_window, text="Parâmetros de scan adicionais:")
        parametros_label.pack(anchor="w", padx=10, pady=2)
        parametros_entry = tk.Entry(terminal_window, width=30)
        parametros_entry.pack(fill="x", padx=10)

        # Comandos Nmap
        comandos_nmap = [
            ("nmap -v", "Exibe a versão do Nmap e informações detalhadas."),
            ("nmap -A", "Detecta sistema operacional, versões de serviços e executa scripts."),
            ("nmap -sS", "Realiza um scan SYN (Stealth Scan), evitando deteções."),
            ("nmap -O", "Identifica o sistema operacional alvo."),
            ("nmap -sP", "Realiza um ping scan, identificando hosts ativos."),
            ("nmap -T4", "Aumenta a velocidade do scan."),
            ("nmap -sV", "Detecta as versões dos serviços em execução."),
            ("nmap -p 80", "Escaneia a porta 80 (HTTP) do alvo."),
            ("nmap --script vuln", "Executa scripts de vulnerabilidade."),
            ("nmap -O --osscan-limit", "Limita a detecção de sistema operacional."),
            ("nmap -Pn", "Desativa o ping, assumindo que o host está ativo."),
            ("nmap -p- 192.168.1.1", "Escaneia todas as portas de um host."),
            ("nmap --top-ports 10", "Escaneia as 10 portas mais comuns."),
            ("nmap -sU", "Escaneia portas UDP."),
            ("nmap -iL targets.txt", "Escaneia múltiplos alvos de um arquivo."),
            ("nmap -sR", "Realiza um scan de portas aleatórias."),
            ("nmap -sA", "Detecta firewalls e filtra pacotes."),
            ("nmap -6", "Realiza um scan em redes IPv6."),
            ("nmap --script discovery", "Executa scripts de descoberta."),
            ("nmap -p 1-65535", "Escaneia todas as portas (1 a 65535)."),
            ("nmap -sF", "Realiza um scan de portas com pacotes FIN."),
            ("nmap -sX", "Realiza um scan com pacotes Xmas."),
            ("nmap -sY", "Realiza um scan UDP para serviços."),
            ("nmap -sL", "Lista todos os hosts especificados sem realizar scan."),
            ("nmap -b", "Escaneia com backdoor."),
            ("nmap -p 22,80,443", "Escaneia portas específicas (22, 80, 443)."),
            ("nmap --traceroute", "Realiza o rastreamento de rotas."),
            ("nmap --max-retries", "Define o número máximo de tentativas de reconexão."),
            ("nmap --open", "Exibe apenas portas abertas."),
            ("nmap -sN", "Realiza um scan de portas com pacotes null."),
            ("nmap -sT", "Realiza um scan TCP Connect."),
            ("nmap -sW", "Escaneia portas usando pacotes com janela."),
            ("nmap -D RND:10", "Usa 10 endereços IP aleatórios para o scan."),
            ("nmap -n", "Evita a resolução DNS."),
            ("nmap --spoof-mac", "Spoof MAC address."),
            ("nmap --dns-servers", "Define servidores DNS específicos."),
            ("nmap --system-dns", "Usa o DNS do sistema."),
            ("nmap --min-rate", "Define a taxa mínima de pacotes a enviar."),
            ("nmap --max-rate", "Define a taxa máxima de pacotes a enviar."),
            ("nmap -p 443,21-80", "Escaneia portas específicas com intervalos."),
            ("nmap -f", "Fragmenta pacotes para evitar detecção."),
            ("nmap -T0", "Define a menor velocidade de scan."),
            ("nmap --unprivileged", "Executa o scan sem privilégios."),
            ("nmap --source-port", "Define a porta de origem."),
            ("nmap -O --osscan-guess", "Tenta adivinhar o sistema operacional."),
            ("nmap -g", "Define um range específico de portas."),
            ("nmap -sZ", "Realiza um scan de portas com pacotes Zigzag."),
            ("nmap --dns-search", "Define o domínio de busca DNS."),
            ("nmap --script http-enum", "Escaneia serviços HTTP para enumerar informações."),
            ("nmap --script smb-os-discovery", "Descobre o sistema operacional via SMB."),
            ("nmap --packet-trace", "Exibe o trace de pacotes durante o scan."),
            ("nmap --spoof-ip", "Spoof IP address."),
            ("nmap --scan-delay", "Define o atraso entre pacotes."),
            ("nmap --min-hostgroup", "Define o número mínimo de hosts por grupo."),
            ("nmap --max-hostgroup", "Define o número máximo de hosts por grupo."),
            ("nmap --resume", "Retoma o scan de onde foi interrompido."),
            ("nmap -T5", "Executa o scan na maior velocidade."),
        ]

        comandos_tree = ttk.Treeview(terminal_window, columns=("Comando", "Descrição"), show="headings", height=15)
        comandos_tree.heading("Comando", text="Comando")
        comandos_tree.heading("Descrição", text="Descrição")
        comandos_tree.pack(padx=10, pady=10, fill="x")

        for comando, descricao in comandos_nmap:
            comandos_tree.insert("", "end", values=(comando, descricao))

        terminal_output = scrolledtext.ScrolledText(terminal_window, height=15, width=80)
        terminal_output.pack(padx=10, pady=10)

        def executar_comando():
            ip = ip_entry.get()
            parametros = parametros_entry.get()
            item_selecionado = comandos_tree.selection()

            if not item_selecionado:
                messagebox.showwarning("Atenção", "Selecione um comando.")
                return

            comando_selecionado = comandos_tree.item(item_selecionado[0], "values")[0]
            comando_completo = f'{comando_selecionado} {ip} {parametros}'

            if self.verificar_instalacao(terminal_output):
                terminal_output.insert(tk.END, f"\nExecutando: {comando_completo}\n", 'blue')
                terminal_output.yview(tk.END)

                def run_nmap():
                    nmap_path = r"C:/Program Files (x86)/Nmap/nmap.exe"
                    process = subprocess.Popen([nmap_path, *comando_completo.split()], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

                    for line in iter(process.stdout.readline, b''):
                        terminal_output.insert(tk.END, line.decode('utf-8'))
                        terminal_output.yview(tk.END)

                    for line in iter(process.stderr.readline, b''):
                        terminal_output.insert(tk.END, line.decode('utf-8'))
                        terminal_output.yview(tk.END)

                    process.stdout.close()
                    process.stderr.close()
                    process.wait()

                self.terminar_scan = False
                self.scan_thread = threading.Thread(target=run_nmap)
                self.scan_thread.start()

        def cancelar_scan():
            if self.scan_thread:
                self.terminar_scan = True
                self.scan_thread.join()  # Espera o thread do Nmap finalizar
                terminal_output.insert(tk.END, "\nScan cancelado.\n", 'red')
                terminal_output.yview(tk.END)

        def limpar_terminal():
            terminal_output.delete(1.0, tk.END)
            
            

        # Organize buttons side by side using a frame
        buttons_frame = tk.Frame(terminal_window)
        buttons_frame.pack(pady=10)

        executar_button = tk.Button(buttons_frame, text="Executar Comando", command=executar_comando, bg="black", fg="lime")
        executar_button.pack(side=tk.LEFT, padx=5)

        cancelar_button = tk.Button(buttons_frame, text="Cancelar Scan", command=cancelar_scan, bg="black", fg="lime")
        cancelar_button.pack(side=tk.LEFT, padx=5)

        limpar_button = tk.Button(buttons_frame, text="Limpar", command=limpar_terminal, bg="black", fg="lime")
        limpar_button.pack(side=tk.LEFT, padx=5)

    def install_nmap_windows(self):
        """Função de instalação do Nmap no Windows"""
        progress_window = tk.Toplevel(self.janela_principal)
        progress_window.title("Instalação do Nmap")

        progress_label = tk.Label(progress_window, text="Baixando o instalador do Nmap...", font="Arial 12")
        progress_label.pack(pady=10)

        progress_bar = ttk.Progressbar(progress_window, length=300, orient=tk.HORIZONTAL, mode='determinate')
        progress_bar.pack(pady=20)

        nmap_installer_url = "https://nmap.org/dist/nmap-7.94-setup.exe"
        nmap_installer_path = "nmap-setup.exe"

        try:
            def update_progress(block_num, block_size, total_size):
                progress = block_num * block_size / total_size * 100
                progress_bar['value'] = progress
                progress_window.update_idletasks()

            urllib.request.urlretrieve(nmap_installer_url, nmap_installer_path, reporthook=update_progress)

            progress_label.config(text="Instalando o Nmap...")
            self.run_as_admin(nmap_installer_path, '/S')
            progress_label.config(text="Instalação concluída!")
            progress_bar['value'] = 100

            self.adicionar_nmap_ao_path()

        except Exception as e:
            progress_label.config(text="Erro ao baixar ou instalar o Nmap.")
            print(f"Erro: {e}")
            progress_bar['value'] = 0

    def run_as_admin(self, executable, *args):
        """Executa um programa com privilégios de administrador"""
        ctypes.windll.shell32.ShellExecuteW(None, "runas", executable, ' '.join(args), None, 1)
        
#------------------------------------------------------------------------------------------------------------------------------------------------------------  
#------------------------------------------------------------------------------------------------------------------------------------------------------------

    def criar_menu(self):
        nmap_menu = tk.Menu(self.menu_bar, tearoff=0)
        nmap_menu.add_command(label="Instalar Nmap", command=self.install_nmap_windows)
        self.menu_bar.add_cascade(label="Nmap", menu=nmap_menu)

        metasploit_menu = tk.Menu(self.menu_bar, tearoff=0)
        metasploit_menu.add_command(label="Instalar MetaSploit", command=self.install_metasploit)
        metasploit_menu.add_command(label="Documentação - Metasploit", command=self.doc_metasploit)
        self.menu_bar.add_cascade(label="Metasploit", menu=metasploit_menu)




    def cria_widgets(self):
        # Botão para abrir o terminal do Nmap
        botao_terminal = tk.Button(self.janela_principal, text="Abrir Terminal Nmap", command=self.executar_comandos_nmap, bg="black", fg="lime")
        botao_terminal.pack(padx=10, pady=(90, 50))  # Ajustado o espaçamento superior e inferior

        # Botão para abrir o terminal do Metasploit
        botao_terminal_metasploit = tk.Button(self.janela_principal, text="Abrir Terminal Metasploit", command=self.executar_terminal_metasploit, bg="black", fg="lime")
        botao_terminal_metasploit.pack(padx=10, pady=(2, 20))  # Ajustado o espaçamento para o Metasploit



root = tk.Tk()
root.title("SecSCAN - Security Tool")
app = SecProject(root)
root.mainloop()
