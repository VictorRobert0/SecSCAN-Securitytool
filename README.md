# SecSCAN - Ferramenta de Segurança

SecSCAN é uma ferramenta de segurança simples desenvolvida em Python que facilita a execução de comandos de ferramentas como Nmap e Metasploit diretamente de uma interface gráfica construída com Tkinter. O projeto visa ajudar a automatizar algumas tarefas de segurança cibernética em ambientes Windows e Linux, com instalação automatizada do Nmap e Metasploit.

## Funcionalidades

- **Executar Nmap**: Execute comandos Nmap diretamente pela interface gráfica.
- **Instalar Nmap no Windows**: Baixe e instale o Nmap automaticamente.
- **Instalar Metasploit no Windows**: Baixe e instale o Metasploit automaticamente.
- **Documentação Nmap**: Acesse facilmente a documentação do Nmap diretamente no navegador.

## Pré-requisitos

Antes de começar, você precisará ter o Python instalado em sua máquina, bem como as dependências necessárias. 

### Python

- Python 3.6 ou superior
- Tkinter (geralmente já incluso nas distribuições do Python, mas verifique se está instalado)

### Dependências

As bibliotecas externas necessárias são listadas no arquivo `requirements.txt`.

## Instalação

Siga as etapas abaixo para configurar o projeto em sua máquina.

### 1. Clonar o Repositório

Clone este repositório para sua máquina local:

```bash
git clone https://github.com/VictorRobert0/SecSCAN-Securitytool.git
cd SecSCAN-Securitytool
2. Instalar as Dependências
Instale as dependências do projeto com o pip:


pip install -r requirements.txt
3. Executar a Ferramenta
Execute o script principal para iniciar a interface gráfica:

SecSCAN.py

Baixar o Executável
Você pode baixar a versão compilada do SecSCAN diretamente da página de Releases do GitHub.

Para Windows:
SecSCAN Windows v1.0.0

Contribuindo
Se você deseja contribuir para o desenvolvimento do SecSCAN, fique à vontade para abrir issues ou enviar pull requests.

Licença
Este projeto está licenciado sob a Licença MIT - veja o arquivo LICENSE para mais detalhes.



### Alterações feitas (exemplo):
1. **Seção "Baixar o Executável"**: Adicionei uma seção com links para baixar o executável diretamente da página de releases no GitHub.
2. **Instruções para compilar o executável**: Explicação sobre como compilar o executável você mesmo usando `PyInstaller`.
3. **Correção no comando de clonagem do repositório**: O comando `git clone` foi corrigido pa
