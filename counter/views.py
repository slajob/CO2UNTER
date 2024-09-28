from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import CO2ConsumptionForm
from .models import CO2Consumption
# from user_comsumption import energy_consumption
from user_comsumption import energy_consumption, water_consumption, waste_consumption, house_heat_consumption, air_conditioning_consumption, private_transport_consumption, every_day_transport_consumption,diet_consumption, fashion_consumption, plane_travel_consumption, go_out_consumption,disposable_packing, mass_events_consumption, mass_events_freq_consumption
import user_comsumption

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
        energy_co2 = energy_consumption(consumption.energy_consumption)
        water_co2 = water_consumption(consumption.water_consumption)
        waste_co2 = waste_consumption(consumption.waste_segregation)
        heating_co2 = house_heat_consumption(consumption.heating_method)
        air_conditioning_co2 = air_conditioning_consumption(consumption.air_conditioning)
        private_transport_co2 = format((consumption.daily_travel_distance/100 * consumption.car_fuel_consumption) * private_transport_consumption(), '.2f') #(distance/100 * car_consumption) * private_transport_consumption
        everyday_travel_co2 = every_day_transport_consumption(consumption.everyday_travel) * consumption.daily_travel_distance
        diet_co2 = diet_consumption(consumption.diet)
        fashion_co2 = fashion_consumption(consumption.clothes_factor) * consumption.clothes_factor
        plane_travel_co2 = plane_travel_consumption(consumption.air_travel_frequency)
        go_out_co2 = go_out_consumption(consumption.going_out_frequency)
        disposable_packing_co2 = disposable_packing(consumption.disposable_packaging)
        mass_event_co2 = mass_events_consumption(consumption.mass_event_preference)
        mass_event_freq_co2 = mass_events_freq_consumption(consumption.mass_event_frequency)
    except CO2Consumption.DoesNotExist:
        consumption = None
        energy_co2 = water_co2 = waste_co2 = heating_co2 = air_conditioning_co2 = None
        private_transport_co2 = everyday_travel_co2 = diet_co2 = fashion_co2 = plane_travel_co2 = None
        go_out_co2 = disposable_packing_co2 = mass_event_co2 = mass_event_freq_co2 = None

    return render(request, 'counter/view_co2_consumption.html', {
        'consumption': consumption,
        'energy_co2': energy_co2,
        'water_co2': water_co2,
        'waste_co2': waste_co2,
        'heating_co2': heating_co2,
        'air_conditioning_co2': air_conditioning_co2,
        'private_transport_co2': private_transport_co2,
        'everyday_travel_co2': everyday_travel_co2,
        'diet_co2': diet_co2,
        'fashion_co2': fashion_co2,
        'plane_travel_co2': plane_travel_co2,
        'go_out_co2': go_out_co2,
        'disposable_packing_co2': disposable_packing_co2,
        'mass_event_co2': mass_event_co2,
        'mass_event_freq_co2': mass_event_freq_co2,
    })