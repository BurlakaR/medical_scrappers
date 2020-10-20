from selenium import webdriver
import tools


def scrap_one_list(list_parser, list):
    list_parser.get(list)
    tools.waiting_load(list_parser)
    questions = []
    while(True):
        try:
            questions.extend([link.get_attribute('href') for link in list_parser.find_elements_by_xpath('.//li/div/h2/a')])
            next = list_parser.find_element_by_xpath('.//li[contains(@class, "next-page")]/a').get_attribute('href')
            list_parser.get(next)
        except:
            break
    return questions

def scrap_one_page(page_parser, page):
    page_parser.get(page)
    text_div = page_parser.find_element_by_xpath('.//div[contains(@class, "article-show-content")]')
    return text_div.text




options = webdriver.ChromeOptions()
options.add_argument('--headless')
options.add_argument('--window-size=1920,1080')
driver = webdriver.Chrome('./chromedriver', chrome_options=options)
driver.get('https://www.mp.pl/pacjent/')
tools.waiting_load(driver)

links = driver.find_elements_by_xpath('.//ul[contains(@class, "list-unstyled")]/li/a')
links_to_scrap = [link.get_attribute('href') + 'lista' for link in links
                  if 'pacjent' in link.get_attribute('href') and 'leki' not in link.get_attribute('href')]
for list in links_to_scrap:
    flag_list = True
    for i in range(5):
        try:
            questions = scrap_one_list(driver, list)
            flag = False
            break
        except:
            pass
    if flag_list:
        continue
    questions = [q for q in questions if 'pacjent' in q]
    print(list + " : " + str(len(questions)))
    for q in questions:
        flag = True
        text = ''
        for i in range(5):
            try:
                text = scrap_one_page(driver, q)
                flag = False
                break
            except:
                pass
        if flag:
            continue
        name = q[q.rindex('/') + 1:]
        name = str(name).replace('?', '').replace('=', '')
        with open('texts/' + name + '.txt', 'w', encoding='utf-8') as text_file:
            text_file.write(text)




