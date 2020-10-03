from selenium import webdriver
import tools


def one_page_scrap(parser, url):
    parser.get(url)
    tools.waiting_load(parser)
    question = parser.find_element_by_xpath('//div[contains(@class, "question-problem__describe")]')
    text = question.text
    answers = parser.find_elements_by_xpath('//div[contains(@class, "question-answer__content")]]')
    for answer in answers:
        text += answer.text
    print(text)
    return text


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
    links = [question.find_element_by_xpath('.//a').get_attribute('href') for question in questions]
    print(links)
    for link in links:
        one_page_scrap(driver, link)

    next = (driver.find_elements_by_class_name('pagination__item'))[-1]
    try:
        next_link = next.find_element_by_xpath('.//a')
    except:
        break
    driver.get(next_link.get_attribute('href'))
    tools.waiting_load(driver)



