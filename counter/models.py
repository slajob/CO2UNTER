from django.db import models
from django.contrib.auth.models import User


class CO2Consumption(models.Model):
    HEATING_CHOICES = [
        ('coal', 'Piec na węgiel'),
        ('gas', 'Piec gazowy'),
        ('oil', 'Piec olejowy'),
        ('district', 'Ogrzewanie miejskie'),
    ]

    TRAVEL_CHOICES = [
        ('bus', 'Autobus'),
        ('car', 'Samochód'),
        ('tram', 'Tramwaj'),
        ('walk', 'Chodzić'),
        ('bike', 'Rower'),
    ]

    DIET_CHOICES = [
        ('vegetarian', 'Wegetariańska'),
        ('vegan', 'Wegańska'),
        ('meat', 'Mięsna'),
        ('mediterranean', 'Śródziemnomorska'),
    ]

    FREQUENCY_CHOICES = [
        ('1_per_week', '1 raz w tygodniu'),
        ('2_per_week', '2 razy w tygodniu'),
        ('1_per_2_weeks', '1 raz na dwa tygodnie'),
        ('1_per_month', '1 raz w miesiącu'),
        ('less_often', 'Rzadziej'),
    ]

    EVENT_PREFERENCE_CHOICES = [
        ('outdoor', 'Na świeżym powietrzu'),
        ('stationary', 'Stacjonarny'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    energy_consumption = models.FloatField(help_text="Zużycie energii na miesiąc (kWh)")
    water_consumption = models.FloatField(help_text="Zużycie wody na miesiąc (m³)")
    waste_segregation = models.BooleanField(help_text="Czy segregujesz odpady?")
    heating_method = models.CharField(max_length=10, choices=HEATING_CHOICES)
    air_conditioning = models.BooleanField(help_text="Czy używasz klimatyzacji?")
    car_fuel_consumption = models.FloatField(help_text="Zużycie paliwa na 100km (L)")
    everyday_travel = models.CharField(max_length=10, choices=TRAVEL_CHOICES)
    daily_travel_distance = models.FloatField(help_text="Codzienna odległość podróży (km)")
    diet = models.CharField(max_length=15, choices=DIET_CHOICES)
    clothes_shopping_frequency = models.CharField(max_length=15, choices=FREQUENCY_CHOICES)
    air_travel_frequency = models.IntegerField(help_text="Ile razy w roku podróżujesz samolotem?")
    going_out_frequency = models.CharField(max_length=15, choices=FREQUENCY_CHOICES, help_text="Jak często wychodzisz?")
    disposable_packaging = models.BooleanField(help_text="Czy używasz jednorazowych opakowań?")
    mass_event_preference = models.CharField(max_length=10, choices=EVENT_PREFERENCE_CHOICES,
                                             help_text="Czy preferujesz masowe wydarzenia na świeżym powietrzu czy stacjonarne?")
    mass_event_frequency = models.CharField(max_length=15, choices=FREQUENCY_CHOICES,
                                            help_text="Jak często chodzisz na masowe wydarzenia?")

    def __str__(self):
        return f"{self.user.username}'s CO2 Consumption"