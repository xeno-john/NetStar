# this script creates 5 users

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

users = ["xenojohn", "remusK", "franzzie", "frederich", "varuuCiucas"]
emails = ["saltyjohn31@gmail.com", "remusromulus@yahoo.com", "franzkafka@outlook.com", "nietzsche.fr@gmail.com",
          "varusandel@gmail.com"]
passwords = ["passw1", "passw2", "passw3", "passw4", "passw5"]

driver = webdriver.Chrome()

if __name__ == "__main__":
    for i in range(5):
        driver.get("localhost:5000/register")
        driver.find_element_by_xpath("/html/body/div/form/div[1]/input").send_keys(emails[i])
        driver.find_element_by_xpath("/html/body/div/form/div[2]/input").send_keys(users[i])
        driver.find_element_by_xpath("/html/body/div/form/div[3]/input").send_keys(passwords[i])
        WebDriverWait(driver, 1).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div/form/div[4]/input"))).click()
    driver.quit()

