from get_soup import get_soup

def extract_first(product_name):
    if "/www.flipkart.com/" in product_name:
        final_url = product_name
    else:
        base_url = "https://www.flipkart.com/search?q="
        final_url = (base_url + product_name).replace(" ", "+")
    
    print(final_url)
    base_soup = get_soup(final_url, 1, True)
    print("GOT FIRST SOUP , EXTRACT_FIRST")
    return extract_link_from_search(base_soup)

def extract_link_from_search(soup):
    anchor_tag = soup.find("a", class_="CGtC98") or \
                 soup.find("a", class_="rPDeLR") or \
                 soup.find("a", class_="VJA3rP")
    
    if not anchor_tag:
        raise ValueError("No valid product link found on the search results page.")
    
    p_name = anchor_tag["href"].split("/p/")[0].replace("-", " ").title().strip("/")
    main_link = anchor_tag["href"].split("&lid=")[0]
    final_main_link = "https://www.flipkart.com" + main_link
    print(final_main_link)
    
    return final_main_link, p_name

