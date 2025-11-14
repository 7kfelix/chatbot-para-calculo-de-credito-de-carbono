# Projeto APS UNIP (Aplicação Web com Flask)

Este repositório contém o código-fonte de uma aplicação web desenvolvida como parte das Atividades Práticas Supervisionadas (APS) da UNIP.

A aplicação é construída utilizando o framework **Flask** (Python) e parece integrar-se com as APIs de Inteligência Artificial do Google (possivelmente Gemini), com base na presença de uma `GOOGLE_API_KEY` no arquivo de configuração.

## 🛠️ Tecnologias Identificadas

* **Backend:** Python
* **Framework:** Flask (identificado pela presença de `flask.exe` no ambiente virtual) 
* **APIs Externas:** Google AI (inferido pela `GOOGLE_API_KEY`) 
* **Gerenciamento de Configuração:** `python-dotenv` (identificado por `.env` e `dotenv.exe`) 
* **Ambiente:** `venv` (Ambiente Virtual Python) 
* **Controle de Versão:** Git (identificado pelo arquivo `.gitignore`) 

## ⚙️ Configuração e Instalação

Para executar este projeto localmente, siga estes passos:

### 1. Pré-requisitos

* Python 3.10 ou superior
* Git (opcional, para controle de versão)

### 2. Clonar o Repositório

```bash
git clone <url-do-repositorio>
cd APS UNIP
```

## 3. Configurar o Ambiente Virtual (venv)

É recomendado criar um novo ambiente virtual em vez de usar o que veio no .rar, pois os caminhos podem ser específicos da máquina de origem.
### Criar um novo ambiente virtual
```bash
python -m venv venv
```
## 4. Ativar o ambiente virtual
### No Windows:
```bash
venv\Scripts\activate
```
### No macOS/Linux:
```bash
source venv/bin/activate
```
## Nota: Para instalar todas as ferramentas, apenas execute o comando
```bash
pip install -r requirements.txt
```

## 5. Configurar Variáveis de Ambiente

Crie um arquivo chamado .env na raiz do diretório. Adicione o seguinte conteúdo, substituindo pelos seus próprios valores:
```bash
# Chave secreta para segurança das sessões do Flask
SECRET_KEY='sua_chave_secreta_aqui'

# Chave de API para os serviços do Google AI
GOOGLE_API_KEY='sua_google_api_key_aqui'
```

## 6. Executar a Aplicação

Com o ambiente virtual ativado, execute o Flask:
```bash
python app.py
```
