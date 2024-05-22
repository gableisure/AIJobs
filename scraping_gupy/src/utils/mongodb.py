from pymongo import MongoClient
from src.config.mongodb import MongoDBConfig

class MongoDB:
    def __init__(self, config: MongoDBConfig):
        """
            Constrói todos os atributos necessários para o objeto MongoDB.

            Args:
                self: Instância da classe.
                config (MongoDBConfig): Instância da classe MongoDBConfig contendo as configurações do banco.
        """
        self.config = config
        self.client = MongoClient(config.host, config.port)
        self.db = self.client[config.db_name]

    def insert_data(self, collection: str, data: dict) -> None:
        """
            Insere um dado no banco de dados.

            Args:
                collection: Nome da coleção.
                data: Um dicionário contendo os dados a serem inseridos no banco de dados.

            Returns:
                dict: Dicionário contendo os dados a serem inseridos no banco de dados.
        """
        collection = self.db[collection] # Seleciona a collection
        collection.insert_many(data) # Insere os dados

    def delete_all_documents(self, collection: str) -> None:
        """
            Deleta todos os documentos de uma colletion.

            Args:
                collection: Nome da colletion.

            Returns:
                None
        """
        self.db[collection].delete_many({}) # Deleta todos os documentos existentes antes de inserir os novos
