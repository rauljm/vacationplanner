# -*- coding: utf-8 -*-
from datetime import datetime

from flask import Flask, render_template, request, jsonify
from flask.ext.api import status
import constants
import exceptions
from controller.tropicalweather import WeatherController
from controller.dump import DumpDeserialize

app = Flask(__name__)


@app.route("/", methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        data = dict(request.form)
        city_id = data.get('city_id')[0] if data.get('city_id') else 0
        total_days = data.get('days')[0] if data.get('days')[0] else 0
        conditions = data.get('conditions') if data.get('conditions') else []
        year = datetime.utcnow().year

        try:
            weather_controller = WeatherController(year, city_id, total_days, conditions)
            best_period = weather_controller.humanize_best_period()

        except exceptions.IdNotValid as e:
            return render_template(
                'home.html', list_city=constants.CITIES.items(),
                list_conditions=constants.CLIMATICS_CONDITIONS,
                error=e.message)

        except exceptions.QtyDaysNotValid as e:
            return render_template(
                'home.html', list_city=constants.CITIES.items(),
                list_conditions=constants.CLIMATICS_CONDITIONS,
                error=e.message)

        except exceptions.ConditionsNotValid as e:
            return render_template(
                'home.html', list_city=constants.CITIES.items(),
                list_conditions=constants.CLIMATICS_CONDITIONS,
                error=e.message)

        return render_template(
            'home.html', list_city=constants.CITIES.items(),
            list_conditions=constants.CLIMATICS_CONDITIONS,
            best_period=best_period,
        )

    return render_template(
        'home.html', list_city=constants.CITIES.items(),
        list_conditions=constants.CLIMATICS_CONDITIONS,
        best_period=[]
    )


@app.route("/cities", methods=['GET'])
def cities():
    return jsonify(constants.CITIES)


@app.route("/cities/<int:city_id>/year/<int:year>", methods=['GET'])
def cities_per_year(city_id, year):
    city = constants.CITIES.get(city_id)
    payload = DumpDeserialize(year).json_loads()

    if not city:
        msg = {status.HTTP_404_NOT_FOUND: u'Cidade não encontrada.'}
        return jsonify(msg)
    if not payload:
        msg = {status.HTTP_404_NOT_FOUND: u'Nenhuma informação com o ano ({}) informado.'.format(year)}
        return jsonify(msg)

    return jsonify(payload[constants.CITIES.get(city_id)])


@app.route("/weather", methods=['GET'])
def weather():
    return jsonify(constants.CLIMATICS_CONDITIONS)


if __name__ == '__main__':
    app.run()
