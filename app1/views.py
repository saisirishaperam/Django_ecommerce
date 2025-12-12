from django.shortcuts import render,redirect
from django.contrib.auth.mixins import LoginRequiredMixin

from django.http import JsonResponse

from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseBadRequest

from django.db.models import Q

from django.db.models import Count
from django.contrib.auth.models import User

from app1.forms import CustomerDetailsForm

from app1.models import Coustomer_Details,Contact
from django.contrib.auth.decorators import login_required

from django.views import View

from django.contrib import messages


from app1.models import Product,Cart,Coustomer_Details,Payment,Wishlist,Order_Placed

from django.contrib.auth import authenticate,login,logout
import razorpay

from django.conf import settings

###############  Authantication  ##################
def Sign_Up(request):
    message = ''
    emailmessage = ''
    usermessage = ''
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password2 = request.POST.get('confirm_password')
        if password == password2:
            if User.objects.filter(username=username).exists():
                usermessage = "Mobile Number already exists"
            elif User.objects.filter(email=email).exists():
                emailmessage = "Email already exists"
            else:
                user = User.objects.create_user(username=username, email=email, password=password)
                user.first_name = first_name
                user.save()
                return redirect('login')
        else:
            message = "Confrim Password is not equal to Password"
    context = {
        'message':message,
        'usermessage':usermessage,
        'emailmessage':emailmessage,
    }

    return render(request,'signup.html',context)

# def Login(request):
#     message = ''
#     if request.method == "POST":
#         email = request.POST.get('email')
#         password = request.POST.get('P1')

#         user = authenticate(request, username = email, password=password)
#         if user:
#             login(request,user)
#             return redirect('home')
#         else:
#             message = 'Email or Password are invalid'
#     return render(request,'login.html',{'message':message})
def Login(request):
    message = ''
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('P1')

        user = User.objects.filter(email=email).first()
        
        if user:
            user = authenticate(request, username=user.username, password=password)
            if user:
                login(request, user)
                return redirect('home')
            else:
                message = 'Invalid Email or Password'
        else:
            message = 'Invalid Email or Password'

    return render(request, 'login.html', {'message': message})

def Logout(request):
    logout(request)
    return redirect('login')

def Signup(request):
    message = ""
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        P1 = request.POST.get("P1")
        P2 = request.POST.get("P2")
        if P1 == P2:
            try:
                user = User.objects.create_user(username,email,P1)
                user.save()
                return redirect ('login')
            except Exception as e:
                message = f"{username} User alredy Exist"
        else:
            message = "P1 != P2"
    context = {
        "message":message
    }
        
    return render (request, "signup.html",context)



# def home(request):
#     return render (request,'home.html')

def home(request):
    
    products =Product.objects.order_by('?') # Fetch latest 6 products
    totalitem = 0
    totalwish = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user = request.user))
        totalwish = len(Wishlist.objects.filter(user = request.user))    

    context = {
        'totalitem' : totalitem,
        'totalwish':totalwish,
        'products': products
    }
    return render(request, 'home.html', context)




def contact(request):
    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')

        # Save to database
        if name and email and subject and message:
            Contact.objects.create(name=name, email=email, subject=subject, message=message)
            messages.success(request, "Your message has been sent successfully!")
            return redirect('contact')  # Make sure 'contact' is the name of the URL
        else:
            messages.error(request, "Please fill all fields correctly.")

    return render(request, 'contact.html')




def View_all(request):
    All_Products = Product.objects.order_by('?')
    totalitem = 0
    totalwish = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user = request.user))
        totalwish = len(Wishlist.objects.filter(user = request.user))
 
    
    context={
        'A_Prod':All_Products,
        'totalitem' : totalitem,
        'totalwish':totalwish,
        
    }
    return render(request,'viewall.html',context)





import difflib


def Search(request):
    query = request.GET.get("search")
    all_products = Product.objects.all()
    matched = []

    totalitem = 0
    totalwish = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user = request.user))
        totalwish = len(Wishlist.objects.filter(user = request.user))

    if query:
        query = query.lower()
        for product in all_products:
            title = product.title.lower()
            brand = product.brand.lower()
            category = product.category.lower()

            if (difflib.SequenceMatcher(None, title, query).ratio() > 0.6 or
                difflib.SequenceMatcher(None, brand, query).ratio() > 0.6 or
                difflib.SequenceMatcher(None, category, query).ratio() > 0.6):
                matched.append(product)
    

    context = {
        'A_Prod': matched,
        'query': query,
        'totalitem' : totalitem,
        'totalwish':totalwish,
    }
    return render(request, 'viewall.html', context)



