import os

from selenium import webdriver
import tools


def one_page_scrap(parser, url):
    parser.get(url)
    tools.waiting_load(parser)
    question = parser.find_element_by_xpath('//div[contains(@class, "question-problem__describe")]')
    text = question.text
    answers = parser.find_elements_by_xpath('//div[contains(@class, "question-answer__content")]')
    for answer in answers:
        text += '\n@\n' + answer.text
    lines = text.split("\n")
    non_empty_lines = [line for line in lines if line.strip() != ""]
    string_without_empty_lines = ""
    for line in non_empty_lines:
        string_without_empty_lines += line + "\n"
    return string_without_empty_lines

options = webdriver.ChromeOptions()
chrome_prefs = {}
options.experimental_options["prefs"] = chrome_prefs
chrome_prefs["profile.default_content_settings"] = {"images": 2}
chrome_prefs["profile.managed_default_content_settings"] = {"images": 2}
options.add_argument('--headless')
options.add_argument('--window-size=1920,1080')
driver = webdriver.Chrome('./chromedriver', chrome_options=options)
driver.get('https://pytania.abczdrowie.pl/pytania-do-specjalistow')
tools.waiting_load(driver)

buttons = driver.find_elements_by_xpath('.//button')
for button in buttons:
    if 'AKCEPTUJĘ' in button.text:
        button.click()

oldquestions = [f.replace('.txt', '') for f in os.listdir('./texts')]
while True:
    questions = driver.find_elements_by_class_name('questions-results__item')
    print(len(questions))
    links = [question.find_element_by_xpath('.//a').get_attribute('href') for question in questions]
    links = [link for link in links if not any(old in link for old in oldquestions)]
    print(links)
    current_page = driver.current_url
    for link in links:
        name = link[link.rindex('/')+1:]
        with open('texts/' + name + '.txt', 'w', encoding='utf-8') as text_file:
            text = one_page_scrap(driver, link)
            if text is not '':
                text_file.write(text)
    driver.get(current_page)
    tools.waiting_load(driver)
    nextPage = (driver.find_elements_by_class_name('pagination__item'))[-1]
    try:
        next_link = nextPage.find_element_by_xpath('.//a')
    except:
        break
    driver.get(next_link.get_attribute('href'))
    tools.waiting_load(driver)



