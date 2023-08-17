from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import declarative_base, sessionmaker, relationship
from sqlalchemy import Column, Integer, String, update, delete
from sqlalchemy.future import select
from asyncio import run
import os

DATABASE_URL = "sqlite+aiosqlite:///mydatabase.db"
engine = create_async_engine(DATABASE_URL, echo=True)

Base = declarative_base()

async_session = sessionmaker(
    engine,
    expire_on_commit=False,
    future=True,
    class_=AsyncSession
)


class Product(Base):
    __tablename__ = 'product'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    price = Column(String)
    quantity = Column(String)

    def __repr__(self):
        return f'Product(name={self.name}, price={self.price}, quantity={self.quantity})'

    REQUIRED_FIELDS = ['name', 'price']  # Campos obrigatórios

    @classmethod
    async def create(cls, s, **kwargs):

        """
        Cria um novo produto com os itens fornecidos.

        :param s: Sessão do SQLAlchemy.
        :param kwargs: Itens do produto (nome do campo: valor).
        :return: O objeto de produto criado ou mensagem de erro.
        """

        async with async_session() as s:
            missing_fields = [field for field in cls.REQUIRED_FIELDS if field not in kwargs]
            if missing_fields:
                return f"Campos obrigatórios faltando: {', '.join(missing_fields)}"

            new_product = cls(**kwargs)
            s.add(new_product)
            await s.commit()
            print(f'Produto {new_product.name} criado com sucesso!')
            # return new_product

    def update(self, s, **kwargs):
        """
        Atualiza os itens do produto atual.

        :param s: Sessão do SQLAlchemy.
        :param kwargs: Itens a serem atualizados (nome do campo: novo valor).
        """
        for field_name, value in kwargs.items():
            if field_name not in self.__class__.__dict__:
                raise AttributeError(f"'{self.__class__.__name__}' object has no attribute '{field_name}'")

            setattr(self, field_name, value)

        s.commit()

    def delete(self, s):
        """
        Deleta o produto atual.

        :param s: Sessão do SQLAlchemy.
        """
        s.delete(self)
        s.commit()

    @classmethod
    async def filter(cls, s=None, **kwargs):
        """
        Filtra os produtos com base nos parâmetros fornecidos. Retorna todos os produtos se nenhum filtro for especificado.

        :param s: Sessão do SQLAlchemy.
        :param kwargs: Parâmetros de filtro (nome do campo: valor).
        :return: Lista de produtos filtrados ou todos os produtos.
        """
        if s is None:
            async with async_session() as s:
                return await cls._filter(s, **kwargs)
        else:
            return await cls._filter(s, **kwargs)

    @classmethod
    async def _filter(cls, s, **kwargs):
        if not kwargs:
            return await s.execute(select(cls)).scalars().all()

        filters = [getattr(cls, field_name) == value for field_name, value in kwargs.items()]

        query = select(cls).where(*filters)
        result = await s.execute(query).scalars().all()

        return result


# if os.path.exists("banco.db"):
#     print("O arquivo banco.db existe.")
#
# else:
#
#     print("Criando o banco de Dados... ")

async def create_database():

    async with engine.begin() as conn:
        # quando conecta o banco faz.
        # dropo todas as tabelas.
        await conn.run_sync(Base.metadata.drop_all)
        # crio todas as tabelas.
        await conn.run_sync(Base.metadata.create_all)

run(create_database())

print('vamos criar um produto ...')
run(Product.create(async_session, name='café', price='10', quantity='10'))
run(Product.create(async_session, name='mamão', price='10', quantity='10'))

print('vamos listar os produtos ...')


# Use a sessão dentro de um bloco 'with'


async def list_products():
    async with AsyncSession(engine) as session:
        products = await session.execute(select(Product))
        for product in products.scalars():
            print(product)

# Executa a função assíncrona
run(list_products())


