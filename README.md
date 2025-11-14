# Projeto APS UNIP (Aplicação Web com Flask)

Este repositório contém o código-fonte de uma aplicação web desenvolvida como parte das Atividades Práticas Supervisionadas (APS) da UNIP.

## Feito por: João Victor Severiano Grama, Leticia Maria dos Santos Silva, Lucas Alves Pereira, Luigi Fernandes Leal, Matheus Lima Prates e Marcelo Felix do Vale

A aplicação é construída utilizando o framework **Flask** (Python) e integra-se com as APIs de Inteligência Artificial do Google, com base na presença de uma `GOOGLE_API_KEY` no arquivo de configuração.

## 🛠️ Tecnologias Identificadas

* **Backend:** Python, JavaScript
* **Framework:** Flask
* **APIs Externas:** Google AI
* **Gerenciamento de Configuração:** `python-dotenv`
* **Ambiente:** `venv`
* **Controle de Versão:** Git
* **Frontend:** HTML e CSS

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

Com o ambiente virtual ativado, execute o Flask:
```bash
python app.py
```

---------------------------------------------------------------------------------------
### Caso tenha dúvidas de como extrair a sua chave de API do Google, siga esses passos:
O processo é gratuito e feito através do **Google AI Studio**.

### 1. Acesse o Google AI Studio

Abra seu navegador e vá para o site oficial:

* **[https://aistudio.google.com](https://aistudio.google.com)**

Você precisará fazer login com sua conta pessoal do Google (a mesma que você usa para o Gmail, por exemplo).

### 2. Crie sua Chave de API

1.  Após entrar no painel principal, procure no menu à esquerda pela opção **"Get API key"** (Obter chave de API) e clique nela.
    
2.  Você será levado para a página de "API keys". Clique no botão **"Create API key"** (Criar chave de API).

3.  Será solicitado que você selecione um projeto do Google Cloud para associar a chave.
    * **Se você já tem um projeto:** Selecione-o na lista.
    * **Se é sua primeira vez:** O sistema geralmente se oferece para criar um novo projeto para você automaticamente. Apenas siga as instruções na tela.

### 3. Copie e Guarde sua Chave

Assim que a chave for criada, ela aparecerá na sua lista. Será uma longa sequência de letras e números, como `AIzaSy...`.

1.  Clique no ícone de "Copiar" ao lado da chave para copiá-la para sua área de transferência.
    
2.  **IMPORTANTE:** Trate essa chave como uma senha! Não a compartilhe publicamente.

### 4. Adicione a Chave ao Projeto

Agora, você precisa "avisar" o nosso projeto qual é a sua chave.

1.  Encontre (ou crie) o arquivo `.env` na pasta raiz do projeto (na mesma pasta que o `app.py`).
2.  Abra este arquivo e adicione ou edite a linha da `GOOGLE_API_KEY`:
3.  Substitua `sua_google_api_key_aqui` pela chave que você acabou de copiar.
4.  Salve o arquivo.
---------------------------------------------------------------------------------------
