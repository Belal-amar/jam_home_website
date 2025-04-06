from django.shortcuts import render,redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from . models import *
from .models import User
from django.contrib import messages
import bcrypt
from django.apps import apps
from django.contrib.auth import logout



def home(request):
    return render (request,"home.html")


def register(request):
    errors = User.objects.user_validator(request.POST)
    if errors:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')

    password = request.POST['password']
    pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

    the_user = User.objects.create(
        first_name=request.POST['fname'],
        last_name=request.POST['lname'],
        email=request.POST['email'],  # Add email field
        password=pw_hash
    )

    request.session['userid'] = the_user.id

    messages.success(request, "Successfully created an account")
    return redirect('categories')


def login(request):
    errors = User.objects.login_validator(request.POST)
    
    if errors:
        # Validation errors present, show messages and stay on login page
        for key, value in errors.items():
            messages.error(request, value)
        print("Validation errors:", errors)  # Debugging print
        return redirect('/')  # Stay on the login page if errors exist

    # Print the email being used to check for typos
    print("Submitted Email:", request.POST['email'])

    try:
        # Try fetching user by email
        user = User.objects.get(email=request.POST['email'])
        print("User found:", user)  # Debugging print
    except User.DoesNotExist:
        # If user does not exist, show error message
        messages.error(request, "Invalid Email or Password")
        print("User not found")  # Debugging print
        return redirect('/')  # Stay on the login page if user is not found

    # Check if the password matches
    if bcrypt.checkpw(request.POST['password'].encode(), user.password.encode()):
        print("Password matches")  # Debugging print
        
        # Set session variable for logged in user
        request.session['userid'] = user.id
        
        # Redirect to categories page on successful login
        messages.success(request, "Successfully logged in")
        print("Redirecting to categories")  # Debugging print
        return redirect('categories')  # Redirect to categories

    # If the password doesn't match, show error message
    messages.error(request, "Invalid Email or Password")
    print("Password mismatch")  # Debugging print
    return redirect('/')  # Stay on the login page if password doesn't match

    



def categories(request):
    if 'userid' in request.session:
        user = User.objects.get(id=request.session['userid'])
    else:
        user = None  # No logged-in user

    context = {
        "categories": Category.objects.all(),
        "user": user
    }
    return render(request, "categories.html", context)


def category_products(request, category_id):
    if 'userid' not in request.session:
        messages.error(request, "You need to log in first!")
        return redirect('home')

    user = User.objects.get(id=request.session['userid'])
    category = Category.objects.get(id=category_id)
    products = Product.objects.filter(category=category)  # Fetch products related to the category

    context = {
        'user': user,
        'category': category,
        'products': products
    }
    return render(request, "category_products.html", context)



def product_detail(request, product_id):
    try:
        product = Product.objects.get(id=product_id)
        data = {
            'name': product.name,
            'description': product.description,
            'price': product.price,
            'image_url': product.image,  # Assuming the image is an ImageField
        }
        return JsonResponse(data)
    except Product.DoesNotExist:
        return JsonResponse({'error': 'Product not found'}, status=404)
    

def add_to_cart(request, product_id):
    if 'userid' not in request.session:
        messages.error(request, "You need to log in first!")
        return redirect('login')
    user=User.objects.get(id=request.session['userid'])
    # user = get_object_or_404(User, id=request.session['userid'])
    product = Product.objects.get(id=product_id)

    # Get or create the order
    order, created = Order.objects.get_or_create(user=user, status="Staged")

    # Check if the item already exists in the order
    order_item, item_created = Orderitem.objects.get_or_create(
        order=order,
        product=product,
        defaults={'quantity': 1}  # Default to 1 if new item
    )

    if not item_created:
        # If item exists, increment quantity
        order_item.quantity += 1
        order_item.save()

    messages.success(request, "Item added to cart!")
    return redirect('cart')


def cart(request):
    if 'userid' not in request.session:
        messages.error(request, "You need to log in first!")
        return redirect('login')

    user = User.objects.get(id=request.session['userid'])

    # Fetch the staged order
    order = Order.objects.filter(user=user, status='Staged').first()

    cart_items = []
    total_price = 0  # Total cart value

    if order:
        for item in order.orderprod.all():  # Use related_name orderprod
            item_total = item.product.price * item.quantity
            total_price += item_total
            cart_items.append({
                'product': item.product,
                'quantity': item.quantity,
                'item_total': item_total,  # Precomputed total price for this item
                'id': item.id
            })

    context = {
        'cart_items': cart_items,  # Pass only items
        'total_price': total_price,
    }

    return render(request, 'cart.html', context)


def location(request):
    return render(request, 'location.html')


def remove_from_cart(request, item_id):
    cart_item = Orderitem.objects.get(id=item_id)
    cart_item.delete()
    return redirect('cart')  # Redirect back to the cart page


def logout(request):
    # Clear all session data
    request.session.flush()
    
    # Redirect to home page after logout
    return redirect('home')  # Cha