# PyLitSurvey

Este é o repositório do projeto PyLitSurvey desenvolvido pelo LAPIG-UFG. Este projeto é destinado à análise de documentos literários. Abaixo estão as instruções para clonar o repositório, instalar as dependências necessárias e configurar o ambiente de desenvolvimento, incluindo a instalação do MongoDB nos sistemas operacionais Windows, Linux e Mac. Além disso, inclui um exemplo de uso no Google Colab.

## Clonando o Projeto

Para começar, clone este repositório em sua máquina local:

```bash
    git clone https://github.com/lapig-ufg/PyLitSurvey.git
    cd PyLitSurvey 
```
## Instalando o Python

Se você ainda não tiver o Python instalado, siga as instruções abaixo para seu sistema operacional:

### Windows

1. Baixe o instalador do Python [aqui](https://www.python.org/downloads/windows/).
2. Execute o instalador e certifique-se de marcar a opção "Add Python to PATH" antes de clicar em "Install Now".
3. Verifique a instalação abrindo o Prompt de Comando e digitando:

```sh
python --version
```

### Linux

1. Abra um terminal e atualize a lista de pacotes:

```sh
sudo apt update
```

2. Instale o Python:

```sh
sudo apt install python3 python3-venv python3-pip
```

3. Verifique a instalação:

```sh
python --version
```

### Mac

1. Instale o Homebrew se ainda não o tiver:

```sh
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```
2. Use o Homebrew para instalar o Python:

```sh
brew install python
```
3. Verifique a instalação:

```sh
python --version
```

## Instalação das Dependências

Instale as dependências listadas no arquivo requirements.txt. Recomendamos o uso de um ambiente virtual para evitar conflitos de versão de pacotes.

### Usando venv para criar um ambiente virtual:

```sh
python -m venv venv
source venv/bin/activate  # Linux e Mac
venv\Scripts\activate  # Windows
```
### Usando venv para criar um ambiente virtual:

```sh
(venv) pip install -r requirements.txt
```

## Instalando o MongoDB


### Windows

1. Baixe o instalador do MongoDB Community Server [aqui](https://www.mongodb.com/try/download/community).
2. Execute o instalador e siga as instruções na tela.
3. Após a instalação, inicie o MongoDB usando o MongoDB Compass ou o terminal com o comando:

```sh
mongod
```

### Linux

1. Importe a chave pública usada pelo sistema de gerenciamento de pacotes:

```sh
wget -qO - https://www.mongodb.org/static/pgp/server-4.4.asc | sudo apt-key add -
```

2. Crie o arquivo de lista para o MongoDB:

```sh
echo "deb [ arch=amd64,arm64 ]https://repo.mongodb.org/apt/ubuntu focal/mongodb-org/4.4 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-4.4.list
```

3. Atualize a lista de pacotes locais e instale o MongoDB:

```sh
sudo apt-get update
sudo apt-get install -y mongodb-org
```
4. Inicie o MongoDB:

```sh
sudo systemctl start mongod
sudo systemctl enable mongod
```
### Mac

1. Instale o Homebrew se ainda não o tiver:

```sh
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```
2. Use o Homebrew para instalar o Python:

```sh
brew tap mongodb/brew
brew install mongodb-community@4.4
```
3. Inicie o MongoDB:

```sh
brew services start mongodb/brew/mongodb-community
```

## Configuração

A configuração do projeto pode ser feita no arquivo settings.toml. Ajuste as configurações conforme necessário para seu ambiente.

## Executando o Script

```sh
python get_lit_page.py
```

## Exemplo no Google Colab

Se preferir usar o Google Colab para executar este projeto, siga o exemplo fornecido [aqui](https://colab.research.google.com/drive/1ay2giAXobqsIt1txrK6V5Civ8Lz93byL?usp=sharing).

## Contribuindo

Se desejar contribuir com este projeto, por favor, envie um pull request com suas alterações. Todos os tipos de contribuição são bem-vindos!

### Mantenedores do Projeto:

* Equipe LAPIG-UFG

Para dúvidas ou suporte, entre em contato com a equipe através do e-mail lapig@ufg.br.