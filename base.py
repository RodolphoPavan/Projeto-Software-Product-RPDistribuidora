import os

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import declarative_base, sessionmaker, relationship
from sqlalchemy import Column, Integer, String, update, delete, ForeignKey
from sqlalchemy.future import select

from asyncio import run

url_do_banco = 'sqlite+aiosqlite:///banco.db'

engine = create_async_engine(url_do_banco)

Base = declarative_base()

session = sessionmaker(
    engine,
    expire_on_commit=False,
    future=True,
    class_=AsyncSession
)


class Pessoa(Base):
    __tablename__ = 'pessoa'

    id = Column(Integer, primary_key=True)
    nome = Column(String)
    email = Column(String)
    posts = relationship('Post', backref='pessoa')

    def __repr__(self):
        return f'Pessoa(nome={self.nome}, email={self.email})'
    

class Post(Base):
    __tablename__ = 'post'

    id = Column(Integer, primary_key=True)
    titulo = Column(String)
    conteudo = Column(String)
    autor_id = Column(Integer, ForeignKey('pessoa.id'))
    autor = relationship('Pessoa', backref='post')

    def __repr__(self):
        return f'Post(titulo={self.titulo}, conteudo={self.conteudo})'


async def create_database():

    async with engine.begin() as conn:
        # quando conecta o banco faz.
        # dropo todas as tabelas.
        await conn.run_sync(Base.metadata.drop_all)
        # crio todas as tabelas.
        await conn.run_sync(Base.metadata.create_all)


async def criar_pessoa(nome, email):

    async with session() as s:
        # passa para o banco o que vai ser salvo.
        pessoa = Pessoa(nome=nome, email=email)
        s.add(pessoa)
        s.add(Post(titulo='titulo', conteudo='conteudo', autor=pessoa))
        # salva no banco e o AWAIT é para esperar o banco salvar.
        await s.commit()


async def listar_pessoas():
    async with session() as s:
        # select para listar todas as pessoas.
        query = select(Pessoa)
        # executa o select.
        result = await s.execute(query)
        # retorna todas as pessoas.
        return result.scalars().all()


async def buscar_pessoa(nome):
    async with session() as s:
        # executor da query.
        query = await s.execute(
            # construtor da query
            select(Pessoa).where(Pessoa.nome == nome)
        )
        return query.scalars().all()

# o buscar_pessoa e o listar_pessoas são a mesma coisa, só muda o where.


async def alterar_nome(nome_antigo, nome_novo):
    async with session() as s:
        await s.execute(
            # construtor da query
            update(Pessoa).where(Pessoa.nome == nome_antigo).values(nome=nome_novo)
        )
        await s.commit()


async def deletar_pessoa(nome):
    async with session() as s:
        await s.execute(
            # construtor da query
            delete(Pessoa).where(Pessoa.nome == nome)
        )
        await s.commit()


async def buscar_post_por_autor(nome):
    async with session() as s:
        query = await s.execute(
            select(Post).join(Pessoa).where(Pessoa.nome == nome)
        )
        return query.scalars().all()

# Verificar se o arquivo "banco.db" existe

if os.path.exists("banco.db"):
    # Fazer algo se o arquivo existe

    print("O arquivo banco.db existe.")

    # print(run(listar_pessoas()))
    # print(run(buscar_pessoa('cesar')))

else:
    print("Criando o banco de Dados... ")
    run(create_database())
    print("Populando o banco... ")
    run(criar_pessoa('Cesar', 'cesar@live.com'))
    run(criar_pessoa('Rodolfo', 'rodolfo@live.com'))
    run(criar_pessoa('valeria', 'valeria@live.com'))



