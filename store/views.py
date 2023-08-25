from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Product, Asset, Collection


# Create your views here.
@login_required(login_url='login')
def index(request):
    products = Product.objects.prefetch_related('collection').all()
    collections = Collection.objects.prefetch_related('asset').all()
    # products = Product.objects.select_related('Collection').prefetch_related('Asset').all()
    return render(request, 'index.html', {'products': products, 'collections':collections})


def u_register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'You have been registered')
            return redirect('login')
    else:
        form = UserCreationForm()

    return render(request, 'registration/register.html', {'form': form})


def u_login(request):
    return render(request, 'registration/login.html')


def about(request):
    return render(request, 'about.html')
