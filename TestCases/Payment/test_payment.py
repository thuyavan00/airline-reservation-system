from selenium import webdriver
from selenium.webdriver.common.by import By
import pytest

@pytest.fixture()
def env_setup():
    global driver
    options = webdriver.ChromeOptions()
    options.add_experimental_option("detach", True)
    driver = webdriver.Chrome(options=options, executable_path="path/to/executable")
    driver.get("http://127.0.0.1:5000/paymentroute")
    driver.maximize_window()
    yield
    driver.close()
#TC_ARS_Payment_001
def test_verify_payment_001(env_setup):
    driver.find_element(By.NAME, "firstname").send_keys("")
    driver.find_element(By.NAME, "email").send_keys("")
    driver.find_element(By.NAME, "address").send_keys("")
    driver.find_element(By.NAME, "city").send_keys("")
    driver.find_element(By.NAME, "pro").send_keys("")
    driver.find_element(By.NAME, "zcode").send_keys("")
    driver.find_element(By.NAME, "cardname").send_keys("")
    driver.find_element(By.NAME, "cardnumber").send_keys("")
    driver.find_element(By.NAME, "expmonth").send_keys("")
    driver.find_element(By.NAME, "expyear").send_keys("")
    driver.find_element(By.NAME, "cvv").send_keys("")
    driver.find_element(By.NAME, "expmonth").send_keys("")
    alert = driver.switch_to.alert
    text = alert.text
    alert.accept()
    print(text)
    driver.back()
#TC_ARS_Payment_002
def test_verify_payment_002(env_setup):
    driver.find_element(By.NAME, "firstname").send_keys("Ajay")
    driver.find_element(By.NAME, "email").send_keys("g.ajaygg@gmail.com")
    driver.find_element(By.NAME, "address").send_keys("Western University")
    driver.find_element(By.NAME, "city").send_keys("London")
    driver.find_element(By.NAME, "pro").send_keys("Ontario")
    driver.find_element(By.NAME, "zcode").send_keys("673j8")
    driver.find_element(By.NAME, "cardname").send_keys("Tester")
    driver.find_element(By.NAME, "cardnumber").send_keys("11112222")
    driver.find_element(By.NAME, "expmonth").send_keys("November")
    driver.find_element(By.NAME, "expyear").send_keys("2024")
    driver.find_element(By.NAME, "cvv").send_keys("456")
    driver.find_element(By.NAME, "expmonth").send_keys("November")
    alert = driver.switch_to.alert
    text = alert.text
    alert.accept()
    print(text)
    driver.back()
#TC_ARS_Payment_003
def test_verify_payment_003(env_setup):
    driver.find_element(By.NAME, "firstname").send_keys("Ajay")
    driver.find_element(By.NAME, "email").send_keys("g.ajayggmail.com")
    driver.find_element(By.NAME, "address").send_keys("Western University")
    driver.find_element(By.NAME, "city").send_keys("London")
    driver.find_element(By.NAME, "pro").send_keys("Ontario")
    driver.find_element(By.NAME, "zcode").send_keys("673j8")
    driver.find_element(By.NAME, "cardname").send_keys("Tester")
    driver.find_element(By.NAME, "cardnumber").send_keys("1111222233334444")
    driver.find_element(By.NAME, "expmonth").send_keys("November")
    driver.find_element(By.NAME, "expyear").send_keys("2024")
    driver.find_element(By.NAME, "cvv").send_keys("456")
    driver.find_element(By.NAME, "expmonth").send_keys("November")
    alert = driver.switch_to.alert
    text = alert.text
    alert.accept()
    print(text)
    driver.back()
#TC_ARS_Payment_004
def test_verify_payment_004(env_setup):
    driver.find_element(By.NAME, "firstname").send_keys("Ajay")
    driver.find_element(By.NAME, "email").send_keys("g.ajaygg@gmail.com")
    driver.find_element(By.NAME, "address").send_keys("Western University")
    driver.find_element(By.NAME, "city").send_keys("London")
    driver.find_element(By.NAME, "pro").send_keys("Ontario")
    driver.find_element(By.NAME, "zcode").send_keys("673j8")
    driver.find_element(By.NAME, "cardname").send_keys("Tester")
    driver.find_element(By.NAME, "cardnumber").send_keys("1111222233334444")
    driver.find_element(By.NAME, "expmonth").send_keys("November")
    driver.find_element(By.NAME, "expyear").send_keys("2024")
    driver.find_element(By.NAME, "cvv").send_keys("456")
    driver.find_element(By.NAME, "expmonth").send_keys("November")
    driver.back()
#check the url
    assert driver.current_url == "http://127.0.0.1:5000/paymentroute"
