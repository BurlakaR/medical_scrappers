from selenium import webdriver
import tools

driver = webdriver.Chrome('chromedriver.exe')
driver.get('https://pytania.abczdrowie.pl/pytania-do-specjalistow')
tools.waiting_load(driver)

buttons = driver.find_elements_by_xpath('.//button')
for button in buttons:
    if 'AKCEPTUJĘ' in button.text:
        button.click()

while True:
    questions = driver.find_elements_by_class_name('questions-results__item')
    print(len(questions))

    next = (driver.find_elements_by_class_name('pagination__item'))[-1]
    try:
        next_link = next.find_element_by_xpath('.//a')
    except:
        break
    driver.get(next_link.get_attribute('href'))
    tools.waiting_load(driver)


