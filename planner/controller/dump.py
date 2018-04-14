# -*- coding: utf-8 -*-
import random
from datetime import timedelta, date
import json

import constants
from models import FileName, DatePeriod


class PeriodGeneretor:

    def get_all_days_of_period(self, date_period):
        for day in range(int((date_period.end - date_period.start).days + 1)):
            yield date_period.start + timedelta(day)


class RandomClimaticsConditions:

    def __init__(self, year):
        self.year = year
        self.data_period = DatePeriod(date(self.year, 1, 1), date(self.year, 12, 31))
        self.period_generator = PeriodGeneretor()
        self.cities = list(constants.CITIES.values())

    def generate_dicit_with_random_climatics_conditions(self):
        """
         Return a dictionary containing all the days of a given year
         and its respective climatic condition for all cities.
        """
        dicio_conditions_per_day = {}

        for city in self.cities:
            dicio_conditions_per_day.update({city: {self.data_period.start.year: {}}})

            for day in self.period_generator.get_all_days_of_period(self.data_period):
                dicio_conditions_per_day[city][self.year][str(day)] = random.choice(constants.CLIMATICS_CONDITIONS)

        return dicio_conditions_per_day

    def save_dicit_with_random_climatics_conditions_in_a_file(self):
        file_name = FileName(self.year).name
        file = open(file_name, 'w')
        file.write(
            json.dumps(self.generate_dicit_with_random_climatics_conditions())
        )
        file.close()


class DumpDeserialize:

    def __init__(self, year):
        self.file_name = FileName(year).name

    def json_loads(self):
        try:
            file = open(self.file_name, 'r')
            data = json.loads(file.read())
        except FileNotFoundError:
            return
        return data


def make(year):
    _random = RandomClimaticsConditions(year)
    _random.save_dicit_with_random_climatics_conditions_in_a_file()
