from bs4 import BeautifulSoup
import pandas as pd  # To export into Excel sheets
import requests
import matplotlib.pyplot as plt
from wordcloud import WordCloud, STOPWORDS

# Function to scrape reviews from Flipkart
def main_flipkart(product_name="iphone 14 pro"):
    main_url = extract_first(product_name)  # Get the main URL for the product search
    soup = get_soup(main_url , 1 ,True)  # Get the soup object for the main URL
    print(main_url)
    total_reviews = get_total_reviews(soup)  # Get the total number of reviews
    if total_reviews == 0:
        print("NO REVIEWS FOR THE PRODUCT GIVEN")
    else:
        count = total_reviews // 10 + 1 if total_reviews % 10 != 0 else total_reviews // 10
        print(count, " times we have to scrape for all reviews.. each page 10 reviews")
        all_reviews = []
        if count > 1:
            for i in range(1, count + 1):
                try:
                    all_reviews += extract_reviews(get_soup(main_url, i, False))
                except Exception as e:
                    print(f"Error on page {i} for URL: {main_url}\nException: {e}")
                    continue
        else:
            try:
                all_reviews += extract_reviews(soup)
            except Exception as e:
                print(f"Error on initial page for URL: {main_url}\nException: {e}")

        df = pd.DataFrame(all_reviews)  # Convert the reviews to a DataFrame
        df.to_excel("reviews.xlsx", index=False)  # Save the reviews to an Excel file
        
        # Extract all mini_reviews from the reviews
        text = ' '.join([review["Mini Review"] for review in all_reviews])

        # Generate a word cloud
        wordcloud = WordCloud(
            background_color="black",
            stopwords=STOPWORDS,
            height=600,
            width=800,
            prefer_horizontal=1
        ).generate(text)
        wordcloud.to_file("wordcloud.png")  # Save the word cloud as an image
        print(len(all_reviews))
        return all_reviews

# Function to extract the first product link from search results
def extract_first(product_name):
    try:
        base_url = "https://www.flipkart.com/search?q="
        final_url = (base_url + product_name).replace(" ", "+")
        print(final_url)
        base_soup = get_soup(final_url, 1, True)
        return extract_link_from_search(base_soup)
    except Exception as e:
        print(f"Error extracting first product link for {product_name}\nException: {e}")

# Function to extract the product link from search results page
def extract_link_from_search(soup):
    try:
        anchor_tag = soup.find("a", class_="CGtC98")
        if not anchor_tag:
            anchor_tag = soup.find("a", class_="rPDeLR")
        if not anchor_tag:
            anchor_tag = soup.find("a", class_="VJA3rP")
        main_link = anchor_tag["href"].split("&lid=")[0]
        final_main_link = "https://www.flipkart.com" + main_link
        print(final_main_link)
        return final_main_link
    except Exception as e:
        print(f"Error extracting link from search results\nException: {e}")

# Function to get the BeautifulSoup object for a given URL
def get_soup(review_url, page_number=1, for_product=False):
    try:
        proxies = {
            'http': 'http://22B81A0595:IamMurali595_@unblock.oxylabs.io:60000',
            'https': 'http://22B81A0595:IamMurali595_@unblock.oxylabs.io:60000',
        }
        if for_product:
            review_url = review_url + f"&page={page_number}"
            response = requests.get(review_url, verify=False, proxies=proxies)
        else:
            review_url = review_url.replace("/p/", "/product-reviews/") + f"&page={page_number}"
            response = requests.get(review_url, verify=False)
        print(response.status_code)
        response.raise_for_status()
        response_html = response.text
        soup = BeautifulSoup(response_html, "lxml")
        return soup
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred for URL: {review_url}, Page: {page_number}\nHTTPError: {http_err}")
    except Exception as e:
        print(f"Error getting soup object for URL: {review_url}, Page: {page_number}\nException: {e}")

# Function to extract reviews from the soup object
def extract_reviews(soup):
    try:
        reviews = soup.find_all("div", class_="col EPCmJX Ma1fCG")
        review_list = []
        for review in reviews:
            customer_name = review.find_all("p", class_="_2NsDsF AwS1CA")[0].text
            mini_review = str(review.find("p", class_="z9E0IG").text).strip()
            if len(mini_review) == 0:
                mini_review = str(review.find("p", class_="_11pzQk").text).strip()
            rating = review.find("div", class_="XQDdHH")
            if not rating:
                rating = review.find("div", class_="XQDdHH Ga3i8K")
            if not rating:
                rating = review.find("div", class_="XQDdHH Js30Fc Ga3i8K")
            rating = str(rating.text).strip() + " out of 5"
            date = str(review.find_all("p", class_="_2NsDsF")[1].text).strip()
            review_body = str(review.find("div", class_="ZmyHeo").text).split("READ MORE")[0].strip()
            review_info = {
                "Product": str(soup.title.text).split("Reviews:")[0].strip(),
                "Customer Name": customer_name.upper(),
                "Rating": rating,
                "Mini Review": mini_review,
                "Date": date,
                "Review Body": review_body
            }
            print(
                " Product       :  " + review_info["Product"],
                " Customer Name :  " + review_info["Customer Name"],
                " Rating        :  " + review_info["Rating"],
                " Mini Review   :  " + review_info["Mini Review"],
                " Review Body   :  " + review_info["Review Body"],
                " Date          :  " + review_info["Date"],
                sep="\n", end="\n\n*****************************\n"
            )
            review_list.append(review_info)
        return review_list
    except Exception as e:
        print(f"Error extracting reviews from the page\nException: {e}")

# Function to get the total number of reviews
def get_total_reviews(soup):
    try:
        pages = soup.find("span", class_="Wphh3N")
        if not pages:
            pages = soup.find("span", class_="Wphh3N d4OmzS")
        if not pages:
            pages = soup.find("div", class_="atZ055")
        pages = pages.text.strip()
        try:
            total_reviews = int(pages.split("&")[1].split("Reviews")[0].strip().replace(",", ""))
        except:
            total_reviews = int(pages.split("and")[1].split("reviews")[0].strip().replace(",", ""))
        print(total_reviews, " reviews in total")
        return total_reviews
    except Exception as e:
        print(f"Error getting total reviews\nException: {e}")

if __name__ == "__main__":
    main_flipkart()  # Run the script with the default product
