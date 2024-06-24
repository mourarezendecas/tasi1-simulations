
# Projeto Python

  

Este projeto é um exemplo de como configurar e executar um arquivo Python (`main.py`) utilizando um ambiente virtual (`virtualenv`). A seguir estão as instruções detalhadas para configuração do ambiente e execução do script.

  

## Pré-requisitos

  

- Python 3.6+ instalado. Você pode verificar a versão do Python instalada executando:

```sh
python --version
```

- pip (gerenciador de pacotes do Python) instalado. Geralmente, ele já vem com a instalação do Python. Verifique a versão do pip executando:

```sh
pip --version
```

# Passo a passo

1. Instalar o virtualenv

O virtualenv é uma ferramenta para criar ambientes isolados do Python. Para instalá-lo, execute:

```sh
pip install virtualenv
```

2. Criar um ambiente virtual

Crie um novo ambiente virtual:
		```sh
    virtualenv venv
    ```

Isso criará um diretório chamado `venv` com um novo ambiente Python isolado.

3. Ativar o ambiente virtual

Para ativar o ambiente virtual, use o comando apropriado para o seu sistema operacional:

**Windows:** 
```sh
.\venv\Scripts\activate
```
**Linux/MacOS**
```sh
source venv/bin/activate
```
Após a ativação, você verá o nome do ambiente (`venv`) aparecendo no prompt do seu terminal, indicando que o ambiente virtual está ativo.

4. Instalar as dependências

Com o ambiente virtual ativado, instale as dependências necessárias para o projeto. Supondo que as dependências estão listadas em um arquivo `requirements.txt`, execute:
```sh
pip install -r requirements.txt
```
5. Executar o script Python

Agora que todas as dependências estão instaladas, você pode executar o script `main.py`:
```sh
python main.py
```
6. Desativar o ambiente virtual

Após terminar de usar o ambiente virtual, você pode desativá-lo executando:
```sh
deactivate
```

# Estrutura do Projeto

A estrutura básica do projeto deve se parecer com isto:
```css
projeto/
├── main.py
├── requirements.txt
└── venv/
```
-   `main.py`: Arquivi referente à execução da simulação.
-   `requirements.txt`: Arquivo contendo as dependências do projeto.
-   `venv/`: Diretório do ambiente virtual (criado pelo `virtualenv`).