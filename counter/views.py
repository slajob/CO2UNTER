from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import CO2ConsumptionForm
from .models import CO2Consumption
from user_comsumption import energy_consumption, water_consumption, waste_consumption, house_heat_consumption, air_conditioning_consumption, private_transport_consumption, every_day_transport_consumption,diet_consumption, fashion_consumption, plane_travel_consumption, go_out_consumption,disposable_packing, mass_events_consumption, mass_events_freq_consumption
from django.shortcuts import render
from django.utils.timezone import now
from .models import CO2ConsumptionHistory
from datetime import timedelta
from absorbtion_data import old_tree, middle_tree, young_tree, parks_absorption
import numpy as np


@login_required
def home(request):
    current_user = request.user

    # Get this month's and year's data (as shown previously)
    first_day_of_month = now().replace(day=1)
    first_day_of_next_month = (first_day_of_month + timedelta(days=32)).replace(day=1)
    last_day_of_month = first_day_of_next_month - timedelta(seconds=1)
    first_day_of_year = now().replace(month=1, day=1)
    first_day_of_next_year = first_day_of_year.replace(year=first_day_of_year.year + 1)
    last_day_of_year = first_day_of_next_year - timedelta(seconds=1)

    month_records = CO2ConsumptionHistory.objects.filter(
        user=current_user,
        timestamp__gte=first_day_of_month,
        timestamp__lt=first_day_of_next_month
    )

    year_records = CO2ConsumptionHistory.objects.filter(
        user=current_user,
        timestamp__gte=first_day_of_year,
        timestamp__lt=first_day_of_next_year
    )

    total_co2_month_records = [record.total_co2 for record in month_records]
    total_co2_year_records = [record.total_co2 for record in year_records]

    # Calculate average for month
    if total_co2_month_records:
        total_co2_month = int(sum(total_co2_month_records) / len(total_co2_month_records))
    else:
        total_co2_month = 0

    # Calculate average for year
    if total_co2_year_records:
        total_co2_year = int(sum(total_co2_year_records) / len(total_co2_year_records))
    else:
        total_co2_year = 0

    old_tree_general_absorb = old_tree(30)
    middle_tree_general_absort = middle_tree(total_co2_month)
    young_tree_general_absorb = young_tree(30, total_co2_month)
    parks_general_absorption = parks_absorption(total_co2_month)
    link = parks_absorption

    # Historical Data for the chart
    historical_data = CO2ConsumptionHistory.objects.filter(user=current_user).order_by('timestamp')

    # Format data for Chart.js
    labels = [record.timestamp.strftime('%Y-%m-%d') for record in historical_data]
    data = [record.total_co2 for record in historical_data]

    return render(request, 'counter/home.html', {
        'total_co2_month': total_co2_month,
        'total_co2_year': total_co2_year,
        'labels': labels,
        'data': data,
        'old_tree_general_absorb': old_tree_general_absorb,
        'middle_tree_general_absort': middle_tree_general_absort,
        'young_tree_general_absorb': young_tree_general_absorb,
        'parks_general_absorption': parks_general_absorption,
    })


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
        private_transport_co2 = (
                                            consumption.daily_travel_distance / 100 * consumption.car_fuel_consumption) * private_transport_consumption() if consumption.everyday_travel == 'car' else 0
        everyday_travel_co2 = every_day_transport_consumption(
            consumption.everyday_travel) * consumption.daily_travel_distance if consumption.everyday_travel != 'car' else 0
        diet_co2 = diet_consumption(consumption.diet)
        fashion_co2 = fashion_consumption(consumption.clothes_factor) * consumption.clothes_factor
        plane_travel_co2 = plane_travel_consumption(consumption.air_travel_frequency)
        go_out_co2 = go_out_consumption(consumption.going_out_frequency)
        disposable_packing_co2 = disposable_packing(consumption.disposable_packaging)
        mass_event_co2 = mass_events_consumption(consumption.mass_event_preference)
        mass_event_freq_co2 = mass_events_freq_consumption(consumption.mass_event_frequency)

        total_co2 = (
                    energy_co2 + water_co2 + waste_co2 + heating_co2 + air_conditioning_co2 + private_transport_co2 + everyday_travel_co2 +
                    diet_co2 + fashion_co2 + plane_travel_co2 + go_out_co2 + disposable_packing_co2 + mass_event_co2 + mass_event_freq_co2)

    except CO2Consumption.DoesNotExist:
        consumption = None
        energy_co2 = water_co2 = waste_co2 = heating_co2 = air_conditioning_co2 = None
        private_transport_co2 = everyday_travel_co2 = diet_co2 = fashion_co2 = plane_travel_co2 = None
        go_out_co2 = disposable_packing_co2 = mass_event_co2 = mass_event_freq_co2 = None
        total_co2 = 0

    return render(
        request,
        'counter/view_co2_consumption.html',
        {
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
            'total_co2': np.round(total_co2, 2)
        }
    )