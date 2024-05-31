
# from PIL import Image
# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.chrome.service import Service
# from selenium.webdriver.chrome.options import Options
# from bs4 import BeautifulSoup
# import sys
# import requests
# from wordcloud import WordCloud, STOPWORDS
# from imgChopper import cropper
import pandas as pd
from get_total_pages import get_total_pages
from generate_word_cloud import generate_word_cloud
from get_soup import get_soup
from extract import extract
from extract_first import extract_first
from capture_element_screenshot import capture_element_screenshot


def main_fk(product_name="everest"):
    try:
        if not "www.flipkart.com/" in product_name:
            print(True , product_name)
            main_url, p_name = extract_first(product_name)

        else:
            print(False , product_name)
            main_url = product_name.split("&lid=")[0]
            p_name = product_name.split("https://www.flipkart.com/")[1].split("/")[0].replace("-"," ").title()
            print(f"{p_name} : product_name")
            
    except ValueError as e:
        raise ValueError("Error occurred during scraping: No valid product link found on the search results page.")
    
    soup = get_soup(main_url)
    print(main_url)
    try:
        count = get_total_pages(soup)
    except:
        # try:
        #     p_name = p_name.lstrip("https://www.flipkart.com/").split("/p/")[0].replace("-", " ")
        # except:
        #     p_name = p_name 
            
        # finally:
            return [],p_name
    revs = []
    global mini_revs

    for i in range(1, count + 1):
        revs += extract(get_soup(main_url, i, False))
        print(f"Scraping page {i} out of {count}")
        if len(revs)>=150:
            break

    df = pd.DataFrame(revs)
    df.to_excel("new.xlsx", index=False)

    mini_revs = []
    generate_word_cloud(revs)
    print(len(revs))
    output_file = './static/rating_container.png'


    return revs, p_name

















    # try:
    #     capture_element_screenshot(main_url, 'HO1dRb xsbJxZ', "row q4T7rk _8-rIO3", output_file)
    # except Exception as e:
    #     raise ValueError(f"Error occurred during screenshot capture: {str(e)}")

    # total_reviews = get_total_pages(soup)
    # if total_reviews == 0:
    #     raise ValueError("NO REVIEWS FOR THE PRODUCT GIVEN")
# from selenium.webdriver.chrome.service import Service

# def capture_element_screenshot(url, class_name, class_name2, output_file):
#     chrome_options = Options()
#     chrome_options.add_argument("--headless")
#     chrome_options.add_argument("--no-sandbox")
#     chrome_options.add_argument("--disable-dev-shm-usage")
#     chrome_options.add_argument("--disable-gpu")

#     try:
#         # Initialize Chrome WebDriver with options
#         driver = webdriver.Chrome(options=chrome_options)
        
#         driver.get(url)
        
#         try:
#             element = driver.find_element(By.CSS_SELECTOR, f'.{class_name2}')
#         except:
#             element = driver.find_element(By.XPATH, '//*[@class="HO1dRb xsbJxZ"]')

#         y_position = element.location['y']
#         x_position = element.location['x']
#         driver.execute_script(f"window.scrollTo({x_position-200}, {y_position - 400});")
#         driver.save_screenshot(output_file)
#         final_addr = cropper()
#         print(f"Screenshot saved to {final_addr}")

#     except Exception as e:
#         print(f"An error occurred: {e}")
#         try:
#             driver.quit()
#         except NameError:
#             pass
        
#         try:
#             driver2 = webdriver.Chrome(options=chrome_options)
#             driver2.get(url.replace('/p/', '/product-reviews/'))
#             element = driver2.find_element(By.XPATH, '//*[@class="cPHDOP col-12-12"]')
#             y_position = element.location['y']
#             x_position = element.location['x']
#             driver2.execute_script(f"window.scrollTo({x_position-200}, {y_position - 400});")
#             driver2.save_screenshot(output_file)
#             cropper(True)
#         except Exception as e:
#             print(f"An error occurred: {e}")
#             sys.exit(1)  # Exit if the second attempt also fails
#         finally:
#             try:
#                 driver2.quit()
#             except NameError:
#                 pass
#     finally:
#         try:
#             driver.quit()
#         except NameError:
#             pass





# def extract_first(product_name):
#     base_url = "https://www.flipkart.com/search?q="
#     final_url = (base_url + product_name).replace(" ", "+")
#     print(final_url)
#     base_soup = get_soup(final_url, 1, True)
#     return extract_link_from_search(base_soup)

# def extract_link_from_search(soup):
#     anchor_tag = soup.find("a", class_="CGtC98") or \
#                  soup.find("a", class_="rPDeLR") or \
#                  soup.find("a", class_="VJA3rP")
    
