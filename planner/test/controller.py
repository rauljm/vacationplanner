# -*- coding: utf-8 -*-
import unittest
from datetime import datetime, date
import json

import mock
from nose.tools import raises

from controller.dump import PeriodGeneretor, RandomClimaticsConditions, DumpDeserialize
from controller.tropicalweather import WeatherController
import constants
import exceptions


class TestRandomClimaticsConditions(unittest.TestCase):

    def setUp(self):
        self.year = 2018
        self.random_climatics = RandomClimaticsConditions(self.year)

        super(TestRandomClimaticsConditions, self).setUp()

    def test_random_climatics(self):
        self.assertEquals(self.random_climatics.data_period.start, datetime(self.year, 1, 1).date())
        self.assertEquals(self.random_climatics.data_period.end, datetime(self.year, 12, 31).date())
        self.assertEquals(self.random_climatics.cities, list(constants.CITIES.values()))

    @mock.patch.object(PeriodGeneretor, 'get_all_days_of_period')
    def test_generate_dicit_with_random_climatics(self, all_days_patched):
        payload_expected = {'São Paulo': {2018: {'2018-01-01': mock.ANY, '2018-01-02': mock.ANY}},
                            'Rio de Janeiro': {2018: {'2018-01-01': mock.ANY, '2018-01-02': mock.ANY}},
                            'Porto Alegre': {2018: {'2018-01-01': mock.ANY, '2018-01-02': mock.ANY}},
                            'Pernambuco': {2018: {'2018-01-01': mock.ANY, '2018-01-02': mock.ANY}}}
        all_days_patched.return_value = [date(self.year, 1, 1), date(self.year, 1, 2)]

        random_dicio_climate = self.random_climatics.generate_dicit_with_random_climatics_conditions()
        self.assertEquals(payload_expected, random_dicio_climate)


class TestDumpDeserialize(unittest.TestCase):

    def setUp(self):
        self.year = 2018
        self.deserializer = DumpDeserialize(self.year)

        self.file = open(self.deserializer.file_name, 'w')
        self.data = {'teste': 1, 'teste': 2}
        self.file.write(json.dumps(self.data))
        self.file.close()

        super(TestDumpDeserialize, self).setUp()

    def test_json_loads(self):
        self.assertEquals(self.deserializer.json_loads(), self.data)


class TestWeatherController(unittest.TestCase):

    @mock.patch.object(RandomClimaticsConditions, 'generate_dicit_with_random_climatics_conditions')
    def setUp(self, random_climatics_patched):
        self.year = datetime.utcnow().year
        self.payload = {
            'São Paulo': {
                self.year: {
                    '{}-01-01'.format(self.year): 'Cold',
                    '{}-01-02'.format(self.year): 'Partly Cloudy',
                    '{}-01-03'.format(self.year): 'Cold',
                    '{}-01-04'.format(self.year): 'Cold',
                    '{}-01-05'.format(self.year): 'Hot',
                }
            },
            'Rio de Janeiro': {
                self.year: {
                    '{}-01-01'.format(self.year): 'Partly Cloudy',
                    '{}-01-02'.format(self.year): 'Cold',
                    '{}-01-03'.format(self.year): 'Hot',
                    '{}-01-04'.format(self.year): 'Fair',
                    '{}-01-05'.format(self.year): 'Cold'
                }
            },
            'Porto Alegre': {
                self.year: {
                    '{}-01-01'.format(self.year): 'Partly Cloudy',
                    '{}-01-02'.format(self.year): 'Cold',
                    '{}-01-03'.format(self.year): 'Hot',
                    '{}-01-04'.format(self.year): 'Fair',
                    '{}-01-05'.format(self.year): 'Fair'
                }
            },
            'Pernambuco': {
                self.year: {
                    '{}-01-01'.format(self.year): 'Hot',
                    '{}-01-02'.format(self.year): 'Hot',
                    '{}-01-03'.format(self.year): 'Hot',
                    '{}-01-04'.format(self.year): 'Hot',
                    '{}-01-05'.format(self.year): 'Hot'
                }
            }}
        random_climatics_patched.return_value = self.payload

        self.random_climatics = RandomClimaticsConditions(self.year)
        self.random_climatics.save_dicit_with_random_climatics_conditions_in_a_file()
        self.qty_days = 2
        self.city_id = 1
        self.wheather = WeatherController(self.year, self.city_id, self.qty_days, ['Cold', 'Partly Cloudy'])

        super(TestWeatherController, self).setUp()

    @raises(ValueError)
    def test_create_wheather_controller_with_conditions_is_not_a_list(self):
        WeatherController(self.year, 1, 2, {})

    @raises(exceptions.ConditionsNotValid)
    def test_create_wheather_controller_with_conditions_is_not_a_empty_list(self):
        WeatherController(self.year, 1, 2, [])

    @raises(exceptions.QtyDaysNotValid)
    def test_create_wheather_controller_with_qty_days_is_zero(self):
        qty_days = 0
        WeatherController(self.year, 1, qty_days, ['Cold', 'Partly Cloudy'])

    @raises(exceptions.IdNotValid)
    def test_create_wheather_controller_withc_city_id_not_valid(self):
        city_id = 20
        WeatherController(self.year, city_id, 5, ['Cold', 'Partly Cloudy'])

    def test_get_best_period(self):
        best_period = self.wheather.get_best_period()
        expected_return = ['{}-01-01'.format(self.year),
                           '{}-01-02'.format(self.year),
                           '{}-01-03'.format(self.year),
                           '{}-01-04'.format(self.year)]
        self.assertEquals(best_period, expected_return)

    def test_humanize_best_period(self):
        best_period = self.wheather.get_best_period()
        initial_date = datetime.strptime(best_period[0], '%Y-%m-%d').strftime('%d/%m/%Y')
        end_date = datetime.strptime(best_period[-1], '%Y-%m-%d').strftime('%d/%m/%Y')
        city = constants.CITIES[self.city_id]
        days = self.qty_days
        expected_return = u'Para a cidade {}, com {} dias livres, o melhor '\
                          'período para as suas férias é de {} até {}.'.format(city, days, initial_date, end_date)
        humanize_best_period = self.wheather.humanize_best_period()

        self.assertEquals(expected_return, humanize_best_period)
