import datetime
from random import shuffle, random
import uuid
from django.contrib import messages
from django.http import HttpResponse
from instamojo_wrapper import Instamojo
from django.db.models import Q
from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,logout,login
from .models import *
from django.conf import settings
from django.utils import timezone
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from .models import Cart, Booking, Status, Profile

from django.utils import timezone
import uuid  # to generate unique booking_id


# Create your views here.

def Home(request):
    search = request.GET.get('search',0)
    search_pro = Product.objects.filter(Q(name__icontains = search) | Q(category__name__icontains = search))
    cat = ""
    pro = ""
    cat = ""
    num = 0
    num1 = 0
    cat = Category.objects.all()
    pro = Product.objects.all()
    num = []
    num1 = 0
    product = None
    try:
        user = User.objects.get(id=request.user.id)
        profile = Profile.objects.get(user=user)
        cart = Cart.objects.filter(profile=profile)
        product = recommended_product(request)
        for i in cart:
            num1 += 1

    except:
        pass
    a = 1
    li = []

    for j in pro:
        b = 1
        for i in cat:
            if i.name == j.category.name:
                if not j.category.name in li:
                    li.append(j.category.name)
                    if b == 1:
                        num.append(a)
                        b = 2
        a += 1


    d = {'pro': pro, 'cat': cat,'num':num,'num1':num1, 'product':product, 'search_pro':search_pro}
    return render(request, 'all_product.html', d)
	

def About(request):
    return render(request, 'about.html')

def Contact(request):
    return render(request, 'contact.html')	
	
	
def Signup(request):
    if request.method == 'POST':
        u = request.POST['uname']
        f = request.POST['fname']
        l = request.POST['lname']
        p = request.POST['pwd']
        d = request.POST['date']
        c = request.POST['city']
        ad = request.POST['add']
        e = request.POST['email']
        i = request.FILES['img']
        con = request.POST['contact']
        t = request.POST['type']
        user = User.objects.create_user(username=u, email=e, password=p, first_name=f,last_name=l)
        Profile.objects.create(user=user, dob=d, city=c, address=ad, contact=con,image=i, user_type=t)
        messages.success(request, "Registeration Successfully")
        return redirect('login')
    return render(request, 'signup.html')


def Login(request):
    if request.method == "POST":
        u = request.POST['uname']
        p = request.POST['pwd']
        user = authenticate(username=u, password=p)
        
        if user:
            if not user.is_staff:
                profile = Profile.objects.get(user=user)
                if profile.user_type == "Seller" and profile.status == "Approved":
                    login(request, user)
                    messages.success(request, "Logged in Successfully")
                    return redirect('home')
                elif profile.user_type == "Seller" and profile.status == "Pending":
                    messages.error(request, "Farmer verification pending. Try again later.")
                elif profile.user_type == "Buyer":
                    login(request, user)
                    messages.success(request, "Logged in Successfully")
                    return redirect('home')
            else:
                messages.error(request, "Invalid credentials for user.")
        else:
            messages.error(request, "Invalid credentials.")
    return render(request, 'login.html')


def Admin_Login(request):
    error = ""
    if request.method == "POST":
        u = request.POST['uname']
        p = request.POST['pwd']
        user = authenticate(username=u, password=p)
        try:
            if user.is_staff:
                login(request, user)
                error = "yes"
            else:
                error = "not"
        except:
            error="not"
    d = {'error': error}
    return render(request,'loginadmin.html',d)


def Logout(request):
    logout(request)
    messages.success(request, 'Logout Successfully')
    return redirect('home')


def View_user(request):
    if not request.user.is_authenticated:
        return redirect('login_admin')
    pro = Profile.objects.filter(user_type="Buyer")
    d = {'user':pro}
    return render(request,'view_user.html',d)

def View_farmer(request):
    if not request.user.is_authenticated:
        return redirect('login_admin')
    pro = Profile.objects.filter(user_type="Seller")
    d = {'user':pro, 'data':'farmer'}
    return render(request,'view_user.html',d)


def Add_Product(request):
    if not request.user.is_authenticated:
        return redirect('login_admin')
        
    cat = Category.objects.all()
    error = False
    
    if request.method == "POST":
        try:
            c = request.POST['cat']
            p = request.POST['pname']
            pr = request.POST['price']
            i = request.FILES.get('img')
            d = request.POST['desc']

            if not i:
                return HttpResponse("Please upload an image.")

            ct = Category.objects.get(name=c)
            Product.objects.create(
                category=ct,
                name=p,
                price=pr,
                image=i,
                desc=d,
                user=request.user
            )
            error = True
        except Exception as e:
            return HttpResponse(f"Error: {e}")
    
    return render(request, 'add_product.html', {'cat': cat, 'error': error})



