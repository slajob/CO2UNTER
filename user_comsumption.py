import json


def load_config(json_file="./green_data/consumption_constans.json"):
    with open(json_file, 'r') as file:
        config = json.load(file)
    return config

def energy_consumption(amount: float):
    # przeliczyć ile KWh to ile kg co2
    return amount * load_config()['energy_factor']


def water_consumption(amount: float):
    # przeliczyć ile m3 to ile kg co2
    return amount * load_config()['water_factor']


def waste_consumption(segregation: bool):
    # przeliczyć ile srednio kg smieci to ile kg co2
    if segregation:
        waste_co2_amount = load_config()['waste_co2']['segregation']
    else:
        waste_co2_amount = load_config()['waste_co2']['non_segregation']
    return waste_co2_amount

def house_heat_consumption(heat_type: str):
    # ile co2 produkuje dany typ ogrzewania
    return load_config()['heat_amount'].get(heat_type, 0)

def air_conditioning_consumption(air_conditioning: bool):
    # ile co2 produkuje uzywanie klimatyzacji
    if air_conditioning:
        return load_config()['air_conditioning']['enabled']
    else:
        return load_config()['air_conditioning']['disabled']

def private_transport_consumption():
    # przeliczyć ile kg co2 produkuje dane zuzycie paliwa na 100km
    return load_config()['fuel_use_factor']

def every_day_transport_consumption(transport_type: str):
    # mnoznik rodzaju transportu
    return load_config()['transport_factors'].get(transport_type, 0)

def diet_consumption(diet_type: str):
    # ile co2 produkuje spozywanie danego rodzaju diety
    return load_config()['diet_factors'].get(diet_type, 0)

def fasion_consumption(new_clothes_freq: str):
    # ile co2 produkuje kupowanie odziezy z dana czestotliwoscia
    return load_config()['fasion_factors'].get(new_clothes_freq, 0)

def plane_travel_consumption(plane_trav_freq: float):
    # ile co2 produkuje podrozowanie samolotem z dana czestotliwoscia (1000km * 2)
    return plane_trav_freq * load_config()['plane_travel_factor']

def go_out_consumption(go_out_freq: str):
    # ile co2 produkuje wychodzneie na miasto z dana czestotliwoscia
    return load_config()['go_out_factors'].get(go_out_freq, 0)

def disposable_packing(disposable: bool):
    # ile co2 produkuje wykorzystywanie jednorazowych opakowan
    if disposable:
        return load_config()['disposable_packing']['enabled']
    else:
        return load_config()['disposable_packing']['disabled']

def mass_events_consumption(mass_event: str):
    # ile co2 produkuje chodzenie na imprezy masowe
    return load_config()['mass_event_factors'].get(mass_event, 0)

def mass_events_freq_consumption(mass_event_freq: str):
    # ile co2 produkuje chodznie na imprezy masowe z dana czestotliwoscia
    return load_config()['mass_event_freq_factors'].get(mass_event_freq, 0)


def main():
    # Przykładowe wywołania funkcji
    print(energy_consumption(100))
    print(water_consumption(50))
    print(waste_consumption(True))
    print(house_heat_consumption('gas'))
    print(air_conditioning_consumption(True))
    print(private_transport_consumption(200))
    print(every_day_transport_consumption('car'))
    print(diet_consumption('vegetarian'))
    print(fasion_consumption('1 per week'))
    print(plane_travel_consumption(2))
    print(go_out_consumption('1 per week'))
    print(disposable_packing(True))
    print(mass_events_consumption('stationary'))
    print(mass_events_freq_consumption('1 per week'))

if __name__ == '__main__':
    main()

