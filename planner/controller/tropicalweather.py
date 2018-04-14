# -*- coding: utf-8 -*-
from datetime import datetime

from controller.dump import DumpDeserialize
import constants
import exceptions


class WeatherController:

    def __init__(self, year, city_id, qty_days, conditions):
        self.year = str(year)
        self.city_id = int(city_id)
        self.qty_days = int(qty_days)
        self.conditions = conditions
        self.data = DumpDeserialize(year).json_loads()
        self.best_period = []
        self.validator()

    def validator(self):
        """
         Raise a exception if any data its wrong.
        """
        if type(self.conditions) != list:
            raise ValueError("Argument 'conditions' must be a list!")
        if not constants.CITIES.get(self.city_id):
            raise exceptions.IdNotValid()
        if self.qty_days == 0:
            raise exceptions.QtyDaysNotValid()
        if self.conditions == []:
            raise exceptions.ConditionsNotValid()

    def get_best_period(self):
        """
          Get the days with condition specified in a determinated period
          for a determinted city
        """
        city_conditions = self.data[constants.CITIES.get(self.city_id)]
        year_condition = city_conditions[self.year]

        for day, condition in year_condition.items():
            if condition in self.conditions:
                self.best_period.append(day)
            elif len(self.best_period) >= self.qty_days:
                return self.best_period
            else:
                self.best_period = []
        return self.best_period

    def humanize_best_period(self):
        best_period = self.get_best_period()
        if best_period:
            initial_date = datetime.strptime(best_period[0], '%Y-%m-%d').strftime('%d/%m/%Y')
            end_date = datetime.strptime(best_period[-1], '%Y-%m-%d').strftime('%d/%m/%Y')
            city = constants.CITIES[self.city_id]
            days = self.qty_days
            return (
                u'Para a cidade {}, com {} dias livres, o melhor '
                'período para as suas férias é de {} até {}.'.format(city, days, initial_date, end_date)
            )