#     if not anchor_tag:
#         raise ValueError("No valid product link found on the search results page.")
    
#     p_name = anchor_tag["href"].split("/p/")[0].replace("-", " ").title().strip("/")
#     main_link = anchor_tag["href"].split("&lid=")[0]
#     final_main_link = "https://www.flipkart.com" + main_link
#     print(final_main_link)
    
#     return final_main_link, p_name

# def get_soup(review_url, page_number=1, for_product=False):
#     while True:
#         try:
#             proxies = {
#                 'http': 'http://22B81A0595:IamMurali595_@unblock.oxylabs.io:60000',
#                 'https': 'http://22B81A0595:IamMurali595_@unblock.oxylabs.io:60000',
#             }

#             if for_product:
#                 # Add page number for product search results
#                 review_url += f"&page={page_number}"
#                 response = requests.get(review_url, verify=False, proxies=proxies)
#                 print(response.status_code)

#                 if response.status_code>299:
#                     response = requests.get(review_url, verify=False, proxies=proxies)
#                     print(response.status_code)

#             else:
#                 # Modify URL for review pages and add page number
#                 review_url = review_url.replace("/p/", "/product-reviews/") + f"&page={page_number}"
#                 response = requests.get(review_url, verify=False , proxies=proxies)
#                 if response.status_code>299:
#                     response = requests.get(review_url, verify=False , proxies=proxies)
#                 print(response.status_code)
#             # Print the HTTP status code for debugging purposes


#             # Parse the page content using BeautifulSoup
#             soup = BeautifulSoup(response.text, "lxml")
#             return soup
#         except:
#             continue
# def extract(soup):
#     reviews = soup.find_all("div", class_="col EPCmJX Ma1fCG")
#     revs = []
#     global mini_revs
#     global product_name_2

#     for review in reviews:
#         product_name_2 = str(soup.title.text).split("Reviews:")[0].strip()
#         customer_name = review.find_all("p", class_="_2NsDsF AwS1CA")[0].text
#         mini_review = str(review.find("p", class_="z9E0IG").text).strip()
#         mini_review = mini_review if mini_review else str(review.find("p", class_="_11pzQk").text).strip()
#         mini_revs.append(mini_review.replace(" ", "_").replace("-", "_"))

#         rating = review.find("div", class_="XQDdHH") or review.find("div", class_="XQDdHH Ga3i8K") or review.find("div", class_="XQDdHH Js30Fc Ga3i8K")
#         rating = int(str(rating.text).strip())

#         date = str(review.find_all("p", class_="_2NsDsF")[1].text).strip()
#         review_body = str(review.find("div", class_="ZmyHeo").text).split("READ MORE")[0].strip()

#         d1 = {
#             "Product": product_name_2,
#             "customer_name": customer_name.upper(),
#             "rating": rating,
#             "mini_review": mini_review,
#             "date": date,
#             "review_body": review_body
#         }
#         revs.append(d1)
#         print(
#             f"Product       :  {d1['Product']}",
#             f"customer_name :  {d1['customer_name']}",
#             f"rating        :  {d1['rating']}",
#             f"mini-review   :  {d1['mini_review']}",
#             f"review-body   :  {d1['review_body']}",
#             f"date          :  {d1['date']}",
#             sep="\n", end="\n\n*****************************\n"
#         )

#     return revs

# def get_total_pages(soup):
#     pages = soup.find("span", class_="Wphh3N") or \
#             soup.find("span", class_="Wphh3N d4OmzS") or \
#             soup.find("div", class_="atZ055")
    
#     pages = pages.text.strip()
#     try:
#         pages = int(pages.split("&")[1].split("Reviews")[0].strip().replace(",", ""))
#     except:
#         pages = int(pages.split("and")[1].split("reviews")[0].strip().replace(",", ""))
    
#     print(f"{pages} reviews in total")
#     return pages

# if __name__ == "__main__":
#     main_fk()

# def main_fk(product_name="everest"):
    
#     output_file = './static/rating_container.png'


#     try:
#         if not "/p/" or not "/product-review/" in product_name:
#             print(True, product_name)
#             main_url, p_name = extract_first(product_name)
#         else:
#             print(False, product_name)
#             main_url = product_name.split("&lid=")[0]
#             p_name = product_name.split("&lid=")[0][0:18]
            
#     except ValueError as e:
#         raise ValueError("Error occurred during scraping: No valid product link found on the search results page.")
    
#     soup = get_soup(main_url)
#     print(main_url)


#     count = get_total_pages(soup)
#     print(f"{count} times we have to scrape for all reviews.. each page 10 revs")

