import os
import motor.motor_asyncio
from pymongo.database import Database
from typing import Optional


class MongoDBClient:
    """Cliente para conexión con MongoDB."""

    _client: Optional[motor.motor_asyncio.AsyncIOMotorClient] = None
    _db: Optional[Database] = None

    @classmethod
    async def connect(cls, connection_string: str = None, db_name: str = None) -> Database:
        """
        Conecta con la base de datos MongoDB.

        Args:
            connection_string: URI de conexión a MongoDB
            db_name: Nombre de la base de datos

        Returns:
            Instancia de la base de datos
        """
        if cls._client is None:
            # Usar variables de entorno si no se proporcionan parámetros
            conn_str = connection_string or os.getenv("MONGODB_URI", "mongodb://localhost:27017")
            database = db_name or os.getenv("MONGODB_DATABASE", "olivia")

            cls._client = motor.motor_asyncio.AsyncIOMotorClient(conn_str)
            cls._db = cls._client[database]

        return cls._db

    @classmethod
    async def disconnect(cls) -> None:
        """Cierra la conexión con MongoDB."""
        if cls._client:
            cls._client.close()
            cls._client = None
            cls._db = None

    @classmethod
    async def get_database(cls) -> Database:
        """
        Obtiene la instancia de la base de datos.

        Returns:
            Instancia de la base de datos

        Raises:
            ValueError: Si no hay conexión establecida
        """
        if cls._db is None:
            await cls.connect()

        return cls._db