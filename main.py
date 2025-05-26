import json
import os
from typing import Literal, Optional
from uuid import uuid4
from fastapi import FastAPI, HTTPException
import random
from  pydantic import BaseModel
from fastapi.encoders import jsonable_encoder


app = FastAPI() #segue as normas do fastapi

class Book (BaseModel):  # define a classe Book que herda de BaseModel
    title: str  # atributo title do tipo string
    price: float  # atributo price do tipo float
    book_id: Optional[str] = uuid4().hex  #optional -> o usuario nao vai definir o id do livro
    # uuid4 gera um identificador único para o livro
    # book_id é um identificador único do livro, gerado automaticamente
    genre: Literal["fiction", "non-fiction"]



BOOKS_FILE = "books.json"  # arquivo para armazenar os livros

'''
BOOK_DATABASE = [
    "Harry Potter and the Philosopher's Stone",
    "The Hobbit",
    "1984",
    "To Kill a Mockingbird"
] #cria uma lista vazia para armazenar os livros   

'''

BOOK_DATABASE = []  # cria uma lista vazia para armazenar os livros

if os.path.exists(BOOKS_FILE):  # verifica se o arquivo já existe
    with open(BOOKS_FILE, "r") as f:  # abre o arquivo em modo leitura
        BOOK_DATABASE = json.load(f)  # carrega os livros do arquivo JSON para a lista BOOK_DATABASE



'''
@app.get("/") #acessar a função root sempre que acessar a raiz do servidor
async def root():
    return {"message": "Hello World"} #retorna un json com a mensagem Hello World

sempre que criar outra função, tem que dar uma rota para ela'''

#planejamento das rotas
# verbo-o que ele faz
# / -> boas vindas
@app.get("/")  # acessar a função root sempre que acessar a raiz do servidor
async def home():
    return "Welcome to my bookstore"


# /list-books -> listar todos os livros
@app.get("/list-books")
async def list_books():
    return { "books": BOOK_DATABASE }  # retorna um dicionário com a lista de livros
        
# se a api tiver muitos livros, e o usuario quiser ver apenas um, entao criar uma rota que apresente
# informações de um livro especifico de acordo com o identificador desse livro
# /list-book-by-index/{index} -> listar um livro especifico

@app.get("/list-book-by-index/{index}")#parametro de rota entre chaves
async def list_book_by_index(index: int): #define o tipo do parametro como inteiro
    if index < 0 or index >= len(BOOK_DATABASE): 
        raise HTTPException(404, "Index out of range")  # se o index for invalido, retorna erro 404 
    else:
        return { "books": BOOK_DATABASE[index] }


# /get-random-book -> retornar um livro aleatorio
@app.get("/get-random-book")
async def get_random_book():
    return { "book": random.choice(BOOK_DATABASE) } 

# /add-book -> adicionar um livro
@app.post("/add-book")
async def add_book(book: Book):
    book.book_id = uuid4().hex  
    json_book = jsonable_encoder(book)  # converte o objeto Book para um dicionário JSON
    BOOK_DATABASE.append(json_book)  # adiciona o livro convertido à lista BOOK_DATABASE
    
    with open(BOOKS_FILE, "w") as f:
        json.dump(BOOK_DATABASE, f)# salva a lista atualizada de livros no arquivo JSON
    # adiciona o livro à lista BOOK_DATABASE e salva no arquivo JSON
    return { "message": f"Book '{book}' added successfully." }

#get - usado para obter informações