#     revs = []

#     for i in range(1, count + 1):
#         revs += extract(get_soup(main_url, i, False))
#         print(f"Scraping page {i} out of {count}")

#     capture_element_screenshot(main_url, 'HO1dRb xsbJxZ', "row q4T7rk _8-rIO3", output_file)
#     # Generate word cloud
#     generate_word_cloud(revs)

#     return revs, p_name

# def generate_word_cloud(revs):
#     text = ' '.join([rev['mini_review'].replace(' ', '_') for rev in revs])
#     wc = WordCloud(
#         background_color="black",
#         stopwords=STOPWORDS,
#         height=600,
#         width=800,
#         prefer_horizontal=1
#     ).generate(text)
#     wc.to_file("./static/wc.png")
#     print("Word cloud generated.")


# def extract_first(product_name):
#     base_url = "https://www.flipkart.com/search?q="
#     final_url = (base_url + product_name).replace(" ", "+")
#     print(final_url)
#     base_soup = get_soup(final_url, 1, True)
#     return extract_link_from_search(base_soup)

# def extract_link_from_search(soup):
#     anchor_tag = soup.find("a", class_="CGtC98") or \
#                  soup.find("a", class_="rPDeLR") or \
#                  soup.find("a", class_="VJA3rP")
    
#     if not anchor_tag:
#         raise ValueError("No valid product link found on the search results page.")
    
#     p_name = anchor_tag["href"].split("/p/")[0].replace("-", " ").title().strip("/")
#     main_link = anchor_tag["href"].split("&lid=")[0]
#     final_main_link = "https://www.flipkart.com" + main_link
#     print(final_main_link)
    
#     return final_main_link, p_name

# def get_soup(review_url, page_number=1, for_product=False):
#     while True:
#         try:
#             proxies = {
#                 'http': 'http://22B81A0595:IamMurali595_@unblock.oxylabs.io:60000',
#                 'https': 'http://22B81A0595:IamMurali595_@unblock.oxylabs.io:60000',
#             }

#             if for_product:
#                 # Add page number for product search results
#                 review_url += f"&page={page_number}"
#                 response = requests.get(review_url, verify=False, proxies=proxies)
#             else:
#                 # Modify URL for review pages and add page number
#                 review_url = review_url.replace("/p/", "/product-reviews/") + f"&page={page_number}"
#                 response = requests.get(review_url, verify=False , proxies=proxies)
            
#             print(response.status_code)  # Print the HTTP status code for debugging purposes

#             # Parse the page content using BeautifulSoup
#             soup = BeautifulSoup(response.text, "lxml")
#             return soup
#         except:
#             continue

# def extract(soup):
#     reviews = soup.find_all("div", class_="col EPCmJX Ma1fCG")
#     revs = []

#     for review in reviews:
#         customer_name = review.find_all("p", class_="_2NsDsF AwS1CA")[0].text
#         mini_review = review.find("p", class_="z9E0IG") or review.find("p", class_="_11pzQk")
#         mini_review = mini_review.text.strip() if mini_review else ""
#         rating = review.find("div", class_="XQDdHH") or review.find("div", class_="XQDdHH Ga3i8K") or review.find("div", class_="XQDdHH Js30Fc Ga3i8K")
#         rating = int(rating.text.strip())
#         date = review.find_all("p", class_="_2NsDsF")[1].text.strip()
#         review_body = review.find("div", class_="ZmyHeo").text.split("READ MORE")[0].strip()

#         d1 = {
#             "customer_name": customer_name.upper(),
#             "rating": rating,
#             "mini_review": mini_review,
#             "date": date,
#             "review_body": review_body
#         }
#         revs.append(d1)
#         print(
#             f"customer_name :  {d1['customer_name']}",
#             f"rating        :  {d1['rating']}",
#             f"mini-review   :  {d1['mini_review']}",
#             f"review-body   :  {d1['review_body']}",
#             f"date          :  {d1['date']}",
#             sep="\n", end="\n\n*****************************\n"
#         )

#     return revs

# def get_total_pages(soup):
#     pages = soup.find("span", class_="Wphh3N") or \
#             soup.find("span", class_="Wphh3N d4OmzS") or \
#             soup.find("div", class_="atZ055")
    
#     pages = pages.text.strip()
#     try:
#         pages = int(pages.split("&")[1].split("Reviews")[0].strip().replace(",", ""))
#     except:
#         pages = int(pages.split("and")[1].split("reviews")[0].strip().replace(",", ""))
    
#     print(f"{pages} reviews in total")
#     return pages

if __name__ == "__main__":
    main_fk()
