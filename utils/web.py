from selenium import webdriver
from bs4 import BeautifulSoup
from webdriver_manager import chrome
from webdriver_manager.chrome import ChromeDriverManager
import re
import os

chrome_options = webdriver.ChromeOptions()
chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--no-sandbox")
class Web:
    async def get_google_predictions(request:str)->list:
        """Returns top list of predictions from google search
            Parameters :string containing the search request
            Returns : list [results] """
        req_list = request.split(" ")
        new_req = "+".join(req_list)
        driver = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"),chrome_options=chrome_options)
        results = []
        driver.get(fr"http://google.com/complete/search?output=toolbar&q={new_req}")
        content = driver.page_source
        soup = BeautifulSoup(content)
        for res in soup.findAll('completesuggestion'):
            results.append(re.findall(r'"([^"]*)"', str(res)))
        return results
