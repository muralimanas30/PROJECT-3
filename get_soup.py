# import time
# import requests
# from bs4 import BeautifulSoup

# # def get_soup(review_url, page_number=1, for_product=False):
    
# #     proxies = {
# #         'http': 'http://22B81A0597:IamRahul597_@unblock.oxylabs.io:60000',
# #         'https': 'https://22B81A0597:IamRahul597_@unblock.oxylabs.io:60000',
# #     }
# #     if for_product:
# #         # Add page number for product search results
# #         review_url += f"&page={page_number}"
# #         response = requests.get(review_url, verify=False, proxies=proxies)
# #         if response.status_code!= 200:
# #             raise ValueError(f"from get Soup , status {response.status_code} ")
# #     else:
# #         # Modify URL for review pages and add page number
# #         review_url = review_url.replace("/p/", "/product-reviews/") + f"&page={page_number}"
# #         response = requests.get(review_url, verify=False)
# #         if response.status_code!=200:
# #             time.sleep(1)

# #     print(response.status_code , " line 41 get_soup")  # Print the HTTP status code for debugging purposes
# #     # Parse the page content using BeautifulSoup
# #     soup = BeautifulSoup(response.text, "lxml")
# #     return soup
    
# def get_soup(review_url, page_number=1, for_product=False):
#     if for_product:
#         # proxies = {
#         #     'http': 'http://muralimanas30:IamMurali591_@unblock.oxylabs.io:60000',
#         #     'https': 'https://muralimanas30:IamMurali591_@unblock.oxylabs.io:60000',
#         # }
#         proxies = {
#             'http': 'http://22B81A0597:IamRahul597_@unblock.oxylabs.io:60000',
#             'https': 'https://22B81A0597:IamRahul597_@unblock.oxylabs.io:60000',
#         }
#     else:
#         proxies = None
    
#     retries = 5
#     backoff_factor = 0.5
    
#     for attempt in range(retries):
#         try:
#             if for_product:
#                 review_url += f"&page={page_number}"
#             else:
#                 review_url = review_url.replace("/p/", "/product-reviews/") + f"&page={page_number}"
            
#             response = requests.get(review_url, verify=False, proxies=proxies)
            
#             if response.status_code == 200:
#                 response_length = len(response.text)
#                 print(f"Received response with length: {response_length}")
                
#                 # Check if the response length falls within the specified range
#                 if not for_product and 36600 <= response_length <= 37000:
#                     print("Response length falls within target range, but not retrying with proxies since !for_product")
#                     continue
                
#                 print(f"Successfully fetched page {page_number}")
#                 soup = BeautifulSoup(response.text, "lxml")
#                 return soup
#             elif response.status_code == 429:
#                 print(f"Received status code 429, retrying... (attempt {attempt + 1}/{retries})")
#                 time.sleep(backoff_factor * (2 ** attempt))
#             else:
#                 print(f"Received unexpected status code {response.status_code}")
#                 break
        
#         except requests.RequestException as e:
#             print(f"Request failed: {e}")
#             time.sleep(backoff_factor * (2 ** attempt))

#     raise ValueError(f"Failed to fetch page {page_number} after {retries} attempts")

import time
import requests
from bs4 import BeautifulSoup

def get_soup(review_url, page_number=1, for_product=False):
    retries = 5
    backoff_factor = 0.5

    proxies = {
            'http': 'http://22B81A0597:IamRahul597_@unblock.oxylabs.io:60000',
            'https': 'https://22B81A0597:IamRahul597_@unblock.oxylabs.io:60000',
        }
    for attempt in range(retries):
        try:
            if for_product:
                review_url += f"&page={page_number}"
                response = requests.get(review_url, verify=False, proxies=proxies)
            else:
                review_url = review_url.replace("/p/", "/product-reviews/") + f"&page={page_number}"
                response = requests.get(review_url, verify=False,proxies=proxies)
            if response.status_code == 200:
                print(f"Successfully fetched page as status 200 for page {page_number}")
                soup = BeautifulSoup(response.text, "lxml")
                return soup
            elif response.status_code == 429:
                print(f"Received status code 429, retrying... (attempt {attempt + 1}/{retries})")
                time.sleep(backoff_factor * (2 ** attempt))
            else:
                print(f"Received unexpected status code {response.status_code}")
                break
        
        except Exception as e:
            print(f"Request failed: {e}")
            time.sleep(backoff_factor * (2 ** attempt))

    raise ValueError(f"Failed to fetch page {page_number} after {retries} attempts")

# # Example usage
# review_url = "https://example.com/p/product-id"
# page_number = 1
# soup = get_soup(review_url, page_number, for_product=True)
# if soup:
#     print(soup.prettify())
# else:
#     print("Skipped this review due to response length within target range after retries.")