def All_product(request):
    if not request.user.is_authenticated:
        return redirect('login')
    user = User.objects.get(id=request.user.id)
    profile = Profile.objects.get(user=user)
    cart = Cart.objects.filter(profile=profile)
    num1=0
    for i in cart:
        num1 += 1
    cat = Category.objects.all()
    pro = Product.objects.all()
    d ={'pro':pro,'cat':cat,'num1':num1}
    return render(request,'all_product.html',d)


def Admin_View_Booking(request):
    if not request.user.is_authenticated:
        return redirect('login_admin')
    book = Booking.objects.all()
    d = {'book': book}
    return render(request, 'admin_viewBokking.html', d)


def View_feedback(request):
    if not request.user.is_authenticated:
        return redirect('login_admin')
    feed = Send_Feedback.objects.all()
    d = {'feed': feed}
    return render(request, 'view_feedback.html', d)


def View_prodcut(request,pid):
    if not request.user.is_authenticated:
        return redirect('login_admin')
    cat = ""
    cat1 = ""
    pro1 = ""
    num1 = 0
    user=""
    profile=""
    cart=""
    pro=""
    num=""
    if not request.user.is_staff:
        user = User.objects.get(id=request.user.id)
        profile = Profile.objects.get(user=user)
        cart = Cart.objects.filter(profile=profile)
        for i in cart:
            num1 += 1

    if pid == 0:
        cat = "All Product"
        pro1 = Product.objects.all()
    else:
        cat1 = Category.objects.get(id=pid)
        pro1 = Product.objects.filter(category=cat1).all()
    cat = Category.objects.all()
    pro = Product.objects.all()
    num = []
    b = 1
    for j in cat:
        a = 1
        for i in pro:
            if j.name == i.category.name:
                if a == 1:
                    num.append(i.id)
                    a = 2
    d = {'pro': pro, 'cat': cat,'cat1': cat1,'num':num,'pro1':pro1,'num1':num1}
    return render(request, 'view_product.html',d)


def Add_Categary(request):
    if not request.user.is_authenticated:
        return redirect('login_admin')
    error=False
    if request.method=="POST":
        n = request.POST['cat']
        Category.objects.create(name=n)
        error=True
    d = {'error':error}
    return render(request, 'add_category.html', d)


def View_Categary(request):
    if not request.user.is_authenticated:
        return redirect('login_admin')
    pro = Category.objects.all()
    d = {'pro': pro}
    return render(request,'view_category.html', d)



def View_Booking(request):
    user = User.objects.get(id=request.user.id)
    profile = Profile.objects.get(user=user)
    cart = Cart.objects.filter(profile=profile)
    book = Booking.objects.filter(profile=profile)
    if profile.user_type == "Seller":
        book = Booking.objects.filter(farmer__icontains=request.user.username)
    pro = recommended_product(request)
    num1=0
    for i in cart:
        num1 += 1
    d = {'book': book,'num1':num1, 'pro':pro}
    return render(request, 'view_booking.html', d)


def Feedback(request, pid):
    if not request.user.is_authenticated:
        return redirect('login')
    error = False
    user1 = User.objects.get(id=request.user.id)
    profile = Profile.objects.get(user=user1)
    cart = Cart.objects.filter(profile=profile)
    num1 =0
    for i in cart:
        num1 += 1
    date1 = date.today()
    user = User.objects.get(id=pid)
    pro = Profile.objects.filter(user=user).first()
    if request.method == "POST":
        d = request.POST['date']
        u = request.POST['uname']
        e = request.POST['email']
        con = request.POST['contact']
        m = request.POST['desc']
        user = User.objects.filter(username=u, email=e).first()
        pro = Profile.objects.filter(user=user, contact=con).first()
        Send_Feedback.objects.create(profile=pro, date=d, message1=m)
        error = True
    d = {'pro': pro, 'date1': date1,'num1':num1,'error':error}
    return render(request, 'feedback.html', d)

