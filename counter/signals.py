from django.db.models.signals import pre_save
from django.dispatch import receiver
from .models import CO2Consumption, CO2ConsumptionHistory


@receiver(pre_save, sender=CO2Consumption)
def create_history_record(sender, instance, **kwargs):
    if instance.pk:  # Check if this is an update and not a new creation
        previous_instance = CO2Consumption.objects.get(pk=instance.pk)

        # Create a historical record
        CO2ConsumptionHistory.objects.create(
            user=previous_instance.user,
            energy_consumption=previous_instance.energy_consumption,
            water_consumption=previous_instance.water_consumption,
            waste_segregation=previous_instance.waste_segregation,
            heating_method=previous_instance.heating_method,
            air_conditioning=previous_instance.air_conditioning,
            car_fuel_consumption=previous_instance.car_fuel_consumption,
            everyday_travel=previous_instance.everyday_travel,
            daily_travel_distance=previous_instance.daily_travel_distance,
            diet=previous_instance.diet,
            clothes_factor=previous_instance.clothes_factor,
            air_travel_frequency=previous_instance.air_travel_frequency,
            going_out_frequency=previous_instance.going_out_frequency,
            disposable_packaging=previous_instance.disposable_packaging,
            mass_event_preference=previous_instance.mass_event_preference,
            mass_event_frequency=previous_instance.mass_event_frequency,
        )