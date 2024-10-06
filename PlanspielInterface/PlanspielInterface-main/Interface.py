from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.support import expected_conditions as EC
import time
import json
import schedule

driver = webdriver.Chrome()
driver.implicitly_wait(0.5)

#global variables
loggedIn = False
totalCapitalInt = 0
print(__name__)


class PlanspielInterface:
    
    def __init__(self, username, password):
        self.username = username
        self.password = password

    def login(self): 
        try: 
            driver.get("https://trading.planspiel-boerse.de/web/auth/login")
            driver.implicitly_wait(3)
            usernameField = driver.find_element(By.XPATH, "/html/body/app-root/app-authentication/div/div/div[2]/app-login/div/form/div[1]/input")
            usernameField.send_keys(self.username)
            usernameField.send_keys(Keys.RETURN)
            passwordField = driver.find_element(By.CSS_SELECTOR, "#password")
            passwordField.send_keys(self.password)
            passwordField.send_keys(Keys.RETURN)
            loginButton = driver.find_element(By.XPATH, "/html/body/app-root/app-authentication/div/div/div[2]/app-login/div/form/div[4]/button")
            loginButton.click()
            driver.implicitly_wait(7)
            loggedIn = True
            depotButton = driver.find_element(By.XPATH, "/html/body/app-root/app-home/app-dashboard/app-main/div[1]/div/div/div/div[2]/button")
            depotButton.click()
            driver.implicitly_wait(5)
            totalCapital = WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".flex-lg-row > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > div:nth-child(3) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > p:nth-child(1)"))).get_attribute("textContent")
            print(totalCapital)
            print(type(totalCapital))
            totalCapitalString = totalCapital.replace(" ", "").replace(".", "").replace(",", "").replace("€", "")
            totalCapitalString = totalCapitalString[:-2]
            print(totalCapitalString)
            totalCapitalInt = int(totalCapitalString)
        except Exception as e:
            print("Error: ", e)

    def readCapital(self):
        try: 
            self.navigateDepot()
            driver.save_screenshot("debug_screenshot.png")
            driver.implicitly_wait(5)
            
            # Locate all elements with the specified class name
            elements = driver.find_elements(By.CSS_SELECTOR, "p.mb-0.card-text-primary")
            
            for element in elements:
                print("Element: ", element.text)
            totalCapital = elements[2].text
            print(f'Total Capital: {totalCapital}')
            print(type(totalCapital))
            totalCapitalString = totalCapital.replace(" ", "").replace(".", "").replace(",", "").replace("€", "")
            totalCapitalString = totalCapitalString[:-2]
            print(totalCapitalString)
            totalCapitalInt = int(totalCapitalString)
            print("Total Capital: ", totalCapitalInt)
        except Exception as e:
            print("Error when reading total capital: ", e)
        
    
    def readHoldedStocks(self):
        pass
        
        
    def navigateHome(self):
        driver.get("https://trading.planspiel-boerse.de/")
        driver.implicitly_wait(5)
        
        
    def navigateDepot(self):
        depot_url = "https://trading.planspiel-boerse.de/web/account/depot/portfolio"
        driver.get(depot_url)
        driver.implicitly_wait(5)
        
        
    def read_row_by_id(self, table_id, row_id):
        # Find the table by its ID
        table = driver.find_element(By.ID, table_id)
        
        # Find the specific row by its ID within the table
        row = table.find_element(By.ID, row_id)
        
        # Get all cells in the row
        cells = row.find_elements(By.TAG_NAME, "td")
        
        # Extract and return the text from each cell
        return [cell.text for cell in cells]
        
    
interface = PlanspielInterface(username="timon.h", password="Golfen_09")
interface.login()
interface.readCapital()
interface.readHoldedStocks()
interface.navigateHome()
#schedule.every(1).minutes.do(readCapital)

#while True:
 #   schedule.run_pending()
  #  time.sleep(1)
