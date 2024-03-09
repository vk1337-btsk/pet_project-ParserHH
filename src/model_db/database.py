from config import settings
from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.orm import sessionmaker
from abc import ABC


class DataBase(ABC):
    """Это класс для получения основных объектов БД"""

    def __init__(self):
        self.url_sync = settings.database_url_psycopg
        self.url_async = settings.database_url_asyncpg

        # Создаём обычный движок
        self.sync_engine = create_engine(
            url=self.url_sync,
            echo=False,  # Вывод логов в консоль
            pool_size=3,  # Максимальное количество соединений
            max_overflow=5  # Дополнительные подключения (сверх)
        )

        # Создаём асинхронный движок
        self.async_engine = create_async_engine(
            url=self.url_async,
            echo=True,          # Вывод логов в консоль
            pool_size=3,        # Максимальное количество соединений
            max_overflow=5      # Дополнительные подключения (сверх)
        )

        self.session_factory = sessionmaker(self.sync_engine)
        self.async_session_factory = async_sessionmaker(self.async_engine)