def About(request):
    totalwish =0
    totalitem = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user = request.user))
        totalwish = len(Wishlist.objects.filter(user = request.user))    

    context = {
        'totalitem' : totalitem,
        'totalwish':totalwish,
    }
    return render(request,'about.html',context)


# class Category(View):
#     def get(self,request,val):

#         product = Product.objects.filter(category = val)
#         brands = Product.objects.filter(category=val).order_by('brand').values_list('brand', flat=True).distinct()
#         context = {
#             'val': val,
#             'product':product,
#             'brands':brands, 
#             }

#         return render(request,'category.html',context)

class Category(View):
    def get(self, request, val):
        selected_brand = request.GET.get('brand', None) 
        totalitem = 0
        totalwish = 0
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user = request.user))
            totalwish = len(Wishlist.objects.filter(user = request.user)) 

        if selected_brand:
            products = Product.objects.filter(category=val, brand=selected_brand)  # Filter by brand
        else:
            products = Product.objects.filter(category=val)  # Show all products in category

        brands = Product.objects.filter(category=val).order_by('brand').values_list('brand', flat=True).distinct()

        context = {
            'val': val,
            'products': products,
            'brands': brands,
            'selected_brand': selected_brand,
            'totalitem':totalitem,
            'totalwish':totalwish,
        }
        return render(request, 'category.html', context)




class Product_Details(View):
    def get(self, request, pk):
        product = Product.objects.get(id=pk)
        category_products = Product.objects.filter(category=product.category).exclude(id=pk)
        All_Products =  Product.objects.order_by('?')
          # Default to False
        in_cart = False

        # Only check cart if user is logged in
        if request.user.is_authenticated:
            in_cart = Cart.objects.filter(user=request.user, product=product).exists()
 
    
    

        # Initialize defaults
        wishlist = None
        totalitem = 0
        totalwish = 0
        cart = None

        if request.user.is_authenticated:
            wishlist = Wishlist.objects.filter(Q(product=product) & Q(user=request.user))
            totalitem = len(Cart.objects.filter(user=request.user))
            totalwish = len(Wishlist.objects.filter(user=request.user))
            cart = Cart.objects.filter(product=product)
        
        context = {
            'product': product,
            'category_products': category_products,
            'totalitem': totalitem,
            'totalwish': totalwish,
            'wishlist': wishlist,
            'cart': cart,
            'A_Prod':All_Products,
            'in_cart': in_cart
        }

        return render(request, 'product_details.html', context)



    



class ProfileView(LoginRequiredMixin, View):  # Ensure LoginRequiredMixin is first
    login_url = 'login'  # Redirect unauthenticated users to login page
    def get(self, request):
        C_Details = User.objects.filter(id=request.user.id)
        data = Coustomer_Details.objects.filter(user=request.user) 
        form = CustomerDetailsForm()
        
        totalitem = 0
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user = request.user))
            totalwish = len(Wishlist.objects.filter(user = request.user))        
        context = {
            'C_Details': C_Details,
            'data': data,
            'form': form,
            
            'totalitem':totalitem,
            'totalwish':totalwish,
        }
        return render(request, 'profile.html', context)

    def post(self, request):
        
        if request.method == "POST":
            form = CustomerDetailsForm(request.POST)
            if form.is_valid():
                customer = form.save(commit=False)  
                customer.user = request.user 
                customer.save()  
                return redirect('profile') 

            
            
        data = Coustomer_Details.objects.filter(user=request.user)
        C_Details = User.objects.filter(id=request.user.id)
        form = CustomerDetailsForm()
        totalitem = 0
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user = request.user))
            totalwish = len(Wishlist.objects.filter(user = request.user))           

        context = {
            'C_Details': C_Details,
            'data': data,
            'form': form,
            'totalitem':totalitem,
            'totalwish':totalwish
        }
        return render(request, 'profile.html', context)


@login_required(login_url='login')
def Orders(request):



    orders = Order_Placed.objects.filter(user=request.user)

    totalitem = 0
    totalwish = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user = request.user))
        totalwish = len(Wishlist.objects.filter(user = request.user)) 
     
    context={
        'totalitem':totalitem,
        'totalwish':totalwish,
        'orders':orders
    }

    return render(request,'your_orders.html',context)

    


    

