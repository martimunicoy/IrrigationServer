import requests
from requests.exceptions import ConnectionError
import threading
from bs4 import BeautifulSoup
import time

from django.core.wsgi import get_wsgi_application
from django.utils import timezone

if (__name__ == '__main__'):
    import os
    import sys

    # derive location to django project setting.py
    proj_path = os.path.split(os.path.abspath(os.path.dirname(__file__)))[0]
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "server.settings")
    sys.path.append(proj_path)
    os.chdir(proj_path)

    application = get_wsgi_application()

    from scheduleManager.models import WeatherData
else:
    from server.scheduleManager.models import WeatherData


WEATHER_STATION_URL = str('http://meteoceloni.molner.com')
WEATHER_STATION_QUERY_FREQUENCY = int(600)  # 10 minutes in seconds


class WeatherScrapper(object):
    def __init__(self):
        self._url = WEATHER_STATION_URL

    @property
    def url(self):
        return self._url

    def _get_table(self):
        try:
            response = requests.get(self.url)
        except ConnectionError:
            return None

        soup = BeautifulSoup(response.text, 'html.parser')
        return soup.find('table')

    def get_rain_intensity(self):
        table = self._get_table()

        if (table is None):
            return None

        rows = table.findAll('tr')

        for row in rows:
            if ('Intensitat pluja' in row.get_text()):
                cols = row.findAll('td')
                try:
                    return float(cols[1].get_text().strip().split('\xa0')[0])
                except ValueError:
                    return None


class PeriodicQuery(object):
    def __init__(self):
        self._frequency = WEATHER_STATION_QUERY_FREQUENCY
        self._thread = None
        self._weather_scrapper = WeatherScrapper()

    @property
    def frequency(self):
        return self._frequency

    @property
    def thread(self):
        return self._thread

    @property
    def weather_scrapper(self):
        return self._weather_scrapper

    def start(self):
        if (self.thread is None):
            self._thread = threading.Timer(self.frequency,
                                           self._periodic_action)
            self.thread.start()

    def _periodic_action(self):
        datetime = timezone.localtime()
        rain_intensity = self.weather_scrapper.get_rain_intensity()

        print(rain_intensity)

        if (rain_intensity is not None):
            weather_data = WeatherData(datetime=datetime,
                                       rain_intensity=rain_intensity)
            weather_data.save()

        self._thread = None
        self.start()

    def stop(self):
        self.thread.cancel()
        self._thread = None


def main():
    """ Main method """
    pq = PeriodicQuery()

    try:
        print('Starting periodic weather queries. Press Ctrl + C to exit.')
        pq.start()
        while(True):
            time.sleep(1)
    except KeyboardInterrupt:
        print()
        print('Cancelling next weather query')
        pq.stop()


if __name__ == "__main__":
    main()
