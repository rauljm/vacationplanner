# -*- coding: utf-8 -*-
import json
from datetime import datetime
from unittest import TestCase

import mock

from controller.dump import RandomClimaticsConditions
from app.app import app
import constants


class TestApi(TestCase):

    @mock.patch.object(RandomClimaticsConditions, 'generate_dicit_with_random_climatics_conditions')
    def setUp(self, random_climatics_patched):
        self.app = app.test_client()
        self.year = datetime.utcnow().year
        self.payload = {
            'São Paulo': {
                str(self.year): {
                    '{}-01-01'.format(self.year): 'Cold',
                    '{}-01-02'.format(self.year): 'Partly Cloudy',
                    '{}-01-03'.format(self.year): 'Cold',
                    '{}-01-04'.format(self.year): 'Cold',
                    '{}-01-05'.format(self.year): 'Hot',
                }
            },
            'Rio de Janeiro': {
                str(self.year): {
                    '{}-01-01'.format(self.year): 'Partly Cloudy',
                    '{}-01-02'.format(self.year): 'Cold',
                    '{}-01-03'.format(self.year): 'Hot',
                    '{}-01-04'.format(self.year): 'Fair',
                    '{}-01-05'.format(self.year): 'Cold'
                }
            },
            'Porto Alegre': {
                str(self.year): {
                    '{}-01-01'.format(self.year): 'Partly Cloudy',
                    '{}-01-02'.format(self.year): 'Cold',
                    '{}-01-03'.format(self.year): 'Hot',
                    '{}-01-04'.format(self.year): 'Fair',
                    '{}-01-05'.format(self.year): 'Fair'
                }
            },
            'Pernambuco': {
                str(self.year): {
                    '{}-01-01'.format(self.year): 'Hot',
                    '{}-01-02'.format(self.year): 'Hot',
                    '{}-01-03'.format(self.year): 'Hot',
                    '{}-01-04'.format(self.year): 'Hot',
                    '{}-01-05'.format(self.year): 'Hot'
                }
            }}
        random_climatics_patched.return_value = self.payload
        self.city_id = 1
        self.random_climatics = RandomClimaticsConditions(self.year)
        self.random_climatics.save_dicit_with_random_climatics_conditions_in_a_file()

    def test_weather_api(self):
        response = self.app.get('/weather')
        self.assertEquals(
            json.loads(response.get_data().decode()), constants.CLIMATICS_CONDITIONS
        )

    def test_cities_api(self):
        response = self.app.get('/cities')
        # I dont use constants here because in decode method the ids of city
        # will turn a string
        CITIES = {
            '1': u'São Paulo', '2': u'Rio de Janeiro', '3': u'Porto Alegre', '4': u'Pernambuco'
        }

        self.assertEquals(
            json.loads(response.get_data().decode()), CITIES
        )

    def test_cities_per_year(self):
        response = self.app.get('/cities/{}/year/{}'.format(self.city_id, self.year))

        self.assertEquals(
            json.loads(response.get_data().decode()),
            self.payload[constants.CITIES.get(self.city_id)]
        )

    def test_cities_per_year_if_city_not_exist(self):
        city_nonexistent = 100000
        response = self.app.get('/cities/{}/year/{}'.format(city_nonexistent, self.year))

        self.assertEquals(
            json.loads(response.get_data().decode()),
            {'404': u'Cidade não encontrada.'}
        )

    def test_cities_per_year_if_payload_not_exist(self):
        year_nonexistent = 2150
        response = self.app.get('/cities/{}/year/{}'.format(self.city_id, year_nonexistent))

        self.assertEquals(
            json.loads(response.get_data().decode()),
            {'404': u'Nenhuma informação com o ano ({}) informado.'.format(year_nonexistent)}
        )

    def test_post_home(self):
        response = self.app.post('/', data={'city_id': 1, 'days': 2, 'conditions': ['Cold', 'Partly Cloudy']})

        initial_date = datetime.strptime('{}-01-01'.format(self.year), '%Y-%m-%d').strftime('%d/%m/%Y')
        end_date = datetime.strptime('{}-01-04'.format(self.year), '%Y-%m-%d').strftime('%d/%m/%Y')
        city = constants.CITIES[self.city_id]
        expected_return = u'Para a cidade {}, com {} dias livres, o melhor '\
                          'período para as suas férias é de {} até {}.'.format(city, 2, initial_date, end_date)

        self.assertIn(expected_return, response.data.decode())

    def test_post_with_city_id_not_valid(self):
        response = self.app.post('/', data={'city_id': 1000, 'days': 2, 'conditions': ['Cold', 'Partly Cloudy']})
        expected_return = u'Selecione uma cidade!'
        self.assertIn(expected_return, response.data.decode())

    def test_post_with_days_not_valid(self):
        response = self.app.post('/', data={'city_id': 1, 'days': 0, 'conditions': ['Cold', 'Partly Cloudy']})
        expected_return = u'Precisamos de ao menos um dia de férias para te dar as melhores opções.'
        self.assertIn(expected_return, response.data.decode())

    def test_post_with_condition_not_valid(self):
        response = self.app.post('/', data={'city_id': 1, 'days': 2, 'conditions': []})
        expected_return = u'Precisamo de ao menos uma condição climática para te dar as melhores opções'
        self.assertIn(expected_return, response.data.decode())
