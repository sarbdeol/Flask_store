from flask import Flask, render_template
import requests
app = Flask(__name__)

@app.route('/')
def index():
    # Fetch product data from the API
    try:
        response = requests.get('https://walluk.s3.eu-north-1.amazonaws.com/themes/themes%26plugins.json')
        data = response.json()
    except Exception as e:
        print(f"Error fetching data: {e}")
        data = []

    # Extract unique categories
    categories = list(set(item['category'] for item in data))

    return render_template('index.html', categories=categories, products=data)

@app.route('/product/<product_id>')
def product_page(product_id):
    # Fetch product data from the API
    try:
        response = requests.get('https://walluk.s3.eu-north-1.amazonaws.com/themes/themes%26plugins.json')
        products = response.json()
        product = next((item for item in products if item['title'] == product_id), None)
    except Exception as e:
        print(f"Error fetching data: {e}")
        product = None

    return render_template('product.html', product=product)
if __name__ == '__main__':
    # app.run(debug=True)
    app.run(host='0.0.0.0', port=5000,debug=True)
