import aiomysql
from loguru import logger
from .database_config import db_config

class DatabasePool:
    def __init__(self, db_config):
        self.db_config = db_config
        self.pool = None
        self.query_counter = 0

    async def create_pool(self):
        self.pool = await aiomysql.create_pool(**self.db_config)
        if self.pool is None:
            logger.critical("Ошибка создания пула")
        else:
            logger.success(f"Успешно, пул создан: {self.pool}")

    async def close_pool(self):
        if self.pool is None:
            logger.critical("Пул не существует")
            return
        logger.warning(f"Закрытие пула: {self.pool}")
        self.pool.close()
        await self.pool.wait_closed()
        logger.success("Успешно, пул закрыт")

    async def is_closed(self):
        logger.warning("Проверка закрыт ли пул...")
        return self.pool is None
    
    async def execute_query(self, query, params=None):
        if self.pool is None:
            logger.critical("Пул не существует")
            return
        try:
            async with self.pool.acquire() as conn:
                async with conn.cursor() as cur:
                    await cur.execute(query, params)
                    self.query_counter += 1
                    logger.success(f"{self.query_counter}) Успешно, запрос выполнен {query}")
                    return await cur.fetchall()
        except Exception as e:
            logger.error(f"Ошибка выполнения запроса {query}: {e}")
            return None
        
    async def fetchval(self, query, params=None):
        if self.pool is None:
            logger.critical("Пул не существует")
            return
        try:
            async with self.pool.acquire() as conn:
                async with conn.cursor() as cur:
                    await cur.execute(query, params)
                    self.query_counter += 1
                    logger.success(f"{self.query_counter}) Успешно, запрос выполнен {query}")
                    return await cur.fetchone()
        except Exception as e:
            logger.error(f"Ошибка выполнения запроса {query}: {e}")
            return None

db_pool = DatabasePool(db_config)