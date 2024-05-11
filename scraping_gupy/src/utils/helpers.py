"""
def test_login_form_present(self):
    login_form = wait_for_element(self.driver, (By.ID, 'login-form'))

"""

"""
    Constrói todos os atributos necessários para o objeto ChatPDF

    Args:
        documents_folder (str): Caminho/Pasta com os documentos que serão carregados para conversação no Chat
        vectordb_folder (str): Caminho/Pasta onde ficarão os arquivos do Chroma (Vector DB)
        model_path (str): Caminho/Pasta que aponta para o modelo LLM a ser utilizado
        sentence_embedding_model (str): Nome do modelo de Embedding que será usado para gerar os tokens dos documentos
        temperature (float, optional): Temperatura para calibrar o nível de aleatoriedade das respostas. O padrão é 0.1 (Muito determinístico, pouco aleatório)
"""

from time import sleep
from datetime import datetime

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class Helpers:

    def __init__(self, browser):
        self.browser = browser
    
    def get_data_jobs(self, link_jobs: list) -> None:
        """
            Recebe o título, a descrição e a data de extração dos dados das vagas disponíveis na plataforma.

            Args:
                self: Instância da classe.
                job_element: Elemento <li> contendo o link com o título da vaga.

            Returns:
                dict: Dicionário contendo o título, a descrição da vaga e a data de extração dos dados.
        """

    def get_date_now(self) -> str:
        """
            Retorna a data atual.

            Args:
                self: Instância da classe.

            Returns:
                str: A data atual formatada no padrão dd/mm/aaaa.
        """
        return datetime.now().strftime("%d/%m/%Y")