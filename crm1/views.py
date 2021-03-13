from django.shortcuts import render, redirect
from .models import *
from .forms import *
from .filters import *
from django.contrib import messages
from django.contrib.auth import login,authenticate,logout
from django.contrib.auth.decorators import login_required
# Create your views here.


def signin(request):
    if request.user.is_authenticated:
        return redirect("home")
    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(request, username=username, password=password)   
            if user is not None:
                login(request, user)
                return redirect('home')

            else:
                messages.info(request, "Username or Password is incorrect")

        context ={}
        return render(request,'crm1/signin.html',context)


def signout(request):
    logout(request)
    return redirect("login")

def signup(request):
    if request.user.is_authenticated:
        return redirect("home")
    else:
        form = CreateUserForm()
        if request.method == "POST":
            form = CreateUserForm(request.POST)

            if form.is_valid():
                form.save()
                user = form.cleaned_data.get("username")
                messages.success(request, user + " Successfully created")
                return redirect("login")

        context = {"form": form}
        return render(request, 'crm1/signup.html', context)

@login_required(login_url='login')
def dashboard(request):

    customers = Customer.objects.all()
    orders = Order.objects.all()
    total_orders = orders.count()
    pending_orders = orders.filter(status="Pending").count()
    delivered_orders = orders.filter(status="Delivered").count()

    context = {"customers": customers, "orders": orders,
               "total": total_orders,
               "pending": pending_orders,
               "delivered": delivered_orders,
               }

    return render(request, 'crm1/dashboard.html', context)

@login_required(login_url='login')
def product(request):

    products = Product.objects.all()
    return render(request, 'crm1/product.html', {"products": products})

@login_required(login_url='login')
def customer(request, pk):

    req_customer = Customer.objects.get(id=pk)
    order = req_customer.order_set.all()
    orderfilter= OrderFilter(request.GET, queryset= order)
    order= orderfilter.qs
    total_count = order.count()

    context = {"customer": req_customer, "order": order, "count": total_count,
                "orderfilter":orderfilter}
    return render(request, 'crm1/customer.html', context)

@login_required(login_url='login')
def create_order(request,pk):
    customer=Customer.objects.get(id=pk) 
    order = OrderForm(initial={'customer':customer})
    if request.method == "POST":
        order = OrderForm(request.POST)
        if order.is_valid():
            order.save()
            return redirect('customer',pk)

    context = {"form": order}
    return render(request, 'crm1/create_order.html', context)

@login_required(login_url='login')
def update_order(request, pk):
    order = Order.objects.get(id=pk)
    order_form = OrderForm(instance=order)
    if request.method == "POST":
        order = OrderForm(request.POST, instance=order)
        if order.is_valid():
            order.save()
            return redirect('/')

    context = {"form": order_form}

    return render(request, 'crm1/update_order.html', context)
@login_required(login_url='login')
def remove_order(request,pk):
    order= Order.objects.get(id=pk)

    context ={"item":order}

    if request.method == 'POST':
        order.delete()
        return redirect('/')
    
    return render(request, 'crm1/remove_order.html',context)
