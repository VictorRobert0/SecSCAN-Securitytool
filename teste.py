import requests
import urllib.request
import threading
import tkinter as tk
from tkinter import scrolledtext, messagebox
from tkinter import ttk
import subprocess
import ctypes
import os
from PIL import Image, ImageTk

class SecProject:
    def __init__(self, janela_principal):
        self.janela_principal = janela_principal
        self.processos = []

        # Configuração de imagem de fundo
        self.imagem_fundo_original = Image.open("./interface-SecSCAN/img/secscan.jpg")
        self.imagem_fundo = ImageTk.PhotoImage(self.imagem_fundo_original)
        self.fundo_label = tk.Label(self.janela_principal, image=self.imagem_fundo)
        self.fundo_label.place(relwidth=1, relheight=1, x=0, y=0)

        # Label de título
        self.resultado_label = tk.Label(self.janela_principal, text="SecSCAN", font="Courier 16", fg="lime", bg="black")
        self.resultado_label.pack(side=tk.TOP, padx=10, pady=10)

        # Criação de menu
        self.menu_bar = tk.Menu(self.janela_principal)
        self.criar_menu()
        self.janela_principal.config(menu=self.menu_bar)

        self.cria_widgets()
        self.janela_principal.geometry("700x500")
        self.janela_principal.resizable(False, False)

        # Variável para controlar o estado de execução do scan
        self.scan_thread = None
        self.terminar_scan = False

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

        # 50 comandos mais utilizados no Nmap
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
            ("nmap -p 1-65535", "Escaneia todas as portas (1 a 65535).")
        ]

        comandos_tree = ttk.Treeview(terminal_window, columns=("Comando", "Descrição"), show="headings", height=10)
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

    def criar_menu(self):
        nmap_menu = tk.Menu(self.menu_bar, tearoff=0)
        nmap_menu.add_command(label="Instalar Nmap", command=self.install_nmap_windows)
        self.menu_bar.add_cascade(label="Nmap", menu=nmap_menu)

        metasploit_menu = tk.Menu(self.menu_bar, tearoff=0)
        metasploit_menu.add_command(label="Opção Metasploit", command=lambda: messagebox.showinfo("Metasploit", "Implementando essa função"))
        self.menu_bar.add_cascade(label="Metasploit", menu=metasploit_menu)

    def cria_widgets(self):
        botao_terminal = tk.Button(self.janela_principal, text="Abrir Terminal Nmap", command=self.executar_comandos_nmap, bg="black", fg="lime")
        botao_terminal.pack(padx=10, pady=100)

        botao_terminal_metasploit = tk.Button(self.janela_principal, text="Abrir Terminal Metasploit", command=lambda: messagebox.showinfo("Metasploit", "Implementando essa função"), bg="black", fg="lime")
        botao_terminal_metasploit.pack(padx=10, pady=0.7)


root = tk.Tk()
app = SecProject(root)
root.mainloop()