def Change_Password(request):
    if not request.user.is_authenticated:
        return redirect('login')
    error = ""
    num1=0
    user = User.objects.get(id=request.user.id)
    profile = Profile.objects.get(user=user)
    cart = Cart.objects.filter(profile=profile)
    for i in cart:
        num1 += 1
    if request.method=="POST":
        n = request.POST['pwd1']
        c = request.POST['pwd2']
        o = request.POST['pwd3']
        if c == n:
            u = User.objects.get(username__exact=request.user.username)
            u.set_password(n)
            u.save()
            error = "yes"
        else:
            error = "not"
    d = {'error':error,'num1':num1}
    return render(request,'change_password.html',d)

def Add_Cart(request,pid):
    if not request.user.is_authenticated:
        return redirect('login')
    if request.method=="POST":
        user = User.objects.get(id=request.user.id)
        profile = Profile.objects.get(user=user)
        product = Product.objects.get(id=pid)
        Cart.objects.create(profile=profile, product=product)
        return redirect('cart')

def recommended_product(request):
    user = User.objects.get(id=request.user.id)
    profile = Profile.objects.get(user=user)
    book = Booking.objects.filter(profile=profile).order_by('-id')[:2]
    recommend = []
    for i in book:
        recommend+=i.booking_id.split('.')[1:]
    pro1 = Product.objects.filter(id__in=recommend)
    cat = []
    for i in pro1:
        if not i.category.id in cat:
            cat.append(i.category.id)
    pro = Product.objects.filter(category__id__in=cat).order_by('?')
    return pro


def view_cart(request):
    if not request.user.is_authenticated:
        return redirect('login')
    user = User.objects.get(id=request.user.id)
    profile = Profile.objects.get(user=user)
    cart =  Cart.objects.filter(profile=profile).all()

    pro = recommended_product(request)
    total=0
    num1=0
    book_id=request.user.username
    message1="Here ! No Any Product"
    for i in cart:
        total+=i.product.price
        num1+=1
        book_id = book_id+"."+str(i.product.id)
    d = {'profile':profile,'cart':cart,'total':total,'num1':num1,'book':book_id,'message':message1,'pro':pro}
    return render(request,'cart.html',d)


def remove_cart(request,pid):
    if not request.user.is_authenticated:
        return redirect('login')
    cart = Cart.objects.get(id=pid)
    cart.delete()
    return redirect('cart')

from datetime import date
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from .models import Profile, Cart, Booking, Status

def Booking_order(request, pid):
    if not request.user.is_authenticated:
        return redirect('login')

    stage = request.GET.get('stage')
    total_price = request.GET.get('total_price')
    data1 = User.objects.get(id=request.user.id)
    data = Profile.objects.filter(user=data1).first()
    cart = Cart.objects.filter(profile=data).all()

    total = 0
    num1 = 0
    farmer = []

    for i in cart:
        total += i.product.price
        farmer.append(i.product.user.username)

    user1 = data1.username
    li = pid.split('.')
    li2 = []
    for j in li:
        if user1 != j:
            li2.append(int(j))
            num1 += 1

    date1 = date.today()

    if request.method == "POST":
        d = request.POST['date1']
        c = request.POST['name']
        c1 = request.POST['city']
        ad = request.POST['add']
        e = request.POST['email']
        con = request.POST['contact']
        b = request.POST['book_id']
        t = request.POST['total']

        try:
            user = User.objects.get(username=c)
        except User.DoesNotExist:
            return HttpResponse("User not found.")

        profile = Profile.objects.get(user=user)

        try:
            status = Status.objects.get(name="pending")
        except Status.DoesNotExist:
            return HttpResponse("Status 'pending' not found. Please add it in the database.")

        book1 = Booking.objects.create(
            profile=profile,
            book_date=d,
            booking_id=b,
            total=t,
            quantity=num1,
            status=status,
            farmer=farmer
        )

        cart2 = Cart.objects.filter(profile=profile).all()
        cart2.delete()

        return redirect('payment', book1.id)

    context = {
        'data': data,
        'data1': data1,
        'book_id': pid,
        'date1': date1,
        'total': total,
        'num1': num1
    }
    return render(request, 'booking.html', context)



def payment(request,book):
    if not request.user.is_authenticated:
        return redirect('login')
    error = False
    book = Booking.objects.get(id=book)
    user = User.objects.get(id=request.user.id)
    profile= Profile.objects.get(user=user)
    cart = Cart.objects.filter(profile = profile).all()
    if request.method=="POST":
        error=True
    d ={'total':book.total,'error':error,'book':book}
    return render(request,'payment2.html',d)


