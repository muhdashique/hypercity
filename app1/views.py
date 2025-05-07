from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Customer
from .forms import CustomerForm

def login(request):
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
    
    return render(request, 'login.html')

@login_required
def dashboard(request):
    customers = Customer.objects.all()
    context = {
        'username': request.user.username,
        'customers': customers
    }
    return render(request, 'dashboard.html', context)

@login_required
def add_data(request):
    if request.method == 'POST':
        form = CustomerForm(request.POST)
        if form.is_valid():
            customer = form.save(commit=False)
            # Store just the username string
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
    return render(request, 'add_data.html', context)

def logout(request):
    auth_logout(request)
    messages.success(request, "You have been logged out successfully.")
    return redirect('login')





from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Customer
from django.urls import reverse
from django.http import HttpResponseRedirect

@login_required
def dashboard(request):
    """
    Display the dashboard with customer data
    """
    customers = Customer.objects.all().order_by('-created_at')
    context = {
        'customers': customers,
        'username': request.user.username,
    }
    return render(request, 'dashboard.html', context)

@login_required
def add_customer(request):
    """
    Add a new customer using the modal form
    """
    if request.method == 'POST':
        name = request.POST.get('name')
        place = request.POST.get('place')
        phone_number = request.POST.get('phone_number')
        card_number = request.POST.get('card_number')
        
        # Create new customer
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
    
    # If someone tries to access this URL directly without POST data
    return redirect('dashboard')

@login_required
def edit_customer(request, customer_id):
    """
    Edit an existing customer using the modal form
    """
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

@login_required
def delete_customer(request, customer_id):
    """
    Delete a customer after confirmation
    """
    customer = get_object_or_404(Customer, id=customer_id)
    customer_name = customer.name
    
    if request.method == 'POST':
        customer.delete()
        messages.success(request, f'Customer "{customer_name}" deleted successfully!')
        return redirect('dashboard')
    
    # If someone tries to access this URL directly without POST data
    return redirect('dashboard')









