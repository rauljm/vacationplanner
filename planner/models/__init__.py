# -*- coding: utf-8 -*-
import constants


class FileName:

    def __init__(self, year):
        self.year = year
        self.name = constants.FILE_WITH_CLIMATICS_CONDITIONS.format(self.year)


class DatePeriod:
    def __init__(self, start, end):
        self.start = start
        self.end = end
