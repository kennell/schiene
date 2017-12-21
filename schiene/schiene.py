#!/usr/bin/env python3
import requests
import json
from datetime import datetime
from bs4 import BeautifulSoup


def parse_connections(html):
    soup = BeautifulSoup(html, "html.parser")
    connections = list()

    for row in soup.find_all("td", class_="overview timelink"):
        columns = row.parent.find_all("td")

        try:
            price_raw = columns[3].find("span", class_="bold").text.strip().replace(',', '.')
            price = float(price_raw)
        except:
            price = None

        data = {
            'details': columns[0].a.get('href'),
            'departure': columns[0].a.contents[0].string,
            'arrival': columns[0].a.contents[2].string,
            'transfers': int(columns[2].contents[0]),
            'time': columns[2].contents[2],
            'products': columns[3].contents[0].split(', '),
            'price': price
        }

        if not columns[1].find('img') and not columns[1].find('span', class_='delay'):
            data['ontime'] = True
            data['canceled'] = False
        else:
            data = parse_delay(data)

        connections.append(data)
    return connections

def parse_stations(html):
    """
        Strips JS code, loads JSON
    """
    html = html.replace('SLs.sls=', '').replace(';SLs.showSuggestion();', '')
    html = json.loads(html)
    return html['suggestions']

def parse_delay(data):
    """
        Prase the delay
    """
    # parse data from the details view
    rsp = requests.get(data['details'])
    soup = BeautifulSoup(rsp.text, "html.parser")

    # get departure delay
    delay_departure_raw = soup.find('div', class_="routeStart").find('span', class_="delay")
    if delay_departure_raw:
        delay_departure = calculate_delay(data['departure'],
                                          delay_departure_raw.text)
    else:
        delay_departure = 0

    # get arrival delay
    delay_arrival_raw = soup.find('div', class_="routeEnd").find('span', class_="delay")
    if delay_arrival_raw:
        delay_arrival = calculate_delay(data['arrival'],
                                        delay_arrival_raw.text)
    else:
        delay_arrival = 0

    # save the parsed data
    if delay_departure + delay_arrival == 0:
        data['ontime'] = True
    else:
        data['ontime'] = False
    data['delay'] = {
        'delay_departure': int(delay_departure),
        'delay_arrival': int(delay_arrival)
    }

    # TODO: this should not be hardcoded!
    data['canceled'] = False

    return data

def calculate_delay(original, delay):
    """
        Calculate the delay
    """
    original = datetime.strptime(original, '%H:%M')
    delayed = datetime.strptime(delay, '%H:%M')
    diff = delayed - original
    return diff.total_seconds() // 60


class Schiene():

    def stations(self, station, limit=10):
        """
        Find stations for given queries

        Args:
            station (str): search query
            limit (int): limit number of results
        """
        query = {
            'start': 1,
            'S': station + '?',
            'REQ0JourneyStopsB': limit
        }
        rsp = requests.get('http://reiseauskunft.bahn.de/bin/ajax-getstop.exe/dn', params=query)
        return parse_stations(rsp.text)


    def connections(self, origin, destination, dt=datetime.now(), only_direct=False):
        """
        Find connections between two stations

        Args:
            origin (str): origin station
            destination (str): destination station
            dt (datetime): date and time for query
            only_direct (bool): only direct connections
        """
        query = {
            'S': origin,
            'Z': destination,
            'date': dt.strftime("%d.%m.%y"),
            'time': dt.strftime("%H:%M"),
            'start': 1,
            'REQ0JourneyProduct_opt0': 1 if only_direct else 0
        }
        rsp = requests.get('http://mobile.bahn.de/bin/mobil/query.exe/dox?', params=query)
        return parse_connections(rsp.text)
