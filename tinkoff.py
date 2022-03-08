import json

import requests

TINKOFF_URL = 'https://api.tinkoff.ru/geo/withdraw/clusters'
USD_AMOUNT = 3000


def get_tinkoff_payload():
    data = {
        "bounds": {
            "bottomLeft": {"lat": 55.61426818188351, "lng": 37.38210081319796},
            "topRight": {"lat": 55.87011191955438, "lng": 37.776235334682326}
        },
        "filters": {"showUnavailable": False, "currencies": ["USD"]},
        "zoom": 12
    }
    resp = requests.post(TINKOFF_URL, json=data)
    return json.loads(resp.content)


def get_atm_info():
    payload = get_tinkoff_payload()
    clusters = payload['payload']['clusters']
    result = []
    for cluster in clusters:
        points = cluster['points']
        for point in points:
            atm = {}
            atm['address'] = point['address']
            atm['location'] = point['location']
            atm['limits'] = point['limits']
            result.append(atm)
    return result
