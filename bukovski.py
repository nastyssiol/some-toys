from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time
import csv

login = 'ikgremlin@gmail.com'
password = 'abc123'

parse_urls = ['https://bukowski.se/product-category/teddy-bears/', 'https://bukowski.se/product-category/baby-items', 'https://bukowski.se/product-category/bunnies/',
'https://bukowski.se/product-category/other-animals/', 'https://bukowski.se/product-category/dolls-2/', 'https://bukowski.se/product-category/news',
'https://bukowski.se/product-category/accessories-2/', 'https://bukowski.se/product-category/discount-corner/']
driver = webdriver.Firefox()

driver.get('https://bukowski.se/sign-in/')
login_input = driver.find_element(By.ID, 'sign-in-email').send_keys(login)
password_input = driver.find_element(By.ID, 'sign-in-pass').send_keys(password)
log_in_btn = driver.find_element(By.XPATH, '/html/body/div[1]/main/form/input[1]').click()
while True:
    try:
        login_input = driver.find_element(By.ID, 'user_login').send_keys(login)
        password_input = driver.find_element(By.ID, 'user_pass').send_keys(password)
        log_in_btn = driver.find_element(By.ID, 'wp-submit').click()
        break
    except:
        time.sleep(2)

def save_csv(items):
        with open('bukowski.csv', 'a', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            for item in items:
                writer.writerow([item[0], item[1], item[2], item[3], item[4]])

def parse(driver, urls):
    data=[]
    for i, url in enumerate(urls):
        driver.get(url)
        cards = driver.find_elements(By.CLASS_NAME,'shop-main__product')
        header = driver.find_element(By.CLASS_NAME, 'shop-main__products__header').text
        for card in cards:
            img_url = card.find_element(By.CLASS_NAME, 'shop-main__product__img').get_attribute('data-src')
            card_id = card.get_attribute('data-id')
            card_name = card.find_element(By.CLASS_NAME, 'shop-main__product__title').text
            card_price = card.find_element(By.CLASS_NAME, 'woocommerce-Price-amount').text
            if i == (len(urls)-1):
                card_price = card.find_element(By.CLASS_NAME, 'current-product-price').text
                card_price = card_price.split()[0]
            data.append([header,img_url, card_id, card_name, card_price])
            print(img_url, card_id, card_name, card_price)
            print(data)
    return(data)


data = parse(driver, parse_urls)
save_csv(data)

