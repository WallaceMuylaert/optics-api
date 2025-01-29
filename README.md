# OPTICS-API

A **OPTICS-API** é uma API desenvolvida para gerenciar fornecedores, pedidos e endereços. Ela foi construída com FastAPI e utiliza SQLAlchemy para interação com o banco de dados. Este projeto é ideal para sistemas de gestão de fornecedores e pedidos.

## Sumário
- [Como começar](#como-começar)
  - [Criar e ativar um ambiente virtual](#criar-e-ativar-um-ambiente-virtual)
  - [Instalar dependências](#instalar-dependências)
- [Executando a API](#executando-a-api)
- [Endpoints](#endpoints)

## Como começar

### Criar e ativar um ambiente virtual

#### Windows
Iniciando a VENV
```sh
python -m venv .venv
```
Ativando o ambiente virtual:
```sh
.venv\Scripts\activate
```

#### Linux/MacOS
Iniciando a VENV
```sh
python3 -m venv .venv
```
Ativando o ambiente virtual:
```sh
source .venv/bin/activate
```

### Instalar dependências

Com o ambiente virtual ativado, execute o comando abaixo para instalar as dependências necessárias:
```sh
pip install -r requirements.txt
```

## Executando a API

Após configurar o ambiente e instalar as dependências, inicie a aplicação utilizando o comando:
```sh
uvicorn main:app --reload
```
A API estará disponível em [http://127.0.0.1:8000](http://127.0.0.1:8000).

## Endpoints

### Usuarios
- **GET /users**: Lista todos os usuarios.
- **POST /users**: Cria um novo usuario.
- **GET /users/{id}**: Retorna os detalhes de um usuario específico.
- **PUT /users/{id}**: Atualiza informações de um usuario.
- **DELETE /users/{id}**: Remove um usuario.

### Fornecedores
- **GET /suppliers**: Lista todos os fornecedores.
- **POST /suppliers**: Cria um novo fornecedor.
- **GET /suppliers/{id}**: Retorna os detalhes de um fornecedor específico.
- **PUT /suppliers/{id}**: Atualiza informações de um fornecedor.
- **DELETE /suppliers/{id}**: Remove um fornecedor.

### Pedidos
- **GET /orders**: Lista todos os pedidos.
- **POST /orders**: Cria um novo pedido.
- **GET /orders/{id}**: Retorna os detalhes de um pedido específico.
- **PUT /orders/{id}**: Atualiza informações de um pedido.
- **DELETE /orders/{id}**: Remove um pedido.

### Endereços
- **GET /addresses**: Lista todos os endereços.
- **POST /addresses**: Cria um novo endereço.
- **GET /addresses/{id}**: Retorna os detalhes de um endereço específico.
- **PUT /addresses/{id}**: Atualiza informações de um endereço.
- **DELETE /addresses/{id}**: Remove um endereço.