from django.shortcuts import render
from django.http import JsonResponse
import json
import datetime
from .models import * 
from .utils import cookieCart, cartData, guestOrder
from django.shortcuts import render,redirect
from django.shortcuts import render
from django.http import HttpResponse
from django.forms import inlineformset_factory
from .forms import OrderForm,UserCreation,CustomerForm
from .formsc import CustomerForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.contrib.auth.models import User

@login_required(login_url='login')
def store(request):
	data = cartData(request)

	cartItems = data['cartItems']
	order = data['order']
	items = data['items']

	products = Product.objects.all()
	products1 = Product.objects.filter(category='1')
	products2 = Product.objects.filter(category='2')
	products3 = Product.objects.filter(category='3')
	context = {'products':products, 'cartItems':cartItems,'products1':products1,'products2':products2,'products3':products3}
	return render(request, 'store/store.html', context)
def accountpage(request):
	customer = request.user.customer
	form = CustomerForm(instance=customer)

	if request.method == 'POST':
		form = CustomerForm(request.POST, request.FILES,instance=customer)
		if form.is_valid():
			form.save()


	context = {'form':form}
	return render(request,'store/account.html',context)

@login_required(login_url='login')
def cart(request):
	data = cartData(request)

	cartItems = data['cartItems']
	order = data['order']
	items = data['items']

	context = {'items':items, 'order':order, 'cartItems':cartItems}
	return render(request, 'store/cart.html', context)
def payment(request):
	return render(request,'store/payment.html')
def homepage(request):
	
	return render(request,'store/homepage.html')

def loginPage(request):
	if request.method=="POST":
		username=request.POST.get('username')
		password=request.POST.get('password')
		user = authenticate(request,username = username,password=password)
		if user is not None:
			login(request,user)
			return redirect('store')
		else:
			messages.info(request,'Username OR Password is incorrect')
	
	return render(request,'store/login.html')
def logoutUser(request):
    logout(request)
    return redirect('login')

def register(request):
	form = UserCreation()
	
	if request.method=="POST":
		form = UserCreation(request.POST)
		if form.is_valid():
			form.save()
			Customer
			user = form.cleaned_data.get('username')

			messages.success(request, 'Congratulations '+user+ ' ,You are now registered')
			
			return redirect('login')

			
	context = {'form':form}
	return render(request,'store\Register.html',context)

@login_required(login_url='login')
def checkout(request):
	data = cartData(request)
	
	cartItems = data['cartItems']
	order = data['order']
	items = data['items']

	context = {'items':items, 'order':order, 'cartItems':cartItems}
	return render(request, 'store/checkout.html', context)

def updateItem(request):
	data = json.loads(request.body)
	productId = data['productId']
	action = data['action']
	print('Action:', action)
	print('Product:', productId)

	customer = request.user
	product = Product.objects.get(id=productId)
	order, created = Order.objects.get_or_create(customer=customer, complete=False)

	orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

	if action == 'add':
		orderItem.quantity = (orderItem.quantity + 1)
	elif action == 'remove':
		orderItem.quantity = (orderItem.quantity - 1)

	orderItem.save()

	if orderItem.quantity <= 0:
		orderItem.delete()

	return JsonResponse('Item was added', safe=False)

def processOrder(request):
	transaction_id = datetime.datetime.now().timestamp()
	data = json.loads(request.body)

	if request.user.is_authenticated:
		customer = request.user
		order, created = Order.objects.get_or_create(customer=customer, complete=False)


	total = float(data['form']['total'])
	order.transaction_id = transaction_id

	if total == order.get_cart_total:
		order.complete = True
	order.save()

	if order.shipping == True:
		ShippingAddress.objects.create(
		customer=customer,
		order=order,
		address=data['shipping']['address'],
		city=data['shipping']['city'],
		state=data['shipping']['state'],
		zipcode=data['shipping']['zipcode'],
		)

	return JsonResponse('Payment submitted..', safe=False)