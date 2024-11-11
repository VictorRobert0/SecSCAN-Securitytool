# SecSCAN - Ferramenta de Segurança

SecSCAN é uma ferramenta de segurança simples desenvolvida em Python que facilita a execução de comandos de ferramentas como Nmap e Metasploit diretamente de uma interface gráfica construída com Tkinter. O projeto visa ajudar a automatizar algumas tarefas de segurança cibernética em ambientes Windows e Linux, com instalação automatizada do Nmap e Metasploit.

## Funcionalidades Windows

- **Executar Nmap**: Execute comandos Nmap diretamente pela interface gráfica.
- **Instalar Nmap no Windows**: Baixe e instale o Nmap automaticamente.
- **Documentação Nmap**: Em breve.
- Executar MetaSploit Windows: Execute comandos Metasploit diretamente pela interface gráfica.
- **Instalar Metasploit no Windows**: Em breve

### Baixar o Executável
Você pode baixar a versão compilada do SecSCAN diretamente da página de Releases do GitHub.

-  Windows:
[SecSCAN Windows v1.0.0](https://github.com/VictorRobert0/SecSCAN-Securitytool/releases/tag/Secscan-v1.0)


## Pré-requisitos (Desenvolvedores) 

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
````
### 2. Instalar as Dependências
``` bash
Instale as dependências do projeto com o pip:
pip install -r requirements.txt
``` 
### 3. Executar a Ferramenta
``` bash
Execute o script principal para iniciar a interface gráfica:

SecSCAN.py
``` 



### Contribuindo
- Se você deseja contribuir para o desenvolvimento do SecSCAN, fique à vontade para abrir issues ou enviar pull requests. Sua contribuição é muito bem-vinda!
``` bash
Como contribuir:
Fork este repositório.
Crie uma nova branch para sua feature (git checkout -b minha-feature).
Faça as mudanças desejadas e commit (git commit -am 'Adicionando uma nova feature').
Envie a branch para o repositório remoto (git push origin minha-feature).
Abra um Pull Request!
```


### Alterações feitas
- Versão 1.0.0:
- Seção "Baixar o Executável": Adicionada uma seção com links para baixar a versão compilada do executável diretamente da página de releases no GitHub.
- Instruções para compilar o executável: Explicação sobre como compilar o executável você mesmo usando PyInstaller.
- Correção no comando de clonagem do repositório: O comando git clone foi corrigido e ajustado para refletir o repositório correto.
### SecSCAN foi desenvolvido por Victor Roberto. Se você tiver alguma dúvida ou sugestão, sinta-se à vontade para abrir uma issue ou enviar uma mensagem.
