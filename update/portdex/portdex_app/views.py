from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages

import requests
from django.utils.text import slugify
# Home page
def main(request):
    return render(request, 'main.html')

# Product listing
def index(request):
    try:
        response = requests.get('https://walluk.s3.eu-north-1.amazonaws.com/themes/themes%26plugins.json')
        data = response.json()

        # Create a slug for each product based on its title
        for product in data:
            product['slug'] = slugify(product['title'])
            product['sub_category'] = product.get('sub-category', 'N/A')
            product['tags'] = product.get('tags', [])

    except Exception as e:
        print(f"Error fetching data: {e}")
        data = []

    categories = list(set(item['category'] for item in data))
    return render(request, 'index.html', {'categories': categories, 'products': data})
# Product details
def product_page(request, product_id):
    try:
        response = requests.get('https://walluk.s3.eu-north-1.amazonaws.com/themes/themes%26plugins.json')
        products = response.json()
        product = next((item for item in products if item['title'] == product_id), None)
    except Exception as e:
        print(f"Error fetching data: {e}")
        product = None

    return render(request, 'product.html', {'product': product})

# User Login View
def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('main')  # Replace 'main' with your homepage
        else:
            messages.error(request, 'Invalid credentials')
    return render(request, 'login.html')

# User Register View
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Account created successfully!')
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})
# User Logout
def user_logout(request):
    logout(request)
    return redirect('login')