@login_required(login_url='login')  
def update_address(request, pk):
    totalitem = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user = request.user))
        totalwish = len(Wishlist.objects.filter(user = request.user)) 
    pi = Coustomer_Details.objects.get(pk=pk)

    if request.method == 'POST':
        form = CustomerDetailsForm(request.POST, instance=pi)
        if form.is_valid():
            form.save()
            return redirect('profile')  # Redirect after saving
    else:
        form = CustomerDetailsForm(instance=pi)  # Load form with instance data on GET request

    context = {
        'updateForm': form,
        'totalitem':totalitem,
        'totalwish':totalwish,
    }
    return render(request, 'update.html', context)

@login_required(login_url='login')
def delete_address(request,pk):
    if request.method =='POST':
        pi = Coustomer_Details.objects.get(id = pk) 
        pi.delete()
        return redirect('profile')
    return render(request,'profile')

@login_required(login_url='login')  
def add_to_cart(request):
    user = request.user
    product_id = request.GET.get('prod_id')
    product = Product.objects.get(id = product_id)
    Cart(user = user, product = product).save()
    return redirect('cart')


@login_required(login_url='login')  
def show_Cart(request):
    totalitem = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user = request.user))
        totalwish = len(Wishlist.objects.filter(user = request.user)) 
    user = request.user
    cart = Cart.objects.filter(user=user)
    amount = 0
    for p in cart:
        value = p.quantity * p.product.discount_price
        amount = amount + value
    totalamount = amount + 500
    context = {
        'cart':cart,
        'totalamount':totalamount,
        'amount':amount,
        'totalitem':totalitem,
        'totalwish':totalwish
    }
    return render(request, 'addtocart.html',context)





# def plus_cart(request):
#     if request.method == 'GET':
#         prod_id = request.GET['prod_id']
#         c= Cart.objects.get(Q(product = prod_id) & Q(user = request.user))
#         c.quantity +=1
#         c.save()
#         user = request.user
#         cart = Cart.objects.filter(user=user)
#         amount = 0
#         for p  in cart:
#             value = p.quantity * p.product.discount_price
#             amount = amount + value
#         totalamount = amount + 500
#         data = {
#             'quantity':c.quantity,
#             'amount':amount,
#             'totalamount':totalamount
#         }
#         return JsonResponse(data)


@login_required(login_url='login') 
def plus_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        try:
            c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))

            if c.quantity >= 2:
                return JsonResponse({'error': 'Maximum quantity limit reached (2 only).'})

            c.quantity += 1
            c.save()

            cart = Cart.objects.filter(user=request.user)
            amount = sum(item.quantity * item.product.discount_price for item in cart)
            totalamount = amount + 500

            return JsonResponse({
                'quantity': c.quantity,
                'amount': amount,
                'totalamount': totalamount
            })

        except Cart.DoesNotExist:
            return JsonResponse({'error': 'Cart item not found.'})


    
# def minus_cart(request):
#     if request.method == 'GET':
#         prod_id = request.GET['prod_id']
#         c= Cart.objects.get(Q(product = prod_id) & Q(user = request.user))
#         c.quantity -=1
#         c.save()
#         user = request.user
#         cart = Cart.objects.filter(user=user)
#         amount = 0
#         for p  in cart:
#             value = p.quantity * p.product.discount_price
#             amount = amount + value
#         totalamount = amount + 500
#         data = {
#             'quantity':c.quantity,
#             'amount':amount,
#             'totalamount':totalamount
#         }
#         return JsonResponse(data)

@login_required(login_url='login')  
def minus_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        try:
            c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))

            if c.quantity <= 1:
                return JsonResponse({'error': 'Minimum quantity is 1. You cannot reduce it further.'})

            c.quantity -= 1
            c.save()

            cart = Cart.objects.filter(user=request.user)
            amount = sum(item.quantity * item.product.discount_price for item in cart)
            totalamount = amount + 500

            return JsonResponse({
                'quantity': c.quantity,
                'amount': amount,
                'totalamount': totalamount
            })

        except Cart.DoesNotExist:
            return JsonResponse({'error': 'Cart item not found.'})

    
