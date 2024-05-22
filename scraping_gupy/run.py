from time import time, sleep
import os
import sys
import logging
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'src'))
from dotenv import dotenv_values

from src.config import Browser
from src.pages import SearchPageGupy
from src.config.mongodb import MongoDBConfig
from src.utils.mongodb import MongoDB
from src.utils.helpers import *
from src.config import *

class RunScraping():
    logging.basicConfig(format='%(asctime)s :: %(levelname)s :: %(message)s', level=logging.INFO, datefmt='%d-%m-%y %H:%M:%S', encoding='utf-8')

    def __init__(self) -> None:
        """
            Constrói todos os atributos necessários para o objeto RunScraping.
            
            Args:
                self: Instância da classe.
        """
        self.env = dotenv_values('.env')
        self.driver = Browser()
        self.browser = self.driver.get_browser()
        self.search_page = SearchPageGupy(self.browser)
        self.helpers = Helpers(self.browser)
        self.mongodb = MongoDB(
            MongoDBConfig(
                host=self.env.get('HOST'),
                port=int(self.env.get('PORT')),
                db_name=self.env.get('DB_NAME')
            )
        )
        
    def run(self) -> None:
        """
            Executa os steps do scraping.

            Args:
                self: Instância da classe.

            Returns:
                None
        """
        self.search_page.go_to_search_page()
        logging.info('Navega para a página de pesquisa')

        self.search_page.click_initial_dialog()
        logging.info('Clica no botão "Ok, entendi." do elemento de dialog inicial')

        self.search_page.insert_search_text()
        logging.info('Insere o texto da vaga "Engenheiro de Dados" na barra de pesquisa')

        self.search_page.click_search_button()
        logging.info('Clica no botão pesquisar')

        logging.info('Rolando a página...')
        self.search_page.page_scrolling()
        
        links = self.search_page.get_links_jobs()

        jobs = []

        """
            TODO: Tratar a exceção para links corrompidos.
        """
        logging.info('Extraindo dados...')
        for link in links:
            logging.info(f'Extraindo dados de {link}')

            try:
                jobs.append({
                    'text_job': self.search_page.extract_text_job_page(link),
                    'extraction_date': self.helpers.get_date_now()
                })
            except Exception as e: continue
        
        logging.info('Deletando todos os documentos da collection...')
        self.mongodb.delete_all_documents(collection="aijobs")
        logging.info('Deletou os documentos')

        logging.info('Inserindo no Mongo...')
        self.mongodb.insert_data(collection="aijobs", data=jobs)
        logging.info('Inseriu dados')
       
        sleep(2)
        
if __name__ == '__main__':
    start_time = time()

    run_sc = RunScraping()
    run_sc.run()