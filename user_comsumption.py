

def energy_consumption(amount: float):
    # przeliczyć ile kwh to ile kg co2
    energy_factor = 1.5
    return amount * energy_factor


def water_consumption(amount: float):
    # przeliczyć ile m3 to ile kg co2
    water_factor = 1.1
    return amount * water_factor


def waste_consumption(segregation: bool):
    # przeliczyć ile srednio kg smieci to ile kg co2
    if segregation:
        waste_co2_amount = 0.9
    else:
        waste_co2_amount = 3.1
    return waste_co2_amount


def house_heat_consumption(heat_type: str):
    # przeliczyć ile srednio kg smieci to ile kg co2
    if heat_type ==  'wegiel':
        heat_amount = 0.9
    elif heat_type ==  'olej':
        heat_amount = 3.1
    elif heat_type ==  'opony':
        heat_amount = 3.1
    elif heat_type ==  'miasto':
        heat_amount = 3.1

    return heat_amount


def air_conditioning_consumption(air_conditioning: bool):
    if air_conditioning:
        air_conditioning_amount = 0.9
    else:
        air_conditioning_amount = 3.1
    return air_conditioning_amount


def private_transport_consumption(fuel_use: float):
    # przeliczyć spalanie na 100 km to ile kg co2
    fuel_use_factor = 1.1
    return fuel_use * fuel_use_factor


def every_day_transport_consumption(transport_type: str):
    #  ile dany srodek transportu produkuje kg co2
    if transport_type ==  'auto':
        transport_factor = 0.9
    elif transport_type ==  'autobus':
        transport_factor = 3.1
    elif transport_type ==  'tramwaj':
        transport_factor = 3.1
    elif transport_type ==  'rower':
        transport_factor = 3.1
    elif transport_type ==  'pieszo':
        transport_factor = 3.1
    else:
        transport_factor = 0.0
    return transport_factor


def transport_distance_consumption(transport_distance: float):
    # przeliczyć spalanie na 100 km to ile kg co2
    # transport_distance = 1.1
    return transport_distance * transport_factor


def transport_consumption():
    pass


def diet_consumption(diet_type: str):
    #  ile dany dieta produkuje kg co2
    if diet_type ==  'vegetarian':
        diet_factor = 0.9
    elif diet_type ==  'vegan':
        diet_factor = 3.1
    elif diet_type ==  'meat':
        diet_factor = 3.1
    elif diet_type ==  'Mediterranean':
        diet_factor = 3.1
    return diet_factor


def fasion_consumption(new_clothes_freq: str):
    #  ile kupowanie ubran produkuje kg co2
    if new_clothes_freq ==  '1 per week':
        fasion_factor = 0.9
    elif new_clothes_freq ==  '2 times per week':
        fasion_factor = 3.1
    elif new_clothes_freq ==  '1 every two weeks':
        fasion_factor = 3.1
    elif new_clothes_freq ==  '1 per month':
        fasion_factor = 3.1
    elif new_clothes_freq ==  'less often':
        fasion_factor = 3.1
    return fasion_factor


def plane_travel_consumption(plane_trav_freq: str):
    #  ile latanie samplotem produkuje kg co2
    if plane_trav_freq ==  '1 per week':
        plane_trav_factor = 0.9
    elif plane_trav_freq ==  '2 times per week':
        plane_trav_factor = 3.1
    elif plane_trav_freq ==  '1 every two weeks':
        plane_trav_factor = 3.1
    elif plane_trav_freq ==  '1 per month':
        plane_trav_factor = 3.1
    elif plane_trav_freq ==  'less often':
        plane_trav_factor = 3.1
    return plane_trav_factor


def go_out_consumption(go_out_freq: str):
    #  jak wychodzienie na miasto produkuje kg co2
    if go_out_freq ==  '1 per week':
        go_out_factor = 0.9
    elif go_out_freq ==  '2 times per week':
        go_out_factor = 3.1
    elif go_out_freq ==  '1 every two weeks':
        go_out_factor = 3.1
    elif go_out_freq ==  '1 per month':
        go_out_factor = 3.1
    return go_out_factor


def disposable_packing(disposable: bool):
    # jak uzywanie jednorazowych opakowan wplywa na produkcje kg co2
    if disposable:
        disposable_packing_amount = 0.9
    else:
        disposable_packing_amount = 3.1
    return disposable_packing_amount


def mass_events_consumption(mass_event: str):
    #  jak rodzaj imprezy wplywa na produkcje kg co2
    if mass_event ==  'stationary':
        mass_event_factor = 0.9
    elif mass_event ==  'outdoor':
        mass_event_factor = 3.1
    return mass_event_factor


def mass_events_freq_consumption(mass_event_freq: str):
    #  jak czestotliwosc impez masowych wplywa na  kg co2
    if mass_event_freq ==  '1 per week':
        mass_event_factor = 0.9
    elif mass_event_freq ==  '2 times per week':
        mass_event_factor = 3.1
    elif mass_event_freq ==  '1 every two weeks':
        mass_event_factor = 3.1
    elif mass_event_freq ==  '1 per month':
        mass_event_factor = 3.1
    return mass_event_factor



def main():
    pass





if __name__ == '__main__':
    main()