def delete_admin_booking(request, pid,bid):
    if not request.user.is_authenticated:
        return redirect('login_admin')
    book = Booking.objects.get(booking_id=pid,id=bid)
    book.delete()
    return redirect('admin_viewBooking')

def delete_booking(request, pid,bid):
    if not request.user.is_authenticated:
        return redirect('login')
    book = Booking.objects.get(booking_id=pid,id=bid)
    book.delete()
    return redirect('view_booking')

def delete_user(request, pid):
    if not request.user.is_authenticated:
        return redirect('login_admin')
    user = User.objects.get(id=pid)
    user.delete()
    return redirect('view_user')

def delete_feedback(request, pid):
    if not request.user.is_authenticated:
        return redirect('login_admin')
    feed = Send_Feedback.objects.get(id=pid)
    feed.delete()
    return redirect('view_feedback')


def booking_detail(request, pid, bid):
    if not request.user.is_authenticated:
        return redirect('login')

    profile = Profile.objects.get(user=request.user)
    try:
        booking = Booking.objects.get(booking_id=pid, id=bid, profile=profile)
    except Booking.DoesNotExist:
        messages.error(request, "Booking not found.")
        return redirect('view_booking')

    # Now this works:
    booked_items = booking.booking_products.all()

    context = {
        'profile': profile,
        'booking': booking,
        'booked_items': booked_items,
        'total': booking.total,
    }
    return render(request, 'booking_detail.html', context)


def admin_booking_detail(request,pid,bid,uid):
    if not request.user.is_authenticated:
        return redirect('login_admin')
    user = User.objects.get(id=uid)
    profile = Profile.objects.get(user=user)
    cart =  Cart.objects.filter(profile=profile).all()
    product = Product.objects.all()
    book = Booking.objects.get(booking_id=pid, id=bid)
    total=0
    num1=0
    user1 = book.profile.user.username
    li = book.booking_id.split('.')
    li2=[]
    for j in li:
        if user1!= j :
            li2.append(int(j))
    for i in cart:
        total+=i.product.price
        num1+=1
    d = {'profile':profile,'cart':cart,'total':total,'num1':num1,'book':li2,'product':product,'total':book}
    return render(request,'admin_view_booking_detail.html',d)

def Edit_status(request,pid,bid):
    if not request.user.is_authenticated:
        return redirect('login_admin')
    book = Booking.objects.get(booking_id=pid,id=bid)
    stat = Status.objects.all()
    if request.method == "POST":
        n = request.POST['book']
        s = request.POST['status']
        book.booking_id = n
        sta = Status.objects.filter(name=s).first()
        book.status = sta
        book.save() 
        return redirect('admin_viewBooking')
    d = {'book': book, 'stat': stat}
    return render(request, 'status.html', d)


def Admin_View_product(request):
    if not request.user.is_authenticated:
        return redirect('login_admin')

    pro = Product.objects.all()
    try:
        profile = Profile.objects.get(user=request.user)
        if profile.user_type == "Seller":
            pro = Product.objects.filter(user=request.user)
    except: 
        pass 
    d = {'pro':pro}
    return render(request,'admin_view_product.html',d)

def delete_product(request,pid):
    if not request.user.is_authenticated:
        return redirect('login_admin')
    pro = Product.objects.get(id=pid)
    pro.delete()
    return redirect('admin_view_product')

from django.shortcuts import get_object_or_404

def profile(request, pid):
    if not request.user.is_authenticated:
        return redirect('login')

    user = get_object_or_404(User, id=pid)
    pro, _ = Profile.objects.get_or_create(user=user)   # ensures a profile exists

    cart = Cart.objects.filter(profile=pro)
    total = sum(item.product.price for item in cart)
    num1  = cart.count()

    context = {'pro': pro, 'user': user, 'num1': num1, 'total': total}
    return render(request, 'profile.html', context)

def farmer_detail(request, pid):
    if not request.user.is_authenticated:
        return redirect('login')
    book = Booking.objects.get(id=pid)
    username = book.farmer[1:][:-1].replace(" ", "")
    if ',' in username:
        username = username.split(',')
    else:
        username = [username] 
    print("All User before = ", username)
    all_user = [i[1:][:-1] for i in username]
    print("My Ysername", all_user)
    all_profile = Profile.objects.filter(user__username__in=all_user)
    d={ 'all_profile':all_profile}
    return render(request,'farmer_detail.html',d)


