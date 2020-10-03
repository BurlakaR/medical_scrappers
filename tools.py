import time


def waiting_load(driver):
    old_page = driver.page_source
    while True:
        time.sleep(1)
        new_page = driver.page_source
        if new_page != old_page:
            old_page = new_page
        else:
            break
    return True