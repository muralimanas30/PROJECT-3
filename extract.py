from bs4 import BeautifulSoup

def extract(soup,rev_link="#"):
    reviews = soup.find_all("div", class_="col EPCmJX Ma1fCG")
    avg_rating = soup.find("div", class_= "ipqd2A")
    avg_rating = avg_rating.text if avg_rating else ""
    
    price = soup.find("div", class_= "Nx9bqj")
    price = price.text if price else ""
    
    revs = []

    for review in reviews:
        product_name_2 = str(soup.title.text).split("Reviews:")[0].strip()
        customer_name = review.find_all("p", class_="_2NsDsF AwS1CA")[0].text
        mini_review = review.find("p", class_="z9E0IG") or review.find("p", class_="_11pzQk")
        mini_review = mini_review.text.strip() if mini_review else ""
        rating = review.find("div", class_="XQDdHH") or review.find("div", class_="XQDdHH Ga3i8K") or review.find("div", class_="XQDdHH Js30Fc Ga3i8K")
        rating = int(rating.text.strip())
        date = review.find_all("p", class_="_2NsDsF")[1].text.strip()
        review_body = review.find("div", class_="ZmyHeo").text.split("READ MORE")[0].strip()


        d1 = {
            "rev_link:":rev_link if rev_link else "#",
            "price":price,
            "avg_rating":avg_rating,
            "Product": product_name_2,
            "customer_name": customer_name.upper(),
            "rating": rating,
            "mini_review": mini_review,
            "date": date,
            "review_body": review_body
        }
        revs.append(d1)
        print(
            f"LINK          :  {rev_link}",
            f"Price         :  {price}",
            f"Product       :  {d1['Product']}",
            f"AVG_RATING    :  {d1['avg_rating']}",
            f"customer_name :  {d1['customer_name']}",
            f"rating        :  {d1['rating']}",
            f"mini-review   :  {d1['mini_review']}",
            f"review-body   :  {d1['review_body']}",
            f"date          :  {d1['date']}",
            sep="\n", end="\n\n*****************************\n"
            )

    return revs