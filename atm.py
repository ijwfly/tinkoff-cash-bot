import math

from tinkoff import get_atm_info


def filter_atms(atms, currency, amount):
    result = []
    for atm in atms:
        usd_limits = [l for l in atm['limits'] if l['currency'] == currency]
        if usd_limits:
            usd_limit, *_ = usd_limits
        else:
            continue
        if usd_limit['amount'] >= amount:
            result.append(atm)
    return result


def calculate_distance(lat1, lng1, lat2, lng2):
    R = 6371e3
    phi1 = lat1 * math.pi/180
    phi2 = lat2 * math.pi/180
    delta_phi = (lat2 - lat1) * math.pi/180
    delta_lambda = (lng2 - lng1) * math.pi/180

    a = math.sin(delta_phi/2) ** 2 + math.cos(phi1) * math.cos(phi2) * (math.sin(delta_lambda/2) ** 2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    distance = R * c
    return distance


def atm_sorted_with_distance(my_lat, my_lng):
    atms = get_atm_info()
    filtered_atms = filter_atms(atms, 'USD', 5000)
    atm_with_distance = []
    for atm in filtered_atms:
        atm_lat = atm['location']['lat']
        atm_lng = atm['location']['lng']
        distance = calculate_distance(my_lat, my_lng, atm_lat, atm_lng)
        atm_with_distance.append((atm, distance))
    atm_sorted = sorted(atm_with_distance, key=lambda x: x[1])
    return atm_sorted
