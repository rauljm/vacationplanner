
class IdNotValid(Exception):
    def __init__(self):
        self.message = u'Selecione uma cidade!'


class QtyDaysNotValid(Exception):
    def __init__(self):
        self.message = u'Precisamos de ao menos um dia de férias para te dar as melhores opções.'


class ConditionsNotValid(Exception):
    def __init__(self):
        self.message = u'Precisamo de ao menos uma condição climática para te dar as melhores opções'
