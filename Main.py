from selenium import webdriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


def try_pass(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception:
            print(f"Erro na função: {func.__name__}")
    return wrapper

@try_pass
def carregou_elemento(driver:webdriver.Chrome, css_selecor:str, time_out=10) -> WebElement:
    element = WebDriverWait(driver, time_out).until(
        EC.presence_of_element_located(
            (By.CSS_SELECTOR, css_selecor)
        )
    )
    return element


LINK = "https://www.canalrural.com.br/agricultura/page/"

SELECTOR = {
    "noticia": "body > main",
}

ARQUIVO = "agro.txt"

if __name__ == "__main__":
    chrome_options = Options()
    chrome_options.add_argument("--headless=new")
    service = Service(ChromeDriverManager().install())

    driver = webdriver.Chrome(service=service, options=chrome_options)
    driver.maximize_window()

    i = 1

    with open(ARQUIVO, "a", encoding="utf-8") as f:
        while True:
            driver.get(f'{LINK}{i}/')
            try:
                if i == 1:
                    final = -7-i
                elif i <= 5:
                    final = -7-i-1
                else:
                    final = -12
                content_raw = carregou_elemento(driver, SELECTOR["noticia"], time_out=5).text.split("\n")
                content = '\n'.join(content_raw[5:final])
                print(content)

                f.write(f"=== Página {i} ===\n"+content+"\n")
                i +=1
            except:
                break