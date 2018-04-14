# -*- coding: utf-8 -*-
from datetime import datetime, timedelta
from nose.tools import raises

from models import FileName, DatePeriod
import constants


def test_common_file_name():
    year = 2018
    file_name = FileName(year)
    assert(file_name.year == year)
    assert(file_name.name == constants.FILE_WITH_CLIMATICS_CONDITIONS.format(year))


@raises(TypeError)
def test_file_name_without_year():
    FileName()


def test_date_period():
    start = datetime.utcnow()
    end = datetime.utcnow() + timedelta(days=1)
    data_period = DatePeriod(start, end)
    assert(data_period.start == start)
    assert(data_period.end == end)


@raises(TypeError)
def test_date_period_without_period():
    DatePeriod()
