from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from imgChopper import cropper

def capture_element_screenshot(url, class_name, class_name2, output_file):
    # Configure Chrome options
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--window-size=1920x1080')
    
    proxy = 'http://muralimanas30:IamMurali591_@unblock.oxylabs.io:60000'
    
    
    
    chrome_options.add_argument(f"--proxy-server={proxy}")

    # Initialize Chrome WebDriver using webdriver-manager
    # driver_path = 'PROJECT\ChromeDriver\chromedriver.exe'
    driver = webdriver.Chrome(
                            #    service=Service('./chrome/chrome.exe'),
                               options=chrome_options
                              )
    # driver.get("https://www.youtube.com")
    try:
        # Load the URL in the WebDriver
        driver.get(url)

        # Find the element to capture the screenshot
        try:
            element = driver.find_element(By.CSS_SELECTOR, f'.{class_name2}')
        except:
            element = driver.find_element(By.XPATH, '//*[@class="HO1dRb xsbJxZ"]')

        # Scroll to the element's position and capture the screenshot
        y_position = element.location['y']
        x_position = element.location['x']
        driver.execute_script(f"window.scrollTo({x_position-200}, {y_position - 400});")
        driver.save_screenshot(output_file)
        final_addr = cropper()

        print(f"Screenshot saved to {final_addr}")

    except Exception as e:
        print(f"An error occurred: {e}")
        # Retry capturing the screenshot from the alternative URL.
 
        driver2 = webdriver.Chrome(
            # service=Service('./chrome/chrome.exe'),
            options=chrome_options)
        try:
            driver2.get(url.replace('/p/', '/product-reviews/'))
            element = driver2.find_element(By.XPATH, '//*[@class="cPHDOP col-12-12"]')
            y_position = element.location['y']
            x_position = element.location['x']
            driver2.execute_script(f"window.scrollTo({x_position-200}, {y_position - 400});")
            driver2.save_screenshot(output_file)
            cropper(second=True)
        finally:
            driver2.quit()
    finally:
        driver.quit()
if __name__ == "__main__":
    url = "https://www.flipkart.com/everest-shahi-biryani-masala/p/itmf2nyfxa4tmpju?pid=SCMEUHHYGUUGYXFY"
    class_name = "HO1dRb xsbJxZ"
    output_file = "./static/rating_final_2.png"
    capture_element_screenshot(url, "row q4T7rk _8-rIO3",class_name, output_file)