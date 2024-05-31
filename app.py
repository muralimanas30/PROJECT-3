from flask import Flask, render_template, request, jsonify
from final_flipkart import main_fk, extract_first, get_total_pages
import threading

app = Flask(__name__)

# Define the Render app URL
render_app_url = "https://flask-pr.onrender.com"

# Global variables for product name, reviews, and main URL
product_name = ""
reviews = []
main_url = ""

@app.route('/')
def index():
    """
    Render the index page with the search form.
    """
    print("Rendering index page")
    return render_template('index.html', render_app_url=render_app_url)

@app.route('/search', methods=['POST'])
def search():
    """
    Handle the product search form submission.

    Extract the product name from the form and render the searching page.
    """
    print("Received search request")
    if request.method == 'POST':
        global product_name
        product_name = request.form['product-name']
        print("Product name:", product_name)
        return render_template('searching.html', product_name=product_name, render_app_url=render_app_url)
    else:
        print("Invalid request method")
        return jsonify(status='error', message='Invalid request, accepts only post')

@app.route('/start_scraping', methods=['POST'])
def start_scraping():
    """
    Start the scraping process for the given product name.

    Get the main URL and total pages for the product, then return the result.
    """
    print("Received start scraping request")
    try:
        if request.method == 'POST':
            global product_name
            global main_url
            product_name = request.json['product_name']
            
            return jsonify(status='success', total_pages=0, product_name=product_name)
        else:
            print("Invalid request method")
            return jsonify(status='error', message='Invalid request method')
    except ValueError as e:
        error_message = str(e)
        return jsonify(status='error', message=error_message)
    except Exception as e:
        print("Error occurred during scraping:", str(e))
        return jsonify(status='error', message=str(e))

@app.route('/fetch_reviews', methods=['GET'])
def fetch_reviews():
    """
    Fetch reviews, generate word cloud, and capture screenshot for the product.
    Render the reviews page with the scraped reviews.
    """
    global product_name, reviews, main_url
    
    print("\033[1;37;41m Fetching reviews for product:", product_name, "\033[0m")
    try:
        reviews, product_name= main_fk(product_name)

        
        print("\033[1;37;42m Scraped reviews for product:", product_name, "\033[0m")
        return render_template('reviews.html', product_name=product_name, reviews=reviews, render_app_url=render_app_url)
    except ValueError as e:
        error_message = str(e)
        print("\033[1;37;41m Error occurred during fetching reviews:", error_message, "\033[0m")
        return render_template('notfound.html', text=error_message)
    except Exception as e:
        error_message = str(e)
        print("\033[1;37;41m Error occurred during fetching reviews:", error_message, "\033[0m")
        return render_template('notfound.html', text=error_message)


@app.route('/reviews', methods=['GET'])
def show_reviews():
    """
    Render the reviews page with the scraped reviews.
    """
    try:
        global product_name
        global reviews
        global main_url
        print("Rendering reviews page")
        return render_template('reviews.html', product_name=product_name, reviews=reviews, render_app_url=render_app_url,main_url=main_url)
    except:
        return render_template('notfound.html')

@app.route('/wordcloud')
def wordcloud():
    """
    Render the word cloud page.
    """
    print("Rendering word cloud page")
    return render_template('wordcloud.html', render_app_url=render_app_url)

@app.route('/notfound')
def notfound():
    return render_template('notfound.html')


@app.route('/sort_reviews', methods=['GET'])
def sort_reviews():
    # Read reviews from Excel file
    
    
    # Sort reviews based on rating
    sorted_reviews = sorted(reviews, key=lambda x: int(x["rating"]), reverse=True)
    
    # Convert sorted reviews to JSON format
    # Return sorted reviews as JSON response
    return render_template('reviews.html', product_name=product_name, reviews=sorted_reviews, render_app_url=render_app_url,main_url=main_url)

if __name__ == '__main__':
    app.run(debug=True)
