from bs4 import BeautifulSoup
from get_soup import get_soup

def get_total_pages(soup):
    # print(type(soup)==str)
    if type(soup)==str:
        soup = get_soup(soup) #means not a soup but link we needd to extract
    pages = soup.find("span", class_="Wphh3N") or \
            soup.find("span", class_="Wphh3N d4OmzS") or \
            soup.find("div", class_="atZ055")
    
    try:
        pages = pages.text.strip()
    except AttributeError as a:
        raise ValueError("Some error occured main_fk.") 
    try:
        pages = int(pages.split("&")[1].split("Reviews")[0].strip().replace(",", ""))
    except:
        pages = int(pages.split("and")[1].split("reviews")[0].strip().replace(",", ""))
    
    print(f"{pages} reviews in total")
    total_reviews = pages
    if total_reviews == 0:
        return 0

    count = total_reviews // 10 + 1 if total_reviews % 10 != 0 else total_reviews // 10
    print(f"{count} times we have to scrape for all reviews.. each page 10 revs")
    
    if count>15:
        print("We have too many reviews, we will try to get 150 most helpful ones !!")
        

    return count
if __name__ =="__main__":
    get_total_pages()