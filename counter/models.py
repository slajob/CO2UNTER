from django.db import models
from django.contrib.auth.models import User


class CO2Consumption(models.Model):
    HEATING_CHOICES = [
        ('coal', 'Coal furnace'),
        ('gas', 'Gas furnace'),
        ('oil', 'Oil furnace'),
        ('district', 'District heating'),
    ]

    TRAVEL_CHOICES = [
        ('bus', 'Bus'),
        ('car', 'Car'),
        ('tram', 'Tram'),
        ('walk', 'Walk'),
        ('bike', 'Bike'),
    ]

    DIET_CHOICES = [
        ('vegetarian', 'Vegetarian'),
        ('vegan', 'Vegan'),
        ('meat', 'Meat'),
        ('mediterranean', 'Mediterranean'),
    ]

    FREQUENCY_CHOICES = [
        ('1_per_week', '1 per week'),
        ('2_per_week', '2 times per week'),
        ('1_per_2_weeks', '1 every two weeks'),
        ('1_per_month', '1 per month'),
        ('less_often', 'Less often'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    energy_consumption = models.FloatField(help_text="Energy consumption per month (kWh)")
    water_consumption = models.FloatField(help_text="Water consumption per month (m³)")
    waste_segregation = models.BooleanField(help_text="Do you segregate waste?")
    heating_method = models.CharField(max_length=10, choices=HEATING_CHOICES)
    air_conditioning = models.BooleanField(help_text="Do you use air conditioning?")
    car_fuel_consumption = models.FloatField(help_text="Car fuel consumption per 100km (L)")
    everyday_travel = models.CharField(max_length=10, choices=TRAVEL_CHOICES)
    daily_travel_distance = models.FloatField(help_text="Daily travel distance (km)")
    diet = models.CharField(max_length=15, choices=DIET_CHOICES)
    clothes_shopping_frequency = models.CharField(max_length=15, choices=FREQUENCY_CHOICES)
    air_travel_frequency = models.CharField(max_length=15, choices=FREQUENCY_CHOICES)

    def __str__(self):
        return f"{self.user.username}'s CO2 Consumption"