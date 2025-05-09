from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.views.decorators.cache import never_cache

from .models import Customer
from .forms import CustomerForm

def login(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            auth_login(request, user)
            messages.success(request, f"Welcome {username}!")
            return redirect('dashboard')
        else:
            messages.error(request, "Invalid username or password.")
    
    response = render(request, 'login.html')
    response['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response['Pragma'] = 'no-cache'
    response['Expires'] = '0'
    return response

@never_cache
@login_required(login_url='login')
def dashboard(request):
    """
    Display the dashboard with customer data
    """
    if not request.user.is_authenticated:
        return redirect('login')
        
    customers = Customer.objects.all().order_by('-created_at')
    from django.contrib.auth.models import User
    superusers = User.objects.filter(is_superuser=True)
    
    context = {
        'customers': customers,
        'username': request.user.username,
        'all_users': superusers,  
    }
    
    response = render(request, 'dashboard.html', context)
    response['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response['Pragma'] = 'no-cache'
    response['Expires'] = '0'
    return response

@never_cache
@login_required(login_url='login')
def add_data(request):
    if not request.user.is_authenticated:
        return redirect('login')
        
    if request.method == 'POST':
        form = CustomerForm(request.POST)
        if form.is_valid():
            customer = form.save(commit=False)
            customer.added_by = request.user.username
            customer.save()
            messages.success(request, "Customer data added successfully!")
            return redirect('dashboard')
    else:
        form = CustomerForm()
    
    context = {
        'username': request.user.username,
        'form': form
    }
    
    response = render(request, 'add_data.html', context)
    response['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response['Pragma'] = 'no-cache'
    response['Expires'] = '0'
    return response

def logout(request):
    auth_logout(request)
    messages.success(request, "You have been logged out successfully.")
    response = redirect('login')
    response['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response['Pragma'] = 'no-cache'  
    response['Expires'] = '0'
    return response

@never_cache
@login_required(login_url='login')
def add_customer(request):
    if not request.user.is_authenticated:
        return redirect('login')
        
    if request.method == 'POST':
        name = request.POST.get('name')
        place = request.POST.get('place')
        phone_number = request.POST.get('phone_number')
        card_number = request.POST.get('card_number') or None
        
        customer = Customer(
            name=name,
            place=place,
            phone_number=phone_number,
            card_number=card_number,
            added_by=request.user.username
        )
        customer.save()

        messages.success(request, f'Customer "{name}" added successfully!')
        return redirect('dashboard')
    
    return redirect('dashboard')

@never_cache
@login_required(login_url='login')
def edit_customer(request, customer_id):
    """
    Edit an existing customer using the modal form
    """
    if not request.user.is_authenticated:
        return redirect('login')
        
    customer = get_object_or_404(Customer, id=customer_id)
    
    if request.method == 'POST':
        customer.name = request.POST.get('name')
        customer.place = request.POST.get('place')
        customer.phone_number = request.POST.get('phone_number')
        customer.card_number = request.POST.get('card_number')
        customer.save()
        
        messages.success(request, f'Customer "{customer.name}" updated successfully!')
        return redirect('dashboard')
    
    # If someone tries to access this URL directly without POST data
    return redirect('dashboard')

@never_cache
@login_required(login_url='login')
def delete_customer(request, customer_id):
    """
    Delete a customer after confirmation
    """
    if not request.user.is_authenticated:
        return redirect('login')
        
    customer = get_object_or_404(Customer, id=customer_id)
    customer_name = customer.name
    
    if request.method == 'POST':
        customer.delete()
        messages.success(request, f'Customer "{customer_name}" deleted successfully!')
        return redirect('dashboard')
    
    return redirect('dashboard')