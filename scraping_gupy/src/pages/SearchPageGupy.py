import re
from time import sleep
import logging

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

from src.utils.helpers import *

class SearchPageGupy:
    logging.basicConfig(format='%(asctime)s :: %(levelname)s :: %(message)s', level=logging.INFO, datefmt='%d-%m-%y %H:%M:%S', encoding='utf-8')
    URL_SEARCH_PAGE_GUPY = 'https://portal.gupy.io/'

    def __init__(self, browser):
        self.browser = browser
        self.helpers = Helpers(self.browser)
        self.jobs_text = []

    def go_to_search_page(self):
        # Navega para a página de pesquisa de vagas de emprego da Gupy
        self.browser.get(SearchPageGupy.URL_SEARCH_PAGE_GUPY)

    def click_initial_dialog(self):
        # Clica no botão "Ok, entendi." do elemento de dialog inicial
        WebDriverWait(self.browser, 10).until(EC.presence_of_element_located((By.XPATH, '//button[text()="Ok, entendi."]'))).click()
        
    def insert_search_text(self):
        # Insere o texto da vaga "Engenheiro de Dados" na barra de pesquisa
        input_search_job = WebDriverWait(self.browser, 10).until(EC.presence_of_element_located((By.XPATH, '//input[@aria-label="Buscar vaga"]')))
        input_search_job.send_keys('Engenheiro de Dados')

    def click_search_button(self):
        WebDriverWait(self.browser, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="undefined-button"]'))).click()


    def page_scrolling(self) -> None:
        """
            Rola a página até o final para carregar todos os elementos.

            Realiza o scroll na página até o final, aguarda o carregamento de novos elementos
            e atualiza a altura da página até que não haja mais alterações.

            Args:
                None

            Returns:
                None
        """
        last_height = self.browser.execute_script("return document.body.scrollHeight")

        while True:
            # Rola a página para baixo
            self.browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")

            # Aguarda até que novos elementos sejam carregados
            WebDriverWait(self.browser, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'sc-1cba52f7-1')))

            sleep(2)

            # Obtém a nova altura da página
            new_height = self.browser.execute_script("return document.body.scrollHeight")

            # Verifica se a altura da página mudou
            if new_height == last_height: break # Se a altura da página não mudou, pare de rolar

            # Atualiza a altura anterior da página
            last_height = new_height

    def get_links_jobs(self) -> list:
        """
            Retorna uma lista com todos os links das vagas retornadas na busca.

            Args:
                self: Instância da classe.

            Returns:
                list: Lista contendo todos os links das vagas retornadas na busca.
        """
        # Encontra todos os elementos <a> com os links das vagas
        a_elements = self.browser.find_elements(By.CLASS_NAME, 'sc-1cba52f7-1')
        
        # Itera sobre as tags <a> e extrai o atributo "href" com o link da vaga
        return [a_element.get_attribute('href') for a_element in a_elements]
    
    def extract_text_job_page(self, link_job: str) -> str:
        """
            description.

            Args:
                self: description.

            Returns:
                type: description.
        """
        self.browser.get(link_job)

        WebDriverWait(self.browser, 30).until(EC.presence_of_element_located((By.XPATH, "//main[@id='main']")))
        main = self.browser.find_element(By.XPATH, "//main[@id='main']")
        
        return main.text

