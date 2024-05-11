import random
import os
import inspect

from selenium import webdriver

CURRENTDIR = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))

class Browser:
    def __init__(self) -> None:
        chrome_options = webdriver.ChromeOptions()
        agents = [
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.129 Safari/537.36 OPR/68.0.3618.63',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.13; rv:63.0) Gecko/20100101 Firefox/63.0',
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36',
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36'
        ]
        agent = agents[random.randint(0, len(agents) - 1)]
        chrome_options.add_argument('user-agent=' + agent)
        chrome_options.add_argument('--start-maximized')
        self.browser = webdriver.Chrome(options=chrome_options)
        
    def get_browser(self): return self.browser

    def close_browser(self) -> None: self.browser.close()