@login_required(login_url='login')  
def remove_cart(request):
    prod_id = request.GET.get('prod_id')
    user = request.user
    cart_item = Cart.objects.filter(user=user, product_id=prod_id)

    if cart_item.exists():
        cart_item.delete()

    # Recalculate totals after deletion
    cart_items = Cart.objects.filter(user=user)
    amount = 0
    for item in cart_items:
        amount += item.quantity * item.product.discount_price
    totalamount = amount + 500  # if you’re adding shipping

    return JsonResponse({
        'amount': amount,
        'totalamount': totalamount
    })






class Checkout(LoginRequiredMixin,View):
    login_url='login'

    def get(self, request):
        user = request.user
        add = Coustomer_Details.objects.filter(user=user)
        cart_items = Cart.objects.filter(user=user)
        totalitem = 0
        totalwish = 0
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user = request.user))
            totalwish = len(Wishlist.objects.filter(user = request.user))

        famount = 0
        for p in cart_items:
            value = p.quantity * p.product.discount_price
            famount += value

        shipping = 500  # flat shipping
        totalamount = famount + shipping
        razoramount = int(totalamount * 100)  # convert to paise

        # Razorpay integration
        client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
        data = {
            "amount": razoramount,
            "currency": "INR",
            "receipt": "order_rcptid_12"
        }
        payment_response = client.order.create(data=data)
        print(payment_response)

        order_id = payment_response['id']
        order_status = payment_response['status']

        if order_status == 'created':
            payment = Payment(
                user=user,
                amount=totalamount,
                razorpay_order_id=order_id  # Save order ID here, not payment ID
            )
            payment.save()

        context = {
            'add': add,
            'totalitem':totalitem,
            'totalwish':totalwish,
            'totalamount': totalamount,
            'cart_items': cart_items,
            'order_id': order_id,  # Pass to template for frontend checkout
            'razorpay_key': settings.RAZORPAY_KEY_ID,  # Needed for JS Razorpay checkout
        }

        return render(request, 'checkout.html', context)





@csrf_exempt
def paymenthandler(request):
    if request.method == "POST":
        try:
            # Get Razorpay payment details from the POST request
            payment_id = request.POST.get('razorpay_payment_id')
            order_id = request.POST.get('razorpay_order_id')
            signature = request.POST.get('razorpay_signature')

            # Fetch the Payment object
            payment = Payment.objects.get(razorpay_order_id=order_id)

            # Initialize Razorpay client
            client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
            
            # Prepare the dictionary for verification
            params_dict = {
                'razorpay_order_id': order_id,
                'razorpay_payment_id': payment_id,
                'razorpay_signature': signature
            }

            # Signature verification
            client.utility.verify_payment_signature(params_dict)

            # Mark payment as successful
            payment.razorpay_payment_id = payment_id
            payment.razorpay_signature = signature
            payment.paid = True
            payment.save()

            # Place orders and clear cart
            cart_items = Cart.objects.filter(user=request.user)
            for item in cart_items:
                customer = Coustomer_Details.objects.filter(user=request.user).first()  # Get the user's customer details
                Order_Placed.objects.create(
                    user=request.user,
                    full_address= str(customer),
                    product=item.product,
                    quantity=item.quantity,
                    payment=payment

                )
                item.delete()

            return render(request, 'payment_success.html')

        except Exception as e:
            print("Payment verification failed:", e)
            return render(request, 'payment_failure.html')

    else:
        return HttpResponseBadRequest("Invalid request method.")


# def paymentsuccess(request):
#     return render(request, 'payment_success.html')




@login_required(login_url='login')  
def wishlist_view(request):
    totalitem = 0
    totalwish = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user = request.user))
        totalwish = len(Wishlist.objects.filter(user = request.user))

    
    wishlist_items = Wishlist.objects.filter(user=request.user)

    context = {
        'wishlist_items': wishlist_items,
        'totalitem':totalitem,
        'totalwish':totalwish,
        

    }
    return render(request, 'wishlist.html',context)



def plus_wishlist(request):
    if request.method == "GET":
        prod_id = request.GET['prod_id']
        product = Product.objects.get(id = prod_id)
        user = request.user
        Wishlist(user= user, product=product).save()
        data={
            'message':'Wishlist Added Successfully',
        }  
        return JsonResponse(data)  
    
    
def minus_wishlist(request):
    if request.method == "GET":
        prod_id = request.GET['prod_id']
        product = Product.objects.get(id = prod_id)
        user = request.user
        Wishlist.objects.filter(user=user, product=product).delete()
        data={
            'message':'Wishlist Remove Successfully',
        }  
        return JsonResponse(data)  

