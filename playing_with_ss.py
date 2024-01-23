from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from PIL import Image

def capture_screenshot(url):
    # Set up the Selenium webdriver
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--blink-settings=imagesEnabled=false")  # Disable images loading
    driver = webdriver.Chrome(options=chrome_options)

    driver.get(url)

    # Wait for the page to be ready
    print("Waiting for the page to be ready...")
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.TAG_NAME, 'body'))
    )
    print("Page is ready!")

    # Extract post ID from the URL
    post_id = url.split('/')[6]  # Assuming the post ID is the 6th part of url

    # Construct the post title selector
    post_title_selector = f'div#t3_{post_id}'

    # Try switching to iframe if present
    try:
        driver.switch_to.frame('iframe_name_or_id')
    except NoSuchElementException:
        pass

    # Wait for the element to be visible
    WebDriverWait(driver, 20).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, post_title_selector))
    )

    # Capture the screenshot of the post title element
    post_title_element = driver.find_element(By.CSS_SELECTOR, post_title_selector)
    post_title_screenshot = capture_element_screenshot(post_title_element)

    # Close the browser
    driver.quit()

    return post_title_screenshot

def capture_element_screenshot(element):
    # Get the location and size of the element
    location = element.location
    size = element.size

    # Capture the screenshot of the element
    screenshot = Image.open("screenshot.png")
    screenshot = screenshot.crop((location['x'], location['y'], location['x'] + size['width'], location['y'] + size['height']))

    return screenshot

# Example usage
url = 'https://www.reddit.com/r/AskReddit/comments/195ydoi/what_common_product_has_a_feature_youre_not_sure/'

post_title_screenshot = capture_screenshot(url)

# Save the screenshot
post_title_screenshot.save('post_title_screenshot.png')


# Save the screenshot
# post_title_screenshot.save('post_title_screenshot.png')


# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from bs4 import BeautifulSoup
# from PIL import Image

# def capture_screenshot(url, comment_ids):
#     # Set up the Selenium webdriver
#     driver = webdriver.Chrome()
#     driver.get(url)

#     # Wait for the page to load
#     driver.implicitly_wait(10)

#     # Get the post title
#     post_title_element = driver.find_element(By.CSS_SELECTOR, 'div[data-test-id="post-content"]')
#     post_title_screenshot = capture_element_screenshot(post_title_element)

#     # Get the comments
#     comment_screenshots = []
#     for comment_id in comment_ids:
#         comment_selector = f'div#t1_{comment_id}'
#         comment_element = driver.find_element(By.CSS_SELECTOR, comment_selector)
#         comment_screenshots.append(capture_element_screenshot(comment_element))

#     # Close the browser
#     driver.quit()

#     return post_title_screenshot, comment_screenshots

# def capture_element_screenshot(element):
#     # Get the location and size of the element
#     location = element.location
#     size = element.size

#     # Capture the screenshot of the element
#     screenshot = Image.open("screenshot.png")
#     screenshot = screenshot.crop((location['x'], location['y'], location['x'] + size['width'], location['y'] + size['height']))

#     return screenshot

# # Example usage
# url = 'https://www.reddit.com/r/AskReddit/comments/195ydoi/what_common_product_has_a_feature_youre_not_sure/'
# comment_ids = ['khqyud8', 'khr5sav', 'khqnaqk', 'khqh43a']  # Replace with your actual comment ids
# post_title_screenshot, comment_screenshots = capture_screenshot(url, comment_ids)

# # Save the screenshots
# post_title_screenshot.save('post_title_screenshot.png')
# for i, comment_screenshot in enumerate(comment_screenshots):
#     comment_screenshot.save(f'comment_{i+1}_screenshot.png')
