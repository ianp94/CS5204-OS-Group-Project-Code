# coding=utf-8


class LogKeys(object):
    def __init__(self):

        self.name = 'name'
        self.id = 'activationId'
        self.causeID = 'cause'
        self.start_time = 'start'
        self.end_time = 'end'
        self.unknown = 'unknown'

    def __str__(self):
        return '\n'.join(['%s:%s' % item for item in self.__dict__.items()])


class Config(object):
    def __init__(self):

        self.logging_path = '/home/cs5204/cold_start/ml_models/logging/'
        self.func2ids = {'unknown': 0,
                         'test': 1,
                         'highProb': 2,
                         'code': 3,
                         'debug': 4,
                         'tripleAndIncrement':5,
                         'demo': 6,
                         'authenticate': 7,
                         'triple': 8,
                         'increment': 9,
                         'composition': 10,
                         'guest': 11,
                         'prob': 12,
                         'randprob': 13}
        self.ids2func = dict((v, k) for k,v in self.func2ids.items())

    def update(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)

    def __str__(self):
        return '\n'.join(['%s:%s' % item for item in self.__dict__.items()])

