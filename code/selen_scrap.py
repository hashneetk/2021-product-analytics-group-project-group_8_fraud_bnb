from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import os


def get_driver():
    '''
    Create headless chrome driver.
    
    Returns
    -------
    chrome driver
    '''
    chrome_options = Options()
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--headless")
    driver = webdriver.Chrome(os.environ['CHROMEDRIVER_PATH'],options=chrome_options)
    # options = webdriver.ChromeOptions()
    # options.add_argument('headless')

    # return webdriver.Chrome(os.environ['CHROMEDRIVER_PATH'], options=options)
    return driver

def get_info(url, waiting_time=3, max_review=10):
    '''Return page info of the given page.

    Paramters
    ---------
    url : string
        The url to the page you want to scrap.
    waiting_time : float or int, optional.
        The time to wait for a page to load after pinging it. Default 3 sec.
    max_review : int, optional.
        The number of review to return for a listing. Default 10.    
    
    Returns
    -------
    result : dict
        A dictionary with the following info:
            - listing_name (str): name of the listing.
            - beds (list of str): description of the number of bed in each room.
            - host_name (str) : name of the host.
            - description (str) : short description of the listing.
            - rating (float) : rating.
            - review_ct (int) : total number of reviews available.
            - reviews (list of list of str :P ) : the reviews.
    '''
    driver = get_driver()

    driver.get(url)
    time.sleep(waiting_time)

    description_url = url + '&modal=DESCRIPTION'

    _svr7sj = driver.find_elements_by_css_selector('div._svr7sj')
    
    while len(_svr7sj) < 6:
        driver.execute_script("arguments[0].scrollIntoView();", _svr7sj[-1])
        _svr7sj = driver.find_elements_by_css_selector('div._svr7sj')

    result = {
        'listing_name': driver.find_element_by_css_selector('h1').text,
        'beds': [room.text for room in driver.find_elements_by_css_selector('div._9342og')],
        'host_name': _svr7sj[5].text,
    }

    driver.get(description_url)
    time.sleep(waiting_time)

    result['description'] = driver.find_element_by_css_selector('div._15pb00k').text

    review_url = driver.find_element_by_css_selector('div._19qg1ru a').get_attribute('href')
    driver.get(review_url)
    time.sleep(waiting_time)

    rating, review_ct = driver.find_elements_by_css_selector('h2._14i3z6h')[-1].text.split(' (')

    result['rating'] = float(rating)
    result['review_ct'] = int(review_ct.split(' ')[0])

    reviews_elements = driver.find_elements_by_css_selector('div._1gjypya')

    while len(reviews_elements) < max_review:
        driver.execute_script("arguments[0].scrollIntoView();", reviews_elements[-1])
        reviews_elements = driver.find_elements_by_css_selector('div._1gjypya')

    result['reviews'] = [ele.text.split('\n') for ele in reviews_elements[:max_review]]

    driver.close()

    return result
