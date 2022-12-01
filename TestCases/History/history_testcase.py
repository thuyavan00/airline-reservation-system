from selenium.webdriver import Chrome
from selenium import webdriver
import time

from selenium.webdriver.common.by import By
import pytest

@pytest.fixture()
def env_setup():
    global driver
    options = webdriver.ChromeOptions()
    options.add_experimental_option("detach", True)
    driver = webdriver.Chrome(options=options)
    driver.get("http://127.0.0.1:5000/login")
    driver.maximize_window()
    yield
    driver.close()
    
#TC_ARS_history_001
def test_verify_history_001(env_setup):
    driver.find_element(By.NAME, "username").send_keys("tk")
    driver.find_element(By.NAME, "password").send_keys("qwerty")
    driver.find_element(By.ID, "logbut").click()
    driver.get("http://127.0.0.1:5000/history")
    driver.find_element(By.ID, "UDlfPSgkVa9HbFM0SB0z").click()
    time.sleep(5)
    driver.back()


