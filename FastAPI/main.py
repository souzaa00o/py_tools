# As dependencias fastapi e uvicorn foram instaladas
# para iniciar a aplicação, subir o ambiente com uvicorn com a linha de comando: "uvicorn main:app --reload"

# FASTAPI

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI() # Iniciando aplicação

# Rota raiz
@app.get("/")
def raiz():
    return{"Ola": "Mundo"}

# Criando a classe usuario
class Usuario(BaseModel): # Um usuario deve ter todos os atributos declarados abaixo
    id: int
    email: str
    senha: str

#Base de dados
data_list = [  # Criando dados para a classe usuario
    Usuario(id=1, email="abc@abc.com.br", senha="123"),
    Usuario(id=2, email="ok@ok.com.br", senha="321"),
]

# Metodo Get todos usuarios

@app.get("/usuarios") # Metodo get no endpoint "/usuarios"
def get_all_users():  # Função do metodo get
    return data_list  # Retorna a lista de dados "data_list" criada acima


# Metodo Get usuario por id

@app.get("/usuarios/{id_usuario}")      # Metodo get no endpoint "/usuarios/{id}", o Id do tipo int é o parametro passado de forma dinamica no endpoint
def get_user_by_id(id_usuario: int):    # Função do metodo get
    for usuario in data_list:           # Laço de repetição dentro da "data_list"
        if(usuario.id == id_usuario):   # Se o "usuario.id" da lista "data_list" for igual a "id_usuario" passado como parametro no endpoint
            return usuario
    return {"Status": 404, "Mensagem": "Usuário não encontrado"}


# Metodo Post inserção de usuario

@app.post("/usuarios")                  # Metodo post no endpoint "/usuarios"
def insert_user(usuario: Usuario):      # Função do metodo post, retorna Usuario
    data_list.append(usuario)           # Add novo usuario ao "data_list"
    return usuario                      # Retorna o usuario criado