from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import CO2ConsumptionForm
from .models import CO2Consumption


def home(request):
    return render(request, 'counter/home.html')


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()

    for field in form.fields.values():
        field.widget.attrs['class'] = 'input'

    return render(request, 'counter/register.html', {'form': form})


def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
    else:
        form = AuthenticationForm()

    for field in form.fields.values():
        field.widget.attrs['class'] = 'input'

    return render(request, 'counter/login.html', {'form': form})


def user_logout(request):
    logout(request)
    messages.info(request, "You have successfully logged out.")
    return redirect('home')


@login_required
def add_co2_consumption(request):
    try:
        consumption = CO2Consumption.objects.get(user=request.user)
    except CO2Consumption.DoesNotExist:
        consumption = None

    if request.method == 'POST':
        form = CO2ConsumptionForm(request.POST, instance=consumption)
        if form.is_valid():
            consumption = form.save(commit=False)
            consumption.user = request.user
            consumption.save()
            messages.success(request, 'Your CO2 consumption data has been updated.')
            return redirect('view_co2_consumption')
    else:
        form = CO2ConsumptionForm(instance=consumption)

    return render(request, 'counter/add_co2_consumption.html', {'form': form})


@login_required
def view_co2_consumption(request):
    try:
        consumption = CO2Consumption.objects.get(user=request.user)
    except CO2Consumption.DoesNotExist:
        consumption = None

    return render(request, 'counter/view_co2_consumption.html', {'consumption': consumption})