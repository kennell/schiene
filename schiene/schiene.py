#!/usr/bin/env python3
from datetime import datetime


class Schiene():
    def __format_timedelta(self, delta):
        """Formats a timedelta duration to [N days] %H:%M:%S format"""
        seconds = int(delta.total_seconds())

        secs_in_a_day = 86400
        secs_in_a_hour = 3600
        secs_in_a_min = 60

        days, seconds = divmod(seconds, secs_in_a_day)
        hours, seconds = divmod(seconds, secs_in_a_hour)
        minutes, seconds = divmod(seconds, secs_in_a_min)

        time_fmt = f"{hours:02d}:{minutes:02d}"

        if days > 0:
            suffix = "s" if days > 1 else ""
            return f"{days} day{suffix} {time_fmt}"

        return time_fmt

    def __parse_journeys(self, journeys, client):
        connections = list()
        for i in range(3):
            journey = client.journey(journeys[i].id)
            products = ''
            cancel_info = ''
            cancelled = False

            for leg in journey.legs:
                product = str(leg.name)

                if len(products) == 0:
                    products = product
                else:
                    products = products + " / " + product

                if leg.cancelled and len(cancel_info) == 0:
                    cancel_info = " (cancelled)"
                    cancelled = True

            time = self.__format_timedelta(journey.duration)
            data = {
                'details': 'To be removed',
                'departure': (journey.legs[0].departure).strftime("%H:%M") + cancel_info,
                'arrival': (journey.legs[0].arrival).strftime("%H:%M") + cancel_info,
                'transfers': len(journey.legs)-1,
                'time': time,
                'products': products,
                'price': 'Not supported at the moment - issue shall be placed in pyhafas',
                'canceled': cancelled
            }

            if journey.legs[0].departureDelay == None:
                delay_departure = 0
            else:
                delay_departure = journey.legs[0].departureDelay

            if journey.legs[len(journey.legs)-1].arrivalDelay == None:
                delay_arrival = 0
            else:
                delay_arrival = journey.legs[len(journey.legs)-1].arrivalDelay

            if delay_departure + delay_arrival == 0:
                data['ontime'] = True
            else:
                data['ontime'] = False
            data['delay'] = {
                'delay_departure': int(delay_departure.seconds/60),
                'delay_arrival': int(delay_arrival.seconds/60)
            }

            connections.append(data)
        return connections

    def connections(self, origin, destination, dt=datetime.now(), only_direct=False):
        from pyhafas import HafasClient
        from pyhafas.profile import DBProfile
        from pyhafas.types.fptf import Leg

        client = HafasClient(DBProfile())

        origin_location = client.locations(origin)[0]
        destination_location = client.locations(destination)[0]

        if only_direct:
            changes = 0
        else:
            changes = 100

        journeys = client.journeys(
            origin=origin_location,
            via=[],
            destination=destination_location,
            date=dt,
            max_changes=changes,
        )
        
        return self.__parse_journeys(journeys, client)