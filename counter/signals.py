from django.db.models.signals import pre_save
from django.dispatch import receiver
from .models import CO2Consumption, CO2ConsumptionHistory
from user_comsumption import energy_consumption, water_consumption, waste_consumption, house_heat_consumption, air_conditioning_consumption, private_transport_consumption, every_day_transport_consumption,diet_consumption, fashion_consumption, plane_travel_consumption, go_out_consumption,disposable_packing, mass_events_consumption, mass_events_freq_consumption


@receiver(pre_save, sender=CO2Consumption)
def create_history_record(sender, instance, **kwargs):
    if instance.pk:  # Check if this is an update and not a new creation
        previous_instance = CO2Consumption.objects.get(pk=instance.pk)

        # Calculations here
        energy_co2 = energy_consumption(previous_instance.energy_consumption)
        water_co2 = water_consumption(previous_instance.water_consumption)
        waste_co2 = waste_consumption(previous_instance.waste_segregation)
        heating_co2 = house_heat_consumption(previous_instance.heating_method)
        air_conditioning_co2 = air_conditioning_consumption(previous_instance.air_conditioning)
        private_transport_co2 = (
                                            previous_instance.daily_travel_distance / 100 * previous_instance.car_fuel_consumption) * private_transport_consumption() if previous_instance.everyday_travel == 'car' else 0
        everyday_travel_co2 = every_day_transport_consumption(
            previous_instance.everyday_travel) * previous_instance.daily_travel_distance if previous_instance.everyday_travel != 'car' else 0
        diet_co2 = diet_consumption(previous_instance.diet)
        fashion_co2 = fashion_consumption(previous_instance.clothes_factor) * previous_instance.clothes_factor
        plane_travel_co2 = plane_travel_consumption(previous_instance.air_travel_frequency)
        go_out_co2 = go_out_consumption(previous_instance.going_out_frequency)
        disposable_packing_co2 = disposable_packing(previous_instance.disposable_packaging)
        mass_event_co2 = mass_events_consumption(previous_instance.mass_event_preference)
        mass_event_freq_co2 = mass_events_freq_consumption(previous_instance.mass_event_frequency)

        total_co2 = (
                    energy_co2 + water_co2 + waste_co2 + heating_co2 + air_conditioning_co2 + private_transport_co2 + everyday_travel_co2 +
                    diet_co2 + fashion_co2 + plane_travel_co2 + go_out_co2 + disposable_packing_co2 + mass_event_co2 + mass_event_freq_co2)

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
            total_co2=total_co2
        )