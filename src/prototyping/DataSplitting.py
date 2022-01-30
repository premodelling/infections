import collections


class DataSplitting:

    def __init__(self, fraction: collections.namedtuple(typename='Fraction', 
                                                        field_names=['training', 'validating', 'testing'])):
        """

        :param fraction:
        """

        self.__second = fraction.training
        self.__penultimate = fraction.training + fraction.validating

    def exc(self, data):
        """

        :param data:
        :return:
        """
        
        instances = data.shape[0]

        training = data[0:int(self.__second * instances)]
        validating = data[int(self.__second * instances):int(self.__penultimate * instances)]
        testing = data[int(self.__penultimate * instances):]

        return training, validating, testing
