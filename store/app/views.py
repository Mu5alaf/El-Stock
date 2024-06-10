from django.shortcuts import render, redirect
from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import User, Product, CartItem, Cart
from .payment import mock_payment_gateway
from django.core.mail import send_mail
from django.conf import settings
import logging

#(__name__)_app_name
logger = logging.getLogger(__name__)

#welcome_View
def welcome(request):
    return render(request, 'welcome.html')

#Home_with_all_product_view
def home(request):
    product = Product.objects.all()
    return render(request, 'home.html', {"product": product})

#unauthorized_login_view
def custom_401(request):
    if not request.user.is_authenticated:
        logger.warning(f" {request.user}  Person try to access a route without login")
    return render(request, '401.html')

#login_view
def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        # Authenticate user
        user = authenticate(request, username=username, password=password)
        # login checker & logging
        if user is not None:
            auth_login(request, user)
            logger.info(f"{username} login successfully")
            return redirect('home')
        else:
            logging.error(f"{username} cannot login")
            messages.error(request, "Invalid username or password")
            return redirect('login')
    return render(request, 'login.html')

#signup_view
def signup(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')
        # Data_Validation_and_i_already_have_Html_required_input
        if not username or not password or not email:
            logger.warning("User Signup Error ")
            messages.error(request, 'All fields are required')
            return redirect('signup')
        # Check_if_username_exist
        if User.objects.filter(username=username).exists():
            logger.warning("User trying to use existing username ")
            messages.warning(request, 'Username already exists')
            return redirect('signup')
        #create_user
        try:
            new_user = User.objects.create_user(username=username, email=email, password=password)
            new_user.save()
            logger.info("New user has been created")
            messages.success(request, "Registration successful. Please login")
            return redirect('login')
        except Exception as e:
            logger.error(f"Error with {e}")
            messages.error(request, f"Error with {e}")
            return redirect('signup')
    return render(request, 'signup.html')


#item_details_view
@login_required(login_url='custom_401')
def item(request, pk):
    product = Product.objects.filter(pk=pk)
    return render(request, 'item.html', {"product": product})

#item_details_view
@login_required(login_url='custom_401')
def cart(request):
    try:
        cart = Cart.objects.get(user=request.user, is_paid=False)
        cart_items = cart.items.all()
        logger.info(f"Cart retrieved for user {request.user.username}.")
        if cart_items:
            #looping cart_item_to_get_back_details 
            item_details = ','.join([f"{item.quantity} of {item.product}"for item in cart_items])
            logger.info(f"{request.user} has add {item_details}")
        else:
            logger.info(f"{request.user} has empty cart")
    except Cart.DoesNotExist:
        cart_items = []
        cart = None
        logger.info(f"{request.user} has no cart")
    context = {'cart': cart, 'cart_items': cart_items}
    return render(request, 'cart.html', context)


#cart_details_view
@login_required(login_url='custom_401')
def add_cart(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        try:
            #Get_quantity_from_POST_data
            quantity = int(request.POST.get('quantity'))
            #Validate_quantity
            if quantity <= 0:
                messages.error(request, "Invalid quantity.")
                return redirect('item', pk=pk)
            # Check if requested quantity exceeds available stock
            if quantity > product.stock:
                logger.warning(f"{request.user} try to add more than the available Quantity")
                messages.error(request, f"Only {product.stock} {product.name}(s) available.")
                return redirect('item', pk=pk)
            # Get_or_create_the_user's_cart
            cart, created = Cart.objects.get_or_create(user=request.user, is_paid=False)
            # Get_or_create_CartItem_for_the_product
            cart_item, item_created = CartItem.objects.get_or_create(
                cart=cart,
                product=product,
                defaults={'quantity': 0, 'price': 0}  # Initialize with defaults
            )
            # Update_quantity_and_price_of_CartItem
            if not item_created:
                new_quantity = cart_item.quantity + quantity
                # Check_if_new_quantity_exceeds_available_stock
                if new_quantity > product.stock:
                    messages.error(request, f"Only {product.stock} {product.name}(s) available.")
                    return redirect('item', pk=pk)
                cart_item.quantity = new_quantity
                cart_item.price = new_quantity * product.price
                cart_item.save()
            else:
                cart_item.quantity = quantity
                cart_item.price = quantity * product.price
                cart_item.save()
            # Update_total_amount_in_the_cart
            cart.total_amount = sum(item.price for item in cart.items.all())
            cart.save()
            messages.success(request, "Item added to cart")
            return redirect('cart')
        except Exception as e :
            logger.error(f"{request.user} have error with {e}")
            messages.error(request, f"error with,{e}")
            return redirect('item', pk=pk)
    return redirect('item', pk=pk)

#remove_from_cart
@login_required(login_url='custom_401')
def remove_cart (request,pk):
    cart_item = get_object_or_404(CartItem,pk=pk)
    if cart_item.cart.user != request.user:
        messages.error(request, "You are not authorized to remove this item.")
        return redirect('cart')
    cart = cart_item.cart
    cart_item.delete()
    # Update_the_cart's_total_amount_after_deleting
    cart.total_amount = sum(item.price for item in cart.items.all())
    cart.save()
    logger.info(f"{request.user} remove {cart_item} from cart")
    messages.success(request, "Item removed from cart.")
    return redirect('cart')

@login_required(login_url='custom_401')
def checkout(request):
    cart = get_object_or_404(Cart, user=request.user, is_paid=False)
    if request.method == 'POST':
        # Process_payment_(mocked)
        payment_response = mock_payment_gateway()
        if payment_response['status'] == 'success':
            # Update_stock
            for item in cart.items.all():
                product = item.product
                product.stock -= item.quantity
                product.save()
            # Mark_cart_as_paid
            cart.is_paid = True
            cart.save()
            # Send_confirmation_email
            send_order_confirmation_email(request.user, cart, payment_response['transaction_id'])
            logger.info(f"{request.user} Payment Transaction and order mail has been Done succsufly")
            messages.success(request, "Checkout successful. Order confirmation has been sent to your email.")
            return redirect('home')
        else:
            logger.error(f"{request.user} has rejected Payment Transaction")
            messages.error(request, f"Payment failed: {payment_response['message']}")
            return redirect('cart')
    return render(request, 'checkout.html', {'cart': cart})

def send_order_confirmation_email(user, cart,transaction_id):
    subject = 'Order Confirmation'
    message = f'Thank you {user.username} for your order. Your order ID is {cart.id} and your transaction ID is {transaction_id}. The total amount is ${cart.total_amount}.'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [user.email]
    send_mail(subject, message, email_from, recipient_list)
    