from django.contrib import messages

from django.contrib import messages  # make sure this is imported

def Edit_profile(request):
    if not request.user.is_authenticated:
        return redirect('login')

    user = User.objects.get(id=request.user.id)
    pro = Profile.objects.get(user=user)
    cart = Cart.objects.filter(profile=pro)  # fixed: use filter

    num1 = 0   
    total = 0
    for i in cart:
        total += i.product.price
        num1 += 1

    if request.method == 'POST':
        f = request.POST['fname']
        l = request.POST['lname']
        u = request.POST['uname']
        c = request.POST['city']
        ad = request.POST['add']
        e = request.POST['email']
        con = request.POST['contact']
        d = request.POST['date']

        # handle optional image upload
        if 'img' in request.FILES:
            pro.image = request.FILES['img']

        if d:
            pro.dob = d

        # update user and profile details
        pro.user.username = u
        pro.user.first_name = f
        pro.user.last_name = l
        pro.user.email = e
        pro.contact = con
        pro.city = c
        pro.address = ad
        pro.user.save()
        pro.save()

        messages.success(request, "Profile updated successfully.")
        return redirect('profile', pid=pro.user.id)  # Corrected here


    d = {'pro': pro, 'num1': num1, 'total': total}
    return render(request, 'edit_profile.html', d)


def Admin_Home(request):
    if not request.user.is_authenticated:
        return redirect('login_admin')
    book = Booking.objects.all()
    customer = Profile.objects.filter(user_type="Buyer")
    seller = Profile.objects.filter(user_type="Seller")
    pro = Product.objects.all()
    total_book = 0
    total_customer = 0
    total_pro = 0
    for i in book:
        total_book+=1
    for i in customer:
        total_customer+=1
    for i in pro:
        total_pro+=1
    d = {'total_pro':total_pro,'total_customer':total_customer,'total_book':total_book, 'seller':seller.count()}
    return render(request,'admin_home.html',d)

def delete_category(request,pid):
    if not request.user.is_authenticated:
        return redirect('login_admin')
    cat = Category.objects.get(id=pid)
    cat.delete()
    return redirect('view_categary')

def change_user_status(request, pid):
    if not request.user.is_authenticated:
        return redirect('login_admin')
    pro = Profile.objects.get(id=pid)
    if pro.status == "Pending":
        pro.status = "Approved"
    else:
        pro.status = "Pending"
    pro.save()
    messages.success(request, "Status Changed Successfully")
    return redirect('view_farmer')

from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

@login_required
def payment_page(request):
    if request.method == 'POST':
        total = request.POST.get('total')
        try:
            #cart = get_object_or_404(Cart, id=cart_id, profile__user=request.user)
            profile = Profile.objects.get(user=request.user)
            cart = Cart.objects.filter(profile=profile).first()
        except Profile.DoesNotExist:
            return redirect('cart')

        if not cart:
            return redirect('cart')

        return render(request, 'payment.html', {
            'total': total,
            'cart': cart
        })

    return redirect('cart')



from django.utils import timezone
import uuid
from .models import Cart, Booking, Status, Profile

@login_required
def cash_on_delivery(request, cart_id):
    profile = Profile.objects.get(user=request.user)

    cart_items = Cart.objects.filter(profile=profile)
    if not cart_items.exists():
        messages.error(request, "Your cart is empty.")
        return redirect('cart')

    total = sum(item.product.price for item in cart_items if item.product and item.product.price)

    # Get the Farmer instance associated with the logged-in user
   # farmer_instance = Farmer.objects.get(user=request.user)

    booking = Booking.objects.create(
        profile=profile,              # associate profile
        #farmer=farmer_instance,       # pass Farmer model instance, not username string
        booking_id=str(uuid.uuid4()),
        total=total,
        status=Status.objects.get(name="Pending"),
        payment_status="Pending",
        book_date=timezone.now().date()
    )
    
    cart_items.delete()

    messages.success(request, "Booking placed successfully with Cash On Delivery.")
    return redirect('view_booking')


def product_detail(request, pid):
    if not request.user.is_authenticated:
        return redirect('login')
    data = Product.objects.get(id=pid)
    data1 = Profile.objects.get(user=request.user)
    latest = Product.objects.filter(category=data.category).exclude(user=request.user).order_by('-id')[:4]
    return render(request, 'product_detail.html', {'data': data,'data1':data1, 'latest': latest})

